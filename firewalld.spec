Summary:	A dynamic firewall daemon
Name:		firewalld
Version:	2.3.1
Release:	1
License:	GPLv2+
Group:		System/Base
URL:		https://github.com/t-woerner/firewalld/
Source0:	https://github.com/firewalld/firewalld/releases/download/v%{version}/%{name}-%{version}.tar.bz2
Source1:	%{name}.rpmlintrc
# (tpg) try to keep nfs and samba enabled for default zones
Patch1:		firewalld-0.3.13-enable-nfs-and-samba.patch
BuildArch:	noarch
BuildRequires:	desktop-file-utils
BuildRequires:	gettext
BuildRequires:	intltool
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	docbook-style-xsl
BuildRequires:	xsltproc
BuildRequires:	pkgconfig(python3)
BuildRequires:	ipset
BuildRequires:	iptables
BuildRequires:	ebtables
BuildRequires:	systemd-rpm-macros
BuildRequires:	docbook-dtd42-xml
Requires:	python-dbus
Requires:	iptables-nft
Requires:	ipset
Requires:	python-nftables > 0.9.2-1
Requires:	typelib(NM)
Requires:	python3dist(pygobject)
Recommends:	python-libcap-ng
Conflicts:	firewall-config < 0.9.3-2
%systemd_requires

%description
A firewall service daemon with D-BUS interface managing a dynamic firewall.

%package -n firewall-applet
Summary:	Firewall panel applet
Group:		System/Base
Requires:	%{name} = %{EVRD}
Requires:	firewall-config = %{EVRD}
Requires:	hicolor-icon-theme
Requires:	python-sip-qt5
Requires:	python-qt5-core
Requires:	python-qt5-dbus
Requires:	python-qt5-gui
Requires:	python-qt5-widgets
Requires:	python-sip
Requires:	typelib(Notify)
Requires:	typelib(GdkPixbuf)

%description -n firewall-applet
The firewall panel applet provides a status information of %{name} and also
the firewall settings.

%package -n firewall-config
Summary:	Firewall configuration application
Group:		System/Base
Requires:	%{name} = %{EVRD}
Requires:	hicolor-icon-theme
Recommends:	polkit

%description -n firewall-config
The firewall configuration application provides an configuration interface for
%{name}.

%package -n firewalld-test
Summary:	Firewalld testsuite
Group:		System/Base
Requires:	%{name} = %{EVRD}

%description -n firewalld-test            
This package provides the firewalld testsuite.

%prep
%autosetup -p1

%build
./autogen.sh
%configure \
    --enable-sysconfig \
    --with-systemd-unitdir=%{_unitdir}

# no make
cd doc
%make_build
cd ..

%install
%make_install

# (tpg) use desktop policy by default
rm -rf %{buildroot}%{_datadir}/polkit-1/actions/org.fedoraproject.FirewallD1.policy
ln -sf org.fedoraproject.FirewallD1.desktop.policy.choice %{buildroot}%{_datadir}/polkit-1/actions/org.fedoraproject.FirewallD1.policy

install -d %{buildroot}%{_presetdir}
cat > %{buildroot}%{_presetdir}/86-firewalld.preset << EOF
enable firewalld.service
EOF

desktop-file-install --delete-original \
  --dir %{buildroot}%{_sysconfdir}/xdg/autostart \
  %{buildroot}%{_sysconfdir}/xdg/autostart/firewall-applet.desktop

desktop-file-install --delete-original \
  --dir %{buildroot}%{_datadir}/applications \
  %{buildroot}%{_datadir}/applications/firewall-config.desktop

# (tpg) not needed
rm -rf %{buildroot}%{_datadir}/zsh

rm -rf %{buildroot}%{_prefix}/lib/firewalld/services/kodi-eventserver.xml

%find_lang %{name} --all-name

