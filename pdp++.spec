Summary:	PDP++ - neural network simulation software
Summary(pl):	PDP++ - oprogramowanie do symulacji sieci neuronowych
Name:		pdp++
Group:		Development
Group(pl):	Programowanie
Version:	2.0a
Release:	1
License:	distributable
Source0:	ftp://grey.colorado.edu/pub/oreilly/pdp++/%{name}_%{version}_src.tar.gz
Source1:	ftp://grey.colorado.edu/pub/oreilly/pdp++/%{name}_%{version}_ext.tar.gz
Source2:	ftp://grey.colorado.edu/pub/oreilly/pdp++/iv-pdp2.tar.gz
Source3:	pdp++-ta_TA.cc
Patch0:		pdp++-2.0a-iv.patch
Patch1:		pdp++-xopen.patch
Patch2:		pdp++-2.0a-link.patch
Patch3:		pdp++-g++.patch
Patch4:		pdp++-strfile.patch
Patch5:		pdp++-DESTDIR.patch
Patch6:		pdp++-ansic.patch
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
#%patch6 -p1

%build
ln -s iv-pdp2/src interviews

cd iv-pdp2
CPU=`make CPU`; export CPU
make World CCDRIVER="g++ -fno-exceptions -fno-rtti $RPM_OPT_FLAGS" \
	OPTIMIZE_CCFLAGS="$RPM_OPT_FLAGS"

cd ../pdp++
LD_LIBRARY_PATH=$RPM_BUILD_DIR/%{name}-%{version}/pdp++/lib/$CPU:$RPM_BUILD_DIR/%{name}-%{version}/interviews/lib/lib-g++/$CPU; export LD_LIBRARY_PATH

make chkcpu include_dir lib_dir bin_dir Makefiles new_lib_h Maketa \
	force_ta new_lib_h \
	LOCAL=$RPM_BUILD_DIR/%{name}-%{version} \
	PDPDESTDIR=%{_datadir}/%{name} \
	OPT_FLAG="$RPM_OPT_FLAGS -Wall -Winline -DPDPDESTDIR=\\\"%{_datadir}/%{name}\\\""

install -m644 %{SOURCE3} src/ta/LINUX/ta_TA.cc
install -m644 %{SOURCE3} src/ta/LINUX/ta_TA.ccx
install -m644 %{SOURCE3} src/ta/ta_TA.cc
install -m644 %{SOURCE3} src/ta/ta_TA.ccx

make Libs LibsPass2 distBins \
	LOCAL=$RPM_BUILD_DIR/%{name}-%{version} \
	PDPDESTDIR=%{_datadir}/%{name} \
	OPT_FLAG="$RPM_OPT_FLAGS -Wall -Winline -DPDPDESTDIR=\\\"%{_datadir}/%{name}\\\""

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_includedir},{%{_datadir}/{pdp++/defaults,interviews}}}
cd pdp++
ln -sf ../iv-pdp2/src interviews

rm -f demo/bench/{pdp++bench/pdp++bench,aptest/[ap]test}
rm -f lib/LINUX/*{hard,min,iberty}* 

install -s bin/LINUX/* $RPM_BUILD_ROOT%{_bindir}/
install -s lib/LINUX/*.so $RPM_BUILD_ROOT%{_libdir}/
install -s interviews/lib/IV/LINUX/libIV.so.* $RPM_BUILD_ROOT%{_libdir}/

cp -a interviews/include $RPM_BUILD_ROOT%{_datadir}/interviews/
cp -a lib/interviews/* $RPM_BUILD_ROOT%{_datadir}/interviews/

cp -a {config,css,defaults,demo,manual} $RPM_BUILD_ROOT%{_datadir}/pdp++/
cp -a {ANNOUNCE*,C*,INSTALL,NEWS,README,TODO} $RPM_BUILD_ROOT%{_datadir}/pdp++/

ln -s ../share/interviews/include $RPM_BUILD_ROOT%{_includedir}/interviews

cd $RPM_BUILD_ROOT%{_datadir}/pdp++

mv -f css/demo/get_trn_epcs.cc css/demo/get_trn_epcs.cc.TMP
sed 's#/usr/local/bin/css#%{_bindir}/css#' css/demo/get_trn_epcs.cc.TMP > css/demo/get_trn_epcs.cc
rm -f css/demo/get_trn_epcs.cc.TMP

mv -f css/tests/exec_test.css css/tests/exec_test.css.TMP
sed 's#/usr/local/bin/css#%{_bindir}/css#' css/tests/exec_test.css.TMP >css/tests/exec_test.css
rm -f css/tests/exec_test.css.TMP

mv -f css/include/css_awk.css css/include/css_awk.css.TMP
sed 's#/usr/local/bin/css#%{_bindir}/css#' css/include/css_awk.css.TMP > css/include/css_awk.css
rm -f css/include/css_awk.css.TMP

mv -f demo/css/get_trn_epcs.cc demo/css/get_trn_epcs.cc.TMP
sed 's#/usr/local/bin/css#%{_bindir}/css#'  demo/css/get_trn_epcs.cc.TMP > demo/css/get_trn_epcs.cc
rm -f demo/css/get_trn_epcs.cc.TMP

sed 's#/usr/local/bin/leabra++ -nogui -f leabra_bench.css#%{_bindir}/leabra++ -nogui#' demo/bench/leabra_bench.css~ > demo/bench/leabra_bench.css
rm -f demo/bench/leabra_bench.css~

rm -f manual/texi2html

chmod 755 css/demo/get_trn_epcs.cc css/tests/exec_test.css \
	css/include/css_awk.css demo/css/get_trn_epcs.cc \
	demo/bench/leabra_bench.css

find $RPM_BUILD_ROOT -name '*~' -print | xargs rm -f

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/*
%attr(755,root,root) %{_includedir}/interviews
%attr(-,root,root) %{_datadir}/*
