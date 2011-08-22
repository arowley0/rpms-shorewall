%global mainver 4.4.22
%global baseurl http://www.shorewall.net/pub/shorewall/4.4/shorewall-%{mainver}/

# A very helpful document for packaging Shorewall is "Anatomy of Shorewall 4.0"
# which is found at http://www.shorewall.net/Anatomy.html

Name:           shorewall
Version:        %{mainver}.3
Release:        2%{?dist}.1
Summary:        An iptables front end for firewall configuration
Group:          Applications/System
License:        GPLv2+
URL:            http://www.shorewall.net/
Provides:	shorewall(firewall) = %{version}-%{release}

Source0:        %{baseurl}/%{name}-%{version}.tar.bz2
Source1:        %{baseurl}/%{name}-lite-%{version}.tar.bz2
Source2:        %{baseurl}/%{name}6-%{version}.tar.bz2
Source3:        %{baseurl}/%{name}6-lite-%{version}.tar.bz2
Source4:        %{baseurl}/%{name}-init-%{version}.tar.bz2

# Init file for all sub-packages except shorewall-init
Source10:       shorewall-foo-init.sh

# Init file for shorewall-init
Source11:   	shorewall-init.sh

BuildRequires:  perl
BuildArch:      noarch

Requires:       iptables iproute
Requires(post): /sbin/chkconfig
Requires(preun):/sbin/chkconfig
Requires(preun):/sbin/service

Obsoletes: shorewall-common < 4.3.0
Obsoletes: shorewall-perl < 4.3.0
Obsoletes: shorewall-shell < 4.3.0

%description
The Shoreline Firewall, more commonly known as "Shorewall", is a
Netfilter (iptables) based firewall that can be used on a dedicated
firewall system, a multi-function gateway/ router/server or on a
standalone GNU/Linux system.

%package -n shorewall6
Summary:        Files for the IPV6 Shorewall Firewall
Group:          Applications/System
Provides:	shorewall(firewall) = %{version}-%{release}
Requires:       shorewall = %{version}-%{release}
Requires:       iptables-ipv6 iproute
Requires(post): /sbin/chkconfig
Requires(preun):/sbin/chkconfig
Requires(preun):/sbin/service

%description -n shorewall6
This package contains the files required for IPV6 functionality of the
Shoreline Firewall (shorewall).

%package lite
Summary:        Shorewall firewall for compiled rulesets
Group:          Applications/System
Provides:	shorewall(firewall) = %{version}-%{release}
Requires:       iptables iproute
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/chkconfig
Requires(preun): /sbin/service

%description lite
Shorewall Lite is a companion product to Shorewall that allows network
administrators to centralize the configuration of Shorewall-based
firewalls. Shorewall Lite runs a firewall script generated by a
machine with a Shorewall rule compiler. A machine running Shorewall
Lite does not need to have a Shorewall rule compiler installed.

%package -n shorewall6-lite
Summary:        Shorewall firewall for compiled IPV6 rulesets
Group:          Applications/System
Provides:	shorewall(firewall) = %{version}-%{release}
Requires:       iptables iproute
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/chkconfig
Requires(preun): /sbin/service

%description -n shorewall6-lite
Shorewall6 Lite is a companion product to Shorewall6 (the IPV6
firewall) that allows network administrators to centralize the
configuration of Shorewall-based firewalls. Shorewall Lite runs a
firewall script generated by a machine with a Shorewall rule
compiler. A machine running Shorewall Lite does not need to have a
Shorewall rule compiler installed.

%package init
Summary:    	Initialization functionality and NetworkManager integration for Shorewall
Group:          Applications/System
Requires:	shorewall(firewall) = %{version}-%{release}
Requires:       NetworkManager
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/chkconfig
Requires(preun): /sbin/service

%description init 
This package adds additional initialization functionality to Shorewall in two
ways. It allows the firewall to be closed prior to bringing up network
devices. This insures that unwanted connections are not allowed between the
time that the network comes up and when the firewall is started. It also
integrates with NetworkManager and distribution ifup/ifdown systems to allow
for 'event-driven' startup and shutdown.

