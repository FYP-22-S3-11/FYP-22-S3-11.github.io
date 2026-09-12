import re
from collections import namedtuple


Prototype = namedtuple('Prototype', ['regex', 'modes'])
HashInfo = namedtuple('HashInfo', ['name'])

list_prototypes = [
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
        regex=re.compile(r'^[a-z0-9/.]{13}$', re.IGNORECASE),
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
        regex=re.compile(r'^_[a-z0-9/.]{19}$', re.IGNORECASE),
        modes=[
            HashInfo(name='BSDi Crypt')]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{24}$', re.IGNORECASE),
        modes=[
            HashInfo(name='CRC-96(ZIP)')]),
    Prototype(
        regex=re.compile(r'^[a-z0-9/.]{24}$', re.IGNORECASE),
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
            HashInfo(name='NTLM'),
            HashInfo(name='RIPEMD-128'),
            HashInfo(name='Haval-128'),
            HashInfo(name='Tiger-128', ),
            HashInfo(name='Skein-256(128)', ),
            HashInfo(name='Skein-512(128)', ),
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
        regex=re.compile(r'^{SHA}[a-z0-9/+]{27}=$', re.IGNORECASE),
        modes=[
            HashInfo(name='SHA-1(Base64)'),
            HashInfo(name='Netscape LDAP SHA')]),
    Prototype(
        regex=re.compile(r'^\$1\$[a-z0-9/.]{0,8}\$[a-z0-9/.]{22}(:.*)?$', re.IGNORECASE),
        modes=[
            HashInfo(name='MD5 Crypt'),
            HashInfo(name='FreeBSD MD5')]),
    Prototype(
        regex=re.compile(r'^0x[a-f0-9]{32}$', re.IGNORECASE),
        modes=[
            HashInfo(name='Lineage II C4')]),
    Prototype(
        regex=re.compile(r'^\$apr1\$[a-z0-9/.]{0,8}\$[a-z0-9/.]{22}$', re.IGNORECASE),
        modes=[
            HashInfo(name='MD5(APR)'),
            HashInfo(name='Apache MD5'),
            HashInfo(name='md5apr1')]),
    Prototype(
        regex=re.compile(r'^{smd5}[a-z0-9$/.]{31}$', re.IGNORECASE),
        modes=[
            HashInfo(name='AIX(smd5)')]),
    Prototype(
        # Base58Check: 26-35 chars, version byte 1 (P2PKH) or 3 (P2SH).
        # Base58 has no 0, O, I or l, so this must stay case-sensitive.
        regex=re.compile(r'^[13][1-9A-HJ-NP-Za-km-z]{25,34}$'),
        modes=[
            HashInfo(name='Bitcoin Address (P2PKH/P2SH, Base58Check)')]),
    Prototype(
        # bech32/bech32m SegWit. Charset excludes 1, b, i and o; the spec allows
        # an all-uppercase form, hence IGNORECASE.
        regex=re.compile(r'^(bc|tb)1[02-9ac-hj-np-z]{11,71}$', re.IGNORECASE),
        modes=[
            HashInfo(name='Bitcoin Address (Bech32/SegWit)')]),
    Prototype(
        regex=re.compile(r'^0x[a-f0-9]{40}$', re.IGNORECASE),
        modes=[
            HashInfo(name='Ethereum Address (Keccak-256 derived)')]),
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
        # WIF, uncompressed: 51 chars, always starts 5H, 5J or 5K. Case-sensitive.
        regex=re.compile(r'^5[HJK][1-9A-HJ-NP-Za-km-z]{49}$'),
        modes=[
            HashInfo(name='Bitcoin WIF Private Key (uncompressed)')]),
    Prototype(
        # WIF, compressed: 52 chars, starts K or L. Was entirely unmatched before.
        regex=re.compile(r'^[KL][1-9A-HJ-NP-Za-km-z]{51}$'),
        modes=[
            HashInfo(name='Bitcoin WIF Private Key (compressed)')]),
    Prototype(
        # BIP32/BIP49/BIP84 extended keys: 4-char prefix plus 107 Base58 chars.
        regex=re.compile(r'^(xprv|xpub|yprv|ypub|zprv|zpub)[1-9A-HJ-NP-Za-km-z]{107}$'),
        modes=[
            HashInfo(name='BIP32 Extended Key')]),
    Prototype(
        regex=re.compile(r'^{ssha1}\d{2}\$[a-z0-9$/.]{44}$', re.IGNORECASE),
        modes=[
            HashInfo(name='AIX(ssha1)')]),
    Prototype(
        regex=re.compile(
            r'^(\$md5,rounds=\d+\$|\$md5\$rounds=\d+\$|\$md5\$)[a-z0-9/.]{0,16}(\$|\$\$)[a-z0-9/.]{22}$',
            re.IGNORECASE),
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
        regex=re.compile(r'^(\$2[abxy]|\$2)\$\d{2}\$[a-z0-9/.]{53}$', re.IGNORECASE),
        modes=[
            HashInfo(name='Blowfish(OpenBSD)'),
            HashInfo(name='bcrypt')]),
    Prototype(
        regex=re.compile(r'^\$bcrypt-sha256\$(2[axy]|2),\d+\$[a-z0-9/.]{22}\$[a-z0-9/.]{31}$', re.IGNORECASE),
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
            HashInfo(name='HMAC-SHA256 (key = $pass)'), ]),
    Prototype(
        regex=re.compile(r'^(\$chap\$0\*)?[a-f0-9]{32}[*:][a-f0-9]{32}(:\d{2})?$', re.IGNORECASE),
        modes=[
            HashInfo(name='MD5(Chap)'),
            HashInfo(name='iSCSI CHAP Authentication')]),
    Prototype(
        regex=re.compile(r'^{ssha256}\d{2}\$[a-z0-9$/.]{60}$', re.IGNORECASE),
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
            HashInfo(name='SHA3-384', ),
            HashInfo(name='Skein-512(384)', ),
            HashInfo(name='Skein-1024(384)', )]),
    Prototype(
        regex=re.compile(r'^{SSHA512}[a-z0-9/+]{96}$', re.IGNORECASE),
        modes=[
            HashInfo(name='SSHA-512(Base64)'),
            HashInfo(name='LDAP(SSHA-512)')]),
    Prototype(
        regex=re.compile(r'^{ssha512}\d{2}\$[a-z0-9/.]{16,48}\$[a-z0-9/.]{86}$', re.IGNORECASE),
        modes=[
            HashInfo(name='AIX(ssha512)')]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{128}(:.+)?$', re.IGNORECASE),
        modes=[
            HashInfo(name='SHA-512'),
            HashInfo(name='Whirlpool'),
            HashInfo(name='Salsa10', ),
            HashInfo(name='Salsa20', ),
            HashInfo(name='SHA3-512'),
            HashInfo(name='Skein-512'),
            HashInfo(name='Skein-1024(512)', ),
            HashInfo(name='HMAC-SHA512 (key = $pass)'), ]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{256}$', re.IGNORECASE),
        modes=[
            HashInfo(name='Skein-1024')]),
    Prototype(
        regex=re.compile(r'^\$5\$(rounds=\d+\$)?[a-z0-9/.]{0,16}\$[a-z0-9/.]{43}$', re.IGNORECASE),
        modes=[
            HashInfo(name='SHA-256 Crypt')]),
    Prototype(
        regex=re.compile(r'^\$6\$(rounds=\d+\$)?[a-z0-9/.]{0,16}\$[a-z0-9/.]{86}$', re.IGNORECASE),
        modes=[
            HashInfo(name='SHA-512 Crypt')]),
    Prototype(
        regex=re.compile(r'^\$y\$[a-z0-9/.]+\$[a-z0-9/.]+\$[a-z0-9/.]{43}$', re.IGNORECASE),
        modes=[
            HashInfo(name='yescrypt')]),
    Prototype(
        regex=re.compile(
            r'^\$argon2(id|i|d)\$v=\d+\$m=\d+,t=\d+,p=\d+(,keyid=[a-z0-9+/]+)?(,data=[a-z0-9+/]+)?\$[a-z0-9+/]+\$[a-z0-9+/]+$',
            re.IGNORECASE),
        modes=[
            HashInfo(name='Argon2')]),
    Prototype(
        regex=re.compile(r'^\$scrypt\$ln=\d+,r=\d+,p=\d+\$[a-z0-9+/.=]*\$[a-z0-9+/.=]+$', re.IGNORECASE),
        modes=[
            HashInfo(name='scrypt(Passlib)')]),
    Prototype(
        regex=re.compile(r'^pbkdf2_(sha1|sha256|sha512)\$\d+\$[a-z0-9+/.=]+\$[a-z0-9+/.=]+$', re.IGNORECASE),
        modes=[
            HashInfo(name='Django(PBKDF2)')]),
    Prototype(
        regex=re.compile(r'^0x[a-f0-9]{4}[a-f0-9]{16}[a-f0-9]{64}$', re.IGNORECASE),
        modes=[
            HashInfo(name='Sybase ASE')]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{130}(:[a-f0-9]{40})?$', re.IGNORECASE),
        modes=[
            HashInfo(name='IPMI2 RAKP HMAC-SHA1')]),
    Prototype(
        regex=re.compile(r'^\$sha1\$\d+\$[a-z0-9/.]{0,64}\$[a-z0-9/.]{28}$', re.IGNORECASE),
        modes=[
            HashInfo(name='SHA-1 Crypt')]),
    Prototype(
        regex=re.compile(r'^\$pbkdf2(-sha1)?\$\d+\$[a-z0-9/.]+\$[a-z0-9/.]{27}$', re.IGNORECASE),
        modes=[
            HashInfo(name='PBKDF2-SHA1(Generic)')]),
    Prototype(
        regex=re.compile(r'^\$pbkdf2-sha256\$\d+\$[a-z0-9/.]+\$[a-z0-9/.]{43}$', re.IGNORECASE),
        modes=[
            HashInfo(name='PBKDF2-SHA256(Generic)')]),
    Prototype(
        regex=re.compile(r'^\$pbkdf2-sha512\$\d+\$[a-z0-9/.]+\$[a-z0-9/.]{86}$', re.IGNORECASE),
        modes=[
            HashInfo(name='PBKDF2-SHA512(Generic)')]),
    Prototype(
        regex=re.compile(r'^\$p5k2\$\d+\$[a-z0-9/+=-]+\$[a-z0-9/+-]{27}=$', re.IGNORECASE),
        modes=[
            HashInfo(name='PBKDF2(Cryptacular)')]),
    Prototype(
        regex=re.compile(r'^\$p5k2\$\d+\$[a-z0-9/.]+\$[a-z0-9/.]{32}$', re.IGNORECASE),
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
        regex=re.compile(r'^SCRYPT:\d+:\d:\d:[a-z0-9:/+=]+$', re.IGNORECASE),
        modes=[
            HashInfo(name='scrypt')]),
    Prototype(
        # 13-char DES block plus one or more 11-char extension blocks (13 + 11n).
        # The previous '{13,}' matched any long alphanumeric string, which made
        # BigCrypt a false positive on nearly every hash.
        regex=re.compile(r'^[a-z0-9/.]{13}([a-z0-9/.]{11})+$', re.IGNORECASE),
        modes=[
            HashInfo(name='BigCrypt')]),
]
