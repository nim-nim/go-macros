-- Copyright (c) 2017-2018 Nicolas Mailhot <nim@fedoraproject.org>
-- This file is distributed under the terms of GNU GPL license version 3, or
-- any later version.
--
-- This file contains Lua code used in rpm macros to create rpm packages past
-- the srpm stage: anything starting with %prep.
--
-- The sister file gosrpm.lua deals with srpm and buildroot setup and is more
-- restricted.

-- The goenv macro main processing function
-- See the documentation in the macros.go-rpm file for argument description
local function goenv(suffix, goipath, verbose, usermetadata)
  local  fedora = require "fedora.common"
  local  suffix = suffix
  local goipath = goipath
  local  ismain = (suffix == "") or (suffix == "0")
  if (goipath ~= "") and (suffix == "") then
    local bettersuffix = fedora.getbestsuffix("goipath",goipath)
    if (bettersuffix ~= nil) then
         suffix = bettersuffix
    end
  end
  if (goipath == "") then
    goipath = "%{goipath" .. suffix .. "}"
  end
  suffixes = fedora.getsuffixes("goipath")
  fedora.safeset(             "goworkdir", "%{_builddir}/%{extractdir" .. suffixes[#suffixes] .. "}",                     verbose)
  fedora.safeset(            "gobuilddir", "%{goworkdir}/_build",                                                         verbose)
  if ismain then
    fedora.zalias({"gosourcedir","gofilelist"}, verbose)
  else
    fedora.safeset("gofilelist" .. suffix, rpm.expand("%gorpmname %{goipath" .. suffix .. "}") .. "-%{gofilelist}",       verbose)
  end
  fedora.safeset( "gosourcedir" .. suffix, "%{?extractdir" .. suffix .. ":%{_builddir}/%{extractdir" .. suffix .. "}}" ..
                                             "%{!?extractdir" .. suffix .. ":%{goworkdir}}",                                 verbose)
  if ismain then
    fedora.zalias({"gosourcedir"}, verbose)
  end
  local   ldflags = ""
  local  metadata = { version = { id = "version" }, tag = {}, commit = {}, branch  = {}, }
  table.sort(metadata)
  for m,_ in pairs(metadata) do
    metadata[m]["id"]    = metadata[m]["id"] or "version." .. m
    metadata[m]["value"] = usermetadata[m] or rpm.expand("%{?" .. m .. suffix .. "}")
    if (metadata[m]["value"] ~= '') then
      ldflags = ldflags .. " -X " .. goipath .. "/" ..  metadata[m]["id"] .. "=" .. metadata[m]["value"]
    end
  end
  for _, v in ipairs({"goipath", "gosourcedir", "gofilelist",
                      "version", "tag", "commit", "branch"}) do
    if (rpm.expand("%{?" .. v .. suffix .. "}") ~= "") then
      fedora.explicitset(  "current" .. v, "%{" .. v .. suffix .. "}", verbose)
    else
      fedora.explicitunset("current" .. v,                             verbose)
    end
  end
  fedora.explicitset(  "currentgoldflags", ldflags,                    verbose)
end

return {
  goenv = goenv,
}

