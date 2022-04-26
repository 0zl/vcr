# vnr. https://shiro.eu.org/
# this is dead simple and not very secure python script w/ bad practices approach.
# simplified version from C(Hastag) .NETF, because its make absolute clusterfuck allocating for a simple Buffers.
# 2022 april, ize.

from urllib.parse import unquote
from flask import Flask, request, Response
import pyvcroid2 # thx /Nkyoku

# load config.txt file with keys and values
config = {}
with open("config.txt", "r", encoding="utf8") as f:
    for line in f.readlines():
        if line.startswith("#"):
            continue
        key, value = line.split("=")
        config[key] = value.strip()

# check if config.dir is empty, throw an error
if config["dir"] == "":
    raise Exception("bruh?")

def synthesize(params):
    with pyvcroid2.VcRoid2(install_path=config["dir"], install_path_x86=config["dir"]) as vc:
        vc.loadLanguage(params["l"])
        vc.loadVoice(params["vc"])

        vc.param.volume = float(params["v"])
        vc.param.speed = float(params["s"])
        vc.param.pitch = float(params["p"])
        vc.param.emphasis = float(params["e"])
        vc.param.pauseMiddle = int(params["pm"])
        vc.param.pauseLong = int(params["pl"])
        vc.param.pauseSentence = int(params["ps"])
        vc.param.masterVolume = float(params["mv"])

        text = unquote(params["t"])
        vp = int(params["vp"])

        # if vp = 1 then append vocalprefix from config
        if vp == 1:
            text = config["vocalprefix"] + text

        speech, _ = vc.textToSpeech(text)

        return speech

#################################
app = Flask(__name__)

@app.route('/')
def index():
    return 'vcr rest api.'

@app.route("/synth")
def synth():
    # create params variable and dump all from query_string
    params = {}
    for key, value in request.args.items():
        params[key] = value

    # validate apikey
    if config["lolikey"] and params["lolipass"] != config["lolikey"]:
        return "where is your loli pass?", 403

    # check if "t" and "vc" is in params, if not, throw an error
    if "t" not in params or "vc" not in params:
        return "wut..??", 400

    # default params
    if "l" not in params:
        params["l"] = "standard"
    if "v" not in params:
        params["v"] = 1.0
    if "s" not in params:
        params["s"] = 1.0
    if "p" not in params:
        params["p"] = 1.0
    if "e" not in params:
        params["e"] = 1.0
    if "pm" not in params:
        params["pm"] = 150
    if "pl" not in params:
        params["pl"] = 370
    if "ps" not in params:
        params["ps"] = 800
    if "mv" not in params:
        params["mv"] = 1.0
    if "vp" not in params:
        params["vp"] = 0
    
    # synthesize speech
    speech = synthesize(params)
    return Response(speech, mimetype="audio/wav")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=config["port"])