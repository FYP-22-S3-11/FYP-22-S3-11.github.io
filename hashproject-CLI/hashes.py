#!/usr/bin/env python3

import io
import os
import re
import sys
import argparse
import requests
from collections import namedtuple

import requests

Prototype = namedtuple('Prototype', ['regex', 'modes'])
HashInfo = namedtuple('HashInfo', ['name'])

prototypes = [
    Prototype(
        regex=re.compile(r'^[a-f0-9]{4}$', re.IGNORECASE),
        modes=[
            HashInfo(name='CRC-16'), 
            HashInfo(name='CRC-16-CCITT'),
            HashInfo(name='FCS-16')]),
    
    Prototype(
        regex=re.compile(r'^[a-f0-9]{8}$', re.IGNORECASE),
        modes=[
            HashInfo(name='Adler-32'),
            HashInfo(name='CRC-32B'),
            HashInfo(name='FCS-32'),
            HashInfo(name='GHash-32-3'),
            HashInfo(name='GHash-32-5'),
            HashInfo(name='FNV-132'),
            HashInfo(name='Fletcher-32'),
            HashInfo(name='Joaat'),
            HashInfo(name='ELF-32'),
            HashInfo(name='XOR-32')]),

    Prototype(
        regex=re.compile(r'^[a-f0-9]{6}$', re.IGNORECASE),
        modes=[HashInfo(name='CRC-24')]),
    
    Prototype(
        regex=re.compile(r'^(\$crc32\$[a-f0-9]{8}.)?[a-f0-9]{8}$', re.IGNORECASE),
        modes=[
            HashInfo(name='CRC-32')]),
    Prototype(
        regex=re.compile(r'^[a-z0-9\/.]{13}$', re.IGNORECASE),
        modes=[
            HashInfo(name='DES(Unix)'),
            HashInfo(name='Traditional DES'),
            HashInfo(name='DEScrypt')]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{16}$', re.IGNORECASE),
        modes=[
            HashInfo(name='FNV-164'),
            HashInfo(name='CRC-64')]),
    Prototype(
        regex=re.compile(r'^_[a-z0-9\/.]{19}$', re.IGNORECASE),
        modes=[
            HashInfo(name='BSDi Crypt')]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{24}$', re.IGNORECASE),
        modes=[
            HashInfo(name='CRC-96(ZIP)')]),
    Prototype(
        regex=re.compile(r'^[a-z0-9\/.]{24}$', re.IGNORECASE),
        modes=[
            HashInfo(name='Crypt16')]),
    Prototype(
        regex=re.compile(r'^(\$md2\$)?[a-f0-9]{32}$', re.IGNORECASE),
        modes=[
            HashInfo(name='MD2')]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{32}(:.+)?$', re.IGNORECASE),
        modes=[
            HashInfo(name='MD5'),
            HashInfo(name='MD4'),
            HashInfo(name='Double MD5'),
            HashInfo(name='LM'),
            HashInfo(name='RIPEMD-128'),
            HashInfo(name='Haval-128'),
            HashInfo(name='Tiger-128', ),
            HashInfo(name='Skein-256(128)', ),
            HashInfo(name='Skein-512(128)', ),
            HashInfo(name='Lotus Notes/Domino 5'),
            HashInfo(name='Skype'),
            HashInfo(name='ZipMonster'),
            HashInfo(name='PrestaShop'),
            HashInfo(name='md5(md5(md5($pass)))'),
            HashInfo(name='md5(strtoupper(md5($pass)))'),
            HashInfo(name='md5(sha1($pass))'),
            HashInfo(name='HMAC-MD5 (key = $pass)'),
            HashInfo(name='md5($username.0.$pass)')]),
    Prototype(
        regex=re.compile(r'^(\$snefru\$)?[a-f0-9]{32}$', re.IGNORECASE),
        modes=[
            HashInfo(name='Snefru-128')]),
    Prototype(
        regex=re.compile(r'^{SHA}[a-z0-9\/+]{27}=$', re.IGNORECASE),
        modes=[
            HashInfo(name='SHA-1(Base64)'),
            HashInfo(name='Netscape LDAP SHA')]),
    Prototype(
        regex=re.compile(r'^\$1\$[a-z0-9\/.]{0,8}\$[a-z0-9\/.]{22}(:.*)?$', re.IGNORECASE),
        modes=[
            HashInfo(name='MD5 Crypt'),
            HashInfo(name='FreeBSD MD5')]),
    Prototype(
        regex=re.compile(r'^0x[a-f0-9]{32}$', re.IGNORECASE),
        modes=[
            HashInfo(name='Lineage II C4')]),
    Prototype(
        regex=re.compile(r'^\$apr1\$[a-z0-9\/.]{0,8}\$[a-z0-9\/.]{22}$', re.IGNORECASE),
        modes=[
            HashInfo(name='MD5(APR)'),
            HashInfo(name='Apache MD5'),
            HashInfo(name='md5apr1')]),
    Prototype(
        regex=re.compile(r'^{smd5}[a-z0-9$\/.]{31}$', re.IGNORECASE),
        modes=[
            HashInfo(name='AIX(smd5)')]),
    Prototype(
        regex=re.compile(r'^[a-z0-9]{34}$', re.IGNORECASE),
        modes=[
            HashInfo(name='CryptoCurrency(Adress)')]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{40}(:.+)?$', re.IGNORECASE),
        modes=[
            HashInfo(name='SHA-1'),
            HashInfo(name='Double SHA-1'),
            HashInfo(name='RIPEMD-160'),
            HashInfo(name='Haval-160'),
            HashInfo(name='Tiger-160'),
            HashInfo(name='HAS-160'),
            HashInfo(name='Skein-256(160)'),
            HashInfo(name='Skein-512(160)'),
            HashInfo(name='sha1(sha1(sha1($pass)))'),
            HashInfo(name='sha1(md5($pass))'),
            HashInfo(name='HMAC-SHA1 (key = $pass)')]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{48}$', re.IGNORECASE),
        modes=[
            HashInfo(name='Haval-192'),
            HashInfo(name='Tiger-192'),
            HashInfo(name='SHA-1(Oracle)')]),
    Prototype(
        regex=re.compile(r'^[a-z0-9]{51}$', re.IGNORECASE),
        modes=[
            HashInfo(name='CryptoCurrency(PrivateKey)')]),
    Prototype(
        regex=re.compile(r'^{ssha1}[0-9]{2}\$[a-z0-9$\/.]{44}$', re.IGNORECASE),
        modes=[
            HashInfo(name='AIX(ssha1)')]),
    Prototype(
        regex=re.compile(r'^(\$md5,rounds=[0-9]+\$|\$md5\$rounds=[0-9]+\$|\$md5\$)[a-z0-9\/.]{0,16}(\$|\$\$)[a-z0-9\/.]{22}$', re.IGNORECASE),
        modes=[
            HashInfo(name='Sun MD5 Crypt')]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{56}$', re.IGNORECASE),
        modes=[
            HashInfo(name='SHA-224'),
            HashInfo(name='Haval-224', ),
            HashInfo(name='SHA3-224', ),
            HashInfo(name='Skein-256(224)', ),
            HashInfo(name='Skein-512(224)')]),
    Prototype(
        regex=re.compile(r'^(\$2[axy]|\$2)\$[0-9]{2}\$[a-z0-9\/.]{53}$', re.IGNORECASE),
        modes=[
            HashInfo(name='Blowfish(OpenBSD)'),
            HashInfo(name='Woltlab Burning Board 4.x'),
            HashInfo(name='bcrypt')]),
    Prototype(
        regex=re.compile(r'^\$bcrypt-sha256\$(2[axy]|2)\,[0-9]+\$[a-z0-9\/.]{22}\$[a-z0-9\/.]{31}$', re.IGNORECASE),
        modes=[
            HashInfo(name='bcrypt(SHA-256)')]),
    Prototype(
        regex=re.compile(r'^(\$snefru\$)?[a-f0-9]{64}$', re.IGNORECASE),
        modes=[
            HashInfo(name='Snefru-256')]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{64}(:.+)?$', re.IGNORECASE),
        modes=[
            HashInfo(name='SHA-256'),
            HashInfo(name='RIPEMD-256', ),
            HashInfo(name='Haval-256'),
            HashInfo(name='GOST R 34.11-94'),
            HashInfo(name='GOST CryptoPro S-Box', ),
            HashInfo(name='SHA3-256'),
            HashInfo(name='Skein-256'),
            HashInfo(name='Skein-512(256)', ),
            HashInfo(name='Ventrilo'),
            HashInfo(name='HMAC-SHA256 (key = $pass)'),]),
    Prototype(
        regex=re.compile(r'^(\$chap\$0\*)?[a-f0-9]{32}[\*:][a-f0-9]{32}(:[0-9]{2})?$', re.IGNORECASE),
        modes=[
            HashInfo(name='MD5(Chap)'),
            HashInfo(name='iSCSI CHAP Authentication')]),
    Prototype(
        regex=re.compile(r'^{ssha256}[0-9]{2}\$[a-z0-9$\/.]{60}$', re.IGNORECASE),
        modes=[
            HashInfo(name='AIX(ssha256)')]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{80}$', re.IGNORECASE),
        modes=[
            HashInfo(name='RIPEMD-320')]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{96}$', re.IGNORECASE),
        modes=[
            HashInfo(name='SHA-384'),
            HashInfo(name='SHA3-384',),
            HashInfo(name='Skein-512(384)',),
            HashInfo(name='Skein-1024(384)',)]),
    Prototype(
        regex=re.compile(r'^{SSHA512}[a-z0-9\/+]{96}$', re.IGNORECASE),
        modes=[
            HashInfo(name='SSHA-512(Base64)'),
            HashInfo(name='LDAP(SSHA-512)')]),
    Prototype(
        regex=re.compile(r'^{ssha512}[0-9]{2}\$[a-z0-9\/.]{16,48}\$[a-z0-9\/.]{86}$', re.IGNORECASE),
        modes=[
            HashInfo(name='AIX(ssha512)')]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{128}(:.+)?$', re.IGNORECASE),
        modes=[
            HashInfo(name='SHA-512'),
            HashInfo(name='Whirlpool'),
            HashInfo(name='Salsa10',),
            HashInfo(name='Salsa20',),
            HashInfo(name='SHA3-512'),
            HashInfo(name='Skein-512'),
            HashInfo(name='Skein-1024(512)', ),
            HashInfo(name='HMAC-SHA512 (key = $pass)'),]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{256}$', re.IGNORECASE),
        modes=[
            HashInfo(name='Skein-1024')]),
    Prototype(
        regex=re.compile(r'^\$5\$(rounds=[0-9]+\$)?[a-z0-9\/.]{0,16}\$[a-z0-9\/.]{43}$', re.IGNORECASE),
        modes=[
            HashInfo(name='SHA-256 Crypt')]),
    Prototype(
        regex=re.compile(r'^0x[a-f0-9]{4}[a-f0-9]{16}[a-f0-9]{64}$', re.IGNORECASE),
        modes=[
            HashInfo(name='Sybase ASE')]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{130}(:[a-f0-9]{40})?$', re.IGNORECASE),
        modes=[
            HashInfo(name='IPMI2 RAKP HMAC-SHA1')]),
    Prototype(
        regex=re.compile(r'^\$sha1\$[0-9]+\$[a-z0-9\/.]{0,64}\$[a-z0-9\/.]{28}$', re.IGNORECASE),
        modes=[
            HashInfo(name='SHA-1 Crypt')]),
    Prototype(
        regex=re.compile(r'^\$pbkdf2(-sha1)?\$[0-9]+\$[a-z0-9\/.]+\$[a-z0-9\/.]{27}$', re.IGNORECASE),
        modes=[
            HashInfo(name='PBKDF2-SHA1(Generic)')]),
    Prototype(
        regex=re.compile(r'^\$pbkdf2-sha256\$[0-9]+\$[a-z0-9\/.]+\$[a-z0-9\/.]{43}$', re.IGNORECASE),
        modes=[
            HashInfo(name='PBKDF2-SHA256(Generic)')]),
    Prototype(
        regex=re.compile(r'^\$pbkdf2-sha512\$[0-9]+\$[a-z0-9\/.]+\$[a-z0-9\/.]{86}$', re.IGNORECASE),
        modes=[
            HashInfo(name='PBKDF2-SHA512(Generic)')]),
    Prototype(
        regex=re.compile(r'^\$p5k2\$[0-9]+\$[a-z0-9\/+=-]+\$[a-z0-9\/+-]{27}=$', re.IGNORECASE),
        modes=[
            HashInfo(name='PBKDF2(Cryptacular)')]),
    Prototype(
        regex=re.compile(r'^\$p5k2\$[0-9]+\$[a-z0-9\/.]+\$[a-z0-9\/.]{32}$', re.IGNORECASE),
        modes=[
            HashInfo(name='PBKDF2(Dwayne Litzenberger)')]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{256}:[a-f0-9]{256}:[a-f0-9]{16}:[a-f0-9]{16}:[a-f0-9]{320}:[a-f0-9]{16}:[a-f0-9]{40}:[a-f0-9]{40}:[a-f0-9]{32}$', re.IGNORECASE),
        modes=[
            HashInfo(name='IKE-PSK MD5')]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{256}:[a-f0-9]{256}:[a-f0-9]{16}:[a-f0-9]{16}:[a-f0-9]{320}:[a-f0-9]{16}:[a-f0-9]{40}:[a-f0-9]{40}:[a-f0-9]{40}$', re.IGNORECASE),
        modes=[
            HashInfo(name='IKE-PSK SHA1')]),
    Prototype(
        regex=re.compile(r'^SCRYPT:[0-9]{1,}:[0-9]{1}:[0-9]{1}:[a-z0-9:\/+=]{1,}$', re.IGNORECASE),
        modes=[
            HashInfo(name='scrypt')]),
    Prototype(
        regex=re.compile(r'^[a-z0-9\/.]{13,}$', re.IGNORECASE),
        modes=[
            HashInfo(name='BigCrypt')]),
]