%prep
%setup -q -c -n %{name}-%{version} -T -a0 -a1 -a2 -a3 -a4

# Overwrite default init files with Fedora specific ones
cp %{SOURCE10} shorewall-%{version}/init.sh

cp %{SOURCE10} shorewall-lite-%{version}/init.sh
sed -i -e 's|prog="shorewall"|prog="shorewall-lite"|' shorewall-lite-%{version}/init.sh
sed -i -e 's|Provides: shorewall|Provides: shorewall-lite|' shorewall-lite-%{version}/init.sh

cp %{SOURCE10} shorewall6-%{version}/init.sh
sed -i -e 's|prog="shorewall"|prog="shorewall6"|' shorewall6-%{version}/init.sh
sed -i -e 's|Provides: shorewall|Provides: shorewall6|' shorewall6-%{version}/init.sh

cp %{SOURCE10} shorewall6-lite-%{version}/init.sh
sed -i -e 's|prog="shorewall"|prog="shorewall6-lite"|' shorewall6-lite-%{version}/init.sh
sed -i -e 's|Provides: shorewall|Provides: shorewall6-lite|' shorewall6-lite-%{version}/init.sh

cp %{SOURCE11} shorewall-init-%{version}/init.sh

# Remove hash-bang from files which are not directly executed as shell
# scripts. This silences some rpmlint errors.
find . -name "lib.*" -exec sed -i -e '/\#\!\/bin\/sh/d' {} \;

%build

%install
export PREFIX=$RPM_BUILD_ROOT
export DEST=%{_initrddir}
export LIBEXEC=%{_libexecdir}
export PERLLIB=%{perl_privlib}

targets="shorewall-%{version} shorewall-lite-%{version} \
shorewall6-%{version} shorewall6-lite-%{version} \
shorewall-init-%{version}"

for i in $targets; do
    pushd $i
    ./install.sh
    popd
done

# Fix up file permissions
chmod 644 $RPM_BUILD_ROOT%{_datadir}/shorewall-lite/{helpers,modules}
chmod 644 $RPM_BUILD_ROOT%{_datadir}/shorewall6-lite/{helpers,modules}
chmod 755 $RPM_BUILD_ROOT/sbin/shorewall-lite
chmod 755 $RPM_BUILD_ROOT/sbin/shorewall6-lite
chmod 644 $RPM_BUILD_ROOT%{_sysconfdir}/shorewall-lite/shorewall-lite.conf
chmod 644 $RPM_BUILD_ROOT%{_sysconfdir}/shorewall6-lite/shorewall6-lite.conf
chmod 755 $RPM_BUILD_ROOT%{_sysconfdir}/NetworkManager/dispatcher.d/01-shorewall

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ $1 = 1 ]; then
   /sbin/chkconfig --add shorewall
fi

