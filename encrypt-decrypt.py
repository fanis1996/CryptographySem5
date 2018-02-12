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
    if args.encrypt:
        if args.cipher == 'AES':
            cipher = AES.new(Padding.pad(args.key.encode(),32),AES.MODE_CBC)
            cryptedtext=cipher.iv+cipher.encrypt(Padding.pad(args.infile.read(),32))
            args.outfile.write(cryptedtext)
        elif args.cipher == 'DES':
            cipher = DES.new(Padding.pad(args.key.encode(),8),DES.MODE_CBC)
            cryptedtext=cipher.iv+cipher.encrypt(Padding.pad(args.infile.read(),8))
            args.outfile.write(cryptedtext)
        elif args.cipher == 'CAST':
            cipher = CAST.new(Padding.pad(args.key.encode(),16),CAST.MODE_CBC)
            cryptedtext=cipher.iv+cipher.encrypt(Padding.pad(args.infile.read(),8))
            args.outfile.write(cryptedtext)
        elif args.cipher == 'Blowfish':
            cipher = Blowfish.new(args.key.encode(),CAST.MODE_CBC)
            cryptedtext=cipher.iv+cipher.encrypt(Padding.pad(args.infile.read(),8))
            args.outfile.write(cryptedtext)
            
    else:
        if args.cipher == 'AES':
            iv=args.infile.read(16)
            cipher = AES.new(Padding.pad(args.key.encode(),32),AES.MODE_CBC,iv)
            text=cipher.decrypt(args.infile.read())
            args.outfile.write(Padding.unpad(text,32))
        elif args.cipher == 'DES':
            iv=args.infile.read(8)
            cipher = DES.new(Padding.pad(args.key.encode(),8),AES.MODE_CBC,iv)
            text=cipher.decrypt(args.infile.read())
            args.outfile.write(Padding.unpad(text,8))
        elif args.cipher == 'CAST':
            iv=args.infile.read(8)
            cipher = CAST.new(Padding.pad(args.key.encode(),16),AES.MODE_CBC,iv)
            text=cipher.decrypt(args.infile.read())
            args.outfile.write(Padding.unpad(text,8))
        elif args.cipher == 'Blowfish':
            iv=args.infile.read(8)
            cipher = Blowfish.new(args.key.encode(),CAST.MODE_CBC,iv)
            text=cipher.decrypt(args.infile.read())
            args.outfile.write(Padding.unpad(text,8))
