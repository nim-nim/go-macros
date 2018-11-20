# Minimal Go alternative import path packaging template.
#
# Sometimes Go projects keep importing deprecated import path names, or use
# forks with different names. Ideally, all codebases should be fixed to use the
# current canonical import path, but that is not always possible.
#
# This template documents the minimal set of spec declarations, necessary to
# publish alternative Go import paths to other packages. The sister
# “go-3-alternative import-path-full” template documents less common
# declarations; read it if your needs exceed this file.
#
# All the “go-*-” spec templates complement one another without documentation
# overlaps. Try to read them all.
#
# Simulating other import paths prevents the duplicate packaging of the a
# codebase when packagers do not notice an import path has been renamed. It
# keeps spec files that refer to the old name working. Those should still be
# fixed to use the new name as soon as possible.
#
%global goipath  
Version:         
%global tag      
%global commit   
%gometa

%global golicenses      
%global godocs          

# A space-separated list of import paths to simulate. Without this nothing will
# happen.
%global goaltipaths     

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

# Generate package declarations for all known kinds of Go subpackages. You can
# replace if with separate “goaltpkg” and “godevelpkg” calls.
%gopkg

%prep
%goprep
#gobuildrequires

%install
# Perform installation steps for all known kinds of Go subpackages. You can
# replace if with separate “goaltinstall” and “godevelinstall” calls.
%gopkginstall

%check
%gocheck

# Generate file sections for all known kinds of Go subpackages. You can replace
# if with separate “goaltfiles” and “godevelfiles” calls.
%gopkgfiles

%changelog

