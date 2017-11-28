%define	snap	20131127
%define	rel	14
Summary:	Primecoin - First Scientific Computing Cryptocurrency
Name:		primecoin
Version:	0.1.2
Release:	2.%{snap}.%{rel}
License:	MIT/X11
Group:		X11/Applications
# Source0:	https://github.com/primecoin/primecoin/archive/v%{version}.tar.gz
Source0:	%{name}-20131127.tar.bz2
# Source0-md5:	10ae9950aba9232a3c035e499c38aa74
Patch0:		build-i486.patch
Patch1:		boost-1.58.patch
Patch2:		miniupnpc-2.0.patch
URL:		http://primecoin.org
BuildRequires:	QtCore-devel
BuildRequires:	QtDBus-devel
BuildRequires:	QtGui-devel
BuildRequires:	boost-devel
BuildRequires:	db-cxx-devel
BuildRequires:	miniupnpc-devel >= 1.5
BuildRequires:	openssl-devel
BuildRequires:	qrencode-devel
BuildRequires:	qt4-qmake
Requires:	perl-base
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Primecoin - First Scientific Computing Cryptocurrency.

%package qt
Summary:	Qt-based Primecoin Wallet
Group:		X11/Applications

%description qt
Qt-based Primecoin Wallet.

%prep
%setup -q -n %{name}-%{snap}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
qmake-qt4 bitcoin-qt.pro \
	USE_UPNP=1 \
	USE_DBUS=1 \
	USE_QRCODE=1

%{__make}

%{__make} -C src -f makefile.unix \
	CXX="%{__cxx}" \
	CXXFLAGS="%{rpmcflags} %{rpmcxxflags} %{rpmcppflags}"

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}/%{name},%{_mandir}/man{1,5},%{_localedir},%{_desktopdir},%{_pixmapsdir},%{_datadir}/kde4/services}

install src/primeminer $RPM_BUILD_ROOT%{_bindir}/primeminer
install primecoin-qt $RPM_BUILD_ROOT%{_bindir}

sed -e 's#bitcoin#primecoin#g' contrib/debian/bitcoin-qt.desktop > $RPM_BUILD_ROOT%{_desktopdir}/primecoin-qt.desktop
sed -e 's#bitcoin#primecoin#g' contrib/debian/bitcoin-qt.protocol > $RPM_BUILD_ROOT%{_datadir}/kde4/services/primecoin-qt.protocol

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc/*.txt contrib/debian/examples/bitcoin.conf
%attr(755,root,root) %{_bindir}/primeminer

%files qt
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/primecoin-qt
%{_datadir}/kde4/services/primecoin-qt.protocol
%{_desktopdir}/primecoin-qt.desktop
