# CTFFUCK
This programming language is designed for CTF.
See how hard it will be to decode!

## CONSTANTS
- prepare box id: `ABCD`

## Functions
`structure: func argument`
### notice that, the following "given box" means, use the argument as id to get a box
|  address   |    usage     |
|:-----------|:------------:|
|EACD|exchange the given box and the prepare box's value|
|AACB|write the prepare box's value to the given box|
|AEAD|print the prepare box's value as prompt and getchar to the given box|
|AABD|random a number between 0xFFFF to zero and put it in the given box|
|0ADD|add the number between given box and the prepare box, assign the result to the given box|