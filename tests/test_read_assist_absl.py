""" test absl """
from absl import flags
from xtl_read_assistant import read_assist


def test_absl():
    """ test absl """
    # app.run(read_assist)
    flags.FLAGS(['app', ])
    m_lang, s_lang, t_lang = read_assist([], debug=True)
    assert m_lang == "zh"
    assert s_lang == "en"
    assert t_lang == "de"
