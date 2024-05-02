Name:		fzf
Version:	0.51.0
Release:	1%{?dist}
Summary:	A command-line fuzzy finder
License:	MIT license
URL:		https://github.com/junegunn/fzf
Source0:	https://github.com/junegunn/fzf/archive/refs/tags/%{version}.tar.gz

BuildRequires:	golang
BuildRequires:	git
BuildRequires:	systemd-rpm-macros

%global _hardened_build 1
%global debug_package %{nil}

%description
fzf is a general-purpose command-line fuzzy finder.

%prep
%autosetup -n %{name}-%{version}

%build
GO111MODULE=on CGO_ENABLED=0 go build -v -trimpath -buildmode=pie -modcacherw -tags netgo -ldflags="-s -w -X main.version=%{version} -X main.revision=tarball" -o %{name}
gzip man/man1/fzf.1
gzip man/man1/fzf-tmux.1
rm -rf shell/key-bindings.fish shell/key-bindings.zsh 
sed -i -e '/^#!\//, 1d' shell/completion.*
sed -i -e '1d;2i#!/bin/bash' bin/fzf-tmux

%install
install -Dpm 0755 %{name} %{buildroot}%{_bindir}/%{name}
install -Dpm 0755 bin/%{name}-tmux %{buildroot}%{_bindir}/%{name}-tmux
install -Dpm 0644 man/man1/fzf.1.gz %{buildroot}%{_mandir}/man1/fzf.1.gz
install -Dpm 0644 man/man1/fzf-tmux.1.gz %{buildroot}%{_mandir}/man1/fzf-tmux.1.gz
install -Dpm 0644 shell/completion.bash %{buildroot}/etc/bash_completion.d/%{name}_completion.bash
	
install -d %{buildroot}%{_datadir}/fzf/shell
install -Dpm0644 shell/key-bindings.* %{buildroot}%{_datadir}/fzf/shell/

%files
%{_bindir}/fzf
%{_bindir}/fzf-tmux
%{_mandir}/man1/fzf.1.gz
%{_mandir}/man1/fzf-tmux.1.gz
%{_sysconfdir}/bash_completion.d/%{name}_completion.bash
%{_datadir}/fzf/shell/key-bindings.bash

%changelog
* Mon May 2 2024 Danie de Jager - 0.51.0-1
* Mon Apr 15 2024 Danie de Jager - 0.50.0-1
* Thu Apr 4 2024 Danie de Jager - 0.49.0-1
* Thu Mar 14 2024 Danie de Jager - 0.48.0-1
* Sun Mar 10 2024 Danie de Jager - 0.47.0-1
* Mon Feb 5 2024 Danie de Jager - 0.46.1-1
- Bug fixes and improvements
- Updated rivo/uniseg dependency to v0.4.6
* Thu Jan 25 2024 Danie de Jager - 0.46.0-1
* Wed Nov 22 2023 Danie de Jager - 0.44.1-2
- fix: version info was previously not correct
* Wed Nov 22 2023 Danie de Jager - 0.44.1-1
- fix: Fixed crash when preview window is hidden on focus event
