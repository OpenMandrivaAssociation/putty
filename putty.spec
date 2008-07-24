%define is_snapshot     0

%if %{is_snapshot}
%define snapshot        2004-02-16
%define release         %mkrel 3
%endif
%if !%{is_snapshot}
%define release         %mkrel 3
%endif

%define title   Putty
%define Summary Free SSH, Telnet and Rlogin client

Name:                   putty
Version:                0.60
Release:                %mkrel 3
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
Buildrequires:          gtk+-devel

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
%if %{is_snapshot}
cd unix && %make -f Makefile.gtk VER="-DSNAPSHOT=%{snapshot}" \
%endif
%if !%{is_snapshot}
cd unix && %make -f Makefile.gtk \
%endif
CC="%{__cc}" CFLAGS="%{optflags} `gtk-config --cflags` -I. -I.. -I../charset"

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
Categories=X-MandrivaLinux-Internet-RemoteAccess;Network;RemoteAccess;
EOF

# icon
# Use {curly braces} here to protect the variable name.
# ie: Is name48.png %{name}48.png or %{name48}.png?
%__install -D -m 644 %{name}48.png %buildroot/%_liconsdir/%name.png
%__install -D -m 644 %{name}32.png %buildroot/%_iconsdir/%name.png
%__install -D -m 644 %{name}16.png %buildroot/%_miconsdir/%name.png

%if %mdkversion < 200900
%post
%update_menus
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%endif

%clean
rm -rf %buildroot

%files
%defattr(-,root,root)
%doc LICENCE README CHECKLST.txt doc/*.html doc/*.css doc/*.txt
%_bindir/*
%defattr(0644,root,root,0755)
%_mandir/man1/*
%{_datadir}/applications/mandriva-%{name}.desktop
%_miconsdir/*.png
%_iconsdir/*.png
%_liconsdir/*.png
