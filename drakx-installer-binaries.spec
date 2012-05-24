%bcond_with	diet

Summary:	DrakX binaries
Name:		drakx-installer-binaries
Version:	1.53
Release:	1
Source0:	%{name}-%{version}.tar.xz
License:	GPLv2+
Group:		Development/Other
Url:		http://wiki.mandriva.com/Tools/DrakX
BuildRequires:	kernel
BuildRequires:	ldetect-devel >= 0.9.1
BuildRequires:	ldetect-lst >= 0.1.222
BuildRequires:	ldetect-lst-devel
%if %{with diet}
BuildRequires:	dietlibc-devel
%else
BuildRequires:	uClibc-devel >= 0.9.33.2-3
%endif
BuildRequires:	kmod-devel
BuildRequires:	sysfsutils-static-devel
BuildRequires:	slang-static-devel
BuildRequires:	newt-devel
BuildRequires:	pkgconfig(libpci)
BuildRequires:	zlib-devel
BuildRequires:	flex byacc
BuildRequires:	pkgconfig(liblzma)

#- not requiring the same version otherwise releasing drakx-installer-images takes a day
#- (restore this when the build system can build a pack of packages)
Requires:	ldetect-lst

%description
binaries needed to build Mandriva installer (DrakX)

%package	probe
Summary:	DrakX probe-modules tool
Group:		Development/Other

%description	probe
probe-modules tool needed to build Mandriva live

%prep
%setup -q

%build
%if %{with diet}
make -C mdk-stage1 LIBC=dietlibc
%else
make -C mdk-stage1 LIBC=uclibc
%endif

%install
cd mdk-stage1
dest=%{buildroot}%{_libdir}/%{name}
mkdir -p $dest
install init stage1 rescue-gui dhcp-client probe-modules $dest
if [ -e pcmcia/pcmcia_probe.o ]; then
 	install -m 644 pcmcia/pcmcia_probe.o $dest
fi

%files
%exclude %{_libdir}/%{name}/probe-modules
%{_libdir}/%{name}

%files probe
%{_libdir}/%{name}/probe-modules
