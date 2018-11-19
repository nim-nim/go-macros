# Minimal Go binary packaging template.
#
# This template documents the minimal set of spec declarations, necessary to
# package Go projects that produce binaries. The sister “go-5-binary-full”
# template documents less common declarations; read it if your needs exceed
# this file.
#
# All the “go-*-” spec templates complement one another without documentation
# overlaps. Try to read them all.
#
# Building Go binaries is less automated than the rest of our Go packaging and
# requires more manual work.
#
%global goipath  
Version:         
%global tag      
%global commit   
%gometa

%global _docdir_fmt     %{name}

%global golicenses      
%global godocs          
%global godevelheader %{expand:
# The devel package will usually benefit from corresponding project binaries.
Requires:  %{name} = %{version}-%{release}
Obsoletes:
}

%global common_description %{expand:
}

# If one of the produced binaries is widely known it should be used to name the
# package instead of “goname”. Separate built binaries in different subpackages
# if needed.
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
# You need to identify manually the project parts that can be built, and how to
# name the result. Practically, it’s any directory containing a main() Go
# section. Nice projects put those in “cmd” subdirectories named after the
# command that will be built, which is what we will document here, but it is
# not a general rule. Sometimes the whole “goipath” builds as a single binary.
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

