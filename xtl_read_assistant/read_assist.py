r"""
X as a third language reading assistant tool

Translate the clipboard content
"""

# based on playground\shortcut-key-python\janus-ctrl-alt-g-activate.py

import asyncio
from textwrap import fill

import janus
from pynput import keyboard
import pyperclip
# from pyperclip import copy, paste
# import langid

from absl import app, flags
import logzero
from logzero import logger

from deepl_tr_async import deepl_tr_async, __version__
# from google_tr import google_tr
from deepl_tr_async.google_tr_async import google_tr_async
# from detect_lang_pg import detect_lang
from deepl_tr_async.detect_lang import detect_lang

# from proc_absl import proc_absl

loop = asyncio.get_event_loop()  # pylint: disable=invalid-name
queue = janus.Queue(loop=loop)  # pylint: disable=invalid-name

# s_lang = "de"  # pylint: disable=invalid-name
# lang_list = ["en", "en", "de"]  # pylint: disable=invalid-name
# services = ["deepl", "google", ]  # pylint: disable=invalid-name

DEEPL_LANG = ["zh", "en", "de", "fr", "es", "pt", "it", "nl", "pt", "ru"]
DEEPL_LANG_STR = ", ".join(DEEPL_LANG)


FLAGS = flags.FLAGS
flags.DEFINE_string(
    "z-extra-info",
    "info",
    "supply text anywhere in the command line when --nocopyfrom",
)
flags.DEFINE_string(
    # 'from-lang',
    "mother-lang",
    "zh",
    "mother tongue language, default chinese (zh). Pick one from: %s" % DEEPL_LANG_STR,
    short_name="m",
)
flags.DEFINE_string(
    # 'to-lang',
    "second-lang",
    "en",
    "second language, default english (en). Pick one from: %s" % DEEPL_LANG_STR,
    short_name="s",
)
flags.DEFINE_string(
    # 'to-lang',
    "third-lang",
    "de",
    "third language, defaut german (de). Pick one from: %s" % DEEPL_LANG_STR,
    short_name="t",
)

flags.DEFINE_boolean(
    "auto",
    True,
    "auto detect source lang, if False, fall back to third-lang",
    short_name="a",
)

flags.DEFINE_integer(
    "width", 60, "display width", short_name="w",
)
flags.DEFINE_boolean(
    "copyto", True, "copy the result to clipboard", short_name="c",
)

flags.DEFINE_boolean(
    "debug", False, "print debug messages", short_name="d",
)
flags.DEFINE_boolean(
    "version", False, "print version and exit", short_name="V",
)

# FLAGS(shlex.split("app --from-lang=en"))


# def proc_absl(argv: list):  # pylint: disable=too-many-statements, too-many-branches
def read_assist(  # pylint: disable=too-many-statements, too-many-branches
        argv: list,
        debug: bool = False,
):
    """ proc_argv """

    del argv
    if FLAGS.debug:  # pragma: no cover
        logzero.loglevel(10)  # logging.DEBUG
    else:
        logzero.loglevel(20)  # logging.INFO

    width = FLAGS.width

    # version = "0.0.2"
    if FLAGS.version:  # pragma: no cover
        indent = " " * 10
        msg = indent + "xtl read-assistant tool %s\n\n" % __version__
        msg1 = "Brought to you by mu@qq41947782. Join qq group 316287378 to be kept updated about this tool."
        msg1 = fill(
            msg1,
            width=width,
            replace_whitespace=False,
            initial_indent=indent,
            subsequent_indent=indent,
        )
        print(msg + msg1)
        raise SystemExit(0)
    if debug:
        return FLAGS.m, FLAGS.s, FLAGS.t

    loop.run_until_complete(trans_clipb())
    return None

# def on_activate():
def on_trans_hk():  # pragma: no cover
    """ hotkey translate clipboard"""
    logger.debug('Global hotkey activated')
    cliptext = pyperclip.paste()
    indent = " " * 4
    _ = fill(
        cliptext,
        replace_whitespace=False,
        initial_indent=indent,
        subsequent_indent=indent,
    )
    # copy to the clipboard
    pyperclip.copy(_)

    queue.sync_q.put(cliptext)


def on_exit_hk():
    """ hotkey inject _exit to queue for exit """
    # print('111 Global hotkey activated!')
    queue.sync_q.put("_exit")


