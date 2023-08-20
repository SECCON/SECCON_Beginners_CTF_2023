import os
import subprocess
import requests

APP_URL = os.environ['APP_URL']

def download():
    subprocess.run(["wget", f"{APP_URL}/public/videos/video0.ts"])
    subprocess.run(["wget", f"{APP_URL}/public/videos/video1.ts"])
    subprocess.run(["wget", f"{APP_URL}/public/videos/video2.ts"])

def make_key():
    key = [99, 9, 61, 110, 94, 114, 119, 194, 42, 163, 63, 8, 97, 114, 131, 41]
    with open("enc.key", "wb") as f:
        f.write(bytes(key))

def make_m3u8():
    m3u8 = """#EXTM3U
#EXT-X-VERSION:3
#EXT-X-TARGETDURATION:3
#EXT-X-MEDIA-SEQUENCE:0
#EXT-X-KEY:METHOD=AES-128,URI="file:///app/enc.key",IV=0x00000000000000000000000000000000
#EXTINF:3.040000,
file:///app/video0.ts
#EXTINF:3.040000,
file:///app/video1.ts
#EXTINF:2.280000,
file:///app/video2.ts
#EXT-X-ENDLIST
"""

    with open("video.m3u8", "w") as f:
        f.write(m3u8)

def combine():
    subprocess.run(["ffmpeg", "-allowed_extensions", "ALL", "-i", "./video.m3u8", "-c", "copy", "video.mp4", "-y"])

def upload():
    mimetype = "video/mp4"
    file = {'video': ('file', open('./video.mp4', 'rb'), mimetype)}
    res = requests.post(f"{APP_URL}/flag", files=file).text
    print(res)

def clean():
    rm_list = ["video0.ts", "video1.ts", "video2.ts", "enc.key", "video.m3u8", "video.mp4"]
    for f in rm_list:
        if os.path.exists(f):
            os.remove(f)

if __name__ == "__main__":
    clean()
    download()
    make_key()
    make_m3u8()
    combine()
    upload()