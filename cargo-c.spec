Summary:	Helper program to build and install C-like libraries
Summary(pl.UTF-8):	Program pomocniczy do budowania i instalowania bibliotek w stylu C
Name:		cargo-c
Version:	0.8.0
Release:	1
License:	MIT
Group:		Development/Tools
#Source0Download: https://github.com/lu-zero/cargo-c/releases
Source0:	https://github.com/lu-zero/cargo-c/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	12a73f24e289ee7cb2a9f59bb1b40e50
# cd %{name}-%{version}
# cargo vendor
# cd ..
# tar cJf cargo-c-crates-%{version}.tar.xz %{name}-%{version}/{vendor,Cargo.lock}
Source1:	%{name}-crates-%{version}.tar.xz
# Source1-md5:	03687edfea85d34bd70887af26108a07
URL:		https://github.com/lu-zero/cargo-c
BuildRequires:	cargo >= 0.45
BuildRequires:	curl-devel
#BuildRequires:	libgit2-devel >= 1.1.0
BuildRequires:	libssh2-devel
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	rust >= 1.49
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Cargo subcommands to build and install C-ABI compatible dynamic and
static libraries.

%description -l pl.UTF-8
Podpolecenia Cargo do budowania i instalowania zgodnych z ABI C
bibliotek dynamicznych i statycznych.

%prep
%setup -q -b1

# bundled:
# curl 7.76.0 vendor/curl-sys/curl
# libgit2 1.1.0 vendor/libgit2-sys/libgit2
# nghttp2 1.43.0 vendor/libnghttp2-sys/nghttp2 (but system nghttp2 is not supported in rust)
# libssh 1.9.0 vendor/libssh2-sys/libssh2
# zlib 1.2.11 vendor/libz-sys/src/zlib
# zlib-ng 1.9.9 vendor/libz-sys/src/zlib-ng

# use our offline registry
export CARGO_HOME="$(pwd)/.cargo"

mkdir -p "$CARGO_HOME"
cat >.cargo/config <<EOF
[source.crates-io]
replace-with = 'vendored-sources'

[source.vendored-sources]
directory = '$PWD/vendor'
EOF

%build
export CARGO_HOME="$(pwd)/.cargo"
export LIBSSH2_SYS_USE_PKG_CONFIG=1

cargo -vv build --release --frozen

%install
rm -rf $RPM_BUILD_ROOT
export CARGO_HOME="$(pwd)/.cargo"
export LIBSSH2_SYS_USE_PKG_CONFIG=1

cargo -vv install --frozen --path . --root $RPM_BUILD_ROOT%{_prefix}
%{__rm} $RPM_BUILD_ROOT%{_prefix}/.crates*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README.md
%attr(755,root,root) %{_bindir}/cargo-capi
%attr(755,root,root) %{_bindir}/cargo-cbuild
%attr(755,root,root) %{_bindir}/cargo-cinstall
