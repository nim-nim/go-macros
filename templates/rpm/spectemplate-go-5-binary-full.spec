# Complete Go binary packaging template.
#
# This template complements “go-5-binary-minimal”, with less usual spec
# declarations.
#
# All the “go-*-” spec templates complement one another without documentation
# overlaps. Try to read them all
#
%global goipath  
%global forgeurl 
Version:         
%global tag      
%global commit   
%global gocid    
%gometa

%global _docdir_fmt     %{name}

%global goipaths        
%global goipathsex      
%global godevelcid      
%global godevelname     
%global godevelsummary  
%global godevelheader %{expand:
Requires:  %{name} = %{version}-%{release}
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
%global gocannonipath   
%global goaltcid        
%global goaltsummary    
%global goaltheader      %{expand:
Requires:  
Obsoletes: 
}
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

%build
for cmd in cmd/* ; do
  %gobuild -o %{gobuilddir}/bin/$(basename $cmd) %{goipath}/$cmd
done

%install
%gopkginstall
install -m 0755 -vd                     %{buildroot}%{_bindir}
install -m 0755 -vp %{gobuilddir}/bin/* %{buildroot}%{_bindir}/

%check
%gocheck

%files
%license %{golicenses}
%doc     
%{_bindir}/*

%gopkgfiles

%changelog

