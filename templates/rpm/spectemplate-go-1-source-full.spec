# Complete Go source code packaging template
#
# This template complements “go-0-source-minimal”, with less usual spec
# declarations. Common declarations are documented in “go-0-source-minimal”.
%global goipath  
Version:         
%global tag      
%global commit   
#
# A compatibility id that should be used in the package naming. It will change
# the generated “goname” to something derived from
# compat-golang-goipath-gocid-devel.
# “gocids” are used to disambiguate compatibility packages from the package
# tracking the recommended distribution version. Usual values:
#  – the version major (if different),
#  – a shortened commit tag such as
#    %{lua:print(string.sub(rpm.expand("%{?commit}"), 1, 7))}
%global gocid    
%gometa

# rpm variables used to tweak the generated golang-*devel package.
# Most of them won’t be needed by the average Go spec file.
#
# A space-separated list of Go import paths to include. Unless specified
# otherwise the first element in the list will be used to name the subpackage.
# (by default, “goipath”)
%global goipaths        
# A space-separated list of Go import paths to exclude. Usually, subsets of the
# elements in goipaths.
%global goipathsex      
# A compatibility id that should be used in the package naming.
# (by default, “gocid”)
%global godevelcid      
# A value that will replace the computed subpackage name.
# (by default “gorpmname-devel”)
%global godevelname     
# The subpackage summary.
# (by default, “summary”)
%global godevelsummary  
# A container for additional subpackage declarations.
%global godevelheader %{expand:
Requires:  
Obsoletes: 
}
# The subpackage base description.
# (by default, “common_description”)
%global godeveldescription %{expand:
}
%global golicenses      
# A space-separated list of shell globs matching files you wish to exclude from
# license lists.
%global golicensesex    
%global godocs          
# A space-separated list of shell globs matching files you wish to exclude from
# documentation lists. Only works for “godocs”-specified files.
%global godocsex        
# A space separated list of extentions that should be included in the devel
# package in addition to Go default file extensions.
%global goextensions    
# A space-separated list of shell globs matching other files to include in the
# devel package.
%global gosupfiles      
# A space-separated list of shell globs matching other files ou wish to exclude from
# package lists. Only works with “gosupfiles”-specified files.
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

