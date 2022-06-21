%define pkg_base ea-openssl11
%define provider cpanel
%global _prefix /opt/%{provider}/%{pkg_base}
%global _opensslconfdir %{_prefix}/etc

# end of distribution specific definitions

Summary:    Cryptography and SSL/TLS Toolkit
Name:       ea-openssl11
%global _path_version 1.1
Version:    1.1.1p
# Doing release_prefix this way for Release allows for OBS-proof versioning, See EA-4544 for more details
%define release_prefix 1
Release: %{release_prefix}%{?dist}.cpanel
License:    OpenSSL
Group:      System Environment/Libraries
URL:        https://www.openssl.org/
Vendor:     OpenSSL
Source0:    https://www.openssl.org/source/openssl-%{version}.tar.gz
BuildRoot:  %{_tmppath}/openssl-%{version}-%{release}-root-%(%{__id_u} -n)

Patch0: 0001-Add-shlib_variant-to-get-an-ea-specific-version-of-o.patch

%description
The OpenSSL Project is a collaborative effort to develop a robust, commercial-grade, full-featured, and Open Source toolkit implementing the Transport Layer Security (TLS) and Secure Sockets Layer (SSL) protocols as well as a full-strength general purpose cryptography library. The project is managed by a worldwide community of volunteers that use the Internet to communicate, plan, and develop the OpenSSL toolkit and its related documentation.
OpenSSL is based on the excellent SSLeay library developed by Eric Young and Tim Hudson. The OpenSSL toolkit is licensed under an Apache-style license, which basically means that you are free to get and use it for commercial and non-commercial purposes subject to some simple license conditions.

%package devel
Summary: Files for development of applications which will use OpenSSL
Group: Development/Libraries
Requires: krb5-devel%{?_isa}, zlib-devel%{?_isa}
Requires: pkgconfig

%global debug_package %{nil}

%description devel
OpenSSL is a toolkit for supporting cryptography. The openssl-devel
package contains include files needed to develop applications which
support various cryptographic algorithms and protocols.

#%package static
#Summary:  Libraries for static linking of applications which will use OpenSSL
#Group: Development/Libraries
#Requires: %{name}-devel%{?_isa} = %{version}-%{release}
#
#%description static
#OpenSSL is a toolkit for supporting cryptography. The openssl-static
#package contains static libraries needed for static linking of
#applications which support various cryptographic algorithms and
#protocols.

%prep

%setup -q -n openssl-%{version}

%patch0 -p1

%build
# Force dependency resolution to pick /usr/bin/perl instead of /bin/perl
# This helps downstream users of our RPMS (see: EA-7468)

export PATH="/usr/bin:$PATH"
./config \
    -Wl,-rpath=%{_prefix}/%{_lib} \
    --prefix=%{_prefix} \
    --openssldir=%{_opensslconfdir}/pki/tls \
    no-ssl2 no-ssl3 shared -fPIC

make depend
make all

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_prefix}/ssl

make DESTDIR=$RPM_BUILD_ROOT install

# so PHP et all can find it on 64 bit machines
rm -rf $RPM_BUILD_ROOT%{_prefix}/lib64
ln -s %{_prefix}/lib $RPM_BUILD_ROOT/%{_prefix}/lib64

ln -s %{_prefix}/lib/libcrypto-ea.so.%{_path_version} $RPM_BUILD_ROOT/%{_prefix}/lib/libcrypto.so.%{_path_version}
ln -s %{_prefix}/lib/libssl-ea.so.%{_path_version} $RPM_BUILD_ROOT/%{_prefix}/lib/libssl.so.%{_path_version}

## Symlink to system certs

%__rm -rf $RPM_BUILD_ROOT%{_opensslconfdir}/pki/tls/{cert.pem,certs,misc,private}
%__ln_s /etc/pki/tls/cert.pem $RPM_BUILD_ROOT%{_opensslconfdir}/pki/tls/
%__ln_s /etc/pki/tls/certs $RPM_BUILD_ROOT%{_opensslconfdir}/pki/tls/
%__ln_s /etc/pki/tls/misc $RPM_BUILD_ROOT%{_opensslconfdir}/pki/tls/
%__ln_s /etc/pki/tls/private $RPM_BUILD_ROOT%{_opensslconfdir}/pki/tls/

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre

