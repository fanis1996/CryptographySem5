#!/bin/python
import argparse
import sys
import copy as _copy
from subprocess import call

def main(argv):
    args, phelp = parse_arguments(argv)
    #print(args, file=sys.stderr)
    if args.__contains__('func'):
        args.func(args)
    else:
        phelp()

def crypt(args):
    '''Encrypt or Decrypt using openssl'''
    openssl_cmd= [
            'openssl',
            'enc',
            '-' + args.alg,
            '-d' if args.d else '-e',
            '-nosalt',
            '-pass', 'pass:' + args.key
          ]
    if args.in_file is not None:
                openssl_cmd += ['-in', args.in_file]
    if args.out_file is not None:
        openssl_cmd += ['-out', args.out_file]
    call(openssl_cmd)

def bit_flip(args):
    inp = bytearray(args.in_file.read())
    if not args.flip_bits is None:
        for B in args.flip_bits:
            inp[B['byte_pos']] ^= B['x']
    args.out_file.write(bytes(inp))

def parse_arguments(args):
    parser = argparse.ArgumentParser(description='Bit-Flipping attack')
    subparsers = parser.add_subparsers()

    parser_enc = subparsers.add_parser('encrypt', aliases=['enc', 'e'], help='Encrypt or Decrypt')
    parser_enc.set_defaults(func=crypt)
    parser_enc.add_argument('-alg', default='aes-256-cbc', choices=['aes-256-cbc', 'des-cbc', 'idea-cbc', 'bf-cbc'])
    parser_enc.add_argument('-in', '--in-file', nargs='?')
    parser_enc.add_argument('-out', '--out-file', nargs='?')
    parser_enc.add_argument('-k', '--key', required=True)
    parser_enc.add_argument('-d', help='Decrypt', action='store_true')

    parser_bf = subparsers.add_parser('bitflip', aliases=['bitf', 'b'], help='Bit-Flipping attack')
    parser_bf.set_defaults(func=bit_flip)
    parser_bf.add_argument('--in-file', nargs='?', type=argparse.FileType('r+b'), default=sys.stdin.buffer)
    parser_bf.add_argument('--out-file', nargs='?', type=argparse.FileType('w+b'), default=sys.stdout.buffer)
    parser_bf.add_argument('-B', '--flip-bits', action=BitFlipAction, help="Flip bits of byte at BYTE_POS", metavar=('BYTE_POS', '\bBitPos1 [BitPos2'))

    return parser.parse_args(args), parser.print_help

def _ensure_value(namespace, name, value):
    if getattr(namespace, name, None) is None:
        setattr(namespace, name, value)
    return getattr(namespace, name)

class BitFlipAction(argparse.Action):
    def __init__(self, option_strings, dest, nargs='+', **kwargs):
        super(BitFlipAction, self).__init__(option_strings, dest, nargs=nargs, **kwargs)
    def __call__(self, parser, namespace, values, option_string=None):
        if not 2<=len(values)<=9:
            msg='argument "{f}": "{v}" requires between 2 and 9 arguments'.format(f=self.dest, v=option_string + ' '+ str(' '.join(values)))
            raise argparse.ArgumentTypeError(msg)
        try:
            V = []
            byte_pos = int(values[0], 0)
            for v in values[1:]:
                n = int(v, 0)
                if not 0<=n<=7:
                    msg='argument "{f}": BitPosition "{n}" in "{v}" must be between 0 and 7'.format(f=self.dest, n=n, v=option_string + ' '+ str(' '.join(values)))
                    raise argparse.ArgumentTypeError(msg)
                V.append(int(v, 0))
        except ValueError:
            msg='argument "{f}": option "{n}" in "{v}" is not a number'.format(f=self.dest, n=v, v=option_string + ' '+ str(' '.join(values)))
            raise argparse.ArgumentTypeError(msg)
        if len(V) != len(set(V)):
            msg='argument "{f}": "{v}" bit flip positions must be unique'.format(f=self.dest, v=option_string + ' '+ str(' '.join(values)))
            raise argparse.ArgumentTypeError(msg)
        items = _copy.copy(_ensure_value(namespace, self.dest, []))
        items.append({'byte_pos':byte_pos, 'x':sum([1<<i for i in V])})
        setattr(namespace, self.dest, items)

if __name__ == "__main__":
    main(sys.argv[1:])
