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

-- Pivot variable definitions for each kind of Go package
local pivot = {devel = "goipathes", compat = "goaltipathes"}

-- Default argument flag for each kind of list
local listflags = {goipathes = "-i", goipathesex = "-t", goextensions = "-e"}

-- The goenv macro main processing function
-- See the documentation in the macros.go-rpm file for argument description
local function env(suffix, goipath, verbose, usermetadata)
  local  fedora = require "fedora.common"
  local      go = require "fedora.srpm.go"
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
    fedora.safeset("gofilelist" .. suffix, go.rpmname("%{goipath" .. suffix .. "}") .. "-%{gofilelist}",                  verbose)
  end
  if rpm.expand("%{goipath" .. suffix .. "}") ~= rpm.expand(goipath) then
    fedora.explicitset("thisgofilelist",   go.rpmname(goipath)                      .. "-%{gofilelist}",                  verbose)
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
  fedora.setcurrent({"goipath", "gosourcedir", "gofilelist",
                     "version", "tag", "commit", "branch"}, suffix, verbose)
  fedora.explicitset(  "currentgoldflags", ldflags,                 verbose)
end

-- Create fallbacks to goipath variables if godevelipath variables are missing
local function develenvinit()
  local  fedora = require "fedora.common"
  if (next(fedora.getsuffixes("goipathes")) == nil) then
    for _, suffix in pairs(fedora.getsuffixes("goipath")) do
      fedora.safeset("goipathes" .. suffix, "%{goipath" .. suffix .. "}")
    end
  end
end

-- Set rpm variables related to the processing of a golang-*-devel subpackage
local function develenv(suffix, verbose)
  local fedora = require "fedora.common"
  local     go = require "fedora.srpm.go"
  local ismain = (suffix == "") or (suffix == "0")
  if ismain then
    fedora.zalias(  {"godevelname", "godevelfilelist", "godevelsummary", "godeveldescription",
                     "godevelheader", "goextensions", "gosupfiles", "gosupfilesex",
                     "goipathes", "goipathesex", "golicenses", "golicensesex", "godocs", "godocsex"},         verbose)
  end
  for flag, list in pairs(listflags) do
    local l = rpm.expand("%{?" .. list .. suffix .. "}")
    if (l ~= "") then
      l = string.gsub(" " .. l, "%s+%" .. flag .. "%s+", " ")
      l = string.gsub(l, "%s+", " ")
      l = string.gsub(l, "^ ", "")
      l = string.gsub(l, " $", "")
      if (list ~= "goipathes") then
        l = string.gsub(l, "([^%s]+)", flag .. " %1")
      end
      fedora.explicitset(list .. suffix, l)
    end
  end
  local goipathes = rpm.expand("%{?goipathes" .. suffix .. "}")
  local goipath   = string.match(goipathes, "[^%s]+")
  fedora.safeset("godevelname"        .. suffix, go.rpmname(goipath) .. "-devel",                             verbose)
  fedora.safeset("godevelfilelist"    .. suffix, go.rpmname(goipath) .. "-%{gofilelist}",                     verbose)
  fedora.safeset("godevelsummary"     .. suffix, "%{summary}",                                                verbose)
  fedora.safeset("godeveldescription" .. suffix, "%{?common_description}",                                    verbose)
  local postdescr = "\n\nThis package provides the following Go import pathes:"
  postdescr = postdescr .. string.gsub(goipathes, "([^%s]+)", "\n – %1")
  fedora.explicitset("currentgodeveldescription", "%{expand:%{godeveldescription" .. suffix .. "}" ..
                                                  postdescr .. "}",                                           verbose)
  fedora.setcurrent({"godevelname", "godevelfilelist", "godevelsummary",
                     "godevelheader", "goextensions", "gosupfiles", "gosupfilesex",
                     "goipathes", "goipathesex", "golicenses", "golicensesex", "godocs", "godocsex"}, suffix, verbose)
  if ismain then
    fedora.zalias(  {"godevelname", "godevelfilelist", "godevelsummary", "godeveldescription"},               verbose)
  end
end

-- Set rpm variables related to the processing of a compat-golang-*-devel subpackage
local function compatenv(suffix, goaltipath, verbose)
  local fedora = require "fedora.common"
  local     go = require "fedora.srpm.go"
  local ismain = (suffix == "") or (suffix == "0")
  if ismain then
    fedora.zalias(  {"goipath", "gocompatipath", "gocompatdescription", "gocompatsummary", "gocompatheader"}, verbose)
  end
  fedora.safeset("gocompatipath"   .. suffix,      "%{goipath" .. suffix .. "}",                              verbose)
  fedora.safeset("gocompatsummary" .. suffix,      "%{summary}",                                              verbose)
  fedora.safeset("gocompatdescription" .. suffix,  "%{?common_description}",                                  verbose)
  fedora.setcurrent( {"gocompatipath", "gocompatheader", "gocompatsummary"}, suffix,                          verbose)
  fedora.explicitset("currentgoaltipath",         goaltipath,                                                 verbose)
  local postdescr = "\n\nThis package provides a symbolic link that aliases the %{currentgoaltipath} "  ..
                    "Go import path to %{currentgocompatipath}. Aliasing Go import paths via symbolic " ..
                    "links or http redirects is fragile. If your Go code depends on this package, you " ..
                    "should patch it to import %{currentgocompatipath} directly."
  fedora.explicitset("currentgocompatdescription", "%{expand:%{?gocompatdescription" .. suffix .. "}" ..
                                                   postdescr .. "}",                                          verbose)
  fedora.explicitset("currentgocompatname",        "compat-" .. go.rpmname(goaltipath) .. "-devel",           verbose)
  fedora.explicitset("currentgocompatfilelist",    "compat-" .. go.rpmname(goaltipath) .. "-%{gofilelist}",   verbose)
  if ismain then
    fedora.zalias(  {"gocompatipath", "gocompatsummary", "gocompatdescription"},                              verbose)
  end
