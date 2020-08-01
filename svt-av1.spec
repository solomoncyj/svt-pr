%global _description %{expand:
The Scalable Video Technology for AV1 Encoder (SVT-AV1 Encoder) is an
AV1-compliant encoder library core. The SVT-AV1 development is a
work-in-progress targeting performance levels applicable to both VOD and Live
encoding / transcoding video applications.}

Name:           svt-av1
Version:        0.8.4
Release:        3%{?dist}
Summary:        Scalable Video Technology for AV1 Encoder

# Main library: BSD-2-Clause-Patent
# Source/Lib/Common/Codec/EbHmCode.c: BSD
# Source/App/EncApp/EbAppString.*
# Source/Lib/Common/Codec/EbString.*
# Source/Lib/Common/Codec/vector.*: MIT
# Source/Lib/Common/ASM_SSE2/x86inc.asm: ISC
# Source/App/DecApp/EbMD5Utility.*: PublicDomain
License:        BSD-2-Clause-Patent and BSD and MIT and ISC and Public Domain
URL:            https://github.com/OpenVisualCloud/SVT-AV1
Source0:        %url/archive/v%{version}/%{name}-%{version}.tar.gz

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
mkdir _build
pushd _build
# https://github.com/OpenVisualCloud/SVT-AV1/issues/999
# Use -fcommon until all tho global variables are fixed upstream
export CFLAGS="%build_cflags -fcommon"
export CXXFLAGS="%build_cxxflags -fcommon"
%cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo \
       -DCMAKE_INSTALL_PREFIX=%{_prefix} \
       -DCMAKE_INSTALL_LIBDIR=%{_lib} \
       -DCMAKE_ASM_NASM_COMPILER=yasm \
       -DCMAKE_SKIP_INSTALL_RPATH=ON \
       -DBUILD_SHARED_LIBS=ON \
       -DBUILD_TESTING=OFF \
       -DNATIVE=OFF \
       ..
%make_build
popd

pushd gstreamer-plugin
    export LIBRARY_PATH="$PWD/../Bin/RelWithDebInfo:$LIBRARY_PATH"
    %meson
    %meson_build
popd

%install
pushd _build
%make_install
rm -f %{buildroot}%{_libdir}/*.{a,la}

mkdir -p %{buildroot}/%{_mandir}/man1
export PATH=$PATH:%{buildroot}%{_bindir}
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:%{buildroot}%{_libdir}
help2man -N --help-option=-help --version-string=%{version} SvtAv1DecApp > %{buildroot}%{_mandir}/man1/SvtAv1DecApp.1
help2man -N --help-option=-help --no-discard-stderr --version-string=%{version} SvtAv1EncApp > %{buildroot}%{_mandir}/man1/SvtAv1EncApp.1
popd

pushd gstreamer-plugin
    %meson_install
popd

%files
%{_bindir}/SvtAv1DecApp
%{_bindir}/SvtAv1EncApp
%{_mandir}/man1/SvtAv1DecApp.1*
%{_mandir}/man1/SvtAv1EncApp.1*

%files libs
%license LICENSE.md
%doc Docs CHANGELOG.md NOTICES.md README.md STYLE.md
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
