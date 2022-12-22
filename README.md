# MYSSO

## Installation

```bash
pip install git+https://github.com/chiemerieezechukwu/mysso.git
```

## Usage

- To refresh your sso credentials and switch profiles, do:

```bash
mysso
```

Note that the current terminal session is not switched automatically. This will happen with subsequent terminal windows. To switch the current terminal, source the ~/.aws_current_profile file

```bash
source ~/.aws_current_profile
```

or to do it more automatedly, add an alias to your ~/.zshrc or ~/.bashrc like below

alias mysso="mysso; source ~/.aws_current_profile"
