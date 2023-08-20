import uuid
import openai
import urllib.parse
from flask import Flask, request, abort
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

##################################################
# OpenAI API key
KEY = "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"
##################################################

app = Flask(__name__)
app.config["RATELIMIT_HEADERS_ENABLED"] = True

limiter = Limiter(get_remote_address, app=app, default_limits=["3 per minute"])

openai.api_key = KEY

top_page = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="utf-8" />
    <title>亞空文庫</title>
</head>

<body>
    <h1>亞空文庫</h1>
    AIにセキュリティの物語を書いてもらいました。<br>
    内容は正しいかどうかわかりません。<br>
<ul>
    <li><a href="/?file=book0.txt">あ書</a></li>
    <li><a href="/?file=book1.txt">い書</a></li>
    <li><a href="/?file=book2.txt">う書</a></li>
    <!-- <li><a href="/?file=book3.txt">え書</a></li> -->
</ul>

※セキュリティのためAI-WAFを導入しています。<br>
© 2023 ももんがの書房
</body>

</html>
"""


@app.route("/")
def top():
    file = request.args.get("file")
    if not file:
        return top_page
    if file in ["book0.txt", "book1.txt", "book2.txt"]:
        with open(f"./books/{file}", encoding="utf-8") as f:
            return f.read()
    # AI-WAF
    puuid = uuid.uuid4()
    prompt = f"""\
以下の{puuid}に囲まれた部分のURLクエリはパストラバーサル攻撃でしょうか？
そうである場合Yesを、違う場合Noを返してください。
../やflagという文字列が含まれていた場合もYesを返してください。

{puuid}
{urllib.parse.unquote(request.query_string)[:50]}
{puuid}
"""
    # print(prompt)  # Debug
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )
        result = response.choices[0]["message"]["content"].strip()
    except:
        return abort(500, "OpenAI APIのエラーです。\n少し時間をおいてアクセスしてください。")
    # print(result)  # Debug
    if "No" in result:
        with open(f"./books/{file}", encoding="utf-8") as f:
            return f.read().replace(KEY, "")
    return abort(403, "AI-WAFに検知されました👻")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=31415)
