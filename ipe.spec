Summary:	Drawing editor for creating figures in PDF or PostScript formats
Summary(pl.UTF-8):	Edytor do tworzenia rysunków w formacie PDF i PostScript
Name:		ipe
Version:	7.1.2
Release:	1
License:	GPL v3
Group:		X11/Applications/Graphics
Source0:	https://downloads.sourceforge.net/ipe7/%{name}-%{version}-src.tar.gz
# Source0-md5:	887f65359d60e184a446cbe77def5176
Patch0:		%{name}-ipeletdir.patch
URL:		https://ipe.otfried.org/
BuildRequires:	QtCore-devel >= 4
BuildRequires:	QtGui-devel >= 4
BuildRequires:	cairo-devel
BuildRequires:	freetype-devel >= 2
BuildRequires:	gtk+2-devel >= 1:2.0
BuildRequires:	libstdc++-devel
BuildRequires:	lua51-devel >= 5.1
BuildRequires:	pkgconfig
BuildRequires:	qt4-build >= 4
BuildRequires:	sed >= 4.0
BuildRequires:	zlib-devel
Requires:	%{name}-libs = %{version}-%{release}
Suggests:	texlive-format-pdflatex
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Ipe is a drawing editor for creating figures in PDF or (encapsulated)
Postscript format. It supports making small figures for inclusion into
LaTeX-documents as well as making multi-page PDF presentations that
can be shown on-line with a PDF viewer.

%description -l pl.UTF-8
Edytor do tworzenia rysunków w formacie PDF lub (osadzonym)
PostScript. Pozwala tworzyć małe rysunki do włączenia do dokumentów
LaTeXa, a także wielostronnicowe prezentacje PDF, nadające się do
pokazywania przy użyciu przeglądarki PDF.

%package libs
Summary:	Ipe libraries
Summary(pl.UTF-8):	Biblioteki Ipe
Group:		X11/Libraries

%description libs
This package provides libraries for Ipe.

%description libs -l pl.UTF-8
Ten pakiet zawiera biblioteki współdzielone Ipe.

%package devel
Summary:	Header files for Ipe libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek Ipe.
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	libstdc++-devel

%description devel
This package provides header files for Ipe libraries.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe bibliotek Ipe.

%prep
%setup -q
%patch0 -p1

%{__sed} -i -e 's/lua5.1/lua51/g' src/config.mak
%{__sed} -i -e '1s,/usr/bin/env ipescript,%{_bindir}/ipescript,' scripts/*.lua

%build
%{__make} -C src \
	IPEPREFIX=%{_prefix} \
	IPELIBDIR=%{_libdir} \
	CXX="%{__cxx}" \
	CXXFLAGS="%{rpmcxxflags} -fPIC" \
	IPE_USE_ICONV="-DIPE_USE_ICONV" \
	luatest=

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C src install \
	INSTALL_ROOT=$RPM_BUILD_ROOT \
	IPEPREFIX=%{_prefix} \
	IPELIBDIR=%{_libdir} \
	luatest=

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc news.txt readme.txt
%attr(755,root,root) %{_bindir}/ipe
%attr(755,root,root) %{_bindir}/ipe6upgrade
%attr(755,root,root) %{_bindir}/ipeextract
%attr(755,root,root) %{_bindir}/iperender
%attr(755,root,root) %{_bindir}/ipescript
%attr(755,root,root) %{_bindir}/ipetoipe
%attr(755,root,root) %{_bindir}/ipeview
%dir %{_libdir}/ipe
%dir %{_libdir}/ipe/7.1.2
%dir %{_libdir}/ipe/7.1.2/ipelets
%attr(755,root,root) %{_libdir}/ipe/7.1.2/ipelets/image.so
%{_libdir}/ipe/7.1.2/ipelets/*.lua
%{_datadir}/ipe
%{_mandir}/man1/ipe.1*
%{_mandir}/man1/ipe6upgrade.1*
%{_mandir}/man1/ipeextract.1*
%{_mandir}/man1/iperender.1*
%{_mandir}/man1/ipescript.1*
%{_mandir}/man1/ipetoipe.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libipe.so.7.1.2
%attr(755,root,root) %{_libdir}/libipecairo.so.7.1.2
%attr(755,root,root) %{_libdir}/libipecanvas.so.7.1.2
%attr(755,root,root) %{_libdir}/libipelua.so.7.1.2
%attr(755,root,root) %{_libdir}/libipeui.so.7.1.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libipe.so
%attr(755,root,root) %{_libdir}/libipecairo.so
%attr(755,root,root) %{_libdir}/libipecanvas.so
%attr(755,root,root) %{_libdir}/libipelua.so
%attr(755,root,root) %{_libdir}/libipeui.so
%{_includedir}/ipe*.h
