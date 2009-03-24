# A very helpful document for packaging Shorewall is "Anatomy of Shorewall 4.0"
# which is found at http://www.shorewall.net/Anatomy.html

%define major_ver 4.2.7
%define common_ver %{major_ver}
%define perl_ver %{major_ver}
%define lite_ver %{major_ver}
%define shell_ver %{major_ver}
%define shorewall6_ver %{major_ver}
%define lite6_ver %{major_ver}

Name:           shorewall
Version:        %{major_ver}
Release:        1%{?dist}
Summary:        An iptables front end for firewall configuration
Group:          Applications/System
License:        GPLv2+
URL:            http://www.shorewall.net/

%define _baseurl http://www.shorewall.net/pub/shorewall/4.2/shorewall-%{version}/base
Source0:        %{_baseurl}/%{name}-common-%{common_ver}.tar.bz2
Source1:        %{_baseurl}/%{name}-perl-%{perl_ver}.tar.bz2
Source2:        %{_baseurl}/%{name}-shell-%{shell_ver}.tar.bz2
Source3:        %{_baseurl}/%{name}-lite-%{lite_ver}.tar.bz2
Source4:        %{_baseurl}/%{name}6-%{shorewall6_ver}.tar.bz2
Source5:        %{_baseurl}/%{name}6-lite-%{lite6_ver}.tar.bz2

# Init file for Fedora
Source10:       init.sh

BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires:  perl
BuildArch:      noarch

Requires:       shorewall-common = %{common_ver}-%{release}
Requires:       shorewall-perl = %{perl_ver}-%{release}
Requires:       shorewall-shell = %{shell_ver}-%{release}

%description
The Shoreline Firewall, more commonly known as "Shorewall", is a
Netfilter (iptables) based firewall that can be used on a dedicated
firewall system, a multi-function gateway/ router/server or on a
standalone GNU/Linux system.

%package common
Summary:        Common files for the shorewall firewall compilers
Group:          Applications/System
Version:        %{common_ver}
Requires:       iptables iproute
Requires(post): /sbin/chkconfig
Requires(preun):/sbin/chkconfig
Requires(preun):/sbin/service

%description common
This package contains files required by both the shorewall-perl and
shorewall-shell compilers for the Shoreline Firewall (shorewall).

%package -n shorewall6
Summary:        Files for the IPV6 Shorewall Firewall
Group:          Applications/System
Version:        %{shorewall6_ver}
Requires:       shorewall-perl = %{perl_ver}-%{release}
Requires:       iptables-ipv6 iproute
Requires(post): /sbin/chkconfig
Requires(preun):/sbin/chkconfig
Requires(preun):/sbin/service

%description -n shorewall6
This package contains the files required for IPV6 functionality of the
Shoreline Firewall (shorewall).

%package perl
Summary:        Perl-based compiler for Shoreline Firewall 
Group:          Applications/System
Version:        %{perl_ver}
Requires:       shorewall-common = %{common_ver}-%{release}
Requires:       perl

%description perl
shorewall-perl is a part of Shorewall that allows faster compilation
and execution than the legacy shorewall-shell compiler.

%package shell
Summary:        Shell-based compiler for Shoreline Firewall 
Group:          Applications/System
Version:        %{shell_ver}
Requires:       shorewall-common = %{common_ver}-%{release}

%description shell
Shorewall-shell is a part of Shorewall that allows running Shorewall
with legacy configurations, but shorewall-perl is the preferred
compiler, please use it for new installations.

%package lite
Group:          Applications/System
Summary:        Shorewall firewall for compiled rulesets
Version:        %{lite_ver}
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
Group:          Applications/System
Summary:        Shorewall firewall for compiled IPV6 rulesets
Version:        %{lite6_ver}
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

%prep
%setup -q -c -n shorewall-%{major_ver}
%setup -q -T -D -a 1
%setup -q -T -D -a 2
%setup -q -T -D -a 3
%setup -q -T -D -a 4
%setup -q -T -D -a 5

# Overwrite default init files with Fedora specific ones
cp %{SOURCE10} shorewall-common-%{common_ver}

cp %{SOURCE10} shorewall-lite-%{lite_ver}
sed -i -e 's|prog="shorewall"|prog="shorewall-lite"|' shorewall-lite-%{lite_ver}/init.sh

cp %{SOURCE10} shorewall6-%{shorewall6_ver}
sed -i -e 's|prog="shorewall"|prog="shorewall6"|' shorewall6-%{shorewall6_ver}/init.sh

cp %{SOURCE10} shorewall6-lite-%{lite6_ver}
sed -i -e 's|prog="shorewall"|prog="shorewall6-lite"|' shorewall6-lite-%{lite6_ver}/init.sh

# Remove hash-bang from files which are not directly executed as shell
# scripts. This silences some rpmlint errors.
find . -name "lib.*" -exec sed -i -e '/\#\!\/bin\/sh/d' {} \;

%build

%install
rm -rf $RPM_BUILD_ROOT

export PREFIX=$RPM_BUILD_ROOT
export DEST=%{_initrddir}

