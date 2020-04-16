""" reading assistant """

import logzero
import pyperclip
from logzero import logger


def read_assistant():
    """ reading assistant """
    logger.info("hello from read_assistant")

def hello():
    print("hello from hello")

def main():
    read_assistant()


if __name__ == "__main__":
    main()
