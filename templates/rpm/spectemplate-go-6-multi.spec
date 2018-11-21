# This template documents advanced Go packaging with multiples of everything.
# Don’t try it before you understand how simpler Go packaging is done.
#
# All the “go-*-” spec templates complement one another without documentation
# overlaps. Try to read them all.
#
# Don’t hesitate to use “rpmspec -P <specfile>” to check the generated code.
#
# You can refer to several upstream archives using the “-a” “gometa” flag and
# blocks of declarations suffixed by a block number, like with “forgemeta”.
# No suffix or zero suffix refers to the main archive. Refer to the forge-multi
# template for more detailed information.
# IT IS A TERRIBLE IDEA TO TRY THIS UNLESS EVERY SOURCE ARCHIVE IS PERFECTLY
# VERSION-LOCKED WITH THE OTHERS. That will produce broken rpm versionning and
# broken upgrade paths. It is always simpler and safer to package separate
# projects with separate spec files.
#
# Main archive
%global goipath0  
%global forgeurl0 
Version:          
%global tag0      
%global commit0   
%global gocid0    
#
# Second archive
%global goipath1  
%global forgeurl1 
%global version1  
%global tag1      
%global commit1   
%global gocid1    
#
# Continue as necessary…
#
# Alternatively, you can use the “-z <number>” “gometa” argument to process a
# specific declaration block only.
%gometa -a

%global _docdir_fmt     %{name}

# Likewise, you can declare several devel subpackages, either one by source
# archive or with any other import path layout.
#
# First golang-*-devel subpackage.
#
# If unset, and no “goipaths<number>” is defined in the spec, fallbacks to
# “goipath<number>”
%global goipaths0        
%global goipathsex0      
%global godevelcid0      
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
%global goipaths1        
%global goipathsex1      
%global godevelcid1      
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
%global goaltipaths0      
# If unset, and no “gocanonipath<number>” is defined in the spec, fallbacks to
# “goipath<number>”
%global gocanonipath0     
%global goaltsummary0     
%global goaltheader0      %{expand:
Requires:  
Obsoletes: 
}
%global goaltdescription0 %{expand:
}
#
# Second compat-golang-*-devel subpackage set.
%global goaltipaths1      
%global gocanonipath1     
%global goaltsummary1     
%global goaltheader1      %{expand:
Requires:  
Obsoletes: 
}
%global goaltdescription1 %{expand:
}
#
# Continue as necessary…

%global common_description %{expand:
}

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
# You can replace “gopkg” with “godevelpkg” and “goaltpkg” calls for finer
# control.
# “godevelpkg” and “goaltpkg” accept the usual selection arguments:
# – “-a”          process everything
# – “-z <number>” process a specific declaration block
# If no flag is specified they only process the zero/nosuffix block.
%gopkg

%prep
# “%goprep” and “gogenbr” accept the usual selection arguments:
# – “-a”          process everything
# – “-z <number>” process a specific declaration block
# If no flag is specified they only process the zero/nosuffix block.
%goprep -a
%gogenbr -a

%build
# When your spec processes multiple Go source archives, you need to call
# “goenv” with the correct “-z <number>” argument before invoquing “%gobuild”.
# Otherwise the binaries risk being built with parameters corresponding to
# another source archive.
for cmd in cmd/* ; do
  %gobuild -o %{gobuilddir}/bin/$(basename $cmd) %{goipath}/$cmd
done

%install
# You can replace “gopkginstall” with  “godevelinstall” and “goaltinstall”
# calls for finer control.
# “godevelinstall” and “goaltinstall” accept the usual selection arguments:
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

# You can replace “gopkgfiles” with  “godevelfiles” and  “goaltfiles”
# calls for finer control.
# “godevelfiles” and “goaltfiles” accept the usual selection arguments:
# – “-a”          process everything
# – “-z <number>” process a specific declaration block
# If no flag is specified they only process the zero/nosuffix block.
%gopkgfiles

%changelog

