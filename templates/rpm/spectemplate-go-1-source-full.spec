# Exhaustive Go source code packaging template
#
# This template complements the “go-0-source-minimal” template with less common
# declarations. The documentation provided in “go-0-source-minimal” is not
# repeated here, you should read this file first.
#
%global goipath  
Version:         
%global tag      
%global commit   
#
# A compatibility id that should be used in the package naming. It will change
# the generated name to something derived from
# compat-golang-goipath-gocid-devel.
# Used to disambiguate compatibility packages from the package tracking the
# recommended distribution version. Recommanded values:
#  – the version major (if differen),
#  – a shortened commit tag such as
#    %{lua:print(string.sub(rpm.expand("%{?commit}"), 1, 7))} etc
%global gocid    
%gometa

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
# A compatibility id that should be used in the package naming, if different
# from “gocid”.
%global godevelcid      
# Force a specific subpackage name.
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
%global golicenses      
# Space-separated list of shell globs matching files you wish to exclude from
# license lists.
%global golicensesex    
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

%global common_description %{expand:
}

Name:    %{goname}
# If not set before
Version: 
Release: 1%{?dist}
Summary: 
URL:	   %{gourl}
Source0: %{gosource}
%description
%{common_description}

%gopkg

%prep
%goprep
#gobuildrequires

%install
%gopkginstall

%check
%gocheck

%gopkgfiles

%changelog