%files
%defattr(-,root,root,-)
%dir %{_prefix}/
%{_prefix}/bin
%{_prefix}/lib
%{_prefix}/lib64
%docdir %{_prefix}/man
%{_prefix}/ssl
%{_prefix}/etc
%{_prefix}/share
%config(noreplace) %{_opensslconfdir}/pki/tls/openssl.cnf
%attr(0755,root,root) %{_prefix}/lib/libcrypto-ea.so.%{_path_version}
%attr(0755,root,root) %{_prefix}/lib/libssl-ea.so.%{_path_version}

%files devel
%defattr(-,root,root)
%{_prefix}/include

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%changelog
* Tue Jun 21 2022 Cory McIntire <cory@cpanel.net> - 1.1.1p-1
- EA-10773: Update ea-openssl11 from v1.1.1o to v1.1.1p
- The c_rehash script allows command injection (CVE-2022-2068)

* Tue May 03 2022 Cory McIntire <cory@cpanel.net> - 1.1.1o-1
- EA-10676: Update ea-openssl11 from v1.1.1n to v1.1.1o

* Tue Mar 15 2022 Cory McIntire <cory@cpanel.net> - 1.1.1n-1
- EA-10564: Update ea-openssl11 from v1.1.1m to v1.1.1n
- Infinite loop in BN_mod_sqrt() reachable when parsing certificates (CVE-2022-0778)

* Tue Dec 28 2021 Dan Muey <dan@cpanel.net> - 1.1.1m-2
- ZC-9589: Update DISABLE_BUILD to match OBS

* Thu Dec 16 2021 Cory McIntire <cory@cpanel.net> - 1.1.1m-1
- EA-10363: Update ea-openssl11 from v1.1.1l to v1.1.1m

* Thu Aug 26 2021 Cory McIntire <cory@cpanel.net> - 1.1.1l-1
- EA-10072: Update ea-openssl11 from v1.1.1k to v1.1.1l

* Thu Mar 25 2021 Cory McIntire <cory@cpanel.net> - 1.1.1k-1
- EA-9664: Update ea-openssl11 from v1.1.1j to v1.1.1k

* Mon Feb 22 2021 Cory McIntire <cory@cpanel.net> - 1.1.1j-1
- EA-9590: Update ea-openssl11 from v1.1.1i to v1.1.1j
  Null pointer deref in X509_issuer_and_serial_hash() (CVE-2021-23841)
  Incorrect SSLv2 rollback protection (CVE-2021-23839)
  Integer overflow in CipherUpdate (CVE-2021-23840)

* Thu Dec 10 2020 Cory McIntire <cory@cpanel.net> - 1.1.1i-1
- EA-9478: Update ea-openssl11 from v1.1.1h to v1.1.1i

* Fri Sep 25 2020 Cory McIntire <cory@cpanel.net> - 1.1.1h-1
- EA-9320: Update ea-openssl11 from v1.1.1g to v1.1.1h

* Wed Sep 16 2020 Tim Mullin <tim@cpanel.net> - 1.1.1g-3
- EA-9303: Fix ea-openssl11 directory removal flags

* Thu May 07 2020 Julian Brown <julian.brown@cpanel.net> - 1.1.1g-2
- ZC-6733: Get it to build on C8

* Tue Apr 21 2020 Cory McIntire <cory@cpanel.net> - 1.1.1g-1
- EA-9017: Update ea-openssl11 from v1.1.1f to v1.1.1g

* Thu Apr 02 2020 Cory McIntire <cory@cpanel.net> - 1.1.1f-1
- EA-8961: Update ea-openssl11 from v1.1.1e to v1.1.1f

* Fri Mar 27 2020 Cory McIntire <cory@cpanel.net> - 1.1.1e-1
- EA-8946: Update ea-openssl11 from v1.1.1d to v1.1.1e

* Wed Sep 25 2019 Julian Brown <julian.brown@cpanel.net> - 1.1.1d-1
- ZC-5506: Create ea-openssl11 package for openssl v1.1.1

