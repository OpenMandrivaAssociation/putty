Name:		putty
Version:	0.83
Release:	1
Summary:	SSH, Telnet and Rlogin client
License:	MIT
Group:		Networking/Remote access
URL:		https://www.chiark.greenend.org.uk/~sgtatham/putty/
Source0:	https://the.earth.li/~sgtatham/putty/latest/%{name}-%{version}.tar.gz
Source1:	%{name}.desktop
Source2:	%{name}-icons.tar.bz2
BuildRequires:	cmake ninja
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	halibut
BuildRequires:	desktop-file-utils
BuildRequires:	perl(Digest::SHA)

%description
This is the Unix port of the popular Windows ssh client, PuTTY. It
supports flexible terminal setup, mid-session reconfiguration using
Ctrl-rightclick, multiple X11 authentication protocols, and various
other interesting things not provided by ssh in an xterm.
%prep
%setup -q
%setup -q -T -D -a2
%cmake -G Ninja

%build
%ninja_build -C build

%install
%ninja_install -C build

desktop-file-install \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  %{SOURCE1}

install -D -m 644 %{name}48.png %buildroot/%{_datadir}/icons/hicolor/48x48/apps/%name.png
install -D -m 644 %{name}32.png %buildroot/%{_datadir}/icons/hicolor/32x32/apps/%name.png
install -D -m 644 %{name}32.png %buildroot/%{_datadir}/icons/%name.png
install -D -m 644 %{name}16.png %buildroot/%{_datadir}/icons/hicolor/16x16/apps/%name.png

%files
%doc LICENCE README CHECKLST.txt
%{_bindir}/*
%{_mandir}/man1/*.1*
%{_datadir}/applications/*
%{_datadir}/icons/hicolor/*/apps/*.png
%{_datadir}/icons/putty.png
