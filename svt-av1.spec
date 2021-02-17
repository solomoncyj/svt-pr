%global _description %{expand:
The Scalable Video Technology for AV1 Encoder (SVT-AV1 Encoder) is an
AV1-compliant encoder library core. The SVT-AV1 development is a
work-in-progress targeting performance levels applicable to both VOD and Live
encoding / transcoding video applications.}

Name:           svt-av1
Version:        0.8.6
Release:        4%{?dist}
Summary:        Scalable Video Technology for AV1 Encoder

# Main library: BSD-2-Clause-Patent
# Source/Lib/Common/Codec/EbHmCode.c: BSD
# Source/App/EncApp/EbAppString.*
# Source/Lib/Common/Codec/EbString.*
# Source/Lib/Common/Codec/vector.*: MIT
# Source/Lib/Common/ASM_SSE2/x86inc.asm: ISC
# Source/App/DecApp/EbMD5Utility.*: PublicDomain
License:        BSD-2-Clause-Patent and BSD and MIT and ISC and Public Domain
URL:            https://github.com/AOMediaCodec/SVT-AV1
Source0:        %url/archive/v%{version}/%{name}-%{version}.tar.gz
# x64inc: mark as noexec
Patch0:         https://gitlab.com/1480c1/SVT-AV1/-/commit/8f9acb7a6215c49297f9cb6c574150e48d8f5b76.patch#/0001-mark-as-noexec.patch

# 64Bits, 5th Generation Intel® Core™ processor only
ExclusiveArch:  x86_64

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  meson
BuildRequires:  yasm
BuildRequires:  help2man
BuildRequires:  gstreamer1-devel
BuildRequires:  gstreamer1-plugins-base-devel

Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description %_description

%package libs
Summary:    SVT-AV1 libraries

%description libs %_description

This package contains SVT-AV1 libraries.

%package devel
Summary:    Development files for SVT-AV1
Requires:   %{name}-libs = %{version}-%{release}

%description devel %_description.

This package contains the development files for SVT-AV1.

%package -n     gstreamer1-%{name}
Summary:        GStreamer 1.0 %{name}-based plug-in
Requires:       gstreamer1-plugins-base%{?_isa}

%description -n gstreamer1-%{name}
This package provides %{name}-based GStreamer plug-in.

%prep
%autosetup -p1 -n SVT-AV1-%{version}
# Patch build gstreamer plugin
sed -e "s|install: true,|install: true, include_directories : [ include_directories('../Source/API') ], link_args : '-lSvtAv1Enc',|" \
-e "/svtav1enc_dep =/d" -e 's|, svtav1enc_dep||' -e "s|svtav1enc_dep.found()|true|" -i gstreamer-plugin/meson.build

%build
%cmake \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo
%cmake_build

export LIBRARY_PATH="$LIBRARY_PATH:$(pwd)/Bin/RelWithDebInfo"
pushd gstreamer-plugin
%meson
%meson_build
popd

%install
%cmake_install
rm -f %{buildroot}%{_libdir}/*.{a,la}

install -d -m0755 %{buildroot}/%{_mandir}/man1
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:%{buildroot}%{_libdir}
help2man -N --help-option=-help --version-string=%{version} %{buildroot}%{_bindir}/SvtAv1DecApp > %{buildroot}%{_mandir}/man1/SvtAv1DecApp.1
help2man -N --help-option=-help --no-discard-stderr --version-string=%{version} %{buildroot}%{_bindir}/SvtAv1EncApp > %{buildroot}%{_mandir}/man1/SvtAv1EncApp.1

pushd gstreamer-plugin
%meson_install
popd

%files
%{_bindir}/SvtAv1DecApp
%{_bindir}/SvtAv1EncApp
%{_mandir}/man1/SvtAv1DecApp.1*
%{_mandir}/man1/SvtAv1EncApp.1*

%files libs
%license LICENSE.md PATENTS.md
%doc Docs CHANGELOG.md CONTRIBUTING.md README.md STYLE.md
%{_libdir}/libSvtAv1Dec.so.0*
%{_libdir}/libSvtAv1Enc.so.0*

%files devel
%{_includedir}/%{name}
%{_libdir}/libSvtAv1Dec.so
%{_libdir}/libSvtAv1Enc.so
%{_libdir}/pkgconfig/SvtAv1Dec.pc
%{_libdir}/pkgconfig/SvtAv1Enc.pc

%files -n gstreamer1-%{name}
%{_libdir}/gstreamer-1.0/libgstsvtav1enc.so

%changelog
* Wed Feb 17 21:30:29 CET 2021 Robert-André Mauchin <zebob.m@gmail.com> - 0.8.6-4
- Use upstream patch to fix rhbz#1927739

* Wed Feb 17 18:28:38 CET 2021 Robert-André Mauchin <zebob.m@gmail.com> - 0.8.6-3
- Add noexecstack
- Fix: rhbz#1927739

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Dec 05 20:20:29 CET 2020 Robert-André Mauchin <zebob.m@gmail.com> - 0.8.6-1
- Update to 0.8.6
- Close: rhbz#1902481

* Tue Nov 10 2020 Andreas Schneider <asn@redhat.com> - 0.8.5-2
- Add patch to fix building on modern Linux system

* Tue Nov 10 11:38:19 CET 2020 Robert-André Mauchin <zebob.m@gmail.com> - 0.8.5-1
- Update to 0.8.5
- Close: rhbz#1876641

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.4-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 30 18:53:17 CEST 2020 Robert-André Mauchin <zebob.m@gmail.com> - 0.8.4-1
- Update to 0.8.4 (#1851799)

* Fri Jun 19 18:36:37 CEST 2020 Robert-André Mauchin <zebob.m@gmail.com> - 0.8.3-1
- Update to 0.8.3

* Sun Feb 02 22:33:18 CET 2020 Robert-André Mauchin <zebob.m@gmail.com> - 0.8.1-1
- Update to 0.8.1

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Dec 23 00:16:09 CET 2019 Robert-André Mauchin <zebob.m@gmail.com> - 0.8.0-1
- Release 0.8.0 (#1785814)

* Thu Dec 05 23:08:19 CET 2019 Robert-André Mauchin <zebob.m@gmail.com> - 0.7.5-1
- Release 0.7.5 (#1776119)

* Thu Oct 10 18:51:11 CEST 2019 Robert-André Mauchin <zebob.m@gmail.com> - 0.7.0-1
- Release 0.7.0

* Wed Sep 18 2019 Vasiliy Glazov <vascom2@gmail.com> - 0.6.0-3
- Added gstreamer plugin

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jul 05 18:37:55 CEST 2019 Robert-André Mauchin <zebob.m@gmail.com> - 0.6.0-1
- Release 0.6.0

* Thu Jun 20 20:36:24 CEST 2019 Robert-André Mauchin <zebob.m@gmail.com> - 0.5.0-1.20190620gitcc2ee45
- Initial release
