# Complete Go alternative import path packaging template.
#
# This template complements “go-2-alternative import-path-minimal”, with less
# usual spec declarations.
#
# All the “go-*-” spec templates complement one another without documentation
# overlaps. Try to read them all.
#
%global goipath  
%global forgeurl 
Version:         
%global tag      
%global commit   
%global gocid    
%gometa

%global goipaths        
%global goipathsex      
%global godevelcid      
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

%global goaltipaths     
#
# rpm variables used to tweak the generated compat-golang-*devel packages.
# Most of them won’t be needed by the average Go spec file.
#
# The import path that will be linked to.
# (by default, “goipath”)
%global gocanonipath    
# A compatibility id that should be used in the package naming.
# (by default, “gocid”)
%global goaltcid        
# The subpackage summary;
# (by default, “summary”)
%global goaltsummary    
# A container for additional subpackage declarations.
%global goaltheader      %{expand:
Requires:  
Obsoletes: 
}
# The subpackage base description;
# (by default, “common_description”)
%global goaltdescription %{expand:
}

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

