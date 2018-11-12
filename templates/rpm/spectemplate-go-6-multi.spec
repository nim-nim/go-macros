# This template documents advanced Go packaging with multiples of everything.
# Don’t try it before you understand how simpler Go packaging is done.
#
# Don’t hesitate to use “rpmspec -P <specfile>” to check the generated code.
#
# It does not repeat the documentation of the usual Go spec elements. To learn
# about those, consult the “go-0-source”, “go-2-alternative-import-path” and
# “go-4-binary” templates.
#
# You can refer to several upstream archives using the “-a” gometa flag and
# blocks of declarations suffixed by a block number, like with forgemeta.
# No suffix or zero suffix refers to the main archive. Refer to the forge-multi
# template for more detailed information.
# IT IS A TERRIBLE IDEA TO TRY THIS UNLESS EVERY SOURCE ARCHIVE IS PERFECTLY
# VERSION-LOCKED WITH THE OTHERS. That will produce broken rpm versionning and
# broken upgrade paths right and left. It is always simpler and safer to
# package separate projects with separate spec files.
#
# Main archive
%global goipath0  
%global forgeurl0 
Version:          
%global tag0      
%global commit0   
#
# Second archive
%global goipath1  
%global forgeurl1 
%global version1  
%global tag1      
%global commit1   
#
# Continue as necessary…
#
# Alternatively, you can use the “-z <number>” gometa argument to process a
# specific declaration block only.
%gometa -a

%global _docdir_fmt     %{name}

%global common_description %{expand:
}

# Likewise, you can declare several devel subpackages, either one by source
# archive or with any other import path layout.
#
# First golang-*-devel subpackage.
#
# If unset, and no “goipathes<number>” is defined in the spec, fallbacks to
# “goipath<number>”
%global goipathes0       
%global goipathesex0     
%global godevelname0     
%global godevelsummary0  
%global godevelheader0 %{expand:
Requires:  
Obsoletes: 
}
%global golicenses0      
%global golicensesex0    
%global godocs0          
%global godocsex0        
%global goextensions0    
%global gosupfiles0      
%global gosupfilesex0    
%global godevelfilelist0 
#
# Second golang-*-devel subpackage.
%global goipathes1       
%global goipathesex1     
%global godevelname1     
%global godevelsummary1  
%global godevelheader1 %{expand:
Requires:  
Obsoletes: 
}
%global golicenses1      
%global golicensesex1    
%global godocs1          
%global godocsex1        
%global goextensions1    
%global gosupfiles1      
%global gosupfilesex1    
%global godevelfilelist1 
#
# Continue as necessary…


# Likewise, you can declare several alternative name sets that will generate
# the corresponding compat-golang-*-devel subpackages
#
# First compat-golang-*-devel subpackage set.
%global goaltipathes0     
# If unset, and no “gocompatipath<number>” is defined in the spec, fallbacks to
# “goipath<number>”
%global gocompatipath0    
%global gocompatsummary0  
%global gocompatheader0 %{expand:
Requires:  
Obsoletes: 
}
%global gocompatdescription0 %{expand:
}
#
# Second compat-golang-*-devel subpackage set.
%global goaltipathes1     
# If unset, and no “gocompatipath<number>” is defined in the spec, fallbacks to
# “goipath<number>”
%global gocompatipath1    
%global gocompatsummary1  
%global gocompatheader1 %{expand:
Requires:  
Obsoletes: 
}
%global gocompatdescription1 %{expand:
}
#
# Continue as necessary…

# Use usual naming rules when generating binaries.
Name:    %{goname}
# If not set before
Version: 
Release: 1%{?dist}
Summary: 
URL:	 %{gourl}
# One for each of the previous goipath blocks
Source0: %{gosource0}
Source1: %{gosource1}
# …
%description
%{common_description}

# “gopkg” will generate all the subpackages package declarations corresponding
# to the elements declared above.
# You can replace “gopkg” with “godevelpkg” and “gocompatpkg” calls for finer
# control.
# “godevelpkg” and “gocompatpkg” accept the usual selection arguments:
# – “-a”          process everything
# – “-z <number>” process a specific declaration block
# If no flag is specified they only process the zero/nosuffix block.
%gopkg

%prep
# “%goprep” and “gobuildrequires” accept the usual selection arguments:
# – “-a”          process everything
# – “-z <number>” process a specific declaration block
# If no flag is specified they only process the zero/nosuffix block.
%goprep -a
#gobuildrequires -a

%build
# When your spec processes multiple Go source archives, you need to call
# “goenv” with the correct “-z <number>” argument before invoquing “%gobuild”.
# Otherwise the binaries risk being built with parameters corresponding to
# another source archive.
for cmd in cmd/* ; do
  %gobuild -o %{gobuilddir}/bin/$(basename $cmd) %{goipath}/$cmd
done

%install
# You can replace “gopkginstall” with  “godevelinstall” and “gocompatinstall”
# calls for finer control.
# “gopkginstall” and “godevelinstall” accept the usual selection arguments:
# – “-a”          process everything
# – “-z <number>” process a specific declaration block
# If no flag is specified they only process the zero/nosuffix block.
%gopkginstall

install -m 0755 -vd                     %{buildroot}%{_bindir}
install -m 0755 -vp %{gobuilddir}/bin/* %{buildroot}%{_bindir}/

%check
%gocheck

%files
%license 
%doc     
%{_bindir}/*

# You can replace “gopkgfiles” with  “godevelfiles” and  “gocompatfiles”
# calls for finer control.
# “godevelfiles” and “gocompatfiles” accept the usual selection arguments:
# – “-a”          process everything
# – “-z <number>” process a specific declaration block
# If no flag is specified they only process the zero/nosuffix block.
%gopkgfiles

%changelog
