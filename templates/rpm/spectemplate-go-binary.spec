# This template documents the packaging of Go projects that produce binaries.
# It does not repeat the documentation of the usual Go spec elements. To learn
# about those, consult the “go-source” and “go-alternative-import-path”
# templates.
#
# Building Go binaries is less automated than the rest of our Go packaging and
# requires more packager manual work.
#
%global goipath  
%global forgeurl 
Version:         
%global tag      
%global commit   
%gometa

%global common_description %{expand:
}

%global goipathes       
%global goipathesex     
%global godevelname     
%global godevelsummary  
%global godevelheader %{expand:
# The devel package will usually benefit from corresponding project binaries.
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

%global goaltipathes     
%global gocompatipath    
%global gocompatsummary  
%global gocompatheader %{expand:
Requires:  
Obsoletes: 
}
%global gocompatdescription %{expand:
}

# If one of the produced binaries is well known it should be used to name the
# package instead of “goname”. Separate built binaries in different subpackages
# if needed.
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
# You need to identify manually the project parts that can be built.
# Practically, it’s any directory containing a main() Go section. You need to
# identify how the resulting binary should be named.
# Nice projects put those in “cmd” subdirectories named after the command that
# will be built, which is what we will document here, but it is not a general
# rule.
for cmd in cmd/* ; do
  %gobuild -o %{gobuilddir}/bin/$(basename $cmd) %{goipath}/$cmd
done

%install
# Perform installation steps for all known kinds of Go subpackages
# You can replace if with “gocompatinstall” to process Go compat subpackages only
%gopkginstall
install -m 0755 -vd                     %{buildroot}%{_bindir}
install -m 0755 -vp %{gobuilddir}/bin/* %{buildroot}%{_bindir}/

%check
%gocheck

%files
%license 
%doc     
%{_bindir}/*

%gopkgfiles

%changelog

