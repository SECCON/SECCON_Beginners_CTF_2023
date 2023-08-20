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