#### Build shorewall-common
pushd shorewall-common-%{common_ver}
./install.sh
popd

#### Build shorewall-perl
pushd shorewall-perl-%{perl_ver}
./install.sh -n
popd

#### Build shorewall-shell
pushd shorewall-shell-%{shell_ver}
./install.sh -n
popd

#### Build shorewall-lite
pushd shorewall-lite-%{lite_ver}
./install.sh -n
popd

#### Build shorewall6
pushd shorewall6-%{shorewall6_ver}
./install.sh -n
popd

#### Build shorewall6-lite
pushd shorewall6-lite-%{lite6_ver}
./install.sh -n
popd

%clean
rm -rf $RPM_BUILD_ROOT

%post common
if [ $1 = 1 ]; then
   /sbin/chkconfig --add shorewall
fi

%preun common
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

%files
%defattr(-,root,root,-)

%files common
%defattr(0644,root,root,0755)
%doc shorewall-common-%{common_ver}/{COPYING,changelog.txt,releasenotes.txt,Samples}
%attr(0755,root,root) %{_initrddir}/shorewall
%attr(0755,root,root) /sbin/shorewall
%dir %{_sysconfdir}/shorewall
%config(noreplace) %{_sysconfdir}/shorewall/*

%dir %{_datadir}/shorewall
%attr(0755,root,root) %{_datadir}/shorewall/firewall
%attr(0755,root,root) %{_datadir}/shorewall/wait4ifup
%{_datadir}/shorewall/action.*
%{_datadir}/shorewall/actions.std
%{_datadir}/shorewall/configpath
%{_datadir}/shorewall/macro.*
%{_datadir}/shorewall/rfc1918
%{_datadir}/shorewall/version
%{_datadir}/shorewall/modules
%{_datadir}/shorewall/configfiles
%{_datadir}/shorewall/functions
%{_datadir}/shorewall/lib.*
%dir %{_localstatedir}/lib/shorewall

# Man files - can't use /man5/* here as shorewall-lite also has man5 pages
%{_mandir}/man5/shorewall-tunnels.5.gz
%{_mandir}/man5/shorewall-nat.5.gz
%{_mandir}/man5/shorewall-proxyarp.5.gz
%{_mandir}/man5/shorewall-vardir.5.gz
%{_mandir}/man5/shorewall-accounting.5.gz
%{_mandir}/man5/shorewall-policy.5.gz
%{_mandir}/man5/shorewall-route_rules.5.gz
%{_mandir}/man5/shorewall-providers.5.gz
%{_mandir}/man5/shorewall-modules.5.gz
%{_mandir}/man5/shorewall-tcrules.5.gz
%{_mandir}/man5/shorewall-params.5.gz
%{_mandir}/man5/shorewall-zones.5.gz
%{_mandir}/man5/shorewall.conf.5.gz
%{_mandir}/man5/shorewall-blacklist.5.gz
%{_mandir}/man5/shorewall-tcclasses.5.gz
%{_mandir}/man5/shorewall-rfc1918.5.gz
%{_mandir}/man5/shorewall-routestopped.5.gz
%{_mandir}/man5/shorewall-rules.5.gz
%{_mandir}/man5/shorewall-actions.5.gz
%{_mandir}/man5/shorewall-tos.5.gz
%{_mandir}/man5/shorewall-ecn.5.gz
%{_mandir}/man5/shorewall-nesting.5.gz
%{_mandir}/man5/shorewall-exclusion.5.gz
%{_mandir}/man5/shorewall-masq.5.gz
%{_mandir}/man5/shorewall-hosts.5.gz
%{_mandir}/man5/shorewall-tcdevices.5.gz
%{_mandir}/man5/shorewall-tcfilters.5.gz
%{_mandir}/man5/shorewall-netmap.5.gz
%{_mandir}/man5/shorewall-interfaces.5.gz
%{_mandir}/man5/shorewall-maclist.5.gz
%{_mandir}/man5/shorewall-notrack.5.gz
%{_mandir}/man8/shorewall.8.gz

%files perl
%defattr(0644,root,root,0755)
%doc shorewall-perl-%{perl_ver}/{COPYING,releasenotes.txt}
%dir %{_datadir}/shorewall-perl
%dir %{_datadir}/shorewall-perl/Shorewall
%attr(755,root,root) %{_datadir}/shorewall-perl/compiler.pl
%{_datadir}/shorewall-perl/prog.*
%{_datadir}/shorewall-perl/version
%{_datadir}/shorewall-perl/Shorewall/*.pm

%files shell
%defattr(0644,root,root,0755)
%doc shorewall-shell-%{shell_ver}/COPYING
%attr(0755,root,root) %dir %{_datadir}/shorewall-shell
%attr(0755,root,root) %{_datadir}/shorewall-shell/compiler
%{_datadir}/shorewall-shell/lib.*
%{_datadir}/shorewall-shell/prog.*
%{_datadir}/shorewall-shell/version

%files lite
%defattr(0644,root,root,0755)
%doc shorewall-lite-%{lite_ver}/{COPYING,changelog.txt,releasenotes.txt}
%attr(0755,root,root) /sbin/shorewall-lite
%dir %{_sysconfdir}/shorewall-lite
%config(noreplace) %{_sysconfdir}/shorewall-lite/shorewall-lite.conf
%{_sysconfdir}/shorewall-lite/Makefile
%attr(0755,root,root) %{_initrddir}/shorewall-lite
%dir %{_localstatedir}/lib/shorewall-lite
%dir %{_datadir}/shorewall-lite
%{_datadir}/shorewall-lite/version
%{_datadir}/shorewall-lite/configpath
%{_datadir}/shorewall-lite/functions
%{_datadir}/shorewall-lite/lib.*
%{_datadir}/shorewall-lite/modules
%attr(0755,root,root) %{_datadir}/shorewall-lite/shorecap
%attr(0755,root,root) %{_datadir}/shorewall-lite/wait4ifup
%{_mandir}/man5/shorewall-lite.conf.5.gz
%{_mandir}/man5/shorewall-lite-vardir.5.gz
%{_mandir}/man8/shorewall-lite.8.gz

%files -n shorewall6
%defattr(0644,root,root,0755)
%doc shorewall6-%{shorewall6_ver}/{COPYING,changelog.txt,releasenotes.txt,Samples6}
%attr(0755,root,root) %{_initrddir}/shorewall6
%attr(0755,root,root) /sbin/shorewall6
%dir %{_sysconfdir}/shorewall6
%config(noreplace) %{_sysconfdir}/shorewall6/*

# Man files - can't use wildcard as shorewall6-lite also installs some man files
%{_mandir}/man5/shorewall6-accounting.5.gz
%{_mandir}/man5/shorewall6-actions.5.gz
%{_mandir}/man5/shorewall6-blacklist.5.gz
%{_mandir}/man5/shorewall6-exclusion.5.gz
%{_mandir}/man5/shorewall6-hosts.5.gz
%{_mandir}/man5/shorewall6-interfaces.5.gz
%{_mandir}/man5/shorewall6-maclist.5.gz
%{_mandir}/man5/shorewall6-modules.5.gz
%{_mandir}/man5/shorewall6-nesting.5.gz
%{_mandir}/man5/shorewall6-params.5.gz
%{_mandir}/man5/shorewall6-policy.5.gz
%{_mandir}/man5/shorewall6-providers.5.gz
%{_mandir}/man5/shorewall6-route_rules.5.gz
%{_mandir}/man5/shorewall6-routestopped.5.gz
%{_mandir}/man5/shorewall6-rules.5.gz
%{_mandir}/man5/shorewall6-tcclasses.5.gz
%{_mandir}/man5/shorewall6-tcdevices.5.gz
%{_mandir}/man5/shorewall6-tcrules.5.gz
%{_mandir}/man5/shorewall6-tos.5.gz
%{_mandir}/man5/shorewall6-tunnels.5.gz
%{_mandir}/man5/shorewall6-vardir.5.gz
%{_mandir}/man5/shorewall6-zones.5.gz
%{_mandir}/man5/shorewall6.conf.5.gz
%{_mandir}/man5/shorewall6-notrack.5.gz
%{_mandir}/man8/shorewall6.8.gz

%attr(0755,root,root) %{_datadir}/shorewall6/wait4ifup
%{_datadir}/shorewall6/action.*
%{_datadir}/shorewall6/actions.std
%{_datadir}/shorewall6/configfiles
%{_datadir}/shorewall6/configpath
%{_datadir}/shorewall6/functions
%{_datadir}/shorewall6/lib.*
%{_datadir}/shorewall6/macro.Ping
%{_datadir}/shorewall6/modules
%{_datadir}/shorewall6/version
%dir %{_localstatedir}/lib/shorewall

%files -n shorewall6-lite
%defattr(0644,root,root,0755)
%doc shorewall6-lite-%{lite6_ver}/{COPYING,changelog.txt,releasenotes.txt}
%attr(0755,root,root) /sbin/shorewall6-lite
%dir %{_sysconfdir}/shorewall6-lite
%config(noreplace) %{_sysconfdir}/shorewall6-lite/shorewall6-lite.conf
%attr(0755,root,root) %{_initrddir}/shorewall6-lite
%{_sysconfdir}/shorewall6-lite/Makefile
%dir %{_localstatedir}/lib/shorewall
%{_mandir}/man5/shorewall6-lite-vardir.5.gz
%{_mandir}/man5/shorewall6-lite.conf.5.gz
%{_mandir}/man8/shorewall6-lite.8.gz
%{_datadir}/shorewall6-lite/configpath
%{_datadir}/shorewall6-lite/functions
%{_datadir}/shorewall6-lite/lib.*
%{_datadir}/shorewall6-lite/modules
%{_datadir}/shorewall6-lite/version
%attr(0755,root,root) %{_datadir}/shorewall6-lite/shorecap
%attr(0755,root,root) %{_datadir}/shorewall6-lite/wait4ifup

%changelog
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

