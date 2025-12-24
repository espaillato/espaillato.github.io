---
layout: post
title: "Windows + WSL Development Environment (Setup Guide)"
date: 2025-12-24
---

This document describes **exactly** how to reproduce my current personal development environment:

- [Windows as host OS](#preconditions)
- [WSL2 (Ubuntu) as the development OS](#wsl2-ubuntu)
- [Bash + Starship](#bash-starship)
- [Java](#java-toolchain), [Python](#python-pyenv), [Rust](#rust), [Node.js](#nodejs) (clean, isolated, reproducible)
- [VS Code + AI (ChatGPT for reasoning, Continue for execution)](#vscode-wsl)
- [Git hardened for SSH + GitHub privacy](#git-ssh-github-privacy)
- [Minimal but powerful CLI tooling](#common-cli-tools)

This is **not** a generic guide. Follow it top-to-bottom for the same result.

---

## 0. Preconditions {#preconditions}

- Windows 10 22H2+ or Windows 11
- Virtualization enabled in BIOS
- A GitHub account
- ChatGPT Plus account (for reasoning; API optional)

---

## 1. Install WSL2 + Ubuntu {#wsl2-ubuntu}

Open **PowerShell as Administrator**:

```powershell
wsl --install
```

Reboot when prompted.

After reboot, open **Windows Terminal** and select **Ubuntu**.

Create:
- Linux username
- Linux password

### Verify WSL version

```powershell
wsl -l -v
```

Expected:
```
Ubuntu    Running    2
```

---

## 2. Update Linux Base System

Inside Ubuntu:

```bash
sudo apt update && sudo apt upgrade -y
```

Install baseline packages:

```bash
sudo apt install -y \
  build-essential \
  curl wget unzip zip \
  ca-certificates gnupg lsb-release
```

---

## 3. Shell: Bash + Starship {#bash-starship}

### Ensure Bash is default shell

```bash
echo $SHELL
```

If not `/bin/bash`:

```bash
chsh -s /bin/bash
exec bash
```

### Install Starship

```bash
curl -sS https://starship.rs/install.sh | sh
```

Enable it:

```bash
echo 'eval "$(starship init bash)"' >> ~/.bashrc
exec bash
```

### Starship configuration

Create config:

```bash
mkdir -p ~/.config
nano ~/.config/starship.toml
```

Paste:

```toml
format = "$username$directory$git_branch$git_status$java$cmd_duration $character"
add_newline = false

[username]
show_always = false
style_user = "dimmed white"
style_root = "bold red"
format = "[$user]($style) "

[directory]
truncate_to_repo = true
style = "bold cyan"
format = "[$path]($style)"

[git_branch]
symbol = "  "
style = "bold purple"
format = "[$symbol$branch]($style)"

[git_status]
style = "yellow"
format = "[$all_status]($style)"

[java]
symbol = " ☕ "
style = "red"
format = "[$symbol$version]($style)"

[cmd_duration]
min_time = 500
style = "dimmed white"
format = " [⏱ $duration]($style)"

[character]
success_symbol = "\\$"
error_symbol = "\\$!"

[hostname]
disabled = true
[time]
disabled = true
[battery]
disabled = true
[memory_usage]
disabled = true
```

Reload:

```bash
exec bash
```

Verify:
```
~ $
```

---

## 4. VS Code + WSL {#vscode-wsl}

### Install VS Code (Windows)

Download: https://code.visualstudio.com

Install with defaults.

### Install extensions

In VS Code → Extensions (Windows side):

- Remote - WSL

Inside the WSL environment (server-side extensions):

- Python
- Pylance
- Python Environments
- Debugpy
- Extension Pack for Java
- Maven for Java
- Gradle for Java
- Java Debugger
- Java Test Runner
- Java Dependency Viewer
- ShellCheck
- Continue

### Launch VS Code from WSL

```bash
cd ~
code .
```

Verify bottom-left shows:
```
WSL: Ubuntu
```

---

## 5. Java Toolchain (SDKMAN) {#java-toolchain}

### Install SDKMAN

```bash
curl -s "https://get.sdkman.io" | bash
source "$HOME/.sdkman/bin/sdkman-init.sh"
```

Verify:
```bash
sdk version
```

### Install JDKs

```bash
sdk install java 21-tem
sdk install java 17-tem
sdk default java 21-tem
```

Verify:
```bash
java -version
```

### Maven & Gradle

```bash
sdk install maven
sdk install gradle
```

---

## 6. Python (pyenv + venv-first) {#python-pyenv}

### Install dependencies

```bash
sudo apt install -y \
  python3 python3-venv python3-pip \
  pipx \
  libssl-dev zlib1g-dev libbz2-dev \
  libreadline-dev libsqlite3-dev \
  libffi-dev xz-utils tk-dev
```

### Install pyenv

```bash
curl https://pyenv.run | bash
```

Add to `~/.bashrc`:

```bash
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
```

Reload:
```bash
exec bash
```

Install Python:

```bash
pyenv install 3.12.8
pyenv global 3.12.8
python --version
```

### Project workflow

```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
```

---

## 7. Node.js (nvm) {#nodejs}

### Install nvm

```bash
curl -fsSL https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
exec bash
```

### Install Node

```bash
nvm install --lts
nvm alias default lts/*
node -v
```

---

## 8. Rust {#rust}

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
exec bash
rustup component add rustfmt clippy
```

---

## 9. Common CLI Tools {#common-cli-tools}

```bash
sudo apt install -y \
  jq ripgrep fd-find bat tree htop \
  lsof dnsutils file less httpie shellcheck
```

Aliases:

```bash
echo "alias fd=fdfind" >> ~/.bashrc
echo "alias bat=batcat" >> ~/.bashrc
exec bash
```

---

## 10. Personal `~/bin` (symlinked)

```bash
mkdir -p ~/projects/oss/dotfiles/bin
ln -s ~/projects/oss/dotfiles/bin ~/bin
```

Add to PATH (if not already):

```bash
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
exec bash
```

---

## 11. Git (SSH + GitHub privacy) {#git-ssh-github-privacy}

### SSH preference

```bash
git config --global url."git@github.com:".insteadOf "https://github.com/"
```

### Conditional identity

Create `~/.gitconfig-github`:

```ini
[user]
  name = <Name>
  email = <Github Public Email>
```

Add to `~/.gitconfig`:

```ini
[includeIf "hasconfig:remote.*.url:https://github.com/**"]
  path = ~/.gitconfig-github
```

Verify:

```bash
git config --show-origin --get user.email
```

---

## 12. Final Verification Checklist

```bash
which java
which python
which node
which cargo
which git
```

All should resolve inside `$HOME`.

Prompt should show `$`, not `>`.

---

## End State

You now have:

- Windows as host
- Linux as dev OS
- Clean multi-language toolchains
- Deterministic shell
- SSH-first Git
- Minimal, professional CLI environment

This setup is intentionally boring — and built to last.