_ = """
def for_canonical(f):
    # return lambda k: f(listener.canonical(k))
    def func(k):
        return f(listener.canonical(k))
    return func

def for_canonical1(f):
    return lambda k: f(l1.canonical(k))
# """


async def trans_clipb():  # pylint: disable=too-many-locals  # pragma: no cover
    """ translate the clipboard """

    while True:
        # wait forever if none in the queue

        # data = await queue.async_q.get()
        # print("data: ", data)

        # raise QueueEmpty if queue is empty
        # no need for await
        # data = queue.async_q.get_nowait()

        try:
            data = queue.async_q.get_nowait()
            # print(" get_nowait: ", data)
            if data.upper() in ["_EXIT", "_QUIT"]:
                break  # exit

            text = data[:]
            try:
                text = text.strip()
            except Exception as exc:
                text = ""
                logger.warning("text.strip() exc: %s, exiting...", exc)

            if not text:
                continue

            # make it unique and not the same as s_lang
            if FLAGS.auto:
                s_lang = detect_lang(text)
                logger.info(" detected language: %s", s_lang)
            else:
                s_lang = FLAGS.t

            lang_list = []
            for elm in [FLAGS.m, FLAGS.s, FLAGS.t, ]:
                if elm not in lang_list and elm not in [s_lang]:
                    lang_list.append(elm)

            if not lang_list:  # this wont ever be true
                logger.info(" languages picked: %s", [FLAGS.m, FLAGS.s, FLAGS.t, ])
                logger.warning(
                    " Nothing to do. Select proper languages and source text and try again, exiting... ..."
                )
                continue

            if len(lang_list) < 2:
                logger.warning(
                    " Only one language %s is selected. We'll proceed tho.", lang_list
                )

            # arg = FLAGS
            # logger.debug("%s %s %s %s", arg.m, arg.s, arg.t, arg.w)

            # check lang in DEEPL_LANG list
            _ = True
            for elm in lang_list:
                if elm not in DEEPL_LANG:
                    _ = False
                    logger.warning(" %s not in %s, deepl cannot be used", elm, DEEPL_LANG)
            if _:
                services = ["dl", "gl"]
            else:
                services = ["gl"]
            logger.info("translate services: %s", services)

            logger.debug("s_lang lang_list, services, copyto, width, debug: %s, %s, %s, %s, %s, %s", s_lang, lang_list, services, FLAGS.copyto, FLAGS.width, FLAGS.debug)

            # data = text[:]
            coros = []
            for lang in lang_list:
                for service in services:
                    if service in ['dl']:
                        coros.append(deepl_tr_async(data, s_lang, lang))
                    else:
                        coros.append(google_tr_async(data, s_lang, lang))

            # loop.get_event_loop()
            try:
                # res = await deepl_tr_async(data)
                logger.info("%s", "diggin ... (takes ~10 secs), Hotkeys: ctrl-alt-g/ctrl-alt-x")
                res = await asyncio.gather(*coros)
            except Exception as exc:
                logger.error("exc: %s, %s", exc, exc.args)
                res = exc.args[0]

            # res = fill("\n".join(res), width=50, replace_whitespace=0)

            width = 82
            width = FLAGS.width
            width_ = width // 2 if detect_lang(data) in ["zh", "ja"] else width
            indent = " " * 3
            text0 = fill(
                data,
                width=width_,
                replace_whitespace=False,
                initial_indent=indent,
                subsequent_indent=indent,
            )

            width = 80
            width = FLAGS.width
            indent = " " * 5
            len2 = len(indent)
            if len(services) < 2:
                prefix_list = ["", ""]
            else:
                prefix_list = ["dl: ", "gl: "] * len(lang_list)

            text = ""
            for idx, elm in enumerate(res):
                width_ = width // 2 if detect_lang(elm) in ["zh", "ja"] else width
                len1 = len(prefix_list[idx])
                initial_indent = prefix_list[idx][:len1] + indent[len1:len2]
                elm_ = fill(
                    elm,
                    width=width_,
                    replace_whitespace=False,
                    initial_indent=initial_indent,
                    subsequent_indent=indent,
                )
                text += f"{elm_}\n"

            pyperclip.copy(text)
            pyperclip.copy(text)
            logger.info("\n%s", f"{text0}\n{text}")
        except asyncio.queues.QueueEmpty:
            # expected
            pass
        except Exception as exc:
            # other exc
            logger.error("exc: %s", exc)
            # break
            continue

        await asyncio.sleep(.4)

    # print('Done.')
    msg = "Brought to you by mu@qq41947782. Join qq-group 316287378 (https://jq.qq.com/?_wv=1027&k=5TuKBSn) to be kept updated about this tool."
    msg = fill(msg, initial_indent=" " * 10, subsequent_indent=" " * 10, width=60)
    qrcode = """
▄▄▄▄▄▄▄ ▄▄   ▄  ▄▄ ▄  ▄▄▄▄▄▄▄
█ ▄▄▄ █ ▄  ▄▄█ ▄█▀█ █ █ ▄▄▄ █
█ ███ █ ██▄█ ▄▄▀███▄▀ █ ███ █
█▄▄▄▄▄█ ▄▀▄ █ █ █ ▄▀█ █▄▄▄▄▄█
▄▄▄▄  ▄ ▄▀ ▀ ██▀▄█▀█▄▄  ▄▄▄ ▄
█▀▀▀ ▀▄█▀▀    ▄▀█▄ ▀▀ ▀▀▀ ▄▄▀
▄▄▀▄▀ ▄██▄ █▀▀▀▀▀▄▄▄██▀▄ ▄▄ ▀
 ▀▄▄▀▄▄▀▀▀▀▄▀▄ ▀█▀▄▄▄▀ ▄ ███
▀ ▀██▀▄▄█▀█▄▀▀ ▀█ ▀█▀█▀█▄▄ █
▄▀▀▄▀ ▄▀▀█▀▄█▀ █ ▄▀ ▄▄ ▄▄▀█▀
▄█▀█▄▄█▄ ▄▄█▄  ▀█▀▀▄███▄▄█
▄▄▄▄▄▄▄ ▀██▄██▀▀█ █▄█ ▄ ██▀█▀
█ ▄▄▄ █  █  ▄ ▄▄▄▄ ▀█▄▄▄█▀▄▀▀
█ ███ █ ██ █▀▄▀▀ ▄ ▀█▀ ▄▀▀▄ █
█▄▄▄▄▄█ █▄ ▀▄ ███  ▄█▄█▄▄▀ █

    """
    qrcode = fill(qrcode, initial_indent="", subsequent_indent="", replace_whitespace=False)
    del qrcode
    # logger.info("%s\n%s", qrcode, msg)
    # print("%s\n%s" % (qrcode, msg))
    print("%s" % msg)


