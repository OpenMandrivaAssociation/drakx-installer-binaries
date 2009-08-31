%define name drakx-installer-binaries
%define version 1.41
%define release %mkrel 1

Summary: DrakX binaries
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{version}.tar.bz2
License: GPL
Group: Development/Other
Url: http://wiki.mandriva.com/Tools/DrakX
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: kernel
BuildRequires: ldetect-devel >= 0.8.1
BuildRequires: ldetect-lst >= 0.1.222
BuildRequires: ldetect-lst-devel
BuildRequires: dietlibc-devel
BuildRequires: modprobe-devel
BuildRequires: pciutils-devel
BuildRequires: zlib-devel
BuildRequires: flex byacc pciutils-devel

#- not requiring the same version otherwise releasing drakx-installer-images takes a day
#- (restore this when the build system can build a pack of packages)
Requires: ldetect-lst

%description
binaries needed to build Mandriva installer (DrakX)

%package probe
Summary: DrakX probe-modules tool
Group: Development/Other

%description probe
probe-modules tool needed to build Mandriva live

%prep
%setup -q

%build
make -C mdk-stage1

%install
rm -rf $RPM_BUILD_ROOT

cd mdk-stage1
dest=$RPM_BUILD_ROOT%{_libdir}/%name
mkdir -p $dest
install init stage1 pppd pppoe rescue-gui dhcp-client probe-modules $dest
if [ -e pcmcia/pcmcia_probe.o ]; then
  install -m 644 pcmcia/pcmcia_probe.o $dest
fi


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%exclude %{_libdir}/%name/probe-modules
%{_libdir}/%name

%files probe
%defattr(-,root,root)
%{_libdir}/%name/probe-modules
