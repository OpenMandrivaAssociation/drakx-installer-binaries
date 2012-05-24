Summary:	DrakX binaries
Name:		drakx-installer-binaries
Version:	1.51
Release:	2
Source0:	%{name}-%{version}.tar.bz2
License:	GPLv2+
Group:		Development/Other
Url:		http://wiki.mandriva.com/Tools/DrakX
BuildRequires:	kernel
BuildRequires:	ldetect-devel >= 0.9.1
BuildRequires:	ldetect-lst >= 0.1.222
BuildRequires:	ldetect-lst-devel
BuildRequires:	dietlibc-devel >= 0.32-4.20090113.4
BuildRequires:	modprobe-devel
BuildRequires:	pciutils-devel >= 3.1.7-2
BuildRequires:	zlib-devel
BuildRequires:	flex byacc pciutils-devel

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
make -C mdk-stage1

%install
cd mdk-stage1
dest=%{buildroot}%{_libdir}/%{name}
mkdir -p $dest
install init stage1 pppd pppoe rescue-gui dhcp-client probe-modules $dest
if [ -e pcmcia/pcmcia_probe.o ]; then
 	install -m 644 pcmcia/pcmcia_probe.o $dest
fi

%files
%exclude %{_libdir}/%{name}/probe-modules
%{_libdir}/%{name}

%files probe
%{_libdir}/%{name}/probe-modules
