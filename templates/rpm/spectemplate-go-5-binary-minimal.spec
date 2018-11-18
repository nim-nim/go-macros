# A simplified version of “go-4-binary”, with only the parts usually needed.
#
# See the “go-4-binary” template for detailed documentation.
#
%global goipath  
Version:         
%global tag      
%global commit   
%gometa

%global _docdir_fmt     %{name}

%global common_description %{expand:
}

%global golicenses      
%global godocs          

Name:    %{goname}
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
%license 
%doc     
%{_bindir}/*

%gopkgfiles

%changelog

