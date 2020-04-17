# from xtl_read_assistant import __version__
from deepl_tr_async import __version__


def test_version():
    assert __version__[:4] == '0.0.'
