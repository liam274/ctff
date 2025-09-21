from typing import Any, Callable, Iterator
import random
import getch  # type: ignore
import sys
import re

MAJOR: int=0
MEDIUM: int=3
MINOR: int=1
VERSION: str=f"{MAJOR}.{MEDIUM}.{MINOR}"
IMPORTANT: dict[str,int]={
    "prepare regex":0xABCD,
    "stdout":0xAB
}

PREPARE_ADDR: int=0xABCD
OUTPUT_ADDR: int=0xAB
MEM_SIZE: int=0xFFFF
memory: list[Any] = [None]*MEM_SIZE
memory[PREPARE_ADDR]=random.randint(0,MEM_SIZE)
memory[OUTPUT_ADDR]=sys.stdout
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
    output: list[str] = []
    for i, v in enumerate(memory):
        if v is not None:
            output.append(f"{i:04X}: {v!r}")
    print("\n".join(output), file=memory[OUTPUT_ADDR])
def chra(arg: int)-> None:
    global memory
    memory[arg]=chr(memory[PREPARE_ADDR]&MEM_SIZE)
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
    0xC0DE:chra
}

for addr,func in funcs.items():
    memory[addr]=func

if __name__=="__main__":
    print("This is ctffuck version",VERSION,"environment.")
    if len(sys.argv)<2:
        print("Usage: ctfuck [script]")
        sys.exit(1)
    with open(sys.argv[1],"r") as f:
        script=non_hex_pattern.sub("", f.read())
    if len(script)%4!=0:
        print("Script length must be multiple of 4",file=sys.stderr)
        sys.exit(1)
    scriptt: list[int]=[int(i,base=16)for i in split(script,4)]
    DEBUG: bool="-d" in sys.argv or "--debug" in sys.argv
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
            if DEBUG:
                print(f"{command:04X}: ",end="")
            print(memory[command],file=memory[OUTPUT_ADDR],end="")
        i+=1