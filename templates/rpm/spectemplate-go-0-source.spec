# Main template for Go packages.
#
# The master Go import path of the project. Take care to identify it
# accurately, changing it later will be inconvenient:
#  – it has not necessarily the same value as the repository URL;
#  – generally, the correct value will be the one used by the project in its
#    documentation, coding examples, and build assertions;
#  – use the gopkg import path for all code states when a project uses it.
# If upstream confused itself after multiple forks and renamings, you need to
# fix references to past names in the Go source files, unit tests included. Do
# this fixing in prep.
%global goipath  
#
# gometa is a thin Go-specific wrapper around forgemeta. Therefore, define
# version, tag, commit… before the gometa line, as you would with forgemeta.
# Only define the rpm variables actually needed by the spec file.
# Remember:
#  – to define %forgeurl, including “https://” prefixing, if the import path
#    does not match the repository URL; otherwise it is not necessary,
%global forgeurl 
#  – to move the Version: line before the %gometa call if you are packaging a
#    release.
Version:         
%global tag      
%global commit   
# Like forgemeta, gometa accepts a “-i” flag to output the rpm variables it
# reads and sets. Most of those can be overriden before or after the gometa
# call. If you use “-i” , remove it before committing and pushing to the
# buildsystem.
# See the forgemeta templates for detailed documentation.
%gometa

# A multiline description block shared between subpackages
%global common_description %{expand:
}

# rpm variables used to tweak the generated golang-*devel package.
# Most of them won’t be needed by the average Go spec file.
#
# Space-separated list of Go import paths to include. Unless specified
# otherwise the first element in the list will be used to name the subpackage.
# If unset, defaults to goipath.
%global goipaths       
# Space-separated list of Go import paths to exclude. Usually, subsets of the
# elements in goipaths.
%global goipathsex     
# Force a specific subpackage name. For exemple, when you need to package an
# old code state, you should create a package with the following godevelname:
# compat-%{goname}-<id>-devel. <id> can be a major version number, a
# shortened commit hash, or anything else useful to distinguish the compat
# package. Shortened commits can be computed with:
#global shortcommit %{lua:print(string.sub(rpm.expand("%{?commit}"), 1, 7))}
%global godevelname     
# The subpackage summary;
# (by default, identical to the srpm summary)
%global godevelsummary  
# A container for additional subpackage declarations
%global godevelheader %{expand:
Requires:  
Obsoletes: 
}
# The subpackage base description;
# (by default, “common_description”)
%global godeveldescription %{expand:
}
# Space-separated list of shell globs matching the project license files.
%global golicenses      
# Space-separated list of shell globs matching files you wish to exclude from
# license lists.
%global golicensesex    
# Space-separated list of shell globs matching the project documentation files.
# Our rpm macros will pick up .md files by default without this.
%global godocs          
# Space-separated list of shell globs matching files you wish to exclude from
# documentation lists. Only works for %godocs-specified files.
%global godocsex        
# Space separated list of extentions that should be included in the devel
# package in addition to Go default file extensions
%global goextensions    
# Space-separated list of shell globs matching other files to include in the
# devel package
%global gosupfiles      
# Space-separated list of shell globs matching other files ou wish to exclude from
# package lists. Only works with %gosupfiles-specified files.
%global gosupfilesex    
# The filelist name associated with the subpackage. Setting this should never
# be necessary unless the default name clashes with something else.
%global godevelfilelist 

# The following lines use  go* variables computed by gometa as default values.
# You can replace them with manual definitions. For example, replace gourl with
# the project homepage if it exists separately from the repository URL. Be
# careful to only replace go* variables when it adds value to the specfile and
# you understand the consequences. Otherwise you will just be introducing
# maintenance-intensive discrepancies in the distribution.
#
# When creating a compat package, use compat-%{goname}-<id> like you did for
# “godevelname”.
Name:    %{goname}
# If not set before
Version: 
Release: 1%{?dist}
Summary: 
URL:	 %{gourl}
Source0: %{gosource}
%description
%{common_description}

# Generate package declarations for all known kinds of Go subpackages
# You can replace if with “godevelpkg” to generate Go devel subpackages only
%gopkg

%prep
# goprep unpacks the Go source archives and creates the project GOPATH tree
# used in the rest of the spec file. It removes vendored (bundled) code:
#  – use the “-k” flag if you wish to keep the vendored code, and deal with the
#    consequences in the rest of the spec.
#  – use the “-e” flag if you wish to perform extraction yourself, and just use
#    the GOPATH creation logic.
%goprep
#
# goprep only performs basic vendoring detection. It will miss inventive ways
# to vendor code. Remove manually missed vendor code, after the goprep line.
# goprep will not fix upstream sources for you. Since all the macro calls that
# follow goprep assume clean problem-free sources, you need to correct them
# just after the goprep line:
#  – replace calls to deprecated import paths with their correct value
#  – patch code problems
#  – remove dead code (some upstreams deliberately ship broken source code in
#    the hope someone will get around to fix it)
# Remember to send fixes and problem reports upstream.
# When you package an import path, that participates in a dependency loop, you
# need bootstraping to manage the initial builds:
# https://fedoraproject.org/wiki/Packaging:Guidelines#Bootstrapping
# For Go code, that usually means your bootstrap section should:
#  – remove unit tests that import other parts of the loop
#  – remove code that import other parts of the loop
# Sometimes one can resolve dependency loops just by splitting specific
# subdirectories in a separate -devel subpackage. See also the devel-multi
# template.
#
# https://github.com/rpm-software-management/rpm/issues/104
# The following will eventually be split from goprep
# gobuildrequires computes the build dependencies of the packaged Go code and
# installs them in the build root. Assuming you fixed source problems after
# goprep, it should just work.
# Right now, gobuildrequires only manages version-less Go dependencies. If your
# project requires a specific dependency version, or something which is not Go
# code, you need to declare the corresponding BuildRequires manually as usual.
#gobuildrequires

%install
# Perform installation steps for all known kinds of Go subpackages
# You can replace if with “godevelinstall” to process Go devel subpackages only
%gopkginstall

%check
# gocheck runs all the unit tests found in the project. This is useful to catch
# API breakage early. Unfortunately, the following kinds of unit tests are
# incompatible with a secure build environment:
#  – tests that call a remote server or API over the internet,
#  – tests that attempt to reconfigure the system,
#  – tests that rely on a specific app running on the system, like a database
#    or syslog server.
# You can disable those tests with the following exclusion flags, that can be
# repeated:
#  – “-d <directory>”     exclude the files contained in <directory>
#                         not recursive (subdirectories are not excluded)
#  – “-t <tree root>”     exclude the files contained in <tree root>
#                         recursive (subdirectories are excluded)
#  – “-r <regexp>”        exclude files matching <regexp>,
# If a test is broken for some other reason, you can disable it
# the same way. However, you should also report the problem upstream.
# Tracking why a particular test was disabled gets difficult quickly. Remember
# to add a comments that explain why each check was disabled before gocheck.
%gocheck

# Generate file sections for all known kinds of Go subpackages
# You can replace if with “godevelfiles” to process Go devel subpackages only
%gopkgfiles

%changelog

