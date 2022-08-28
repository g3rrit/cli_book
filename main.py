#!/usr/bin/env python3

import sys
import json
import os
import signal
import re
import subprocess

import requests
import click
from py_stringmatching.similarity_measure.monge_elkan import MongeElkan


CONF_FILE = os.path.expanduser("~/.config/.cli_book.json")
CONFIG = None

CLQ = "«"
CRQ = "»"
ELLIPSIS = "…"

class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


def translate(sentence: str, src_lang: str, target_lang: str):
    cmd = f"echo {sentence} | trans -b -s {src_lang} -t {target_lang}"
    p = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE)
    out = p.communicate()[0]
    return out.decode().replace("\n", "")


def save_config(*args):

    global CONFIG

    if CONFIG is None:
        return

    with open(CONF_FILE, "w") as fd:
        json.dump(CONFIG, fd)

    print("Quitting")
    sys.exit(0)


def normalize(ins: str) -> str:
    return ins.lower()

def compare(s1: str, s2: str) -> float:
    me = MongeElkan()
    return me.get_raw_score(s1.split(" "), s2.split(" "))


@click.command()
@click.option("--book", type=str, required=True, help="Name of the book")
@click.option("--path", type=str, required=False, help="Path to the text file of the book")
@click.option("--lang", type=str, required=False, help="Language of the book")
@click.option("--nlang", default="de", type=str, required=False, help="Native language")
def main(book: str, path: str, lang: str, nlang: str):

    global CONFIG

    if not os.path.exists(CONF_FILE):
        with open(CONF_FILE, "w") as fd:
            json.dump({ "version": 1 }, fd)

    signal.signal(signal.SIGINT, save_config)

    with open(CONF_FILE, "r") as fd:
        CONFIG = json.load(fd)

    print(f"Selected book: {book}")

    if book not in CONFIG:
        print(f"Creating new book")

        if path is None:
            print("Please specify a path")
            sys.exit(-1)

        if lang is None:
            print("Please specify a language")
            sys.exit(-1)

        CONFIG[book] = {
            "path": path,
            "lang": lang,
            "nlang": nlang,
            "sentence": 0,
        }

    book_config = AttrDict(CONFIG[book])

    with open(book_config.path, "r") as fd:
        book_text = fd.read()

    regex = r"(.*?(?:" + "|".join([f"\.{CRQ}", f"\!{CRQ}", f"\?{CRQ}", "\.", "\!", "\?"]) + r"))"
    book_text = re.split(regex, book_text)

    book_text = [ s.strip() for s in book_text if s.strip() != "" ]

    book_text = book_text[book_config.sentence:]

    for sentence in book_text:

        print("#################")
        print(sentence)
        print("-")
        in_trans = input(":")
        in_trans = normalize(in_trans)
        print("=")
        out_trans = translate(normalize(sentence), book_config.lang, book_config.nlang)
        out_trans = normalize(out_trans)
        me_score = compare(in_trans, out_trans)
        print(f"[{me_score:.2f}] ::: {out_trans}")

        CONFIG[book]["sentence"] += 1

    save_config()


if __name__ == "__main__":
    main()