%preun
if [ $1 = 0 ]; then
   /sbin/service shorewall stop >/dev/null 2>&1
   /sbin/chkconfig --del shorewall
   rm -f /var/lib/shorewall/*
fi

%post -n shorewall6
if [ $1 = 1 ]; then
   /sbin/chkconfig --add shorewall6
fi

%preun -n shorewall6
if [ $1 = 0 ]; then
   /sbin/service shorewall6 stop >/dev/null 2>&1
   /sbin/chkconfig --del shorewall6
   rm -f /var/lib/shorewall6/*
fi

%post lite
if [ $1 = 1 ]; then
   /sbin/chkconfig --add shorewall-lite
fi

%preun lite
if [ $1 = 0 ]; then
   /sbin/service shorewall stop >/dev/null 2>&1
   /sbin/chkconfig --del shorewall-lite
   rm -f /var/lib/shorewall-lite/*
fi

%post -n shorewall6-lite
if [ $1 = 1 ]; then
   /sbin/chkconfig --add shorewall6-lite
fi

%preun -n shorewall6-lite
if [ $1 = 0 ]; then
   /sbin/service shorewall6-lite stop >/dev/null 2>&1
   /sbin/chkconfig --del shorewall6-lite
   rm -f /var/lib/shorewall6-lite/*
fi

%post init
if [ $1 = 1 ]; then
   /sbin/chkconfig --add shorewall-init
fi

%preun init
if [ $1 = 0 ]; then
   /sbin/service shorewall-init stop >/dev/null 2>&1
   /sbin/chkconfig --del shorewall-init
fi

%files
%defattr(-,root,root,-)
%doc shorewall-%{version}/{COPYING,changelog.txt,releasenotes.txt,Samples}
%{_initrddir}/shorewall
/sbin/shorewall
%dir %{_sysconfdir}/shorewall
%config(noreplace) %{_sysconfdir}/shorewall/*
%config(noreplace) %{_sysconfdir}/logrotate.d/shorewall
%{_libexecdir}/shorewall
%{_datadir}/shorewall
%{perl_privlib}/Shorewall
%{_mandir}/man5/shorewall*
%exclude %{_mandir}/man5/shorewall6*
%exclude %{_mandir}/man5/shorewall-lite*
%{_mandir}/man8/shorewall*
%exclude %{_mandir}/man8/shorewall6*
%exclude %{_mandir}/man8/shorewall-lite*
%exclude %{_mandir}/man8/shorewall-init*
%dir %{_localstatedir}/lib/shorewall

%files lite
%defattr(-,root,root,-)
%doc shorewall-lite-%{version}/{COPYING,changelog.txt,releasenotes.txt}
%{_initrddir}/shorewall-lite
/sbin/shorewall-lite
%dir %{_sysconfdir}/shorewall-lite
%config(noreplace) %{_sysconfdir}/shorewall-lite/shorewall-lite.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/shorewall-lite
%{_sysconfdir}/shorewall-lite/Makefile
%{_datadir}/shorewall-lite
%{_libexecdir}/shorewall-lite
%{_mandir}/man5/shorewall-lite*
%{_mandir}/man8/shorewall-lite*
%dir %{_localstatedir}/lib/shorewall-lite

%files -n shorewall6
%defattr(-,root,root,-)
%doc shorewall6-%{version}/{COPYING,changelog.txt,releasenotes.txt,Samples6}
%{_initrddir}/shorewall6
/sbin/shorewall6
%dir %{_sysconfdir}/shorewall6
%config(noreplace) %{_sysconfdir}/shorewall6/*
%config(noreplace) %{_sysconfdir}/logrotate.d/shorewall6
%{_mandir}/man5/shorewall6*
%exclude %{_mandir}/man5/shorewall6-lite*
%{_mandir}/man8/shorewall6*
%exclude %{_mandir}/man8/shorewall6-lite*
%{_libexecdir}/shorewall6
%{_datadir}/shorewall6
%dir %{_localstatedir}/lib/shorewall6

%files -n shorewall6-lite
%defattr(-,root,root,-)
%doc shorewall6-lite-%{version}/{COPYING,changelog.txt,releasenotes.txt}
%{_initrddir}/shorewall6-lite
/sbin/shorewall6-lite
%dir %{_sysconfdir}/shorewall6-lite
%config(noreplace) %{_sysconfdir}/shorewall6-lite/shorewall6-lite.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/shorewall6-lite
%{_sysconfdir}/shorewall6-lite/Makefile
%{_mandir}/man5/shorewall6-lite*
%{_mandir}/man8/shorewall6-lite*
%{_datadir}/shorewall6-lite
%{_libexecdir}/shorewall6-lite
%dir %{_localstatedir}/lib/shorewall6-lite

%files init
%defattr(-,root,root,-)
%doc shorewall-init-%{version}/{COPYING,changelog.txt,releasenotes.txt}
%{_initrddir}/shorewall-init
%{_sysconfdir}/NetworkManager/dispatcher.d/01-shorewall
%config(noreplace) %{_sysconfdir}/sysconfig/shorewall-init
%{_mandir}/man8/shorewall-init.8.*
%{_datadir}/shorewall-init
%{_libexecdir}/shorewall-init

%changelog
* Mon Aug 22 2011 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.4.22.3-2.1
- Fix up error in files list

* Mon Aug 22 2011 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.4.22.3-2
- Change file list defattr to (-,root,root,-)
- Fix up file lists and permissions
- Fix up a missing virtual Provides
- Rename _baseurl macro to baseurl

* Sat Aug 20 2011 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.4.22.3-1
- Update to 4.4.22.3
- Remove patches already upstream

* Wed Aug  3 2011 Orion Poplawski <orion@cora.nwra.com> - 4.4.22-2
- Add upstream ALL patch to fix handling zones that begin with 'all'
- Add patch to close stdin to prevent some SELinux denial messages (bug 727648)
- Make libexec files executable

* Tue Aug  2 2011 Orion Poplawski <orion@cora.nwra.com> - 4.4.22-1
- Update to 4.4.22

* Sat Jul 23 2011 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.4.21.1-3.1
- Make files in libexec directory executable

* Thu Jul 21 2011 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.4.21-3
- Properly use PERLLIB environment variable for installation of the perl libraries

* Thu Jul 21 2011 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.4.21-2
- Fix Source URL versioning in spec file

* Thu Jul 21 2011 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.4.21-1
- Update to 4.4.21.1
- Fix BZ 720713 (incorrect init file LSB headers)

* Wed May 25 2011 Orion Poplawski <orion@cora.nwra.com> - 4.4.19.4-1
- Update to 4.4.19.4

* Sat Mar  5 2011 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.4.17-2
- Add executable permission to getparams

* Mon Feb 14 2011 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.4.17-1
- Update to 4.4.17

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.4.11.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Aug  7 2010 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.4.11.1-1
- Update to version 4.4.11.1

* Fri Jul  2 2010 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.4.10-4
- Fix spec file typo

* Wed Jun 16 2010 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.4.10-3
- Remove separate macros for each tarball version - upstream now releases all
  tarballs with the same version number
- Add virtual Provides for shorewall(firewall) to shorewall, shorewall-lite
  and shorewall6-lite, and a Requires shorewall(firewall) to shorewall-init. 
  Note that shorewall6 Requires shorewall, so virtual provides not needed there

* Sun Jun 13 2010 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.4.10-2
- Add doc files to shorewall-lite subpackage

* Sun Jun 13 2010 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.4.10-1
- Update to version 4.4.10
- Add new shorewall-init subpackage
- Rename init.sh to shorewall-foo-init.sh
- Add shorewall-init.sh for init subpackage

* Thu Apr  1 2010 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.4.8-1
- Update to version 4.4.8
- Remove %%buildroot setting
- Remove cleaning of buildroot during %%install
- Fix %%files

* Tue Feb  9 2010 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.4.6-2
- Fix missing man pages in file lists

* Mon Feb  8 2010 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.4.6-1
- Update to version 4.4.6

* Thu Dec 10 2009 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.4.4.2-3
- Fix typo in logrotate script name for shorewall6-lite

* Thu Dec 10 2009 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.4.4.2-2
- Add logrotate files to packages

* Thu Dec 10 2009 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.4.4.2-1
- Update to 4.4.4.2

* Thu Nov  6 2009 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.4.3-1
- Update to 4.4.3

* Thu Sep  3 2009 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.4.1-1
- Update to 4.4.1

* Tue Aug 18 2009 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.4.0-2
- Spec file cleanups with respect to package versioning

* Tue Aug 18 2009 Orion Poplawski <orion@cora.nwra.com> - 4.4.0-1
- Update to 4.4.0 final

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.4.0-0.2.Beta3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul  7 2009 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.4.0-0.1.Beta3
- Update to 4.4.0-Beta3

* Fri Jun 13 2009 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.3.12-3
- Fix filelist for shorewall6 to include macro.Trcrt

* Fri Jun 13 2009 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.3.12-2
- Remove rfc1918 entries from filelists as no longer included

* Thu Jun 12 2009 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.3.12-1
- Update to version 4.3.12
- Change init files to start as number 28 (previously 25) to ensure starting
  after NetworkManager (BZ 505444)

* Wed May 27 2009 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.3.10-2
- Fix up /var/lib directories (BZ 502929)

* Fri May  8 2009 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.3.10-1
- Update to development branch, rearrange sub-packages accordingly
- Remove shorewall-shell, shorewall-perl, shorewall-common subpackages

* Fri May  8 2009 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.2.8-1
- Update to version 4.2.8
- Update shorewall-perl to 4.2.8.2
- Use global instead of define in macros to comply with packaging guidelines

* Mon Apr 13 2009 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.2.7-5
- Update shorewall-perl to version 4.2.7.3

* Fri Apr  3 2009 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.2.7-4
- Update shorewall-perl to version 4.2.7.1 (BZ 493984)

* Thu Mar 26 2009 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.2.7-3
- Really make the perl compiler default

* Tue Mar 24 2009 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.2.7-2
- Make the perl compiler the default. Drop shorewall-shell requirement from
  shorewall package

* Tue Mar 24 2009 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.2.7-1
- Update to version 4.2.7

* Fri Mar  6 2009 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.2.6-2
- Update shorewall-perl to version 4.6.2.2

* Thu Feb 26 2009 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.2.6-1
- Update to version 4.2.6

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Feb  1 2009 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.2.5-2
- Update shorewal-perl to version 4.2.5.1

* Sat Jan 24 2009 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.2.5-1
- Update to version 4.2.5

* Thu Jan 15 2009 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.2.4-4
- Really update shorewall-perl to 4.2.4.6

* Thu Jan 15 2009 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.2.4-3
- Update shorewall-perl to 4.2.4.6

* Thu Jan 15 2009 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.2.4-2
- Fix up dependencies between sub-packages
- No longer attempt to own all files in /var/lib/shorewall* but rather clean
  them up on package removal

* Sun Jan 11 2009 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.2.4-1
- Update to version 4.2.4 which adds IPV6 support and two new sub-packages
  (shorewall6 and shorewall6-lite) 
- Add proper versioning to sub-packages
- Remove patch patch-perl-4.2.3.1

* Tue Dec 30 2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.2.3-2
- Add upstream patch patch-perl-4.2.3.1

* Thu Dec 18 2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.2.3-1
- Update to version 4.2.3

* Mon Nov 24 2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.2.2-1
- Update to version 4.2.2
- Remove patch patch-perl-4.2.1.1

* Fri Oct 31 2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.2.1-2
- Added upstream patch patch-perl-4.2.1.1

* Sun Oct 26 2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.2.1-1
- Update to version 4.2.1
- Correct source URLs

* Sun Oct 12 2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.2.0-1
- Update to version 4.2.0
- New sysv init files which are no longer maintained as patches, but as a 
  Fedora specific file

* Sun Sep 28 2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.0.14-1
- Update to version 4.0.14

* Tue Jul 29 2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.0.13-1
- Update to version 4.0.13
- Remove patch-perl-4.0.12.1
- Update BuildRoot to mktemp variant

* Sat Jul  5 2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.0.12-2
- Apply patch-perl-4.0.12.1 from upstream

* Fri Jun 27 2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.0.12-1
- Update to version 4.0.12

* Sun May 25 2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.0.11-1
- Update to version 4.0.11
- Remove patches for version 4.0.10

* Sun May  4 2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.0.10-2
- Add upstream patches patch-perl-4.0.10-1.diff and patch-common-4.0.10-1.diff

* Sun Apr  6 2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.0.10-1
- Update to version 4.0.10
- Remove 4.0.9 patches

* Tue Mar 25 2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.0.9-2
- Replace patch-perl-4.0,9-1 with patch-perl-4.0.9.1
- Add patch-shell-4.0.9.1

* Thu Feb 28 2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.0.9-1
- Update to version 4.0.9
- Remove 4.0.8 series patches
- Add upstream patch patch-perl-4.0,9-1 (the comma is not a typo)

* Sat Feb 16 2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.0.8-3
- Added patch-perl-4.0.8-3.diff and patch-perl-4.0.8-4.diff patches from
  upstream

* Wed Feb  6 2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.0.8-2
- Add upstream patches patch-perl-4.0.8-1.diff and patch-perl-4.0.8-2.diff

* Sun Jan  27 2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.0.8-1
- Update to version 4.0.8
- Remove 4.0.7 patches

* Sun Jan  6 2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.0.7-2
- Remove 4.0.7.1 patch as it seems that's already been applied to the tarball
  contents

* Sun Jan  6 2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.0.7-2
- Fix error in patching commands in spec file (change -p0 to -p1 for new patches)

* Sun Jan  6 2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.0.7-1
- Update to version 4.0.7
- Added 4.0.7.1 patch and all parts of the 4.0.7.2 patch that are relevant
  (i.e. not the parts working around the iproute2-2.23 bug, as we don't ship the
  broken iproute2)
- Clarified notes about tarball and patch locations

* Sat Dec  8 2007 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.0.6-3
- Added patch-perl-4.0.6-2.diff and patch-perl-4.0.6-3.diff
- Fixed URLs for tarballs to match where upstream has moved them to

* Wed Nov 28 2007 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.0.6-2
- Add Requires for shorewall-common to shorewall-shell and shorewall-perl (Orion
  Poplawski)

* Sat Nov 24 2007 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.0.6-1
- Update to 4.0.6 plus patch-perl-4.0.6-1.diff upstream errata

* Sat Oct 27 2007 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.0.5-1
- Update to 4.0.5 which removes the need for the buildports.pl functionality

* Mon Oct  8 2007 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.0.4-2
- Add ghost files for /var/lib/shorewall/.modules and /var/lib/shorewall/.modulesdir
- Fix ownership of /var/lib/shorewall-lite

* Sun Oct  7 2007 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.0.4-1
- Initial version 4 packaging based upon upstream specs by Tom Eastep and
  version 3 spec by Robert Marcano
- Split into shorewall-common, shorewall-shell, shorewall-perl,
  shorewall-lite subpackages

* Sun Sep 09 2007 Robert Marcano <robert@marcanoonline.com> - 3.4.6-1
- Update to upstream 3.4.6

* Tue Jul 17 2007 Robert Marcano <robert@marcanoonline.com> - 3.4.5-1
- Update to upstream 3.4.5

* Mon Jun 18 2007 Robert Marcano <robert@marcanoonline.com> - 3.4.4-1
- Update to upstream 3.4.4

* Fri May 11 2007 Robert Marcano <robert@marcanoonline.com> - 3.4.3-1
- Update to upstream 3.4.3

* Sun Apr 15 2007 Robert Marcano <robert@marcanoonline.com> - 3.4.2-1
- Update to upstream 3.4.2

* Mon Mar 26 2007 Robert Marcano <robert@marcanoonline.com> - 3.4.1-1
- Update to upstream 3.4.1

* Tue Feb 06 2007 Robert Marcano <robert@marcanoonline.com> - 3.2.8-1
- Update to upstream 3.2.8

* Thu Dec 21 2006 Robert Marcano <robert@marcanoonline.com> - 3.2.7-1
- Update to upstream 3.2.7

* Tue Nov 07 2006 Robert Marcano <robert@marcanoonline.com> - 3.2.5-1
- Update to upstream 3.2.5

* Fri Sep 29 2006 Robert Marcano <robert@marcanoonline.com> - 3.2.4-1
- Update to upstream 3.2.4

* Mon Aug 28 2006 Robert Marcano <robert@marcanoonline.com> - 3.2.3-2
- Rebuild

* Sat Aug 26 2006 Robert Marcano <robert@marcanoonline.com> - 3.2.3-1
- Update to upstream 3.2.3

* Sun Aug 20 2006 Robert Marcano <robert@marcanoonline.com> - 3.2.2-1
- Update to upstream 3.2.2

* Fri Jul 28 2006 Robert Marcano <robert@marcanoonline.com> - 3.2.1-1
- Update to upstream 3.2.1

* Sat Jun 24 2006 Robert Marcano <robert@marcanoonline.com> - 3.2.0-0.1.RC4
- Update to upstream 3.2.0-RC4

* Thu Jun 01 2006 Robert Marcano <robert@marcanoonline.com> - 3.2.0-0.1.Beta8
- Update to upstream 3.2.0-Beta8

* Sun May 14 2006 Robert Marcano <robert@marcanoonline.com> - 3.2.0-0.1.Beta7
- Update to upstream 3.2.0-Beta7

* Fri Apr 14 2006 Robert Marcano <robert@marcanoonline.com> - 3.2.0-0.1.Beta4
- Update to upstream 3.2.0-Beta4

* Fri Mar 31 2006 Robert Marcano <robert@marcanoonline.com> - 3.0.6-1
- Update to upstream 3.0.6

* Mon Feb 13 2006 Robert Marcano <robert@marcanoonline.com> - 3.0.5-1
- Rebuild for Fedora Extras 5, Update to upstream 3.0.5

* Thu Jan 12 2006 Robert Marcano <robert@marcanoonline.com> - 3.0.4-1
- Update to upstream 3.0.4

* Tue Jan 03 2006 Robert Marcano <robert@marcanoonline.com> - 3.0.3-1
- Update to upstream 3.0.3

* Sun Nov 27 2005 Robert Marcano <robert@marcanoonline.com> - 3.0.2-1
- Update to upstream 3.0.2

* Fri Nov 11 2005 Robert Marcano <robert@marcanoonline.com> - 3.0.0-1
- Update to final 3.0.0 release

* Thu Nov 03 2005 Robert Marcano <robert@marcanoonline.com> - 3.0.0-0.3.RC3
- Update to upstream 3.0.0-RC3. Samples added to the doc directory

* Sun Oct 23 2005 Robert Marcano <robert@marcanoonline.com> - 3.0.0-0.3.RC2
- Update to upstream 3.0.0-RC2

* Thu Oct 17 2005 Robert Marcano <robert@marcanoonline.com> - 3.0.0-0.2.RC1
- Update to upstream 3.0.0-RC1

* Thu Oct 14 2005 Robert Marcano <robert@marcanoonline.com> - 3.0.0-0.1.Beta1
- Update to upstream 3.0.0-Beta1, package README.txt as a documentation file

* Sat Oct 08 2005 Robert Marcano <robert@marcanoonline.com> - 2.4.5-1
- Update to upstream version 2.4.5

* Wed Sep 28 2005 Robert Marcano <robert@marcanoonline.com> - 2.4.4-4
- Spec cleanup following review recomendations

* Tue Sep 27 2005 Robert Marcano <robert@marcanoonline.com>
- Update to 2.4.4, removing doc subpackage because it is not distributed
  with the source package anymore, it is on a different tarball

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Tue Nov 11 2003 Miguel Armas <kuko@maarmas.com> - 1.4.8-1.fdr.2
- Clean backup doc files
- Fix some entries in files section

* Mon Nov 10 2003 Miguel Armas <kuko@maarmas.com> - 1.4.8-1.fdr.1
- Upgraded to shorewall 1.4.8

* Fri Oct 31 2003 Miguel Armas <kuko@maarmas.com> - 1.4.7-1.fdr.3.a
- Start shorewall *before* network for better security.
- Added clear command to shorewall init script to run "shorewall clear"
- Changed status command in shorewall init script to run "shorewall status"

* Thu Oct 30 2003 Miguel Armas <kuko@maarmas.com> - 1.4.7-1.fdr.2.a
- Lots of bugfixes in spec file (Thanks to Michael Schwendt)

* Sat Oct 25 2003 Miguel Armas <kuko@maarmas.com> - 1.4.7-1.fdr.1.a
- Fedorized package
- Split documentation in a subpackage (we don't need de docs in a production
  firewall)

