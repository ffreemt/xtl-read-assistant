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

This is no longer necessary. But make sure an updated version of deepl-tr-async is used (at least 0.0.3, deepl-tr-async 0.0.3 and up uses pyppeteer2). E.g.
```
pip install deepl-tr-async -U
```

If for some reason you have to use `pyppeteer` istead of `pyppeteer2`, do this patch https://github.com/miyakogi/pyppeteer/pull/160/files

(
`xtl-read-assistant` relies on `deepl-tr-async` which in turns relies on `pyppeteer` that again replies on `websockets`. `pyppeteer`, however, does not play well with new versions of websockets 8.x. Hence, either downgrade websockts to 6.x or patch manually according to [https://github.com/miyakogi/pyppeteer/pull/160/files] or use pyppeteer2)

### Usage

Run `read-assist.exe`; Copy text to the clipboard (`ctrl-c`); Activate hotkey (`ctrl-alt-g`)

The translated text is stored in the clipboard.

#### default setup: --mother-lang=zh --second-lang=en --third-lang=de
`read-assist`

`ctrl-alt-g`: to activate clipboard translation
`ctrl-alt-x`: to exit

#### other setup exmaple: --mother-lang=zh --second-lang=en --third-lang=fr

`read-assist --third-lang=fr`
