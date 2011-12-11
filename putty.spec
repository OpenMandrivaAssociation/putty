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

%build
#gw work around build failure:
%define optflags "%{echo "%optflags"|sed s/-Wstrict-aliasing=2//}"
%if %{is_snapshot}
cd unix 
%configure2_5x
%make  VER="-DSNAPSHOT=%{snapshot}"
%endif
%if !%{is_snapshot}
cd unix 
%configure2_5x
%make
%endif


# temporary man pages
echo ".so putty.1" > pscp.1
echo ".so putty.1" > psftp.1

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
