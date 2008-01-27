Summary: Security module for the Apache HTTP Server
Name: mod_security 
Version: 2.1.5
Release: 1%{?dist}
License: GPLv2
URL: http://www.modsecurity.org/
Group: System Environment/Daemons
Source: http://www.modsecurity.org/download/modsecurity-apache_%{version}.tar.gz
Source1: mod_security.conf
Source2: modsecurity_localrules.conf
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: libxml2 pcre httpd httpd-mmn = %([ -a %{_includedir}/httpd/.mmn ] && cat %{_includedir}/httpd/.mmn || echo missing)
BuildRequires: httpd-devel libxml2-devel pcre-devel

%description
ModSecurity is an open source intrusion detection and prevention engine
for web applications. It operates embedded into the web server, acting
as a powerful umbrella - shielding web applications from attacks.

%prep

%setup -n modsecurity-apache_%{version}

%build
make -C apache2 CFLAGS="%{optflags}" top_dir="%{_libdir}/httpd"
perl -pi.orig -e 's|LIBDIR|%{_libdir}|;' %{SOURCE1}

%install
rm -rf %{buildroot}
install -D -m755 apache2/.libs/mod_security2.so %{buildroot}/%{_libdir}/httpd/modules/mod_security2.so
install -D -m644 %{SOURCE1} %{buildroot}/%{_sysconfdir}/httpd/conf.d/mod_security.conf
install -d %{buildroot}/%{_sysconfdir}/httpd/modsecurity.d/blocking/
cp -r rules/*.conf %{buildroot}/%{_sysconfdir}/httpd/modsecurity.d/
cp -r rules/blocking/*.conf %{buildroot}/%{_sysconfdir}/httpd/modsecurity.d/blocking/
install -D -m644 %{SOURCE2} %{buildroot}/%{_sysconfdir}/httpd/modsecurity.d/modsecurity_localrules.conf

%clean
rm -rf %{buildroot}

%files
%defattr (-,root,root)
%doc CHANGES LICENSE README.* modsecurity* doc
%{_libdir}/httpd/modules/mod_security2.so
%config(noreplace) %{_sysconfdir}/httpd/conf.d/mod_security.conf
%dir %{_sysconfdir}/httpd/modsecurity.d
%dir %{_sysconfdir}/httpd/modsecurity.d/blocking
%config(noreplace) %{_sysconfdir}/httpd/modsecurity.d/*.conf
%config(noreplace) %{_sysconfdir}/httpd/modsecurity.d/blocking/*.conf


%changelog
* Sat Jan 27 2008 Michael Fleming <mfleming+rpm@enlartenment.com> 2.1.5-1
- Update to 2.1.5 (bz#425986)

* Thu Sep  13 2007 Michael Fleming <mfleming+rpm@enlartenment.com> 2.1.3-1
- Update to 2.1.3
- Update License tag per guidelines.

* Mon Sep  3 2007 Joe Orton <jorton@redhat.com> 2.1.1-3
- rebuild for fixed 32-bit APR (#254241)

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 2.1.1-2
- Rebuild for selinux ppc32 issue.

* Tue Jun 19 2007 Michael Fleming <mfleming+rpm@enlartenment.com> 2.1.1-1
- New upstream release
- Drop ASCIIZ rule (fixed upstream)
- Re-enable protocol violation/anomalies rules now that REQUEST_FILENAME
  is fixed upstream.

* Sun Apr 1 2007 Michael Fleming <mfleming+rpm@enlartenment.com> 2.1.0-3
- Automagically configure correct library path for libxml2 library.
- Add LoadModule for mod_unique_id as the logging wants this at runtime

* Mon Mar 26 2007 Michael Fleming <mfleming+rpm@enlartenment.com> 2.1.0-2
- Fix DSO permissions (bz#233733)

* Tue Mar 13 2007 Michael Fleming <mfleming+rpm@enlartenment.com> 2.1.0-1
- New major release - 2.1.0
- Fix CVE-2007-1359 with a local rule courtesy of Ivan Ristic
- Addition of core ruleset
- (Build)Requires libxml2 and pcre added.

* Sun Sep 3 2006 Michael Fleming <mfleming+rpm@enlartenment.com> 1.9.4-2
- Rebuild
- Fix minor longstanding braino in included sample configuration (bz #203972)

* Mon May 15 2006 Michael Fleming <mfleming+rpm@enlartenment.com> 1.9.4-1
- New upstream release

* Tue Apr 11 2006 Michael Fleming <mfleming+rpm@enlartenment.com> 1.9.3-1
- New upstream release
- Trivial spec tweaks

* Wed Mar 1 2006 Michael Fleming <mfleming+rpm@enlartenment.com> 1.9.2-3
- Bump for FC5

* Fri Feb 10 2006 Michael Fleming <mfleming+rpm@enlartenment.com> 1.9.2-2
- Bump for newer gcc/glibc

* Wed Jan 18 2006 Michael Fleming <mfleming+rpm@enlartenment.com> 1.9.2-1
- New upstream release

* Fri Dec 16 2005 Michael Fleming <mfleming+rpm@enlartenment.com> 1.9.1-2
- Bump for new httpd

* Thu Dec 1 2005 Michael Fleming <mfleming+rpm@enlartenment.com> 1.9.1-1
- New release 1.9.1 

* Wed Nov 9 2005 Michael Fleming <mfleming+rpm@enlartenment.com> 1.9-1
- New stable upstream release 1.9

* Sat Jul 9 2005 Michael Fleming <mfleming+rpm@enlartenment.com> 1.8.7-4
- Add Requires: httpd-mmn to get the appropriate "module magic" version
  (thanks Ville Skytta)
- Disabled an overly-agressive rule or two..

* Sat Jul 9 2005 Michael Fleming <mfleming+rpm@enlartenment.com> 1.8.7-3
- Correct Buildroot
- Some sensible and safe rules for common apps in mod_security.conf

* Thu May 19 2005 Michael Fleming <mfleming+rpm@enlartenment.com> 1.8.7-2
- Don't strip the module (so we can get a useful debuginfo package)

* Thu May 19 2005 Michael Fleming <mfleming+rpm@enlartenment.com> 1.8.7-1
- Initial spin for Extras
