# A simplified version of “go-0-source”, with only the parts usually needed.
#
# See the “go-0-source” template for detailed documentation.
#
%global goipath  
Version:         
%global tag      
%global commit   
%gometa

%global common_description %{expand:
}

%global golicenses      
%global godocs          

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

