Summary:	A dynamic firewall daemon
Name:		firewalld
Version:	0.3.11
Release:	1
URL:		https://fedorahosted.org/firewalld/
License:	GPLv2+
Group:		System/Base
Source0:	https://fedorahosted.org/released/firewalld/%{name}-%{version}.tar.bz2
Source1:	firewalld.rpmlintrc
Patch0:		firewalld-0.2.6-MDNS-default.patch
BuildArch:	noarch
BuildRequires:	desktop-file-utils
BuildRequires:	gettext
BuildRequires:	intltool
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	systemd-units
BuildRequires:	docbook-style-xsl
BuildRequires:	pkgconfig(python3)
Requires:	python-dbus
Requires:	python-slip-dbus >= 0.2.7
Requires:	python-decorator
Requires:	iptables
#Requires:	ebtables
Requires(post,preun):	rpm-helper

%description
A firewall service daemon with D-BUS interface managing a dynamic firewall.

%package -n	firewall-applet
Summary:	Firewall panel applet
Group:		System/Base
Requires:	%{name} = %{version}-%{release}
Requires:	firewall-config = %{version}-%{release}
Requires:	hicolor-icon-theme
Requires:	python-gobject3

%description -n firewall-applet
The firewall panel applet provides a status information of firewalld and also 
the firewall settings.

%package -n firewall-config
Summary:	Firewall configuration application
Group:		System/Base
Requires:	%{name} = %{version}-%{release}
Requires:	hicolor-icon-theme
Requires:	python-gobject3
Requires:	typelib(NetworkManager)

%description -n firewall-config
The firewall configuration application provides an configuration interface for 
firewalld.

%prep
%setup -q
%patch0 -p1

%build
%configure \
		--enable-sysconfig \
        --with-systemd-unitdir=%{_unitdir}

# no make

%install
%makeinstall_std

desktop-file-install --delete-original --set-key=Hidden --set-value=true \
  --dir %{buildroot}%{_sysconfdir}/xdg/autostart \
  %{buildroot}%{_sysconfdir}/xdg/autostart/firewall-applet.desktop

desktop-file-install --delete-original \
  --dir %{buildroot}%{_datadir}/applications \
  %{buildroot}%{_datadir}/applications/firewall-config.desktop


%find_lang %{name} --all-name

%post
%systemd_post firewalld.service

%preun
%systemd_preun firewalld.service

%postun
%systemd_postun_with_restart firewalld.service

%files -f %{name}.lang
%doc COPYING README
%{_sbindir}/firewalld
%{_bindir}/firewall-cmd
%{_bindir}/firewall-offline-cmd
%dir %{_datadir}/bash-completion/completions
%{_datadir}/bash-completion/completions/firewall-cmd
%dir %{_prefix}/lib/firewalld
%dir %{_prefix}/lib/firewalld/icmptypes
%dir %{_prefix}/lib/firewalld/services
%dir %{_prefix}/lib/firewalld/zones
%{_prefix}/lib/firewalld/icmptypes/*.xml
%{_prefix}/lib/firewalld/services/*.xml
%{_prefix}/lib/firewalld/zones/*.xml
%dir %{_sysconfdir}/firewalld
%config(noreplace) %{_sysconfdir}/firewalld/firewalld.conf
%config(noreplace) %{_sysconfdir}/firewalld/lockdown-whitelist.xml
%dir %{_sysconfdir}/firewalld/icmptypes
%dir %{_sysconfdir}/firewalld/services
%dir %{_sysconfdir}/firewalld/zones
%config(noreplace) %{_sysconfdir}/sysconfig/firewalld
%{_unitdir}/firewalld.service
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/FirewallD.conf
%{_datadir}/polkit-1/actions/org.fedoraproject.FirewallD1.policy
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
%{_mandir}/man1/firewall*cmd*.1*
%{_mandir}/man1/firewalld*.1*
%{_mandir}/man5/firewall*.5*

%files -n firewall-applet
%{_bindir}/firewall-applet
%{_sysconfdir}/xdg/autostart/firewall-applet.desktop
%{_datadir}/icons/hicolor/*/apps/firewall-applet*.*
%{_datadir}/glib-2.0/schemas/org.fedoraproject.FirewallApplet.gschema.xml
%{_mandir}/man1/firewall-applet*.1*

%files -n firewall-config
%{_bindir}/firewall-config
%{_datadir}/firewalld/firewall-config.glade
%{_datadir}/firewalld/gtk3_chooserbutton.py*
%{_datadir}/applications/firewall-config.desktop
%{_datadir}/icons/hicolor/*/apps/firewall-config*.*
%{_datadir}/glib-2.0/schemas/org.fedoraproject.FirewallConfig.gschema.xml
%{_datadir}/appdata/firewall-config.appdata.xml
%{_datadir}/polkit-1/actions/org.fedoraproject.FirewallD1.desktop.policy
%{_datadir}/polkit-1/actions/org.fedoraproject.FirewallD1.server.policy
%{_mandir}/man1/firewall-config*.1*
