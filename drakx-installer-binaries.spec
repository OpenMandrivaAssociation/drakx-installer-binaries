%define	family	drakx-installer

Summary:	DrakX binaries
Name:		drakx-installer-binaries
Version:	2.0
Release:	1
Source0:	%{name}-%{version}.tar.xz
License:	GPLv2+
Group:		Development/Other
Url:		http://wiki.mandriva.com/Tools/DrakX
BuildRequires:	kernel
BuildRequires:	ldetect-devel >= 0.9.1
BuildRequires:	ldetect-lst >= 0.1.222
BuildRequires:	ldetect-lst-devel
BuildRequires:	uClibc-devel >= 0.9.33.2-3
BuildRequires:	uClibc++
BuildRequires:	pkgconfig(libkmod)
BuildRequires:	sysfsutils-devel
BuildRequires:	newt-devel >= 0.52.14-6
BuildRequires:	pkgconfig(libpci)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	flex byacc
BuildRequires:	pkgconfig(liblzma)
BuildRequires:	grub2

#- not requiring the same version otherwise releasing drakx-installer-images takes a day
#- (restore this when the build system can build a pack of packages)
Requires:	ldetect-lst
%rename		%{name}-probe

%description
Binaries needed to build the Mandriva Linux installer (DrakX).

%prep
%setup -q

%build
%make -C mdk-stage1 LIBC=uclibc OPTFLAGS="%{uclibc_cxxflags}"

%install
%makeinstall_std -C mdk-stage1

%files
%doc mdk-stage1/NEWS
%dir %{_libdir}/%{family}
%dir %{_libdir}/%{family}/binaries
%{_libdir}/%{family}/binaries/stage1
%{_libdir}/%{family}/binaries/rescue-gui
%{_libdir}/%{family}/binaries/dhcp-client
%{_libdir}/%{family}/binaries/drvinst
%{_libdir}/%{family}/binaries/lspcidrake
%{_libdir}/%{family}/binaries/pcmcia_probe.o
%{_libdir}/%{family}/binaries/probe-modules
