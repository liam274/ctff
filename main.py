from typing import Any, Callable, Iterator, Union
import random
import getch # type: ignore
import sys
import re
import traceback

MAJOR: int=0
MEDIUM: int=5
MINOR: int=0
VERSION: str=f"{MAJOR}.{MEDIUM}.{MINOR}"
IMPORTANT: dict[str,int]={
    "prepare regex":0xABCD,
    "stdout":0xAB
}

PREPARE_ADDR: int=0xABCD
OUTPUT_ADDR: int=0xAB
MEM_SIZE: int=0xFFFF
PTR_ADDR: int=0xAAAA
CONDITION_ADDR: int=0xAAA0
memory: list[Any] = [None]*MEM_SIZE
memory[PREPARE_ADDR]=random.randint(0,MEM_SIZE)
memory[OUTPUT_ADDR]=sys.stdout
memory[PTR_ADDR]=0
non_hex_pattern=re.compile(r"[^0-9A-Fa-f;]")
i: int=0

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

def exchange(arg: int) -> Union[None,int]:
    global memory
    memory[arg],memory[memory[PREPARE_ADDR]]=memory[memory[PREPARE_ADDR]],memory[arg]
def write(arg: int) -> Union[None,int]:
    global memory
    memory[memory[PREPARE_ADDR]]=arg
def read(arg: int) -> Union[None,int]:
    global memory
    if memory[PREPARE_ADDR] is None:
        print("Invaild prepare box value",file=sys.stderr,end="")
        return 1
    memory[arg]=getchar(chr(memory[PREPARE_ADDR]))
def rand(arg: int) -> Union[None,int]:
    global memory
    memory[arg]=random.randint(0,MEM_SIZE)
def add(arg: int) -> Union[None,int]:
    global memory
    memory[arg]=(memory[arg]+memory[memory[PREPARE_ADDR]])&MEM_SIZE
def sub(arg: int) -> Union[None,int]:
    global memory
    memory[arg]=(memory[arg]-memory[memory[PREPARE_ADDR]])&MEM_SIZE
def xor(arg: int) -> Union[None,int]:
    global memory
    memory[arg]=(memory[arg]^memory[memory[PREPARE_ADDR]])&MEM_SIZE
def prepare(arg: int) -> Union[None,int]:
    global memory
    memory[PREPARE_ADDR]=arg
def reset(arg: int):
    global memory
    memory[arg]=None
def debug(arg: int) -> Union[None,int]:
    print(memory,file=memory[OUTPUT_ADDR])
def chra(arg: int)-> Union[None,int]:
    global memory
    if memory[PREPARE_ADDR] is None:
        print("Invaild prepare box value",file=sys.stderr,end="")
        return 1
    memory[arg]=chr(memory[PREPARE_ADDR])
def print_mem(arg: int) -> Union[None,int]:
    global memory
    print(memory[arg],file=memory[OUTPUT_ADDR],end="")
def adds(arg: int) -> Union[None,int]:
    global memory
    if memory[PREPARE_ADDR] is None:
        print("Invaild prepare box value, not inited",file=sys.stderr,end="")
        return 1
    memory[arg]=(memory[arg] or "")+chr(memory[PREPARE_ADDR])
def addint(arg: int) -> Union[None,int]:
    global memory
    if memory[PREPARE_ADDR] is None:
        print("Invaild prepare box value, not inited",file=sys.stderr,end="")
        return 1
    memory[arg]=(memory[arg] or "")+str(memory[PREPARE_ADDR])
def print_raw(arg: int) -> Union[None,int]:
    global memory
    print(chr(arg),end="",file=memory[OUTPUT_ADDR])
def pops(arg: int)-> Union[None,int]:
    global memory
    if memory[arg] is None or len(memory[arg])==0:
        return 1
    memory[PREPARE_ADDR]=ord(memory[arg][-1])
    memory[arg]=memory[arg][:-1]
def pop(arg: int)-> Union[None,int]:
    global memory
    memory[PTR_ADDR]=(memory[PTR_ADDR]-arg if memory[PTR_ADDR]>=arg else 0)
    memory[memory[PTR_ADDR]]=None
