from typing import Any, Callable
import random
import getch  # type: ignore
import sys
import re

memory: list[Any] = [None]*0xFFFF
memory[0xABCD]=random.randint(0,0xFFFF)
memory[0xAB]=sys.stdout
IMPORTANT: dict[str,int]={
    "prepare regex":0xABCD,
    "stdout":0xAB
}

class stack:
    def __init__(self,sta:list[Any]):
        self.sta=sta
        self.ptr=0
    def push(self,val: Any) -> None:
        self.sta[self.ptr]=val
        self.ptr+=1
    def pop(self) -> Any:
        self.ptr-=1
        return self.sta[self.ptr]
def getchar(prompt: str=""):
    print(prompt, end="", flush=True)
    try:
        import msvcrt
        ch = msvcrt.getche()
        if isinstance(ch, bytes):
            ch = ch.decode()
        print()
        return ch
    except ImportError:
        ch = getch.getch()
        if isinstance(ch, bytes):
            ch = ch.decode()
        print(ch, end="", flush=True)
        print()
        return ch
def split(s: str,l: int)-> list[str]:
    return list(s[i:i+l] for i in range(0,len(s),l))

def exchange(arg: int) -> None:
    global memory
    memory[arg],memory[memory[0xABCD]]=memory[memory[0xABCD]],memory[arg]
def write(arg: int) -> None:
    global memory
    memory[arg]=memory[0xABCD]
def read(arg: int) -> None:
    global memory
    memory[arg]=getchar()
def rand(arg: int) -> None:
    global memory
    memory[arg]=random.randint(0,0xFFFF)
def add(arg: int) -> None:
    global memory
    memory[arg]=(memory[arg]+memory[memory[0xABCD]])&0xFFFF
def sub(arg: int) -> None:
    global memory
    memory[arg]=(memory[arg]-memory[memory[0xABCD]])&0xFFFF
def xor(arg: int) -> None:
    global memory
    memory[arg]=(memory[arg]^memory[memory[0xABCD]])&0xFFFF
def prepare(arg: int) -> None:
    global memory
    memory[0xABCD]=arg
def reset(arg: int):
    global memory
    memory[arg]=None
def debug(arg: int)-> None:
    global memory
    print("\n".join(f"{i:04X}: {repr(v)}" for i,v in enumerate(memory) if v is not None),file=memory[0xAB])
def chra(arg: int)-> None:
    global memory
    memory[arg]=chr(memory[0xABCD]&0xFFFF)
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

for i,func in funcs.items():
    memory[i]=func
# STACK: stack=stack(memory)
if __name__=="__main__":
    if len(sys.argv)<2:
        print("Usage: ctfuck [script]")
        sys.exit(1)
    with open(sys.argv[1],"r") as f:
        script=re.sub(r"[^0-9A-Fa-f]", "", f.read())
    if len(script)%4!=0:
        print("Script length must be multiple of 4",file=sys.stderr)
        sys.exit(1)
    scriptt: list[int]=[int(i,base=16)for i in split(script,4)]
    DEBUG: bool="-d" in sys.argv or "--debug" in sys.argv
    i: int=0
    while i<len(scriptt):
        command: int=scriptt[i]
        try:
            if callable(memory[command]):
                memory[command](scriptt[i+1])
                i+=1
            else:
                if DEBUG:
                    print(str(command)+": ",end="")
                print(memory[command],file=memory[0xAB],end="")
        except ValueError:
            print(f"Invalid instruction: {i}",file=sys.stderr)
            sys.exit(1)
        i+=1