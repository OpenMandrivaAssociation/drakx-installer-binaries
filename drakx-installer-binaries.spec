#bcond_without	diet

%define	family	drakx-installer

Summary:	DrakX binaries
Name:		drakx-installer-binaries
Version:	1.60
Release:	5
Source0:	%{name}-%{version}.tar.xz
Patch1:	drakx-installer-binaries-1.60-rosa.patch
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
%rename		%{name}-probe

%description
Binaries needed to build the Mandriva Linux installer (DrakX).

%prep
%setup -q
%apply_patches

%build
#if %{with diet}
#make -C mdk-stage1 LIBC=dietlibc LDFLAGS="%{ldflags}"
#else
#make -C mdk-stage1 LIBC=uclibc CFLAGS="%{uclibc_cflags}" LDFLAGS="%{ldflags}"
#endif

make -C mdk-stage1 LDFLAGS="%{ldflags}"

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


%changelog
* Mon Sep 10 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 1.60-1
+ Revision: 816723
- new version:
  	o compile libkmod, libpci & libsysfs sources directly into binary rather
  	 than linking in objects from static libraries
  	o use kmod for module loading everywhere
- merge probe-modules package as it's now only a hardlink of same binary as the
  rest

* Wed Sep 05 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 1.59-1
+ Revision: 816383
- new version:
  	o move back newt & slang to our own tree to be able to compile with
  	  -fwhole-program
  	o move tree from mdk-stage1 to images dir
  	o use more regular paths for various configuration files etc.
  	  created/needed bythe installer
  	o beef up init script process inspired by SysV
  	o just compile all of ldetect's source directly into the stage1 binary
  	  rather than linking it through a static library
  	o compile and link 'drvinst' & lspcidrake directly into stage1 binary in
  	  order to save space and make it available from earlier on
  	o don't write directly to /dev/tty3, inittab takes care of this now
  	o log any errors from init scripts to /var/log/stage1.log
  	o removal of stage1 files conflicting with files from stage2 is now
  	  automatically handled by init scripts
  	o fix a bug in selection of http install where going back during
  	  configuration would invoke ftp install option rather than http
  	o move stage1.log from /tmp to /var/log/stage1.log
  	o log syslog & klog to /var/log/messages
  	o handle moving to new root etc. through inittab
  	o add a 'nettest' option for automatically selecting (my) personal
  	  options for loading stage 2 installer
  	o migrate to using 'init' implementation from busybox rather than our
  	  own
  	o properly grab controlling tty for child processes forked from init
  	o add support for virtio discs
  	o fix glibc build
  	o "move" mount points from stage 1 to stage 2 overlayfs root

* Fri Aug 10 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 1.57-1
+ Revision: 813863
- new version:
  	o merge 'init' into the 'stage1' binary
  	o do all mounting in stage 1
  	o fix mounting overlayfs for stage 2 otherwise than just rescue mode

* Sat Aug 04 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 1.56-1
+ Revision: 811700
- new version:
  	o merge dhcp-client, probe-modules, rescue-gui & stage1 into just one
  	  binary
  	o use overlayfs for new root rather than symlinks
  	o mount /dev as devtmpfs
  	o fix remaining aliasing violations for dietlibc build
  	o fix building of init.c against dietlibc
  	o compile everything with -fwhole-program by default

* Thu Jun 07 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 1.55-1
+ Revision: 803194
- fix unitialized memory screwing up dialog input

