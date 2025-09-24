# CTFF
This programming language is designed for CTF.
See how hard it will be to decode!

## CONSTANTS
- prepare box id: `ABCD`
- output box id: `AB`
- condition box id: `AAA0`

## Functions
`structure: func argument`
### Notice that, the following "given box" means, use the argument as id to get a box
|  address   |    usage     |
|:-----------:|:------------:|
|`EACD`|exchange the given box and the prepare box's value|
|`AACB`|boxs[prepare box]=given box|
|`AEAD`|print the prepare box's value as prompt and getchar to the given box|
|`AABD`|random a number between 0xFFFF to zero and put it in the given box|
|`0ADD`|add the number between given box and the prepare box, assign the result to the given box|
|`05AB`|given box=given box - prepare box|
|`0B01`|given box=given box xor prepare box|
|`AEAE`|reset a box's value to `None`(or `null`, as you like)|
|`0BEE`|prepare box=argument|
|`DEAD`|output every non-None(non-null) value to the output box|
|`C0DE`|given box=chr(prepare box)|
|`BEEF`|print the given box to output box|
|`ADD5`|boxs[given box value]+=chr(prepare box value or 0)|
|`AD15`|boxs[given box value]+=str(prepare boc value or 0)|
|`1BEF`|print the given argument as char rawly|
|`A0A5`|pop the last char of a box, and put it in the prepare box|
|`05A5`|move the ptr and set the ptr pointed box to None|
|`00F0`|open file name in prepare box and put it to boxs[given box value]|
|`0BFF`|prepare box=ord(given box)|
|`0BAA`|condition box=given box > boxs[prepare box]|
|`0EAA`|condition box=given box == boxs[prepare box]|
|`05AA`|condition box=given box < boxs[prepare box]|
|`0BEA`|condition box=given box >= boxs[prepare box]|
|`05EA`|condition box=given box <= boxs[prepare box]|
|`00AA`|condition box=not condition box|
|`BBBB`|jmp if condition box is True|
|`C0D3`|given box=boxs[prepare box]|

## Skills
You can exchange build-in functions and any boxes to rename them:
```ctff
0BEE AACB
EACD 0100
```
Then you can use `0100` to access the write function!

## Attention!
- If the program is running too long time, don't panic. It's just the script being WAY too long. Any Infinity loop will be inturpeted.

## Copyright
**You need to state the source before you use our project in any way**

# 一些對比

歡迎來到CTFF的世界~
本電腦語言為解釋型語言，相對於傳統語言有優點如下：
|CTFF|傳統機械碼|
|:-----------:|:------------:|
|✔️效能比傳統機械碼慢數百倍或以上|❌效能過高，讓人們忘記要改進電腦芯片|
|✔️有許多BUG，讓程序員更注重語法|❌沒有BUG，讓程序員很容易就寫好一條程序|
|✔️讓你體驗到傳統機械碼，同時又更flexible和更複雜|❌比CTFF更加簡單，太容易讓人看懂|
|✔️可以亂加字符，超容錯|❌不可以亂加字符，會爆錯|