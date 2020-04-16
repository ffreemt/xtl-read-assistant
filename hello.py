""" __main__, to run:
python -m xtl_reading_assistant

"""

import logzero
import pyperclip
from logzero import logger

from absl import app, flags
FLAGS = flags.FLAGS
# flags.DEFINE_string("names", None, "cookie names (default ['BDUSS', 'BAIDUID'].")  # noqa=E501

flags.DEFINE_list(
    'names',
    ['BDUSS', 'BAIDUID', 'STOKEN', 'PTOKEN'],
    "cookie names, if set to * (--names=*), output all available cookie values.",  # noqa=E501
)

flags.DEFINE_boolean('copyto', True, 'copy to clipboard')
# flags.DEFINE_boolean('bduss_only', True, 'copy only BDUSS to clipboard')
flags.DEFINE_boolean(
    'cookies',
    False,
    'if True copy cookies format (BDUSS=x..z; BAIDUID=...) else, copy value',
)
flags.DEFINE_boolean('debug', False, 'print debug messages.')

# ['names', 'copyto', 'bduss_only', 'cookies', 'debug', ]

# import shlex
# FLAGS(shlex.split('app --names=*'))
# print(FLAGS)


def main0(argv):
    '''__main__.main'''
    text = " ".join(argv[1:])
    # del argv  # Unused

    logger.info("text: %s", text)
    if FLAGS.debug:
        logzero.loglevel(10)
    else:
        logzero.loglevel(20)

    # logger.debug('\n\t args: %s', FLAGS)
    logger.debug('\n\t args: %s', [(elm, getattr(FLAGS, elm)) for elm in FLAGS])  # noqa=E501

    _ = ['names', 'copyto', 'cookies', 'debug']
    # args = dict((elm, getattr(FLAGS, elm)) for elm in _)

    # logger.debug('\n\t args: %s', args)

    # get everything first


def main():
    app.run(main0)
    # print("hello")

if __name__ == '__main__':
    # app.run(main)  # => sys.exit(main(sys.argv))
    main()
