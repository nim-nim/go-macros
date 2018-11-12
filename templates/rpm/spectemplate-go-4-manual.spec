# This template documents old-style semi-manual Go packaging. This packaging
# mode provides the most packager control and is adapted to highly peculiar
# projects that do not fit in automated processing. However, the result is also
# more complex to get right and to maintain.
#
# Using this packaging mode is not recommended unless you really need it.
#
# This template does not repeat the documentation of the usual Go spec
# elements. To learn about those, consult the “go-0-source” template.
#
%global goipath  
%global forgeurl 
Version:         
%global tag      
%global commit   
%gometa

%global common_description %{expand:
}

Name:    %{goname}
# If not set before
Version: 
Release: 1%{?dist}
Summary: 
URL:	 %{gourl}
Source0: %{gosource}
%description
%{common_description}

%prep
%goprep
#gobuildrequires

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

%changelog

