import os
import sys
import uuid
import shutil
import subprocess

print(
    f"""\033[36m\
 ____       _             _       _     _____    _ _ _
|  _ \ ___ | |_   _  __ _| | ___ | |_  | ____|__| (_) |_ ___  _ __
| |_) / _ \| | | | |/ _` | |/ _ \| __| |  _| / _` | | __/ _ \| '__|
|  __/ (_) | | |_| | (_| | | (_) | |_  | |__| (_| | | || (_) | |
|_|   \___/|_|\__, |\__, |_|\___/ \__| |_____\__,_|_|\__\___/|_|
              |___/ |___/
{"-" * 68}
>> """,
    end="",
)

file = b""
for _ in range(10):
    text = sys.stdin.buffer.readline()
    if b"QUIT" in text:
        break
    file += text

print(f"{'-' * 68}\033[0m")

if len(file) >= 50000:
    print("ERROR: File size too large. (len < 50000)")
    sys.exit(0)

f_id = uuid.uuid4()
os.makedirs(f"tmp/{f_id}", exist_ok=True)
with open(f"tmp/{f_id}/{f_id}", mode="wb") as f:
    f.write(file)
try:
    f_type = subprocess.run(
        ["file", "-bkr", f"tmp/{f_id}/{f_id}"], capture_output=True
    ).stdout.decode()
except:
    print("ERROR: Failed to execute command.")
finally:
    shutil.rmtree(f"tmp/{f_id}")

types = {"JPG": False, "PNG": False, "GIF": False, "TXT": False}
if "JPEG" in f_type:
    types["JPG"] = True
if "PNG" in f_type:
    types["PNG"] = True
if "GIF" in f_type:
    types["GIF"] = True
if "ASCII" in f_type:
    types["TXT"] = True

for k, v in types.items():
    v = "🟩" if v else "🟥"
    print(f"| {k}: {v} ", end="")
print("|")

if all(types.values()):
    print("FLAG: ctf4b{****REDACTED****}")
else:
    print("FLAG: No! File mashimashi!!")
