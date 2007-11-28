# A very helpful document for packaging Shorewall is "Anatomy of Shorewall 4.0"
# which is found at http://www.shorewall.net/Anatomy.html

Name:           shorewall
Version:	4.0.6
Release:	2%{?dist}
Summary:	An iptables front end for firewall configuration
Group:		Applications/System
License:	GPLv2+
URL:		http://www.shorewall.net/

Source0: 	http://www.shorewall.net/pub/shorewall/4.0/shorewall-%{version}/shorewall-common-%{version}.tar.bz2
Source1: 	http://www.shorewall.net/pub/shorewall/4.0/shorewall-%{version}/shorewall-perl-%{version}.tar.bz2
Source2: 	http://www.shorewall.net/pub/shorewall/4.0/shorewall-%{version}/shorewall-shell-%{version}.tar.bz2
Source3: 	http://www.shorewall.net/pub/shorewall/4.0/shorewall-%{version}/shorewall-lite-%{version}.tar.bz2
Patch0: 	shorewall-4.0.4-init.patch
Patch1: 	shorewall-lite-4.0.4-init.patch
Patch2:		patch-perl-4.0.6-1.diff

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	perl
BuildArch:	noarch


Requires:	shorewall-common = %{version}-%{release}
Requires:	shorewall-perl = %{version}-%{release}
Requires:	shorewall-shell = %{version}-%{release}

%description
The Shoreline Firewall, more commonly known as "Shorewall", is a
Netfilter (iptables) based firewall that can be used on a dedicated
firewall system, a multi-function gateway/ router/server or on a
standalone GNU/Linux system.

%package common
Summary:	Common files for the shorewall firewall compilers
Group: 		Applications/System
Requires: 	iptables iproute
Requires(post): /sbin/chkconfig
Requires(preun):/sbin/chkconfig
Requires(preun):/sbin/service

%description common
This package contains files required by both the shorewall-perl and
shorewall-shell compilers for the Shoreline Firewall (shorewall).

%package perl
Summary:	Perl-based compiler for Shoreline Firewall 
Group: 	 	Applications/System
Requires:	shorewall-common = %{version}-%{release}
Requires:	perl

%description perl
shorewall-perl is a part of Shorewall that allows faster compilation
and execution than the legacy shorewall-shell compiler.

%package shell
Summary:	Shell-based compiler for Shoreline Firewall 
Group: 	 	Applications/System
Requires:	shorewall-common = %{version}-%{release}

%description shell
Shorewall-shell is a part of Shorewall that allows running Shorewall
with legacy configurations, but shorewall-perl is the preferred
compiler, please use it for new installations.

%package lite
Group: 	 	Applications/System
Summary:	Shorewall firewall for compiled rulesets
Requires: 	iptables iproute
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/chkconfig
Requires(preun): /sbin/service

%description lite
Shorewall Lite is a companion product to Shorewall that allows network
administrators to centralize the configuration of Shorewall-based
firewalls. Shorewall Lite runs a firewall script generated by a
machine with a Shorewall rule compiler. A machine running Shorewall
Lite does not need to have a Shorewall rule compiler installed.

%prep
%setup -q -c -n shorewall-%{version}
%setup -q -T -D -a 1
%setup -q -T -D -a 2
%setup -q -T -D -a 3

pushd shorewall-common-%{version}
%patch0 -p1
popd

pushd shorewall-lite-%{version}
%patch1 -p1
popd

pushd shorewall-perl-%{version}
%patch2 -p0

# Remove hash-bang from files which are not directly executed as shell
# scripts. This silences some rpmlint errors.
find . -name "lib.*" -exec sed -i -e '/\#\!\/bin\/sh/d' {} \;

%build

%install
rm -rf $RPM_BUILD_ROOT

export PREFIX=$RPM_BUILD_ROOT
export DEST=%{_initrddir}

#### Build shorewall-common
pushd shorewall-common-%{version}
./install.sh
popd

# Create %ghost files
install -d $RPM_BUILD_ROOT/%{_localstatedir}/lib/shorewall
touch $RPM_BUILD_ROOT/%{_localstatedir}/lib/shorewall/{chains,nat,proxyarp,restarted,zones,restore-base,restore-tail,state,.modules,.modulesdir}

#### Build shorewall-perl
pushd shorewall-perl-%{version}
./install.sh -n
popd

#### Build shorewall-shell
pushd shorewall-shell-%{version}
./install.sh -n
popd

#### Build shorewall-lite
pushd shorewall-lite-%{version}
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
fi

%post lite
if [ $1 = 1 ]; then
   /sbin/chkconfig --add shorewall-lite
fi

%preun lite
if [ $1 = 0 ]; then
   /sbin/service shorewall stop >/dev/null 2>&1
   /sbin/chkconfig --del shorewall-lite
fi

%files
%defattr(-,root,root,-)

%files common
%defattr(0644,root,root,0755)
%doc shorewall-common-%{version}/{COPYING,changelog.txt,releasenotes.txt,Samples}
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
%ghost %{_localstatedir}/lib/shorewall/*
%ghost %{_localstatedir}/lib/shorewall/.*

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
%{_mandir}/man5/shorewall-netmap.5.gz
%{_mandir}/man5/shorewall-interfaces.5.gz
%{_mandir}/man5/shorewall-maclist.5.gz
%{_mandir}/man8/shorewall.8.gz

%files perl
%defattr(0644,root,root,0755)
%doc shorewall-perl-%{version}/{COPYING,releasenotes.txt}
%dir %{_datadir}/shorewall-perl
%dir %{_datadir}/shorewall-perl/Shorewall
%attr(755,root,root) %{_datadir}/shorewall-perl/compiler.pl
%{_datadir}/shorewall-perl/prog.*
%{_datadir}/shorewall-perl/version
%{_datadir}/shorewall-perl/Shorewall/*.pm

%files shell
%defattr(0644,root,root,0755)
%doc shorewall-shell-%{version}/COPYING
%attr(0755,root,root) %dir %{_datadir}/shorewall-shell
%attr(0755,root,root) %{_datadir}/shorewall-shell/compiler
%{_datadir}/shorewall-shell/lib.*
%{_datadir}/shorewall-shell/prog.*
%{_datadir}/shorewall-shell/version

%files lite
%defattr(0644,root,root,0755)
%doc shorewall-lite-%{version}/{COPYING,changelog.txt,releasenotes.txt}
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

%changelog
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

