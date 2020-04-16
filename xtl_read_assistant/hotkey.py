r"""
based on ctrl-alt-g-activate.py detect_lang via polyglot

playground\shortcut-key-python\ctrl-alt-g-activate.py
"""
# pylint: disable=invalid-name, missing-docstring

import asyncio
import traceback

# from textwrap import wrap
from textwrap import fill

from pynput import keyboard
from pyperclip import copy, paste
# import langid

from logzero import logger

# from google_tr import google_tr
from deepl_tr_async import deepl_tr_async as deepl_tr
from deepl_tr_async.deepl_tr_async import LOOP
from deepl_tr_async.google_tr_async import google_tr_async as google_tr
from detect_lang_pg import detect_lang
from load_env import load_env

# LOOP = asyncio.get_event_loop()
# arun = lambda _: LOOP.run_until_complete(_)


def arun(_):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(_)


def on_activate(from_lang="auto", to_lang="auto", width=50):
    # print('Global hotkey activated!')
    print('on_activate')

    try:
        cliptext = paste()
    except Exception as exc:
        logger.warning(" pyperclip paste error: %s", exc)
        return

    if from_lang == "auto":
        try:
            # fromlang = langid.classify(cliptext)[0]
            from_lang = detect_lang(cliptext)
        except Exception as exc:
            # logger.error("longid classify [cliptext[:10]:%s", exc)
            logger.error(" detect_lang exc: %s, setting to 'en'", exc)
            from_lang = "en"

    # trtext = google_tr(cliptext, to_lang=to_lang)
    coros = [
        deepl_tr(cliptext, from_lang=from_lang, to_lang=to_lang),
        google_tr(cliptext, from_lang=from_lang, to_lang=to_lang),
    ]
    # also translate to en if source not en
    if from_lang not in ["en"]:
        coros.extend([
            deepl_tr(cliptext, from_lang=from_lang, to_lang="en"),
            google_tr(cliptext, from_lang=from_lang, to_lang="en"),
        ])

    # also translate to en if source not en
    _ = """
    if from_lang not in ["en"]:
        _ = google_tr(cliptext, to_lang="en")
        outtext = f"{outtext}\n" + fill(_, wrap_width)
    _ = asyncio.gather(*coros)
    # """

    # _ = asyncio.gather(*coros)
    try:
        # loop = asyncio.get_event_loop()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        res = loop.run_until_complete(asyncio.gather(*coros))
        # res = arun(asyncio.gather(*coros))
    except Exception as exc:
        logger.error("%s, exiting...", exc)
        traceback.print_stack()
        return

    # _ = '\n'.join(wrap(trtext, wrap_width // 2))
    if to_lang in ['zh', 'ja']:
        outtext = fill('\n'.join(res), width // 2)
    else:
        outtext = fill('\n'.join(res), width)

    try:
        copy(outtext)
    except Exception as exc:
        logger.error("pyperclip copy error: %s", exc)

    logger.info(
        '\n%s -> translated and saved to clipboard-> \n%s',
        cliptext, outtext,
    )


def for_canonical(f):
    return lambda k: f(listener.canonical(k))
    # def func(k):
        # f(listener.canonical(k))  # pylint: disable=undefined-variable
    # return func


# def main():
if 1:
    """ main """

    hotkey_ = load_env("hotkey")
    if not hotkey_.strip():
        hotkey_ = "<ctrl>+<alt>+g"

    try:
        hotkey = keyboard.HotKey(
            # keyboard.HotKey.parse('<ctrl>+<alt>+g'),
            keyboard.HotKey.parse(hotkey_),
            lambda: on_activate(to_lang="zh"),
        )
    except Exception as exc:
        logger.error("%s, fallback to '<ctrl>+<alt>+g'", exc)
        hotkey_ = "<ctrl>+<alt>+g"
        hotkey = keyboard.HotKey(
            # keyboard.HotKey.parse('<ctrl>+<alt>+g'),
            keyboard.HotKey.parse(hotkey_),
            lambda: on_activate(to_lang="zh"),
        )

    # listener: keyboard.Listener  # pylint: disable=unused-variable
    with keyboard.Listener(
            # on_press=for_canonical(hotkey.press),
            # on_release=for_canonical(hotkey.release),
            on_press=lambda k: hotkey.press(listener.canonical(k)),
            on_release=lambda k: hotkey.release(listener.canonical(k)),
            # on_press=for_canonical(hotkey.press, listener),
            # on_release=for_canonical(hotkey.release, listener),
            # on_press=lambda _: listener.canonical(hotkey.press(_)),
            # on_release=lambda _: listener.canonical(hotkey.release(_)),
    ) as listener:
        logger.info(" Ready: %s ", hotkey_)
        listener.join()

# if __name__ == "__main__": main()
