from Crypto.Cipher import AES
from Crypto.Util import Padding
from Crypto.Cipher import DES
from Crypto.Cipher import Blowfish
from Crypto.Cipher import CAST
import argparse
import sys
import io

def parse_args(argv):
    parser=argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--encrypt',action='store_true')
    group.add_argument('--decrypt',action='store_true')
    parser.add_argument('-cipher',choices='AES DES CAST Blowfish'.split(),required=True)
    parser.add_argument('-key',required=True)
    parser.add_argument('infile',type=argparse.FileType('rb'))
    parser.add_argument('outfile',type=argparse.FileType('wb'),default='out.txt')
    return parser.parse_args(argv)

if __name__ == "__main__":
    args = parse_args(sys.argv[1:])

    ciopts = {
              "AES":{"cipher": AES,
                     "key":    Padding.pad(args.key.encode(), 32),
                     "mode":   AES.MODE_CBC,
                     "pad":    32,
                     "iv" :    16},
              "DES":{"cipher": DES,
                     "key":    Padding.pad(args.key.encode(), 8),
                     "mode":   DES.MODE_CBC,
                     "pad":    8,
                     "iv" :    8},
             "CAST":{"cipher": CAST,
                     "key":    Padding.pad(args.key.encode(), 16),
                     "mode":   CAST.MODE_CBC,
                     "pad":    8,
                     "iv" :    8},
        "Blowfish": {"cipher": Blowfish,
                     "key":    args.key.encode(),
                     "mode":   CAST.MODE_CBC,
                     "pad":    8,
                     "iv" :    8},
        }

    c = ciopts[args.cipher]
    iv = None if args.encrypt else args.infile.read(c['iv'])
    cipher = c["cipher"].new(c["key"], c["mode"], iv)

    if args.encrypt:
        cryptedtext=cipher.iv+cipher.encrypt(Padding.pad(args.infile.read(), c["pad"]))
        args.outfile.write(cryptedtext)
    else:
        text=cipher.decrypt(args.infile.read())
        args.outfile.write(Padding.unpad(text, c["pad"]))