# def main0():
def main():  # pragma: no cover
    """ main """

    hotkey = keyboard.HotKey(
        keyboard.HotKey.parse('<ctrl>+<alt>+g'),
        # lambda: on_activate(to_lang="zh"),
        # on_activate,
        on_trans_hk,
    )

    hotkey1 = keyboard.HotKey(
        keyboard.HotKey.parse('<ctrl>+<alt>+x'),
        # lambda: on_activate(to_lang="zh"),
        # on_activate1,
        on_exit_hk,
    )

    _ = """
    with keyboard.Listener(
            on_press=for_canonical(hotkey.press),
            on_release=for_canonical(hotkey.release)
    ) as l:
        logger.info(" ready: ctrl-alt-g to activate ")
        l.join()
    # """

    listener = keyboard.Listener(
        # on_press=for_canonical(hotkey.press),
        # on_release=for_canonical(hotkey.release),
        on_press=lambda k: hotkey.press(listener.canonical(k)),
        on_release=lambda k: hotkey.release(listener.canonical(k)),  # type: ignore
        # on_press=hotkey.press(getattr(listener, "canonical")),  # this does not work
    )
    listener.start()
    print("hotkey ctrl-alt-g ...")

    ln1 = keyboard.Listener(
        # on_press=for_canonical1(hotkey1.press),
        # on_release=for_canonical1(hotkey1.release)
        on_press=lambda k: hotkey1.press(ln1.canonical(k)),
        on_release=lambda k: hotkey1.release(ln1.canonical(k)),  # type: ignore
    )
    ln1.start()
    print("hotkey ctrl-alt-x to quit ...")

    app.run(read_assist)


if __name__ == "__main__":
    main()
