%define is_snapshot     0

%define title   Putty
%define Summary Free SSH, Telnet and Rlogin client

Name:                   putty
Version:                0.62
Release:                %mkrel 1
Epoch:                  1
Summary:                %Summary
License:                MIT
Group:                  Networking/Remote access
%if %{is_snapshot}
URL:                    http://www.tartarus.org/~simon/putty-unix/
Source0:                %name-%version-%snapshot.tar.bz2
%endif
%if !%{is_snapshot}
URL:                    http://the.earth.li/~sgtatham/putty/latest/
Source0:                http://the.earth.li/~sgtatham/putty/latest/%name-%version.tar.gz
%endif
Source1:                %name-icons.tar.bz2
Source2:                http://the.earth.li/~sgtatham/putty/latest/%name-%version.tar.gz.DSA
Patch0:			putty-0.62-mdv-disable-Werror.patch
BuildRoot:              %_tmppath/%name-%{version}-%{release}-root
Buildrequires:          gtk+2-devel

%description
This is the Unix port of the popular Windows ssh client, PuTTY. It
supports flexible terminal setup, mid-session reconfiguration using
Ctrl-rightclick, multiple X11 authentication protocols, and various
other interesting things not provided by ssh in an xterm.

%prep
%if %{is_snapshot}
%setup -q -n %name-%version-%snapshot
%setup -q -T -D -a1 -n %name-%version-%snapshot
%endif
%if !%{is_snapshot}
%setup -q -n %name-%version
%setup -q -T -D -a1 -n %name-%version
%endif
%patch0 -p1

%build
pushd unix
#gw work around build failure:
%define optflags "%{echo "%optflags"|sed s/-Wstrict-aliasing=2//}"
%if %{is_snapshot}
%configure2_5x
%make  VER="-DSNAPSHOT=%{snapshot}"
%endif
%if !%{is_snapshot}
%configure2_5x
%make
%endif

# temporary man pages
echo ".so putty.1" > pscp.1
echo ".so putty.1" > psftp.1
popd

%install
rm -rf %buildroot

# preparing directories
%__mkdir_p %{buildroot}%{_bindir}
%__mkdir_p %{buildroot}%{_mandir}/man1

(cd unix && %__make -f Makefile.gtk install DESTDIR=%buildroot \
prefix=%{_prefix} mandir=%{_mandir})

# Menu
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=%title
Comment=%Summary
Exec=%_bindir/%{name}
Icon=%name
Terminal=false
Type=Application
StartupNotify=true
Categories=GTK;Network;RemoteAccess;
EOF
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-pterm.desktop << EOF
[Desktop Entry]
Name=Putty Terminal
Comment=X Terminal emulator based on Putty
Exec=%_bindir/pterm
Icon=%name
Terminal=false
Type=Application
StartupNotify=true
Categories=GTK;Utility;TerminalEmulator;
EOF

# icon
%__install -D -m 644 %{name}48.png %buildroot/%_liconsdir/%name.png
%__install -D -m 644 %{name}32.png %buildroot/%_iconsdir/%name.png
%__install -D -m 644 %{name}16.png %buildroot/%_miconsdir/%name.png

#gw remove obsolete puttytel, same functionality is in putty:
rm -f %buildroot{%_bindir/puttytel,%_mandir/man1/puttytel.1}

%clean
rm -rf %buildroot

%files
%defattr(-,root,root)
%doc LICENCE README CHECKLST.txt doc/*.html doc/*.css doc/*.txt
%_bindir/*
%defattr(0644,root,root,0755)
%_mandir/man1/*
%{_datadir}/applications/mandriva-%{name}.desktop
%{_datadir}/applications/mandriva-pterm.desktop
%_miconsdir/*.png
%_iconsdir/*.png
%_liconsdir/*.png


%changelog
* Sun Dec 11 2011 Dmitry Mikhirev <dmikhirev@mandriva.org> 1:0.62-1
+ Revision: 740278
- Removed -Werror flag
- Update to 0.62

* Mon Aug 01 2011 Götz Waschk <waschk@mandriva.org> 1:0.61-2
+ Revision: 692689
- remove puttytel
- add menu entry for pterm
- fix menu category

* Wed Jul 13 2011 Götz Waschk <waschk@mandriva.org> 1:0.61-1
+ Revision: 689890
- new version
- fix build
- use gtk+ 2.0

* Fri Aug 01 2008 Thierry Vignaud <tv@mandriva.org> 1:0.60-4mdv2009.0
+ Revision: 259363
- rebuild

* Thu Jul 24 2008 Thierry Vignaud <tv@mandriva.org> 1:0.60-3mdv2009.0
+ Revision: 247241
- rebuild

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Fri Jan 11 2008 Thierry Vignaud <tv@mandriva.org> 1:0.60-1mdv2008.1
+ Revision: 148326
- drop old menu
- kill re-definition of %%buildroot on Pixel's request
- kill desktop-file-validate's 'warning: key "Encoding" in group "Desktop Entry" is deprecated'

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Sat May 12 2007 David Walluck <walluck@mandriva.org> 1:0.60-1mdv2008.0
+ Revision: 26418
- 0.60


* Thu Jan 25 2007 Götz Waschk <waschk@mandriva.org> 0.59-1mdv2007.0
+ Revision: 113481
- Import putty

* Thu Jan 25 2007 G�tz Waschk <waschk@mandriva.org> 0.59-1mdv2007.1
- fix doc file list
- xdg menu
- New version 0.59

* Wed May 10 2006 Tibor Pittich <Tibor.Pittich@mandriva.org> 0.58-2mdk
- rebuild
- mkrel

* Thu Apr 07 2005 Götz Waschk <waschk@linux-mandrake.com> 0.58-1mdk
- New release 0.58

* Tue Feb 22 2005 Götz Waschk <waschk@linux-mandrake.com> 0.57-1mdk
- New release 0.57

* Thu Oct 28 2004 G�tz Waschk <waschk@linux-mandrake.com> 0.56-1mdk
- don't bzip2 source for sig checks
- add signature
- New release 0.56

* Thu Aug 05 2004 Tibor Pittich <Tibor.Pittich@mandrake.org> 1:0.55-1mdk
- 0.55
- added support to build stable or snapshot versions

* Mon Feb 16 2004 David Walluck <walluck@linux-mandrake.com> 1:0.54-0.20040216.3mdk
- fix changelog entries

* Sun Feb 15 2004 David Walluck <walluck@linux-mandrake.com> 1:0.54-0.20040216.2mdk
- bump epoch to fix improper version tag in the 0.53b release

* Sun Feb 15 2004 David Walluck <walluck@linux-mandrake.com> 0:0.54-0.20040216.1mdk
- 0.54 (20040216)