end

-- Create a single %package section for a known kind of Go subpackage
local function singlepkg(kind, suffix, verbose)
  if     (kind == "devel")  then
    develenv(suffix, verbose)
    print(rpm.expand('%__godevelpkg\n'))
  elseif (kind == "compat") then
    local fedora = require "fedora.common"
    local ismain = (suffix == "") or (suffix == "0")
    if ismain then
      fedora.zalias({"goaltipathes"}, verbose)
    end
    for goaltipath in string.gmatch(rpm.expand("%{goaltipathes" .. suffix .. "}"), "[^%s,]+") do
      compatenv(suffix, goaltipath, verbose)
      print(rpm.expand('%__gocompatpkg\n'))
    end
  else
    rpm.expand("%{error:Unknown kind of Go subpackage: " .. kind .. "}")
  end
end

-- Create one or all %package sections for a known kind of go subpackage
local function pkg(kind, suffix, processall, verbose)
  local fedora = require "fedora.common"
  if (kind == "devel") then
    develenvinit()
  end
  if processall then
    for _, suffix in pairs(fedora.getsuffixes(pivot[kind])) do
       singlepkg(kind, suffix, verbose)
    end
  else
    singlepkg(kind, suffix, verbose)
  end
end

-- Create a single set of %install tasks for a known kind of Go subpackage
local function singleinstall(kind, suffix, verbose)
  if     (kind == "devel")  then
    develenv(suffix, verbose)
    for goipath in string.gmatch(rpm.expand("%{currentgoipathes}"), "[^%s]+") do
      env('', goipath, verbose, {})
      local vflag = verbose and " -v" or ""
      print(rpm.expand("%__godevelinstall -i " .. goipath .. vflag .. "\n"))
    end
    print(rpm.expand("%__godevelinstalldoc\n"))
  elseif (kind == "compat") then
    local fedora = require "fedora.common"
    local ismain = (suffix == "") or (suffix == "0")
    if ismain then
      fedora.zalias({"goaltipathes"}, verbose)
    end
    for goaltipath in string.gmatch(rpm.expand("%{goaltipathes" .. suffix .. "}"), "[^%s,]+") do
      compatenv(suffix, goaltipath, verbose)
      gocompatipath = rpm.expand("%{currentgocompatipath}")
      print(rpm.expand('install -m 0755 -vd "%{buildroot}%{gopath}/src/%(dirname ' .. goaltipath .. ')"\n'                ..
                       'ln -s         "%{gopath}/src/' .. gocompatipath .. '" "%{buildroot}%{gopath}/src/' .. goaltipath .. '"\n' ..
                       'echo          "%{gopath}/src/' .. goaltipath    .. '"   >> "%{goworkdir}/%{currentgocompatfilelist}"\n'))
      goaltipath    = string.gsub(goaltipath, "/?[^/]+/?$", "")
      while (not string.match(gocompatipath, "^" .. goaltipath)) do
        print(rpm.expand('echo \'%dir "%{gopath}/src/' .. goaltipath    .. '"\' >> "%{goworkdir}/%{currentgocompatfilelist}"\n'))
        goaltipath  = string.gsub(goaltipath, "/?[^/]+/?$", "")
      end
    end
  else
    rpm.expand("%{error:Unknown kind of Go subpackage: " .. kind .. "}")
  end
end

-- Create one or all %install tasks for a known kind of go subpackage
local function install(kind, suffix, processall, verbose)
  local  fedora = require "fedora.common"
  if (kind == "devel") then
    develenvinit()
  end
  if processall then
    for _, suffix in pairs(fedora.getsuffixes(pivot[kind])) do
       singleinstall(kind, suffix, verbose)
    end
  else
    singleinstall(kind, suffix, verbose)
  end
end

-- Create a single %files section for a known kind of Go subpackage
local function singlefiles(kind, suffix, verbose)
  if     (kind == "devel")  then
    develenv(suffix, verbose)
    print(rpm.expand('%files -n %{currentgodevelname}    -f "%{goworkdir}/%{currentgodevelfilelist}"\n'))
  elseif (kind == "compat") then
    local fedora = require "fedora.common"
    local ismain = (suffix == "") or (suffix == "0")
    if ismain then
      fedora.zalias({"goaltipathes"}, verbose)
    end
    for goaltipath in string.gmatch(rpm.expand("%{goaltipathes" .. suffix .. "}"), "[^%s,]+") do
      compatenv(suffix, goaltipath, verbose)
      print(rpm.expand('%files -n %{currentgocompatname} -f "%{goworkdir}/%{currentgocompatfilelist}"\n'))
    end
  else
    rpm.expand("%{error:Unknown kind of Go subpackage: " .. kind .. "}")
  end
end

-- Create one or all %files sections for a known kind of go subpackage
local function files(kind, suffix, processall, verbose)
  local fedora = require "fedora.common"
  if (kind == "devel") then
    develenvinit()
  end
  if processall then
    for _, suffix in pairs(fedora.getsuffixes(pivot[kind])) do
       singlefiles(kind, suffix, verbose)
    end
  else
    singlefiles(kind, suffix, verbose)
  end
end

return {
  env       = env,
  develenv  = develenv,
  compatenv = compatenv,
  pkg       = pkg,
  install   = install,
  files     = files,
}

