# This template documents old-style semi-manual Go packaging. This packaging
# mode provides the most packager control. However, the result is also more
# difficult to get right and to maintain.
#
# Using this packaging mode is not recommended unless you really need it. If
# you prepare your sources correctly in prep you should not need it.
#
# All the “go-*-” spec templates complement one another without documentation
# overlaps. Try to read them all..
#
%global goipath  
%global forgeurl 
Version:         
%global tag      
%global commit   
%gometa

# Old naming of the same project
%global oldgoipath xxxx
%global oldgoname  %gorpmname %{oldgoipath}

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

%package -n %{goname}-devel
Summary: %{summary}

# If the package builds some binaries
Requires:  %{name} = %{version}-%{release}

%description -n %{goname}-devel
%{common_description}

This package contains the source code needed for building packages that
reference the following Go import paths:
 –  %{goipath}

# If you’ve defined an alternative go name
%package -n compat-%{oldgoname}-devel
Summary:   %{summary}
Obsoletes: %{oldgoname}-devel < %{version}-%{release}

%description -n compat-%{oldgoname}-devel
%{common_description}

This package provides symbolic links that alias the following Go import paths
to %{goipath}:
 – %{oldgoipath}

Aliasing Go import paths via symbolic links or http redirects is fragile. If
your Go code depends on this package, you should patch it to import directly
%{goipath}.

%prep
%goprep
%gobuildrequires

%install
# goinstall is our Go source installation workhorse. It accepts a huge and
# bewildering array of arguments. Most of those have good default values,
# changing them is more likely to compound existing spec problems than fix
# anything.
#
# Selection arguments, that can not be repeated:
#  – “-a”                  process everything
#  – “-z <number>”         process a specific declaration block
#  – “-i <go import path>” use the specified import path value
#                          default: %{goipath<number>}
#
# If no “-a”, “-z” or “-i ”flag is specified goinstall will only process the
# zero/nosuffix Go import path.
#
# Miscellaneous settings:
#  – “-b <bindir>”         read binaries already produced in <bindir>
#                          default: %{gobuilddir}/bin
#  – “-s <sourcedir>”      read expanded and prepared Go sources in
#                          <sourcedir>/src
#                          <sourcedir> should be populated in %prep
#                          default: %{gobuilddir}
#  – “-o <filename>”       output installed file list in <filename>
#                          default: %{gofilelist<number>}
#  – “-O <directory>”      output <filename> in <directory>
#  – “-l <ldflags>”        add those flags to LDFLAGS when building unit tests
#  – “-v”                  be verbose
#
# Inclusion arguments, that can be repeated:
#  – “-e <extension>”      include files with the provided extension
#
# Exclusion ar²guments, that can be repeated, relative to the go import path
# root:
#  – “-d <directory>”      exclude the files contained in <directory>
#                          not recursive (subdirectories are not excluded)
#  – “-t <tree root>”      exclude the files contained in <tree root>
#                          recursive (subdirectories are excluded)
#  – “-r <regexp>”         exclude files matching <regexp>,
#
# Optional versionning metadata, that can not be repeated:
#  – “-V <version>”        should only be specified when creating subpackages
#                          with distinct versions. Excellent tool for producing
#                          broken packages.
#                          default: %{version}.%{release}
#  – “-T <tag>”            default: %{tag<number>}
#  – “-C <commit>”         default: %{commit<number>}
#  – “-B <branch>”         default: %{branch<number>}
#
%goinstall
#
# Old name aliasing
install -m 0755 -vd %{buildroot}%{gopath}/src/%(dirname %{oldgoipath})
ln -s %{gopath}/src/%{goipath} %{buildroot}%{gopath}/src/%{oldgoipath}
#
install -m 0755 -vd                     %{buildroot}%{_bindir}
install -m 0755 -vp %{gobuilddir}/bin/* %{buildroot}%{_bindir}/

%check
%gocheck

%files
%license 
%{_bindir}/*

%files -n %{goname}-devel -f %{gofilelist}

%files -n compat-%{oldgoname}-devel
# You need as many of those as necessary to own the levels of directories
# between %{gopath}/src and %{gopath}/src/%{oldgoipath}, that are not already
# owned by the %{goname}-devel subpackage
%dir %{gopath}/src/%(dirname %(dirname %{oldgoipath}))
%dir %{gopath}/src/%(dirname %{oldgoipath})
%{gopath}/src/%{oldgoipath}

%changelog

