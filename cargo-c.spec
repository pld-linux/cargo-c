Summary:	Helper program to build and install C-like libraries
Summary(pl.UTF-8):	Program pomocniczy do budowania i instalowania bibliotek w stylu C
Name:		cargo-c
Version:	0.6.9
Release:	2
License:	MIT
Group:		Development/Tools
#Source0Download: https://github.com/lu-zero/cargo-c/releases
Source0:	https://github.com/lu-zero/cargo-c/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	2028688ba7eef600d3667e97210369cd
# cd %{name}-%{version}
# cargo vendor
# cd ..
# tar cJf cargo-c-crates-%{version}.tar.xz %{name}-%{version}/{vendor,Cargo.lock}
Source1:	%{name}-crates-%{version}.tar.xz
# Source1-md5:	e4386b8606d728f945e7dcf5eecde9cc
URL:		https://github.com/lu-zero/cargo-c
BuildRequires:	cargo >= 0.45
BuildRequires:	curl-devel
#BuildRequires:	libgit2-devel >= 1.0.0
BuildRequires:	libssh2-devel
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	rust
BuildRequires:	zlib-devel
ExclusiveArch:	%{ix86} %{x8664} x32 aarch64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_debugsource_packages	0
%ifarch	x32
%define		target_opt	--target x86_64-unknown-linux-gnux32
%else
%define		target_opt	%{nil}
%endif

%description
Cargo subcommands to build and install C-ABI compatible dynamic and
static libraries.

%description -l pl.UTF-8
Podpolecenia Cargo do budowania i instalowania zgodnych z ABI C
bibliotek dynamicznych i statycznych.

%prep
%setup -q -b1

# bundled:
# curl 7.71.1 vendor/curl-sys/curl
# libgit2 1.0.1 vendor/libgit2-sys/libgit2
# nghttp2 1.33.90 vendor/libnghttp2-sys/nghttp2 (but system nghttp2 is not supported in rust)
# libssh 1.9.0 vendor/libssh2-sys/libssh2
# zlib 1.2.11 vendor/libz-sys/src/zlib

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
export PKG_CONFIG_ALLOW_CROSS=1

cargo -vv build --release --frozen %{target_opt}

%install
rm -rf $RPM_BUILD_ROOT
export CARGO_HOME="$(pwd)/.cargo"
export LIBSSH2_SYS_USE_PKG_CONFIG=1
export PKG_CONFIG_ALLOW_CROSS=1

cargo -vv install --frozen %{target_opt} \
	--path . \
	--root $RPM_BUILD_ROOT%{_prefix}

%{__rm} $RPM_BUILD_ROOT%{_prefix}/.crates*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README.md
%attr(755,root,root) %{_bindir}/cargo-capi
%attr(755,root,root) %{_bindir}/cargo-cbuild
%attr(755,root,root) %{_bindir}/cargo-cinstall
