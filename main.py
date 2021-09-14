from flask import abort, jsonify, Response
from svg_generator import svg_generate
from json_generator import json_generate

URL = "https://us-central1-universal-stats-326006.cloudfunctions.net"


def parse(request):
    request_args = request.args

    tokenId = ""

    if request_args and 'tokenId' in request_args:
        tokenId = request_args['tokenId']

    if not tokenId:
        abort(404)

    hexstr = tokenId

    if not tokenId.startswith("0x"):
        hexstr = "{0:#0{1}x}".format(int(tokenId), 66)

    if not hexstr.startswith("0x"):
        abort(404)

    workStr = hexstr[2:]

    if len(workStr) != 64:
        abort(404)

    return workStr


def add_cache_control(response):
    # Cache response for 24 hours
    response.headers.add("Cache-Control", "public, max-age=86400")

    return response


def metadata(request):
    tokenId = parse(request)

    return add_cache_control(
        jsonify(json_generate(tokenId, URL)))


def image(request):
    tokenId = parse(request)

    return add_cache_control(
        Response(svg_generate(tokenId), mimetype="image/svg+xml"))