%triggerin -- %{_prefix}/lib/firewalld/services/*.xml
%{_bindir}/firewall-cmd --reload --quiet || :

%triggerun -- %{_prefix}/lib/firewalld/services/*.xml
%{_bindir}/firewall-cmd --reload --quiet || :

%post
%systemd_post firewalld.service

%preun
%systemd_preun firewalld.service

%postun
%systemd_postun_with_restart firewalld.service

%files -f %{name}.lang
%{_presetdir}/86-firewalld.preset
%{_sbindir}/%{name}
%{_bindir}/firewall-cmd
%{_bindir}/firewall-offline-cmd
%dir %{_datadir}/bash-completion/completions
%{_datadir}/bash-completion/completions/firewall-cmd
%dir %{_prefix}/lib/%{name}
%dir %{_prefix}/lib/%{name}/helpers
%dir %{_prefix}/lib/%{name}/icmptypes
%dir %{_prefix}/lib/%{name}/ipsets
%dir %{_prefix}/lib/%{name}/services
%dir %{_prefix}/lib/%{name}/zones
%{_prefix}/lib/%{name}/helpers/*.xml
%{_prefix}/lib/%{name}/icmptypes/*.xml
%{_prefix}/lib/%{name}/ipsets/README.md
%{_prefix}/lib/%{name}/services/*.xml
%{_prefix}/lib/%{name}/zones/*.xml
%{_prefix}/lib/firewalld/xmlschema/
%{_prefix}/lib/firewalld/policies/allow-host-ipv6.xml
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
#config(noreplace) %{_sysconfdir}/%{name}/lockdown-whitelist.xml
%dir %{_sysconfdir}/%{name}/icmptypes
%dir %{_sysconfdir}/%{name}/services
%dir %{_sysconfdir}/%{name}/zones
%{_sysconfdir}/logrotate.d/firewalld
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_sysconfdir}/modprobe.d/*.conf
%{_unitdir}/%{name}.service
%{_datadir}/dbus-1/system.d/FirewallD.conf
%{_datadir}/polkit-1/actions/org.fedoraproject.FirewallD1.policy
%{_datadir}/polkit-1/actions/org.fedoraproject.FirewallD1.desktop.policy.choice
%{_datadir}/polkit-1/actions/org.fedoraproject.FirewallD1.server.policy.choice
%dir %{python_sitelib}/firewall
%dir %{python_sitelib}/firewall/config
%dir %{python_sitelib}/firewall/core
%dir %{python_sitelib}/firewall/core/io
%dir %{python_sitelib}/firewall/server
%{python_sitelib}/firewall/*.py*
%{python_sitelib}/firewall/config/*.py*
%{python_sitelib}/firewall/core/*.py*
%{python_sitelib}/firewall/core/io/*.py*
%{python_sitelib}/firewall/server/*.py*
%doc %{_mandir}/man1/firewall*cmd*.1*
%doc %{_mandir}/man1/%{name}*.1*
%doc %{_mandir}/man5/firewall*.5*

%files -n firewall-applet
%{_bindir}/firewall-applet
%{_sysconfdir}/xdg/autostart/firewall-applet.desktop
%{_sysconfdir}/firewall/applet.conf
%{_datadir}/icons/hicolor/*/apps/firewall-applet*.*
%doc %{_mandir}/man1/firewall-applet*.1*

%files -n firewall-config
%{_bindir}/firewall-config
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/firewall-config.glade
%{_datadir}/%{name}/gtk3_chooserbutton.py*
%{_datadir}/%{name}/gtk3_niceexpander.py
%{_datadir}/applications/firewall-config.desktop
%{_datadir}/icons/hicolor/*/apps/firewall-config*.*
%{_datadir}/glib-2.0/schemas/org.fedoraproject.FirewallConfig.gschema.xml
%{_datadir}/metainfo/firewall-config.appdata.xml
%doc %{_mandir}/man1/firewall-config*.1*

%files -n firewalld-test
%dir %{_datadir}/firewalld/testsuite
%{_datadir}/firewalld/testsuite/testsuite
%{_datadir}/firewalld/testsuite/README.md
%dir %{_datadir}/firewalld/testsuite/integration
%{_datadir}/firewalld/testsuite/integration/testsuite
%dir %{_datadir}/firewalld/testsuite/python
%{_datadir}/firewalld/testsuite/python/firewalld_config.py
%{_datadir}/firewalld/testsuite/python/firewalld_direct.py
%{_datadir}/firewalld/testsuite/python/firewalld_rich.py
%{_datadir}/firewalld/testsuite/python/firewalld_misc.py
