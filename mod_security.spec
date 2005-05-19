Summary: Security module for the Apache HTTP Server
Name: mod_security 
Version: 1.8.7
Release: 1%{?dist}
License: GPL
URL: http://www.modsecurity.org/
Group: System Environment/Daemons
Source: http://www.modsecurity.org/download/modsecurity-1.8.7.tar.gz
Source1: mod_security.conf
BuildRoot: %{_tmppath}/%{name}-root/
Requires: httpd >= 2.0.38
BuildRequires: httpd-devel >= 2.0.38

%description
ModSecurity is an open source intrusion detection and prevention engine for web
applications. It operates embedded into the web server, acting as a powerful
umbrella - shielding web applications from attacks.

%prep

%setup -q -n modsecurity-%{version}

%build
/usr/sbin/apxs -Wc,"%{optflags}" -c apache2/mod_security.c

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_libdir}/httpd/modules/
mkdir -p %{buildroot}/%{_sysconfdir}/httpd/conf.d/
install -s -p apache2/.libs/mod_security.so %{buildroot}/%{_libdir}/httpd/modules/
install -m644 %{SOURCE1} %{buildroot}/%{_sysconfdir}/httpd/conf.d/

%clean
rm -rf %{buildroot}

%files
%defattr (-,root,root)
%doc CHANGES LICENSE INSTALL README httpd* *.pdf util
%{_libdir}/httpd/modules/mod_security.so
%config(noreplace) /etc/httpd/conf.d/mod_security.conf

%changelog
* Thu May 19 2005 Michael Fleming <mfleming+rpm@enlartenment.com> 1.8.7-1
- Initial spin for Extras
