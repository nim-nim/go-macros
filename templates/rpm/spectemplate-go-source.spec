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

# gometa is a thin Go-specific wrapper around forgemeta. Therefore, define
# version, tag, commit… before the gometa line, as you would with forgemeta.
# Remember:
#  – to define %forgeurl, including “https://” prefixing, if the import path
#    does not match the repository URL;
#  – to move the Version: line before the %gometa call if you are packaging a
#    release.
# Like forgemeta, gometa accepts a “-i” flag to output the rpm variables it
# reads and sets. Most of those can be overriden before or after the gometa
# call. If you use “-i” , remove it before committing and pushing to the
# buildsystem.
# See the forge templates for more forgemeta documentation.
#global forgeurl 
#Version:        
#global tag      
#global commit   
%gometa

# The following lines use  go* variables computed by gometa as default values.
# You can replace them with manual definitions. For example, replace gourl with
# the project homepage if it exists separately from the repository URL. Be
# careful to only replace go* variables when it adds value to the specfile and
# you understand the consequences. Otherwise you will just be introducing
# maintenance-intensive discrepancies in the distribution.
Name:    %{goname}
Version: 
Release: 1%{?dist}
Summary: 
URL:	 %{gourl}
Source0: %{gosource}
%description


%prep
# goprep unpacks the Go source archives and creates the project GOPATH tree
# used in the rest of the spec file. It removes vendored (bundled) code:
#  – use the “-k” flag if you wish to keep the vendored code, and deal with the
#    consequences in the rest of the spec.
#  – use the “-e” flag if you wish to perform extraction yourself, and just use
#    the GOPATH creation logic.
# goprep only performs basic vendoring detection. It will miss inventive ways
# to vendor code. Remove manually missed vendor code, after the goprep line.
# goprep will not fix upstream sources for you. Since the macro call that
# follows goprep will start processing those sources, you need to correct them
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
# subdirectories in a separate -devel subpackage.
%goprep
# https://github.com/rpm-software-management/rpm/issues/104
# gobuildrequires computes the build dependencies of the packaged Go code and
# installs them in the build root. Assuming you fixed source problems after
# goprep, it should just work.
# Right now, gobuildrequires only manages version-less Go dependencies. If your
# project requires a specific dependency version, or something which is not Go
# code, you need to write the corresponding BuildRequires line manually.
%gobuildrequires

%install
%goinstall

%check
# gocheck runs all the unit tests found in the project. This is useful to catch
# API breakage early. Unfortunately, the following kinds of unit tests are
# incompatible with a secure build environment:
#  – tests that call a remote server or API over the internet,
#  – tests that attempt to reconfigure the system,
#  – tests that rely on a specific app running on the system, like a database
#    or syslog server.
# You can disable those tests with the same “-d” “-t” “-r” exclusion flags
# goinstall uses. If a test is broken for some other reason, you can disable it
# the same way. However, you should also report the problem upstream.
# Tracking why a particular test was disabled gets difficult quickly. Remember
# to add a comments that explain why each check was disabled before gocheck.
%gocheck

%files
%doc



%changelog

