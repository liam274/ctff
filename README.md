# CTFF
This programming language is designed for CTF.
See how hard it will be to decode!

## CONSTANTS
- prepare box id: `ABCD`
- output box id: `AB`

## Functions
`structure: func argument`
### Notice that, the following "given box" means, use the argument as id to get a box
|  address   |    usage     |
|:-----------|:------------:|
|EACD|exchange the given box and the prepare box's value|
|AACB|write the prepare box's value to the given box|
|AEAD|print the prepare box's value as prompt and getchar to the given box|
|AABD|random a number between 0xFFFF to zero and put it in the given box|
|0ADD|add the number between given box and the prepare box, assign the result to the given box|
|05AB|given box=given box - prepare box|
|0B01|given box=given box xor prepare box|
|AEAE|reset a box's value to `None`(or `null`, as you like)|
|0BEE|prepare box=argument|
|DEAD|output every non-None(non-null) value to the output box|
|C0DE|given box=chr(prepare box)|

## Skills
You can exchange build-in functions and any boxes to rename them:
```ctff
0BEE AACB
EACD 0100
```
Then you can use 0100 to access the write function!