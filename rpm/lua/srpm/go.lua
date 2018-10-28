-- Copyright (c) 2017-2018 Nicolas Mailhot <nim@fedoraproject.org>
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
-- This file contains Lua code used in rpm macros needed to create and process
-- source rpm (srpm) Go (golang) packages.
--
-- The resulting code must not use any package except redhat-rpm-macros

-- Sanitize a Go import path that can then serve as rpm package name
-- Mandatory parameter: a Go import path
local function gorpmname(goipath)
  -- lowercase and end with '/'
  goname       = string.lower(goipath .. "/")
  -- remove eventual protocol prefix
  goname       = string.gsub(goname, "^http(s?)://",         "")
  -- remove eventual .git suffix
  goname       = string.gsub(goname, "%.git/*",              "")
  -- remove eventual git. prefix
  goname       = string.gsub(goname, "^git%.",              "")
  -- add golang prefix
  goname       = "golang-" .. goname
  -- remove FQDN root (.com, .org, etc)
  goname       = string.gsub(goname, "^([^/]+)%.([^%./]+)/", "%1/")
  -- special-case x.y.z number-strings as that’s an exception in our naming
  -- guidelines
  repeat
    goname, i = string.gsub(goname, "(%d)%.(%d)",            "%1:%2")
  until i == 0
  -- replace various separators rpm does not like with -
  goname       = string.gsub(goname, "[%._/%-]+",            "-")
  -- because of the Azure sdk
  goname       = string.gsub(goname, "%-for%-go%-",          "-")
  -- Tokenize along - separators and remove duplicates to avoid
  -- golang-foo-foo-bar-foo names
  local result = ""
  local tokens = {}
  tokens["go"]     = true
  for token in string.gmatch(goname, "[^%-]+") do
     if not tokens[token] then
        result = result .. "-" .. token
        tokens[token] = true
     end
  end
  -- reassemble the string, restore x.y.z runs, convert the vx.y.z
  -- Go convention to x.y.z as prefered in rpm naming
  result = string.gsub(result, "^-", "")
  result = string.gsub(result, ":", ".")
  -- some projects have a name that end up in a number, and *also* add release
  -- numbers on top of it, keep a - prefix before version strings
  result = string.gsub(result, "%-v([%.%d])", "-%1")
  return(result)
end

-- The gometa macro main processing function
-- See the documentation in the macros.go-srpm file for argument description
local function gometa(suffix, verbose, informative, silent)
  local  fedora = require "fedora.common"
  local   forge = require "fedora.srpm.forge"
  local zsuffix = ""
  if (suffix ~= "") then
        zsuffix = " -z " .. suffix
  end
  local ismain = (suffix == "") or (suffix == "0")
  if ismain then
    fedora.zalias({"forgeurl", "goipath", "goname", "gourl", "gosource"}, verbose)
  end
  local spec = {}
  for _, v in ipairs({'goipath', 'forgeurl'}) do
    spec[v] = rpm.expand("%{?" .. v .. suffix .. "}")
  end
  -- All the Go packaging automation relies on goipath being set
  if (spec["goipath"] == "") then
    rpm.expand("%{error:Please set the Go import path in the %%{goipath" .. suffix .. "} variable before calling %%gometa" .. zsuffix .. "!}")
  end
  if (spec["forgeurl"] ~= "") then
    fedora.safeset("gourl"    .. suffix, "%{forgeurl"        .. suffix .. "}",verbose)
  else
    fedora.safeset("gourl"    .. suffix, "https://%{goipath" .. suffix .. "}",verbose)
    fedora.safeset("forgeurl" .. suffix, "%{gourl"           .. suffix .. "}",verbose)
  end
  forge.forgemeta(suffix, verbose, informative, silent)
  if (rpm.expand("%{?forgesource" .. suffix .. "}") ~= "") then
    fedora.safeset("gosource" .. suffix, "%{forgesource" .. suffix .. "}",verbose)
  else
    fedora.safeset("gosource" .. suffix, "%{gourl" .. suffix .. "}/%{archivename" .. suffix .. "}.%{archiveext" .. suffix .. "}",verbose)
  end
  fedora.safeset(  "goname"   .. suffix, "%gorpmname %{goipath" .. suffix .. "}",verbose)
  fedora.zalias({"forgeurl","goname","gourl","gosource"},verbose)
  -- Final spec variable summary if the macro was called with -i
  if informative then
    rpm.expand("%{echo:Packaging variables read or set by %%gometa}")
    fedora.echovars({"goipath","goname","gourl","gosource"}, suffix)
  end
end

return {
  gorpmname = gorpmname,
  gometa    = gometa,
}
