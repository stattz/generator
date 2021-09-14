#! /usr/local/bin/python

import json
from svg_generator import svg_generate
from json_generator import json_generate


def read():
    val = input("Enter your token ID: ")

    hexstr = val

    if not val.startswith("0x"):
        hexstr = "{0:#0{1}x}".format(int(val), 66)

    print(f"Considering: {hexstr}")

    if not hexstr.startswith("0x"):
        raise Exception("Invalid hex string")

    workStr = hexstr[2:]

    if len(workStr) != 64:
        raise Exception("Invalid hex string size")

    return workStr


tokenId = read()

print(json.dumps(json_generate(tokenId, "")))

with open(f"out/0x{tokenId}.svg", 'w') as wf:
    wf.write(svg_generate(tokenId))
