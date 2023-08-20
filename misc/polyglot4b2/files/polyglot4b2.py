import os
import re
import sys
import uuid
import shutil
import subprocess

print(
    f"""\033[31m\
 ____       _             _       _     _____    _ _ _               ____
|  _ \ ___ | |_   _  __ _| | ___ | |_  | ____|__| (_) |_ ___  _ __  |___ \\
| |_) / _ \| | | | |/ _` | |/ _ \| __| |  _| / _` | | __/ _ \| '__|   __) |
|  __/ (_) | | |_| | (_| | | (_) | |_  | |__| (_| | | || (_) | |     / __/
|_|   \___/|_|\__, |\__, |_|\___/ \__| |_____\__,_|_|\__\___/|_|    |_____|
              |___/ |___/
{"-" * 76}
>> """,
    end="",
)

file = ""
for _ in range(10):
    text = sys.stdin.buffer.readline().decode()
    if not re.fullmatch("[A-Z]+", text.replace("\n", "")):
        print("ERROR: Hi, Hacker.")
        sys.exit(0)
    if "QUIT" in text:
        break
    file += text

print(f"{'-' * 76}\033[0m")

if len(file) >= 5000:
    print("ERROR: File size too large. (len < 5000)")
    sys.exit(0)

f_id = uuid.uuid4()
os.makedirs(f"tmp/{f_id}", exist_ok=True)
with open(f"tmp/{f_id}/{f_id}", mode="w") as f:
    f.write(file)
try:
    f_type = subprocess.run(
        ["file", "-bkr", f"tmp/{f_id}/{f_id}"], capture_output=True
    ).stdout.decode()
except:
    print("ERROR: Failed to execute command.")
finally:
    shutil.rmtree(f"tmp/{f_id}")

# You are a beginner!!!!
_4bflag = True
if "4b" not in f_type:
    print("ERROR: You are not a beginner.")
    _4bflag = False

types = {
    "JPG": False,
    "PNG": False,
    "GIF": False,
    "PDF": False,
    "ELF": False,
    "TXT": False,
}
f_type = f_type.split("\n")
try:
    if "JPEG" in f_type[0]:
        types["JPG"] = True
    if "PNG" in f_type[1]:
        types["PNG"] = True
    if "GIF" in f_type[2]:
        types["GIF"] = True
    if "PDF" in f_type[3]:
        types["PDF"] = True
    if "ELF" in f_type[4]:
        types["ELF"] = True
    if "ASCII" in f_type[5]:
        types["TXT"] = True
except:
    pass

for k, v in types.items():
    v = "🟩" if v else "🟥"
    print(f"| {k}: {v} ", end="")
print("|")

if _4bflag and all(types.values()):
    print("FLAG: ctf4b{****REDACTED****}")
else:
    print("FLAG: No! File koime!!")
