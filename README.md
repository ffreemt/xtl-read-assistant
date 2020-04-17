# xtl-read-assistant ![build](https://github.com/ffreemt/xtl-read-assistant/workflows/build/badge.svg)[![codecov](https://codecov.io/gh/ffreemt/xtl-read-assistant/branch/master/graph/badge.svg)](https://codecov.io/gh/ffreemt/xtl-read-assistant)[![PyPI version](https://badge.fury.io/py/xtl-read-assistant.svg)](https://badge.fury.io/py/xtl-read-assistant)
x as a third language reading assistant tool

### Pre-installation of libicu

###### For Linux/OSX

E.g.
* Ubuntu: `sudo apt install libicu-dev`
* Centos: `yum install libicu`
* OSX: `brew install icu4c`

###### For Windows

Download and install the pyicu and pycld2 whl packages for your OS version from https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyicu and https://www.lfd.uci.edu/~gohlke/pythonlibs/#pycld2

### Installation
```pip install xtl-read-assistant```

Validate installation
```
python -c "import xtl_read_assistant; print(xtl_read_assistant.__version__)"
# 0.0.2 or other version info
```
#### Patch `pyppeteer/connection.py`

This is no longer necessary. But may sure an updated version of deepl-tr-async (at least 0.0.3, deepl-tr-async 0.0.3 and up uses pyppeteer2) is used. E.g.
```
pip install deepl-tr-async -U
```

### Usage

Run `read-assist.exe`; Copy text to the clipboard (`ctrl-c`); Activate hotkey (`ctrl-alt-g`)

The translated text is stored in the clipboard.

#### default setup: --mother-lang=zh --second-lang=en --third-lang=de
`read-assist`

`ctrl-alt-g`: to activate clipboard translation
`ctrl-alt-x`: to exit

#### other setup exmaple: --mother-lang=zh --second-lang=en --third-lang=fr

`read-assist --third-lang=fr`