* Thu Jun 07 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 1.54-1
+ Revision: 803139
- add NEWS as %%doc
- use %%makeinstall_std
- build with %%optflags & %%ldflags
- new version:
  	o drop some dead code
  	o comment out code operating on an uninitialized sockaddr
  	o get rid of unused variables
  	o fix aliasing violations
  	o fix bogus sizeof(int) == sizeof(int32_t) assumptions
  	o take out -fno-strict-aliasing
  	o revert to "linux" terminfo
  	o make sure ncurses get initialized in UTF-8 (mga#4894)
  	o fix 'format not a string literal and no format arguments'
  	o add install with DESTDIR support
  	o install under /usr/lib(64)/drakx-installer
  	o don't strip binaries in Makefile, leave it to rpm to do
  	o hide "KA server" option (mga#5944)
  	o support dynamic uClibc build
  	o first attempt at supporting XenBlk discs
  	o switch from gethostbyname() to getaddrinfo() (mga#4056)
  	o switch from gethostbyaddr() to getnameinfo()

* Thu May 24 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 1.53-1
+ Revision: 800440
- new version:
  	o try mounting as btrfs
  	o load btrfs module to mount btrfs
  	o default to "screen" instead of "linux" terminfo (mga#4894)
  	o do not try to load obsolete sqlzma & squashfs_lzma kernel modules
  	o fix segfaulting when ISO directory is not valid (mga#4592)
  	o recognize c67x00, imx21-hcd, fhci, isp1362-hcd, oxu210hp-hcd &
  	  renesas-usbhs USB host drivers (mga#4905)

* Thu May 24 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 1.52-1
+ Revision: 800360
- new version:
  	o build against uClibc by default
  	o fix parallel build
  	o clean up Makefile
  	o support xz & gz compressed kernel modules in addition to uncompressed
  	o add support for doing a dynamically linked build
  	o build against system libraries of libsysfs, slang & newt
  	o add support for building with uClibc
  	o fix building with newer dietlibc/zlib
  	o (handle_pcmcia) kill obsolete test for 2.2 kernel (tv)
  	o try to use arch-prefixed location for FTP & HTTP installs (mga#2578)
  	o add support for kernel compressed as XZ
  	o link with libkmod instead of libmodprobe
  	o kill 10 years old snapshot of pppd & pppoe
  	o (now using upstream pppd & pppoe)
  	o display distro name in mirror list too (mga#191)
  	o sync with kernel-3.1.0
  	  * add hid devices:
  	        hid-keytouch, hid-uclogic
  	  * add sas/raid driver:
  	        isci
  	  * add sound devices:
  	        snd-lola, snd-firewire-speakers snd-isight, snd-usb-6fire
  	  * add usb/storage:
  	        ums-eneub6250, ums-realtek
  	  * add wireless drivers:
  	        brcmsmac, rtl8187se, rtusb, rtl8192se, rtl8192cu, rtl8192de
  	o add ums-* (USB mass storage) modules in disk/usb category
- drop unnecessary patch to disable -Werror
- add version to license
- cleanups

* Wed Dec 07 2011 Antoine Ginies <aginies@mandriva.com> 1.51-2
+ Revision: 738537
- fix missing declaration and headers
- arm/mips support (from MGA)
- (pcmcia_probe) do not attempt to perform ISA probe for PCMCIA controller on
  x86_64 as it fails with kvm_amd (#1156) (from MGA)
- (pci_probe) add vendor name for 0x1217 (from MGA)
- (pci_probe) all "O2 Micro" devices are know managed by yenta_socket (from MGA)
- "i82365" driver was renamed "pd6729" (from MGA)
- update yenta_socket ID list from kernel, thus handling more PCMCIA controllers (from MGA)
- sort pci_id table (from MGA)
- fix time argument type (upstream commit 8d07ad78c8a32b9c89bfcea25d775e8440fd4172 on pppd/session.c) (from MGA)
- try to handle built-in modules (from MGA)
- Don't depend on /sbin/init for now
- Since we switched to systemd and we don't want to include its whole
  deps, we choose the fast path and remove the use of init entirely
  since it's not really used.
- ide_cd_mod doesnt exist anymore
- kernel doesnt provides compressed module now

* Thu Apr 28 2011 Antoine Ginies <aginies@mandriva.com> 1.50-1
+ Revision: 660026
- restore ppp and ppoe disable by error
- update stage1 color

* Tue Apr 26 2011 Antoine Ginies <aginies@mandriva.com> 1.48-3
+ Revision: 659367
- remove those old colors...
- bump release
- latest tarball
- fix newt build problem

* Wed Oct 13 2010 Thierry Vignaud <tv@mandriva.org> 1.47-1mdv2011.0
+ Revision: 585504
- Patch0 : temporary disable -Werror in order to fix build
- 2011.0 build

* Fri May 21 2010 Pascal Terjan <pterjan@mandriva.org> 1.46-2mdv2010.1
+ Revision: 545631
- rebuild with fixed dietlibc

* Thu May 13 2010 Pascal Terjan <pterjan@mandriva.org> 1.46-1mdv2010.1
+ Revision: 544673
- create device listed in /proc/partitions with correct major/minor (#57032)

* Tue Mar 30 2010 Pascal Terjan <pterjan@mandriva.org> 1.45-1mdv2010.1
+ Revision: 529931
- do not list /dev/fd0 when no floppy is found (#58390)

* Wed Mar 17 2010 Thierry Vignaud <tv@mandriva.org> 1.44-1mdv2010.1
+ Revision: 523761
- BR pciutils-devel with diet library
- rebuild with latest list_modules.pm (might fix #57833)
- 1.43 aka automatically bump version (#57466)
- rebuild (might fix #57466)

  + Oden Eriksson <oeriksson@mandriva.com>
    - rebuilt for 2010.1

* Mon Oct 12 2009 Olivier Blin <blino@mandriva.org> 1.42-2mdv2010.0
+ Revision: 456839
- rebuild for new ldetect

* Tue Sep 22 2009 Olivier Blin <blino@mandriva.org> 1.42-1mdv2010.0
+ Revision: 447357
- 1.42
- list asix module in network/usb group
- virtio: fix device probing: use PCI subdevices
- fix format string bug from 1.41

* Tue Sep 15 2009 Bogdano Arendartchuk <bogdano@mandriva.com> 1.41-3mdv2010.0
+ Revision: 443240
- added patch fixing virtio device probing: use PCI subdevices

* Tue Sep 01 2009 Bogdano Arendartchuk <bogdano@mandriva.com> 1.41-2mdv2010.0
+ Revision: 423686
- added patch fixing format string bug in 1.41
- new version 1.41, handle virtio devices

* Thu Jul 09 2009 Christophe Fergeau <cfergeau@mandriva.com> 1.40-1mdv2010.0
+ Revision: 393933
- update tarball
- fix build, rebuild to get 2010.0 strings
- rebuild stage1 to get updated strings for 2010.0 alphas

* Wed Apr 22 2009 Pascal Terjan <pterjan@mandriva.org> 1.39-1mdv2009.1
+ Revision: 368637
- set uevent helper which will load firmware and do not set firmware
  timeout to 1 second (it will fail if firmware is not there)

* Mon Apr 20 2009 Christophe Fergeau <cfergeau@mandriva.com> 1.38-1mdv2009.1
+ Revision: 368380
- 1.38:
- handle hybrid ISOs (ISO images dumped to USB keys)

* Wed Apr 15 2009 Christophe Fergeau <cfergeau@mandriva.com> 1.37.2-1mdv2009.1
+ Revision: 367443
- 1.37.2:
  * reroll tarball, the previous one contained outdated code (?)

* Tue Apr 07 2009 Christophe Fergeau <cfergeau@mandriva.com> 1.37.1-1mdv2009.1
+ Revision: 364909
- 1.37.1:
  * fix build

  + Thierry Vignaud <tv@mandriva.org>
    - enumerate hid bus and load hid quirk modules, fixes #47167

* Sun Mar 08 2009 Pascal Terjan <pterjan@mandriva.org> 1.36-1mdv2009.1
+ Revision: 352905
- load appropriate modules before trying to mount ext4/reiser4 (#48573)

* Mon Feb 16 2009 Pascal Terjan <pterjan@mandriva.org> 1.35-1mdv2009.1
+ Revision: 340819
- allow installing from ext3/ext4/reiser

* Fri Feb 13 2009 Pascal Terjan <pterjan@mandriva.org> 1.34-2mdv2009.1
+ Revision: 340068
- Rebuild with new dietlibc

* Thu Feb 12 2009 Olivier Blin <blino@mandriva.org> 1.34-1mdv2009.1
+ Revision: 339745
- 1.34
- adapt to new modules.dep format (prefix modules with directory path)
- try to use arch-prefixed location for automatic disk installs

* Wed Feb 04 2009 Pascal Terjan <pterjan@mandriva.org> 1.33-1mdv2009.1
+ Revision: 337450
- Update to 1.33

* Fri Sep 26 2008 Olivier Blin <blino@mandriva.org> 1.32-1mdv2009.0
+ Revision: 288566
- 1.32
- automatically find compressed stage2 with automatic=method:disk

* Wed Aug 27 2008 Pixel <pixel@mandriva.com> 1.31-1mdv2009.0
+ Revision: 276470
- 1.31: usbkbd is dead, using usbhid instead

* Wed Aug 06 2008 Thierry Vignaud <tv@mandriva.org> 1.30-2mdv2009.0
+ Revision: 264420
- rebuild early 2009.0 package (before pixel changes)

* Thu Jun 12 2008 Olivier Blin <blino@mandriva.org> 1.30-1mdv2009.0
+ Revision: 218500
- 1.30
- add back "ide-generic" support (incorrectly removed in 1.17), the
  module that we want to avoid is "ide-pci-generic" (previously
  "generic"),
  and this is handled by ldetect-lst preferred modules list
- handle ide-cd being renamed as ide-cd_mod

* Thu Jun 12 2008 Olivier Blin <blino@mandriva.org> 1.29-1mdv2009.0
+ Revision: 218453
- 1.29
- allow to pass module options to probe-modules
- build fixes for gcc 4.3

  + Oden Eriksson <oeriksson@mandriva.com>
    - rebuilt against dietlibc-devel-0.32

* Thu Apr 24 2008 Olivier Blin <blino@mandriva.org> 1.28-2mdv2009.0
+ Revision: 197263
- rebuild for new ldetect-lst (to default to libata pata drivers)

* Thu Apr 03 2008 Olivier Blin <blino@mandriva.org> 1.28-1mdv2008.1
+ Revision: 192223
- 1.28
- fix segfault with empty device description (can happen for USB devices)

* Mon Mar 31 2008 Olivier Blin <blino@mandriva.org> 1.27.1-1mdv2008.1
+ Revision: 191276
- 1.27.1
- fix build
- 1.27
- do not set firmware timeout to 1 second in probe-modules helper for
  Mandriva One (#39216)

* Thu Mar 20 2008 Olivier Blin <blino@mandriva.org> 1.26-1mdv2008.1
+ Revision: 189275
- 1.26
- load bus/firewire controllers (#31356)
- really ask dhcp domain if not guessed

* Tue Mar 18 2008 Olivier Blin <blino@mandriva.org> 1.25-1mdv2008.1
+ Revision: 188587
- build with newer ldetect-lst to fix jmicron support (#38343)
- 1.25
- do not allow to choose outdated cooker mirror list (#37278)
- 1.24
- load disk/ide before disk/scsi (#38451, to prevent sata deps from
  overriding non-libata pata modules, like in stage2)
- fix asking modules when no controller is detected

* Thu Feb 28 2008 Olivier Blin <blino@mandriva.org> 1.23-1mdv2008.1
+ Revision: 176458
- 1.23
- probe usb-storage/sbp2 only when probing USB/SCSI buses
  (to make automatic boot faster on IDE)
- make dhcp the first choice (instead of static) in the network type
  menu
- clear tty2 after shell is killed
- log "killed shell" message on tty3
- add a space in front of top line (like help message)
- space-pad top line with spaces to the right (like help message)

* Thu Feb 28 2008 Olivier Blin <blino@mandriva.org> 1.22-1mdv2008.1
+ Revision: 175954
- 1.22
- fix automatic IDE media detection
  (was broken with multiple CD drives, #36161)
- fix bootsplash in automatic CD-Rom mode
  (as a result of IDE media detection fix)
- wait only 1 second for firmware upload
  (not to hang boot with iwl3945, #37279)

* Tue Feb 12 2008 Olivier Blin <blino@mandriva.org> 1.21-1mdv2008.1
+ Revision: 165635
- 1.21
- load nls_cp437 and nls_iso8859_1 when loading vfat
   (used to be in custom modules.dep)

* Mon Feb 11 2008 Olivier Blin <blino@mandriva.org> 1.20-1mdv2008.1
+ Revision: 165417
- 1.20
- probe-modules:
  o handle the "--usb" option instead of "usb"
  o load module passed as argument (if any), instead of probing bus
- switch to modules from /lib/modules/`uname -r`, modules.dep containing full filename
- restore BuildRoot

* Fri Dec 21 2007 Olivier Blin <blino@mandriva.org> 1.19-1mdv2008.1
+ Revision: 136226
- 1.19
- rebuild with list_modules to handle atl2 ethernet driver

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Thu Oct 04 2007 Olivier Blin <blino@mandriva.org> 1.18-2mdv2008.0
+ Revision: 95485
- rebuild for latest ldetect-lst

* Thu Oct 04 2007 Olivier Blin <blino@mandriva.org> 1.18-1mdv2008.0
+ Revision: 95274
- 1.18
- add probe-modules helper in drakx-installer-binaries-probe
  sub-package (to be used in live systems, #34277)

* Mon Sep 24 2007 Olivier Blin <blino@mandriva.org> 1.17-1mdv2008.0
+ Revision: 92520
- 1.17
- use modules from disk/ide category (#33043)
- do not explicitely try to load ide-generic, ldetect will fallback
  to ide-generic when appropriate (#33043)

* Wed Sep 19 2007 Olivier Blin <blino@mandriva.org> 1.16-2mdv2008.0
+ Revision: 91077
- rebuild with latest ldetect (for /lib/module-init-tools/ldetect-lst-modules.alias support)

* Wed Sep 05 2007 Pixel <pixel@mandriva.com> 1.16-1mdv2008.0
+ Revision: 80118
- 1.16:
- if you give nfs directory xxx, try to use xxx/ARCH
- handle cdroms with and without ARCH at the root

* Mon Aug 27 2007 Olivier Blin <blino@mandriva.org> 1.15-1mdv2008.0
+ Revision: 71932
- 1.15
- ask loading modules from /modules if needed
- read modules description from /modules/modules.description

* Thu Aug 23 2007 Olivier Blin <blino@mandriva.org> 1.14-1mdv2008.0
+ Revision: 70515
- 1.14: fix segfault in USB detection code (when no module match, #32624)

* Tue Aug 21 2007 Olivier Blin <blino@mandriva.org> 1.13-1mdv2008.0
+ Revision: 68637
- 1.13
- use module names instead of filenames
- convert module name to filename before loading it
  (using modules.dep to get filename)
- keep module in dependencies list even if it has no dependencies
  (to keep track of its filename)
- use '_' in module names when explicitely loading modules (cosmetics)

* Tue Aug 21 2007 Olivier Blin <blino@mandriva.org> 1.12-1mdv2008.0
+ Revision: 68128
- 1.12: adapt to new list_modules

* Mon Aug 20 2007 Olivier Blin <blino@mandriva.org> 1.11-2mdv2008.0
+ Revision: 67890
- rebuild with latest ldetect-lst

* Wed Aug 15 2007 Olivier Blin <blino@mandriva.org> 1.11-1mdv2008.0
+ Revision: 63570
- 1.11:
  o use ldetect/libmodprobe/libpci (dietlibc version)
    instead of custom pci/usb probe
  o rename rescue "GUI" as rescue "menu"

* Tue Jul 17 2007 Olivier Blin <blino@mandriva.org> 1.10.1-1mdv2008.0
+ Revision: 52947
- 1.10:
  o add ide-disk module
  o load ide-disk when detecting disks (ide is now modularized...)
- 1.10.1:
  o link init with dietlibc instead of minilibc on ix86/x86-64
  o add missing includes for wireless
  o fix build of pppoe by using dietlibc termios header

* Fri Jun 29 2007 Pixel <pixel@mandriva.com> 1.9-1mdv2008.0
+ Revision: 45680
- new release 1.9: ide is now modularized