def open_file(arg: int)-> Union[None,int]:
    global memory
    try:
        memory[memory[arg]]=open(memory[PREPARE_ADDR],"a+")
    except:
        print(traceback.format_exc(),file=sys.stderr,end="")
def char_prepare(arg: int) -> Union[None,int]:
    global memory
    if memory[arg] is None:
        print("Invaild sting given",file=sys.stderr,end="")
        return 1
    memory[PREPARE_ADDR]=ord(memory[arg])
def b(arg: int)-> Union[None,int]:
    global memory
    if memory[memory[PREPARE_ADDR]] is None:
        print("Invaild box value",file=sys.stderr,end="")
        return 1
    memory[CONDITION_ADDR]=(memory[arg]>memory[memory[PREPARE_ADDR]])
def s(arg: int)-> Union[None,int]:
    global memory
    if memory[memory[PREPARE_ADDR]] is None:
        print("Invaild box value",file=sys.stderr,end="")
        return 1
    memory[CONDITION_ADDR]=(memory[arg]<memory[memory[PREPARE_ADDR]])
def e(arg: int)-> Union[None,int]:
    global memory
    if memory[memory[PREPARE_ADDR]] is None:
        print("Invaild box value",file=sys.stderr,end="")
        return 1
    memory[CONDITION_ADDR]=(memory[arg]==memory[memory[PREPARE_ADDR]])
def be(arg: int)-> Union[None,int]:
    global memory
    if memory[memory[PREPARE_ADDR]] is None:
        print("Invaild box value",file=sys.stderr,end="")
        return 1
    memory[CONDITION_ADDR]=(memory[arg]>=memory[memory[PREPARE_ADDR]])
def se(arg: int)-> Union[None,int]:
    global memory
    if memory[memory[PREPARE_ADDR]] is None:
        print("Invaild box value",file=sys.stderr,end="")
        return 1
    memory[CONDITION_ADDR]=(memory[arg]<=memory[memory[PREPARE_ADDR]])
def _not(arg:int)->Union[None,int]:
    global memory
    if memory[memory[PREPARE_ADDR]] is None:
        print("Invaild box value",file=sys.stderr,end="")
        return 1
    memory[CONDITION_ADDR]=not memory[CONDITION_ADDR]
def jmp(arg: int)->None:
    global memory,i
    if memory[CONDITION_ADDR]:
        i=arg
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
    0xF0:open_file,
    0xBFF:char_prepare,
    0xBAA:b,
    0x5AA:s,
    0xEAA:e,
    0xBEA:be,
    0x5EA:se,
    0x0AA:_not,
    0xBBBB:jmp
}

for addr,func in funcs.items():
    memory[addr]=func

if __name__!="__main__":
    sys.exit(0)
print("This is ctff version",VERSION,"environment.")
if len(sys.argv)<2:
    print("Usage: ctff scriptFile [commands...]")
    sys.exit(1)
if "-c" in sys.argv or "--command" in sys.argv:
    for key,func in funcs.items():
        print(f"{key:04X}: {func.__name__}")
    sys.exit(0)
with open(sys.argv[1],"r") as f:
    script=non_hex_pattern.sub("", f.read())
tmp: str=""
skip: bool=False
for n in script:
    if n==";":
        skip=not skip
        continue
    if skip:
        continue
    tmp+=n
script=tmp
del tmp
if len(script)%4!=0:
    print("Script length must be multiple of 4",file=sys.stderr)
    sys.exit(1)
scriptt: list[int]=[int(i,base=16)for i in split(script,4)]
script_length: int=len(scriptt)
while i<script_length:
    command: int=scriptt[i]
    result: int
    if callable(memory[command]):
        if i+1>=script_length:
            print("Missing argument for instruction at the last chunk.",file=sys.stderr)
            sys.exit(1)
        result=memory[command](scriptt[i+1])
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
        result=memory[command](scriptt[i+1])
        i+=1
    if result==1:
        print(" at chunk",hex(i)[2:],file=sys.stderr)
        sys.exit(1)
    i+=1
del memory