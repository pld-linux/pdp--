Summary:	PDP++ - neural network simulation software
Summary(pl):	PDP++ - oprogramowanie do symulacji sieci neuronowych
Name:		pdp++
Group:		Development
Group(pl):	Programowanie
Version:	1.3
Release:	1
License:	distributable
Source0:	ftp://grey.colorado.edu/pub/oreilly/pdp++/%{name}_%{version}_src.tar.gz
Source1:	ftp://grey.colorado.edu/pub/oreilly/pdp++/%{name}_%{version}_ivinc.tar.gz
Source2:	ftp://grey.colorado.edu/pub/oreilly/pdp++/%{name}_%{version}_ivlib_LINUX_g++.tar.gz
BuildRequires:	gcc-c++
BuildRequires:	libstdc++-devel
BuildRequires:	XFree86-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description

%description -l pl

%prep
%setup -q -c -a 1

%build
cd pdp++
make LOCAL=$RPM_BUILD_DIR/%{name}-%{version} CPU=LINUX IDIRS_EXTRA="-I. -I.."

%install

%files
%defattr(644,root,root,755)
