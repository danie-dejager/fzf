Name:		fzf
Version:	0.60.1
Release:	1%{?dist}
Summary:	A command-line fuzzy finder
License:	MIT license
URL:		https://github.com/junegunn/fzf
Source0:	https://github.com/junegunn/fzf/archive/refs/tags/v%{version}.tar.gz

BuildRequires:	golang
BuildRequires:	git
BuildRequires:	systemd-rpm-macros
Requires:	bash

%global _hardened_build 1
%global debug_package %{nil}

%description
fzf is a general-purpose command-line fuzzy finder.

%package fish-completion
Summary: Fish completion files for %{name}
Requires: fish
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description fish-completion
%{summary}

%package zsh-completion
Summary: ZSH completion files for %{name}
Requires: zsh
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description zsh-completion
%{summary}

%prep
%autosetup -n %{name}-%{version}

%build
GO111MODULE=on CGO_ENABLED=0 go build -v -trimpath -buildmode=pie -modcacherw -tags netgo -ldflags="-s -w -X main.version=%{version} -X main.revision=tarball" -o %{name}
gzip man/man1/fzf.1
gzip man/man1/fzf-tmux.1

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_mandir}/man1
mkdir -p %{buildroot}%{_sysconfdir}/bash_completion.d
mkdir -p %{buildroot}%{_datadir}/fish/completions
mkdir -p %{buildroot}%{_datadir}/zsh/site-functions

install -pm 0755 %{name} %{buildroot}%{_bindir}/%{name}
install -pm 0755 bin/%{name}-tmux %{buildroot}%{_bindir}/%{name}-tmux
install -pm 0644 man/man1/fzf.1.gz %{buildroot}%{_mandir}/man1/fzf.1.gz
install -pm 0644 man/man1/fzf-tmux.1.gz %{buildroot}%{_mandir}/man1/fzf-tmux.1.gz

# Create shell completion configuration files
echo 'eval "$(fzf --bash)"' > %{buildroot}%{_sysconfdir}/bash_completion.d/fzf-completion.sh
echo 'source <(fzf --zsh)' > %{buildroot}%{_datadir}/zsh/site-functions/_fzf
echo 'fzf --fish | source' > %{buildroot}%{_datadir}/fish/completions/fzf.fish

%files
%{_bindir}/fzf
%{_bindir}/fzf-tmux
%{_mandir}/man1/fzf.1.gz
%{_mandir}/man1/fzf-tmux.1.gz
%{_sysconfdir}/bash_completion.d/fzf-completion.sh

%files zsh-completion
%{_datadir}/zsh/site-functions/_fzf

%files fish-completion
%{_datadir}/fish/completions/fzf.fish

%changelog
* Fri Feb 21 2025 - Danie de Jager - 0.60.1-1
* Wed Feb 12 2025 - Danie de Jager - 0.60.0-1
* Mon Feb 3 2025 - Danie de Jager - 0.59.0-1
* Mon Jan 20 2025 - Danie de Jager - 0.58.0-1
* Tue Dec 17 2024 - Danie de Jager - 0.57.0-1
* Mon Nov 25 2024 - Danie de Jager - 0.56.3-2
- Improve shell completions for fish and zsh.
* Mon Nov 25 2024 - Danie de Jager - 0.56.3-1
- Bug fixes in zsh scripts
-- fix(zsh): handle backtick trigger edge case (#4090)
-- revert(zsh): remove 'fc -RI' call in the history widget (#4093)
* Mon Nov 25 2024 - Danie de Jager - 0.56.3-1
- Bug fixes in zsh scripts
-- fix(zsh): handle backtick trigger edge case (#4090)
-- revert(zsh): remove 'fc -RI' call in the history widget (#4093)
* Mon Nov 11 2024 - Danie de Jager - 0.56.2-1
* Mon Nov 11 2024 - Danie de Jager - 0.56.1-1
* Sun Oct 27 2024 - Danie de Jager - 0.56.0-1
* Fri Aug 30 2024 - Danie de Jager - 0.55.0-1
* Thu Aug 1 2024 - Danie de Jager - 0.54.3-1
- Fixed incompatibility of adaptive height specification and 'start:reload'
- Environment variables are now available to $FZF_DEFAULT_COMMAND
* Fri Jul 26 2024 - Danie de Jager - 0.54.2-1
* Fri Jul 19 2024 - Danie de Jager - 0.54.1-1
* Mon Jul 8 2024 - Danie de Jager - 0.54.0-1
* Fri Jun 7 2024 - Danie de Jager - 0.53.0-1
* Tue May 7 2024 - Danie de Jager - 0.52.0-1
* Mon May 2 2024 - Danie de Jager - 0.51.0-1
* Mon Apr 15 2024 - Danie de Jager - 0.50.0-1
* Thu Apr 4 2024 - Danie de Jager - 0.49.0-1
* Thu Mar 14 2024 - Danie de Jager - 0.48.0-1
* Sun Mar 10 2024 - Danie de Jager - 0.47.0-1
* Mon Feb 5 2024 - Danie de Jager - 0.46.1-1
- Bug fixes and improvements
- Updated rivo/uniseg dependency to v0.4.6
* Thu Jan 25 2024 - Danie de Jager - 0.46.0-1
* Wed Nov 22 2023 - Danie de Jager - 0.44.1-2
- fix: version info was previously not correct
* Wed Nov 22 2023 - Danie de Jager - 0.44.1-1
- fix: Fixed crash when preview window is hidden on focus event
