Summary:	PDP++ - neural network simulation software
Summary(pl):	PDP++ - oprogramowanie do symulacji sieci neuronowych
Name:		pdp++
Group:		Development
Version:	2.01
Release:	1
License:	distributable
Source0:	ftp://grey.colorado.edu/pub/oreilly/pdp++/%{name}_%{version}_src.tar.gz
# Source0-md5:	626d2f517438a063ec3e2e3593fdb06a
Source1:	ftp://grey.colorado.edu/pub/oreilly/pdp++/%{name}_2.0_ext.tar.gz
# Source1-md5:	f98e57f9dceeac972eb7272e1b9d81bd
Source2:	ftp://grey.colorado.edu/pub/oreilly/pdp++/iv-pdp-r2.0.tar.gz
# Source2-md5:	b532ca00a4662ba8fef0c111e61831ed
Patch0:		%{name}-xopen.patch
Patch1:		%{name}-link.patch
Patch2:		%{name}-g++.patch
Patch3:		%{name}-strfile.patch
Patch4:		%{name}-DESTDIR.patch
Patch5:		%{name}-leabra.patch
Patch6:		%{name}-FLT_MAX.patch
BuildRequires:	gcc-c++
BuildRequires:	libstdc++-devel
BuildRequires:	XFree86-devel
BuildRequires:	ncurses-devel
BuildRequires:	ed
BuildRequires:	perl
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
ExclusiveArch:	%{ix86}

%description
Neural network simulation software.

%description -l pl
Oprogramowanie do symulacji sieci neuronowych.

%prep
%setup -q -c -a 1 -a 2
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%build
ln -sf iv-pdp-r2.0/src interviews

cd iv-pdp-r2.0
CXXFLAGS="%{rpmcflags} -fno-exceptions -fno-rtti"
%configure2_13
%{__make}

cd ../pdp++
CPU=LINUX; export CPU
LD_LIBRARY_PATH=$RPM_BUILD_DIR/%{name}-%{version}/pdp++/lib/$CPU:$RPM_BUILD_DIR/%{name}-%{version}/interviews/lib/lib-g++/$CPU; export LD_LIBRARY_PATH

%{__make} world \
	LOCAL=$RPM_BUILD_DIR/%{name}-%{version} \
	PDPDESTDIR=%{_datadir}/%{name} \
	OPT_FLAG="%{rpmcflags} -Wall -Winline -DPDPDESTDIR=\\\"%{_datadir}/%{name}\\\""

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_infodir},%{_datadir}/pdp++/defaults}

cd iv-pdp-r2.0
%{__make} install DESTDIR=$RPM_BUILD_ROOT

cd ../pdp++

rm -f demo/bench/{pdp++bench/pdp++bench,aptest/[ap]test}
rm -f lib/LINUX/*{hard,min,iberty}*
rm -f manual/html/.log

install bin/LINUX/* $RPM_BUILD_ROOT%{_bindir}/
install lib/LINUX/*.so $RPM_BUILD_ROOT%{_libdir}/

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

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc pdp++/{ANNOUNCE*,CopyRight,NEWS,README,TODO}
%doc pdp++/manual/{*.ps*,html}
%attr(755,root,root) %{_bindir}/*
%{_libdir}/lib*.la
%attr(755,root,root) %{_libdir}/lib*.so
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%{_includedir}/*
%{_infodir}/*
%dir %{_datadir}/pdp++
%attr(-,root,root) %{_datadir}/pdp++/*
