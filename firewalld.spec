%define _disable_rebuild_configure 1

Summary:	A dynamic firewall daemon
Name:		firewalld
Version:	0.6.3
Release:	4
URL:		https://github.com/t-woerner/firewalld/
License:	GPLv2+
Group:		System/Base
Source0:	https://github.com/firewalld/firewalld/archive/v%{version}.tar.gz
Source1:	%{name}.rpmlintrc
Patch0:		firewalld-0.2.6-MDNS-default.patch
# (tpg) try to keep nfs and samba enabled for default zones
Patch1:		firewalld-0.3.13-enable-nfs-and-samba.patch
# Make sure firewalld is started after interfaces are up
Patch2:		firewalld-0.5.3-start-after-NetworkManager.patch
BuildArch:	noarch
BuildRequires:	desktop-file-utils
BuildRequires:	gettext
BuildRequires:	intltool
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(libsystemd)
BuildRequires:	docbook-style-xsl
BuildRequires:	xsltproc
BuildRequires:	pkgconfig(python3)
BuildRequires:	ipset
BuildRequires:	iptables
BuildRequires:	ebtables
BuildRequires:	nftables
BuildRequires:	systemd-macros
Requires:	python-dbus
Requires:	python-slip-dbus >= 0.2.7
Requires:	python-decorator
Requires:	iptables >= 1.4.21-11
Requires:	ebtables
Requires:	nftables
Requires:	ipset
Requires:	typelib(NM)
Requires(post,preun):	rpm-helper

%description
A firewall service daemon with D-BUS interface managing a dynamic firewall.

%package -n firewall-applet
Summary:	Firewall panel applet
Group:		System/Base
Requires:	%{name} = %{EVRD}
Requires:	firewall-config = %{EVRD}
Requires:	hicolor-icon-theme
Requires:	python-qt5-core
Requires:	python-qt5-dbus
Requires:	python-qt5-gui
Requires:	python-qt5-widgets
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
Requires:	typelib(NetworkManager)

%description -n firewall-config
The firewall configuration application provides an configuration interface for
%{name}.

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

%find_lang %{name} --all-name

%triggerin -- %{_prefix}/lib/firewalld/services/*.xml
%{_bindir}/firewall-cmd --reload --quiet || :

%triggerun -- %{_prefix}/lib/firewalld/services/*.xml
%{_bindir}/firewall-cmd --reload --quiet || :

%files -f %{name}.lang
%doc README
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
%{_prefix}/lib/%{name}/ipsets/README
%{_prefix}/lib/%{name}/services/*.xml
%{_prefix}/lib/%{name}/zones/*.xml
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%config(noreplace) %{_sysconfdir}/%{name}/lockdown-whitelist.xml
%dir %{_sysconfdir}/%{name}/icmptypes
%dir %{_sysconfdir}/%{name}/services
%dir %{_sysconfdir}/%{name}/zones
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_sysconfdir}/modprobe.d/*.conf
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/FirewallD.conf
%{_datadir}/polkit-1/actions/org.fedoraproject.FirewallD1.policy
%dir %{python_sitelib}/firewall
%dir %{python_sitelib}/firewall/config
%dir %{python_sitelib}/firewall/core
%dir %{python_sitelib}/firewall/core/io
%dir %{python_sitelib}/firewall/server
%{python_sitelib}/firewall/*.py*
%{python_sitelib}/firewall/__pycache__
%{python_sitelib}/firewall/config/*.py*
%{python_sitelib}/firewall/config/__pycache__
%{python_sitelib}/firewall/core/*.py*
%{python_sitelib}/firewall/core/__pycache__
%{python_sitelib}/firewall/core/io/*.py*
%{python_sitelib}/firewall/core/io/__pycache__
%{python_sitelib}/firewall/server/*.py*
%{python_sitelib}/firewall/server/__pycache__
%{_mandir}/man1/firewall*cmd*.1*
%{_mandir}/man1/%{name}*.1*
%{_mandir}/man5/firewall*.5*

%files -n firewall-applet
%{_bindir}/firewall-applet
%{_sysconfdir}/xdg/autostart/firewall-applet.desktop
%{_sysconfdir}/firewall/applet.conf
%{_datadir}/icons/hicolor/*/apps/firewall-applet*.*
%{_mandir}/man1/firewall-applet*.1*

%files -n firewall-config
%{_bindir}/firewall-config
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/firewall-config.glade
%{_datadir}/%{name}/gtk3_chooserbutton.py*
%{_datadir}/%{name}/gtk3_niceexpander.py
%{_datadir}/%{name}/__pycache__
%{_datadir}/applications/firewall-config.desktop
%{_datadir}/icons/hicolor/*/apps/firewall-config*.*
%{_datadir}/glib-2.0/schemas/org.fedoraproject.FirewallConfig.gschema.xml
%{_datadir}/metainfo/firewall-config.appdata.xml
%{_datadir}/polkit-1/actions/org.fedoraproject.FirewallD1.desktop.policy.choice
%{_datadir}/polkit-1/actions/org.fedoraproject.FirewallD1.server.policy.choice
%{_mandir}/man1/firewall-config*.1*
