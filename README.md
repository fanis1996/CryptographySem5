# CryptographySem5
## Crypto
### Help
```
usage: crypto.py [-h] {encrypt,enc,e,bitflip,bitf,b} ...

Bit-Flipping attack

positional arguments:
  {encrypt,enc,e,bitflip,bitf,b}
    encrypt (enc, e)    Encrypt or Decrypt
    bitflip (bitf, b)   Bit-Flipping attack

optional arguments:
  -h, --help            show this help message and exit
```

```
usage: crypto.py encrypt [-h] [-alg {aes-256-cbc,des-cbc,idea-cbc,bf-cbc}]
                         [-in [IN_FILE]] [-out [OUT_FILE]] -k KEY [-d]

optional arguments:
  -h, --help            show this help message and exit
  -alg {aes-256-cbc,des-cbc,idea-cbc,bf-cbc}
  -in [IN_FILE], --in-file [IN_FILE]
  -out [OUT_FILE], --out-file [OUT_FILE]
  -k KEY, --key KEY
  -d                    Decrypt
```

```
usage: crypto.py bitflip [-h] [--in-file [IN_FILE]] [--out-file [OUT_FILE]]
                         [-B BYTE_POS BitPos1 [BitPos2 ...]]
                         [-x BYTE_POS XOR_EXP]

optional arguments:
  -h, --help            show this help message and exit
  --in-file [IN_FILE]
  --out-file [OUT_FILE]
  -B BYTE_POS BitPos1 [BitPos2 ...], --flip-bits BYTE_POS BitPos1 [BitPos2 ...]
                        Flip bits of byte at BYTE_POS
  -x BYTE_POS XOR_EXP, --xor-byte BYTE_POS XOR_EXP
                        xor byte at BYTE_POS with value of XOR_EXP expression
```

## Hex Editor
```./hex-edit.py FILE-PATH```
### Key bindings
#### Normal Mode
* Move cursor : up/down/left/right (or h/j/k/l) 
* Edit Byte(bits): Enter (or i) 
* Save and exit: q 
#### Byte Edit Mode
* Move cursor: left/right (or h/l) 
* Flip bit: Space (or c or ~) 
* Store Byte: Enter (or q, i)
