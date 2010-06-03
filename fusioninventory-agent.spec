Name:		fusioninventory-agent
Version:	2.0.6
Release:	%mkrel 1
Summary:	Linux agent for OCSNG
License:	GPL
Group:		System/Servers
URL:		http://fusioninventory.org/wordpress/
Source0:	http://search.cpan.org/CPAN/authors/id/F/FU/FUSINV/FusionInventory-Agent-%{version}.tar.gz
Source1:	%{name}.init
Patch0:     FusionInventory-Agent-2.0.6-fix-syslog-usage.patch
Patch1:     FusionInventory-Agent-2.0.6-add-bios-informations-for-xen-pv-hosts.patch
BuildArch:  noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
FusionInventory-Agent is an agent for OCS NG & GLPI.

%prep
%setup -q -n FusionInventory-Agent-%{version}
%patch0 -p 1
%patch1 -p 1

%build
%__perl Makefile.PL INSTALLDIRS=vendor
%make

%install
rm -rf  %{buildroot}
rm -f run-postinst
%makeinstall_std

install -d -m 755 %{buildroot}%{_sysconfdir}/cron.daily
cat > %{buildroot}%{_sysconfdir}/cron.daily/fusioninventory-agent <<EOF
#!/bin/sh
%{_bindir}/fusioninventory-agent > /dev/null 2>&1
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

install -d -m 755 %{buildroot}%{_initrddir}
install -m 755 %{SOURCE1} %{buildroot}%{_initrddir}/fusioninventory-agent

install -d -m 755 %{buildroot}%{_localstatedir}/log/%{name}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS Changes README THANKS LICENSE
%{_bindir}/fusioninventory-agent
%{_bindir}/fusioninventory-agent-config
%{_mandir}/man1/*
%{_mandir}/man3/*
%{perl_vendorlib}/FusionInventory
%{_localstatedir}/log/fusioninventory-agent
%config(noreplace) %{_sysconfdir}/sysconfig/fusioninventory-agent
%config(noreplace) %{_sysconfdir}/logrotate.d/fusioninventory-agent
%config(noreplace) %{_sysconfdir}/cron.daily/fusioninventory-agent
%{_initrddir}/fusioninventory-agent

