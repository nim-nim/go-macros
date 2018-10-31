-- Copyright © 2017-2018 Nicolas Mailhot <nim@fedoraproject.org>
--
-- This program is free software: you can redistribute it and/or modify
-- it under the terms of the GNU General Public License as published by
-- the Free Software Foundation, either version 3 of the License, or
-- (at your option) any later version.
--
-- This program is distributed in the hope that it will be useful,
-- but WITHOUT ANY WARRANTY; without even the implied warranty of
-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
-- GNU General Public License for more details.
--
-- You should have received a copy of the GNU General Public License
-- along with this program.  If not, see <https://www.gnu.org/licenses/>.
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
  if rpm.expand("%{goipath" .. suffix .. "}") ~= rpm.expand(goipath) then
    fedora.explicitset("thisgofilelist",   rpm.expand("%gorpmname " .. goipath)                .. "-%{gofilelist}",       verbose)
  else
    fedora.explicitset("thisgofilelist",   "%{gofilelist"  .. suffix .. "}",                                              verbose)
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

