from typing import Any, Callable, Iterator
import random
import getch # type: ignore
import sys
import re
import traceback

MAJOR: int=0
MEDIUM: int=4
MINOR: int=3
VERSION: str=f"{MAJOR}.{MEDIUM}.{MINOR}"
IMPORTANT: dict[str,int]={
    "prepare regex":0xABCD,
    "stdout":0xAB
}

PREPARE_ADDR: int=0xABCD
OUTPUT_ADDR: int=0xAB
MEM_SIZE: int=0xFFFF
PTR_ADDR: int=0xAAAA
memory: list[Any] = [None]*MEM_SIZE
memory[PREPARE_ADDR]=random.randint(0,MEM_SIZE)
memory[OUTPUT_ADDR]=sys.stdout
memory[PTR_ADDR]=0
non_hex_pattern = re.compile(r"[^0-9A-Fa-f]")

def getchar(prompt: str = "") -> str:
    print(prompt, end="", flush=True)
    try:
        import msvcrt
        ch = msvcrt.getch()
    except ImportError:
        ch = getch.getch()
    
    if isinstance(ch, bytes):
        ch = ch.decode()
    return ch # type: ignore
def split(s: str,l: int)-> Iterator[str]:
    return (s[i:i+l] for i in range(0,len(s),l))

def exchange(arg: int) -> None:
    global memory
    memory[arg],memory[memory[PREPARE_ADDR]]=memory[memory[PREPARE_ADDR]],memory[arg]
def write(arg: int) -> None:
    global memory
    memory[arg]=memory[PREPARE_ADDR]
def read(arg: int) -> None:
    global memory
    memory[arg]=getchar(chr(memory[PREPARE_ADDR] or 0))
def rand(arg: int) -> None:
    global memory
    memory[arg]=random.randint(0,MEM_SIZE)
def add(arg: int) -> None:
    global memory
    memory[arg]=(memory[arg]+memory[memory[PREPARE_ADDR]])&MEM_SIZE
def sub(arg: int) -> None:
    global memory
    memory[arg]=(memory[arg]-memory[memory[PREPARE_ADDR]])&MEM_SIZE
def xor(arg: int) -> None:
    global memory
    memory[arg]=(memory[arg]^memory[memory[PREPARE_ADDR]])&MEM_SIZE
def prepare(arg: int) -> None:
    global memory
    memory[PREPARE_ADDR]=arg
def reset(arg: int):
    global memory
    memory[arg]=None
def debug(arg: int) -> None:
    print(memory,file=memory[OUTPUT_ADDR])
def chra(arg: int)-> None:
    global memory
    memory[arg]=chr(memory[PREPARE_ADDR] or 0)
def print_mem(arg: int) -> None:
    global memory
    print(memory[arg],file=memory[OUTPUT_ADDR],end="")
def adds(arg: int) -> None:
    global memory
    memory[arg]=(memory[arg] or "")+chr(memory[PREPARE_ADDR] or 0)
def addint(arg: int) -> None:
    global memory
    memory[arg]=(memory[arg] or "")+str(memory[PREPARE_ADDR] or 0)
def print_raw(arg: int) -> None:
    global memory
    print(chr(arg),end="",file=memory[OUTPUT_ADDR])
def pops(arg: int)-> None:
    global memory
    if memory[arg] is None or len(memory[arg])==0:
        return
    memory[PREPARE_ADDR]=ord(memory[arg][-1])
    memory[arg]=memory[arg][:-1]
def pop(arg: int)-> None:
    global memory
    memory[PTR_ADDR]=(memory[PTR_ADDR]-arg if memory[PTR_ADDR]>=arg else 0)
    memory[memory[PTR_ADDR]]=None
def open_file(arg: int)-> None:
    global memory
    try:
        memory[memory[arg]]=open(memory[PREPARE_ADDR],"a+")
    except:
        print(traceback.format_exc(),file=sys.stderr)
def char_prepare(arg: int) -> None:
    global memory
    memory[PREPARE_ADDR]=ord(memory[PREPARE_ADDR] or "\x00")
funcs: dict[int,Callable[...,Any]]={
    0xEACD:exchange,
    0xAACB:write,
    0xAEAD:read,
    0xAABD:rand,
    0xADD:add,
    0x5AB:sub,
    0xB01:xor,
    0xAEAE:reset,
    0xBEE:prepare,
    0xDEAD:debug,
    0xC0DE:chra,
    0xBEEF:print_mem,
    0xADD5:adds,
    0xAD15:addint,
    0x1BEF:print_raw,
    0xA0A5:pops,
    0x5A5:pop,
    0xF0:open_file
}

for addr,func in funcs.items():
    memory[addr]=func

if __name__!="__main__":
    sys.exit(0)
print("This is ctff version",VERSION,"environment.")
if len(sys.argv)<2:
    print("Usage: ctff [script]")
    sys.exit(1)
with open(sys.argv[1],"r") as f:
    script=non_hex_pattern.sub("", f.read())
if len(script)%4!=0:
    print("Script length must be multiple of 4",file=sys.stderr)
    sys.exit(1)
scriptt: list[int]=[int(i,base=16)for i in split(script,4)]
i: int=0
script_length: int=len(scriptt)
while i<script_length:
    command: int=scriptt[i]
    if callable(memory[command]):
        if i+1>=script_length:
            print("Missing argument for instruction at the last chunk.",file=sys.stderr)
            sys.exit(1)
        memory[command](scriptt[i+1])
        i+=1
    else:
        if memory[command] is None:
            i+=1
            continue
        if not isinstance(memory[command],int) and not callable(memory[command]):
            print(f"Invalid command at chunk {i}: {memory[command]}",file=sys.stderr)
            sys.exit(1)
        time: int=0
        while not callable(memory[command]):
            command=memory[command]
            time+=1
            if time>MEM_SIZE:
                print("Possible infinite loop detected.",file=sys.stderr)
                sys.exit(1)
        if i+1>=script_length:
            print("Missing argument for instruction at the last chunk.",file=sys.stderr)
            sys.exit(1)
        memory[command](scriptt[i+1])
        i+=1
    i+=1
del memory