class HashID(object):
    """
    HashID with configurable prototypes
    """

    def __init__(self, prototypes=prototypes):
        super(HashID, self).__init__()

        # Set self.prototypes to a copy of prototypes to allow
        # modification after instantiation
        self.prototypes = list(prototypes)

    def identifyHash(self, phash):
        """
        Returns identified HashInfo
        """
        phash = phash.strip()
        for prototype in self.prototypes:
            if prototype.regex.match(phash):
                for mode in prototype.modes:
                    yield mode


def writeResult(identified_modes, outfile, hashcatMode=False, johnFormat=False, extended=False):
    """
    Write human readable output from identifyHash
    """
    count = 0
    hashTypes = ""
    for mode in identified_modes:
        count += 1
        hashTypes += u"[+] {0} ".format(mode.name)
        hashTypes += "\n"
    outfile.write(hashTypes)
    if count == 0:
        outfile.write(u"[+] Unknown hash\n")
    return (count > 0)


def main():
    usage = "{0} [-h] [-o FILE] [-c COIN] INPUT".format(os.path.basename(__file__))

    parser = argparse.ArgumentParser(
        description="Identify the different types of hashes. Default mode is to identify the hash type and write to stdout",
        usage=usage,
        add_help=False,
        formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=27)
    )
    parser.add_argument("strings",
                        metavar="INPUT", type=str, nargs="*",
                        help="input to analyze (default: STDIN)")
    group = parser.add_argument_group('options')
    group.add_argument("-o", "--outfile",
                       metavar="FILE", type=str,
                       help="Write output to file")
    
    group.add_argument("-c", "--coin",
                       metavar="COIN", type=str,
                       help="Type of cryptocurrency coin to search for")

    group.add_argument("-h", "--help",
                       action="help",
                       help="Show this help message and exit")

    args = parser.parse_args()

    hashID = HashID()

    if not args.outfile:
        outfile = sys.stdout
    else:
        try:
            outfile = io.open(args.outfile, "w", encoding="utf-8")
        except EnvironmentError:
            parser.error("Could not open {0}".format(args.output))


    if not args.strings or args.strings[0] == "-":
        if args.coin:
            url = "https://crytop.appsndevs.com/api/coinDetail/coin/"
            r = requests.get(url + args.coin)
            print("Id: " + str(r.json().get('data').get('id')))
            print("Name: " + r.json().get('data').get('name'))
            print("Hash: " + r.json().get('data').get('hash'))
        
        while True:
            line = input("> ")
            if not line:
                break
            outfile.write(u"Analyzing '{0}'\n".format(line.strip()))
            writeResult(hashID.identifyHash(line), outfile)
            sys.stdout.flush()
    else:
        for string in args.strings:
            if os.path.isfile(string):
                try:
                    with io.open(string, "r", encoding="utf-8") as infile:
                        outfile.write("--File '{0}'--\n".format(string))
                        for line in infile:
                            if line.strip():
                                outfile.write(u"Analyzing '{0}'\n".format(line.strip()))
                                writeResult(hashID.identifyHash(line), outfile, args.mode, args.john, args.extended)
                except (EnvironmentError, UnicodeDecodeError):
                    outfile.write("--File '{0}' - could not open--".format(string))
                else:
                    outfile.write("--End of file '{0}'--".format(string))
            else:
                outfile.write(u"Analyzing '{0}'\n".format(string.strip()))
                writeResult(hashID.identifyHash(string), outfile, args.mode, args.john, args.extended)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass