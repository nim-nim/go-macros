# This template documents the packaging of alternative Go import paths. It does
# not repeat the documentation of the usual Go spec elements. To learn about
# those, consult the “go-0-source” template.
#
# Sometimes Go projects keep importing deprecated import path names, or use
# forks with different names. Ideally, all codebases should be fixed to use
# the current canonical import path, but that is not always possible. This
# template shows how to simulate those other names via symbolic links.
#
# The simulation is not perfect, it will fail if parts of the linked codebase
# assert the current canonical name. However it will work just as well as the
# https(s) redirects many Go projects use for the same purpose.
#
# Simulating other import paths prevents the duplicate packaging of the a
# codebase when packagers do not notice an import path has been renamed. It
# keeps spec files that refer to the old name working (even though those should
# be fixed to use the new name as soon as possible).

%global goipath  
%global forgeurl 
Version:         
%global tag      
%global commit   
%gometa

%global common_description %{expand:
}

%global goipaths        
%global goipathsex      
%global godevelname     
%global godevelsummary  
%global godevelheader %{expand:
Requires:  
Obsoletes: 
}
%global golicenses      
%global golicensesex    
%global godocs          
%global godocsex        
%global goextensions    
%global gosupfiles      
%global gosupfilesex    
%global godevelfilelist 

# Space-separated list of import paths to simulate. Without this nothing will happen
%global goaltipaths     
# rpm variables used to tweak the generated compat-golang-*devel packages.
# Most of them won’t be needed by the average Go spec file.
# The import path that will be linked to, if different from “goipath”.
%global gocompatipath   
# The subpackage summary;
# (by default, identical to the srpm summary)
%global gocompatsummary 
# A container for additional subpackage declarations
%global gocompatheader %{expand:
Requires:  
Obsoletes: 
}
# The subpackage base description;
# (by default, “common_description”)
%global gocompatdescription %{expand:
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

# Generate package declarations for all known kinds of Go subpackages
# You can replace if with “gocompatpkg” to generate Go compat subpackages only
%gopkg

%prep
%goprep
#gobuildrequires

%install
# Perform installation steps for all known kinds of Go subpackages
# You can replace if with “gocompatinstall” to process Go compat subpackages only
%gopkginstall

%check
%gocheck

# Generate file sections for all known kinds of Go subpackages
# You can replace if with “gocompatfiles” to process Go compat subpackages only
%gopkgfiles

%changelog

