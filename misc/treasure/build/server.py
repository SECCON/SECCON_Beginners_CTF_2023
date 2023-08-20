import os
import random
import timeout_decorator

def open_as(path: str, fd: int):
  old_fd = os.open(path, os.O_RDONLY)
  os.dup2(old_fd, fd)
  os.close(old_fd)

@timeout_decorator.timeout(60)
def main():
    # ask the path to open
    path = input('path: ')
    if not path.startswith('/proc'):
      exit('[-] path not allowed')
    elif 'flag' in path or '.' in path:
      exit('[-] path not allowed')
    elif not os.path.exists(path):
      exit('[-] file not found')
    elif not os.path.isfile(path):
      exit('[-] not a file')

    # open 'flag' with a random fd
    fd = random.randint(16, pow(2, 16))
    open_as('flag', fd)

    # open path with `fd+1` and read
    open_as(path, fd + 1)
    print(os.read(fd + 1, 256))

    # read from an arbitraly fd
    try:
      fd = int(input('fd: '))
      print(os.read(fd, 256))
    except:
      exit('[-] failed to read')

if __name__ == '__main__':
    try:
        main()
    except timeout_decorator.timeout_decorator.TimeoutError:
        print("Timeout")
