Summary:	PDP++ - neural network simulation software
Summary(pl):	PDP++ - oprogramowanie do symulacji sieci neuronowych
Name:		pdp++
Group:		Development
Group(pl):	Programowanie
Version:	2.01
Release:	1
License:	distributable
Source0:	ftp://grey.colorado.edu/pub/oreilly/pdp++/%{name}_%{version}_src.tar.gz
Source1:	ftp://grey.colorado.edu/pub/oreilly/pdp++/%{name}_2.0_ext.tar.gz
Source2:	ftp://grey.colorado.edu/pub/oreilly/pdp++/iv-pdp-r2.0.tar.gz
Patch0:		pdp++-xopen.patch
Patch1:		pdp++-link.patch
Patch2:		pdp++-g++.patch
Patch3:		pdp++-strfile.patch
Patch4:		pdp++-DESTDIR.patch
Patch5:		pdp++-leabra.patch
BuildRequires:	gcc-c++
BuildRequires:	libstdc++-devel
BuildRequires:	XFree86-devel
BuildRequires:	ncurses-devel
BuildRequires:	ed
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
ExclusiveArch:	%{ix86}

%description

%description -l pl

%prep
%setup -q -c -a 1 -a 2
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
ln -sf iv-pdp-r2.0/src interviews

cd iv-pdp-r2.0
CXXFLAGS="-fno-exceptions -fno-rtti $RPM_OPT_FLAGS" ; export CXXFLAGS
%configure
%{__make}

cd ../pdp++
CPU=LINUX; export CPU
LD_LIBRARY_PATH=$RPM_BUILD_DIR/%{name}-%{version}/pdp++/lib/$CPU:$RPM_BUILD_DIR/%{name}-%{version}/interviews/lib/lib-g++/$CPU; export LD_LIBRARY_PATH

%{__make} world \
	LOCAL=$RPM_BUILD_DIR/%{name}-%{version} \
	PDPDESTDIR=%{_datadir}/%{name} \
	OPT_FLAG="$RPM_OPT_FLAGS -Wall -Winline -DPDPDESTDIR=\\\"%{_datadir}/%{name}\\\""

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_infodir},%{_datadir}/pdp++/defaults}

cd iv-pdp-r2.0
%{__make} install DESTDIR=$RPM_BUILD_ROOT

cd ../pdp++

rm -f demo/bench/{pdp++bench/pdp++bench,aptest/[ap]test}
rm -f lib/LINUX/*{hard,min,iberty}* 
rm -f manual/html/.log

install -s bin/LINUX/* $RPM_BUILD_ROOT%{_bindir}/
install -s lib/LINUX/*.so $RPM_BUILD_ROOT%{_libdir}/

cp -a manual/info/{pdp,ta}* $RPM_BUILD_ROOT%{_infodir}/
cp -a {config,css,defaults,demo} $RPM_BUILD_ROOT%{_datadir}/pdp++/

(cd $RPM_BUILD_ROOT%{_datadir}/pdp++
perl -pi -e "s|/usr/local/bin/css|%{_bindir}/css|g" \
	css/demo/get_trn_epcs.cc css/tests/exec_test.css \
	css/include/css_awk.css demo/css/get_trn_epcs.cc

chmod 755 css/demo/get_trn_epcs.cc css/tests/exec_test.css \
	css/include/css_awk.css demo/css/get_trn_epcs.cc \
	demo/bench/leabra_bench.css)

find $RPM_BUILD_ROOT -name '*~' -print | xargs rm -f

gzip -9nf ANNOUNCE* CopyRight NEWS README TODO

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc pdp++/{ANNOUNCE*,CopyRight,NEWS,README,TODO}.gz
%doc pdp++/manual/{*.ps.gz,html}
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.la
%attr(755,root,root) %{_libdir}/lib*.so
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%{_includedir}/*
%{_infodir}/*
%dir %{_datadir}/pdp++
%attr(-,root,root) %{_datadir}/pdp++/*
