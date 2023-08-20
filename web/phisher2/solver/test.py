import json
import requests

ENDPOINT = "http://192.168.11.9:16161"

tests = [
    {
        "text": "https://phisher2.beginners.seccon.games/",
        "expect": "admin: Very good web site. Thanks for sharing!"
    },
    {
        "text": "http://example.com",
        "expect": "admin: It's not url or safe url."
    },
    {
        "text": "‮http://ryuse.dev/semag.nocces.srennigeb.2rehsihp//:sptth",
        "expect": "admin: Very good web site. Thanks for sharing!"
    },
    {
        "text": "<!--http://ryuse.dev-->https://phisher2.beginners.seccon.games/",
        "expect": "admin: Very good web site. Thanks for sharing!"
    },
    {
        "text": '<input type="hidden" value="http://ryuse.dev" />https://phisher2.beginners.seccon.games/',
        "expect": "admin: Very good web site. Thanks for sharing!"
    },
    {
        "text": "һττр://ɴɡіɴх/",
        "expect": "admin: It's not url or safe url."
    }
]

for test in tests:
    res = requests.post(f"{ENDPOINT}", json={"text": test["text"]}).text
    message = json.loads(res)["message"]
    assert message == test["expect"], f"NG: {test['text']} -> {message}"
    print(f"OK: {test['text']} -> {message}")