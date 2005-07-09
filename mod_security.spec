Summary: Security module for the Apache HTTP Server
Name: mod_security 
Version: 1.8.7
Release: 4%{?dist}
License: GPL
URL: http://www.modsecurity.org/
Group: System Environment/Daemons
Source: http://www.modsecurity.org/download/modsecurity-%{version}.tar.gz
Source1: mod_security.conf
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: httpd  httpd-mmn = %([ -a %{_includedir}/httpd/.mmn ] && cat
%{_includedir}/httpd/.mmn || echo missing)
BuildRequires: httpd-devel

%description
ModSecurity is an open source intrusion detection and prevention engine
for web applications. It operates embedded into the web server, acting
as a powerful umbrella - shielding web applications from attacks.

%prep

%setup -q -n modsecurity-%{version}

%build
/usr/sbin/apxs -Wc,"%{optflags}" -c apache2/mod_security.c

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_libdir}/httpd/modules/
mkdir -p %{buildroot}/%{_sysconfdir}/httpd/conf.d/
install -p apache2/.libs/mod_security.so %{buildroot}/%{_libdir}/httpd/modules/
install -m644 %{SOURCE1} %{buildroot}/%{_sysconfdir}/httpd/conf.d/

%clean
rm -rf %{buildroot}

%files
%defattr (-,root,root)
%doc CHANGES LICENSE INSTALL README httpd* *.pdf util
%{_libdir}/httpd/modules/mod_security.so
%config(noreplace) /etc/httpd/conf.d/mod_security.conf

%changelog
* Sat Jul 9 2005 Michael Fleming <mfleming+rpm@enlartenment.com> 1.8.7-4
- Add Requires: httpd-mmn to get the appropriate "module magic" version
  (thanks Ville Skyttä)
- Disabled an overly-agressive rule or two..

* Sat Jul 9 2005 Michael Fleming <mfleming+rpm@enlartenment.com> 1.8.7-3
- Correct Buildroot
- Some sensible and safe rules for common apps in mod_security.conf

* Thu May 19 2005 Michael Fleming <mfleming+rpm@enlartenment.com> 1.8.7-2
- Don't strip the module (so we can get a useful debuginfo package)

* Thu May 19 2005 Michael Fleming <mfleming+rpm@enlartenment.com> 1.8.7-1
- Initial spin for Extras
