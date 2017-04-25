#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Encrypt/decrypt files with symmetric AES cipher-block chaining (CBC) mode.

Usage:

File Encryption:

    aescrypt.py [-f] infile [outfile]

File decryption:

    aescrypt.py -d [-f] infile [outfile]

This script is derived from an answer to this StackOverflow question:

http://stackoverflow.com/questions/16761458/

I changed the key derivation function to use PBKDF2.

"""

from __future__ import print_function, unicode_literals

__all__ = ('encrypt', 'decrypt')

import argparse
import os
import struct
import sys

from getpass import getpass
from os.path import exists, splitext

from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from pbkdf2 import PBKDF2


SALT_MARKER = b'$'
ITERATIONS = 1000


def encrypt(infile, outfile, password, key_size=32, salt_marker=SALT_MARKER,
            kdf_iterations=ITERATIONS, hashmod=SHA256):
    """Encrypt infile and write it to outfile using password to generate key.

    The encryption algorithm used is symmetric AES in cipher-block chaining
    (CBC) mode.

    ``key_size`` may be 16, 24 or 32 (default).

    The key is derived via the PBKDF2 key derivation function (KDF) from the
    password and a random salt of 16 bytes (the AES block size) minus the
    length of the salt header (see below).

    The hash function used by PBKDF2 is SHA256 per default. You can pass a
    different hash function module via the ``hashmod`` argument. The module
    must adhere to the Python API for Cryptographic Hash Functions (PEP 247).

    PBKDF2 uses a number of iterations of the hash function to derive the key,
    which can be set via the ``kdf_iterations` keyword argumeent. The default
    number is 1000 and the maximum 65535.

    The header and the salt are written to the first block of the encrypted
    file. The header consist of the number of KDF iterations encoded as a
    big-endian word bytes wrapped by ``salt_marker`` on both sides. With the
    default value of ``salt_marker = b'$'``, the header size is thus 4 and the
    salt 12 bytes. The salt marker must be a byte string of 1-6 bytes length.

    The last block of the encrypted file is padded with up to 16 bytes, all
    having the value of the length of the padding.

    """
    if not 1 <= len(salt_marker) <= 6:
        raise ValueError('The salt_marker must be one to six bytes long.')
    elif not isinstance(salt_marker, bytes):
        raise TypeError('salt_marker must be a bytes instance.')

    if kdf_iterations >= 65536:
        raise ValueError('kdf_iterations must be <= 65535.')

    bs = AES.block_size
    header = salt_marker + struct.pack('>H', kdf_iterations) + salt_marker
    salt = os.urandom(bs - len(header))
    kdf = PBKDF2(password, salt, min(kdf_iterations, 65535), hashmod)
    key = kdf.read(key_size)
    iv = os.urandom(bs)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    outfile.write(header + salt)
    outfile.write(iv)
    finished = False

    while not finished:
        chunk = infile.read(1024 * bs)

        if len(chunk) == 0 or len(chunk) % bs != 0:
            padding_length = (bs - len(chunk) % bs) or bs
            chunk += (padding_length * chr(padding_length)).encode()
            finished = True

        outfile.write(cipher.encrypt(chunk))


def decrypt(infile, outfile, password, key_size=32, salt_marker=SALT_MARKER,
            hashmod=SHA256):
    """Decrypt infile and write it to outfile using password to derive key.

    See `encrypt` for documentation of the encryption algorithm and parameters.

    """
    mlen = len(salt_marker)
    hlen = mlen * 2 + 2

    if not 1 <= mlen <= 6:
        raise ValueError('The salt_marker must be one to six bytes long.')
    elif not isinstance(salt_marker, bytes):
        raise TypeError('salt_marker must be a bytes instance.')

    bs = AES.block_size
    salt = infile.read(bs)

    if salt[:mlen] == salt_marker and salt[mlen + 2:hlen] == salt_marker:
        kdf_iterations = struct.unpack('>H', salt[mlen:mlen + 2])[0]
        salt = salt[hlen:]
    else:
        kdf_iterations = ITERATIONS

    if kdf_iterations >= 65536:
        raise ValueError('kdf_iterations must be <= 65535.')

    iv = infile.read(bs)
    kdf = PBKDF2(password, salt, kdf_iterations, hashmod)
    key = kdf.read(key_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    next_chunk = b''
    finished = False

    while not finished:
        chunk, next_chunk = next_chunk, cipher.decrypt(infile.read(1024 * bs))

        if not next_chunk:
            padlen = chunk[-1]
            if isinstance(padlen, str):
                padlen = ord(padlen)
                padding = padlen * chr(padlen)
            else:
                padding = (padlen * chr(chunk[-1])).encode()

            if padlen < 1 or padlen > bs:
                raise ValueError("bad decrypt pad (%d)" % padlen)

            # all the pad-bytes must be the same
            if chunk[-padlen:] != padding:
                # this is similar to the bad decrypt:evp_enc.c
                # from openssl program
                raise ValueError("bad decrypt")

            chunk = chunk[:-padlen]
            finished = True

        outfile.write(chunk)


def main(args=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('-d', '--decrypt', action="store_true",
                    help="Decrypt input file")
    ap.add_argument('-f', '--force', action="store_true",
                    help="Overwrite output file if it exists")
    ap.add_argument('infile', help="Input file")
    ap.add_argument('outfile', nargs='?', help="Output file")

    args = ap.parse_args(args if args is not None else sys.argv[1:])

    if not args.outfile:
        if args.decrypt:
            args.outfile = splitext(args.infile)[0]
        else:
            args.outfile = args.infile + '.enc'

    if args.outfile == args.infile:
        print("Input and output file must not be the same.")
        return 1

    if exists(args.outfile) and not args.force:
        print("Output file '%s' exists. "
              "Use option -f to override." % args.outfile)
        return 1

    with open(args.infile, 'rb') as infile, \
            open(args.outfile, 'wb') as outfile:
        if args.decrypt:
            decrypt(infile, outfile, getpass("Enter decryption password: "))
        else:
            try:
                while True:
                    passwd = getpass("Enter encryption password: ")
                    passwd2 = getpass("Verify password: ")

                    if passwd != passwd2:
                        print("Password mismatch!")
                    else:
                        break
            except (EOFError, KeyboardInterrupt):
                return 1

            encrypt(infile, outfile, passwd)

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]) or 0)

# Copyright --> https://gist.github.com/SpotlightKid/53e1eb408267315de620
