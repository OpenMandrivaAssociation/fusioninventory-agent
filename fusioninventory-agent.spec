%if %{_use_internal_dependency_generator}
%define __noautoreq 'perl\\(Win32(.*)\\)'
%endif

Name:		fusioninventory-agent
Version:	2.1.9
Release:	6
Summary:	Linux agent for OCSNG
License:	GPL
Group:		System/Servers
URL:		http://fusioninventory.org/wordpress/
Source0:	http://search.cpan.org/CPAN/authors/id/F/FU/FUSINV/FusionInventory-Agent-%{version}.tar.gz
Source1:	%{name}.service
Source100:	%{name}.rpmlintrc
BuildArch:  noarch
Requires:	perl-Net-SSLeay
BuildRequires: perl-devel

%description
FusionInventory-Agent is an agent for OCS NG & GLPI.

%prep
%setup -q -n FusionInventory-Agent-%{version}

%build
%__perl Makefile.PL INSTALLDIRS=vendor
%make

%install
rm -f run-postinst
%makeinstall_std

install -d -m 755 %{buildroot}%{_sysconfdir}/cron.daily
cat > %{buildroot}%{_sysconfdir}/cron.daily/fusioninventory-agent <<EOF
#!/bin/sh
. /etc/sysconfig/fusioninventory-agent
%{_bindir}/fusioninventory-agent --no-ssl-check --server="\${SERVER}" > /dev/null 2>&1
EOF
chmod 755 %{buildroot}%{_sysconfdir}/cron.daily/fusioninventory-agent

install -d -m 755 %{buildroot}%{_sysconfdir}/logrotate.d
cat > %{buildroot}%{_sysconfdir}/logrotate.d/fusioninventory-agent <<EOF
%{_localstatedir}/log/%{name}/*.log {
    compress
    notifempty
    missingok
}
EOF

install -d -m 755 %{buildroot}%{_sysconfdir}/sysconfig
cat > %{buildroot}%{_sysconfdir}/sysconfig/fusioninventory-agent <<EOF
SERVER="localhost"
EOF

install -d -m 755 %{buildroot}%{_unitdir}
install -m 755 %{SOURCE1} %{buildroot}%{_unitdir}/fusioninventory-agent.service

install -d -m 755 %{buildroot}%{_localstatedir}/log/%{name}
install -d -m 755 %{buildroot}%{_localstatedir}/lib/%{name}

%files
%doc AUTHORS Changes THANKS LICENSE
%{_bindir}/fusioninventory-agent
%{_bindir}/fusioninventory-agent-config
%{_bindir}/fusioninventory-injector
%{_mandir}/man1/*
%{_mandir}/man3/*
%{perl_vendorlib}/FusionInventory
%{perl_vendorlib}/auto/share/dist/FusionInventory-Agent
%{_localstatedir}/log/fusioninventory-agent
%{_localstatedir}/lib/fusioninventory-agent
%config(noreplace) %{_sysconfdir}/sysconfig/fusioninventory-agent
%config(noreplace) %{_sysconfdir}/logrotate.d/fusioninventory-agent
%config(noreplace) %{_sysconfdir}/cron.daily/fusioninventory-agent
%{_unitdir}/fusioninventory-agent.service
