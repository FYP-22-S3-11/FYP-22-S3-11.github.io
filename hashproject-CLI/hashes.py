#!/usr/bin/env python3

import io
import os
import re
import sys
import argparse
from collections import namedtuple

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
        regex=re.compile(r'^\+[a-z0-9\/.]{12}$', re.IGNORECASE),
        modes=[
            HashInfo(name='Eggdrop IRC Bot')]),
    
    Prototype(
        regex=re.compile(r'^[a-z0-9\/.]{13}$', re.IGNORECASE),
        modes=[
            HashInfo(name='DES(Unix)'),
            HashInfo(name='Traditional DES'),
            HashInfo(name='DEScrypt')]),
    
    Prototype(
        regex=re.compile(r'^[a-f0-9]{16}$', re.IGNORECASE),
        modes=[
            HashInfo(name='MySQL323'),
            HashInfo(name='DES(Oracle)'),
            HashInfo(name='Half MD5'),
            HashInfo(name='Oracle 7-10g'),
            HashInfo(name='FNV-164'),
            HashInfo(name='CRC-64')]),
    
    Prototype(
        regex=re.compile(r'^[a-z0-9\/.]{16}$', re.IGNORECASE),
        modes=[
            HashInfo(name='Cisco-PIX(MD5)')]),
    Prototype(
        regex=re.compile(r'^\([a-z0-9\/+]{20}\)$', re.IGNORECASE),
        modes=[
            HashInfo(name='Lotus Notes/Domino 6')]),
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
            HashInfo(name='md5($pass.$salt)'),
            HashInfo(name='md5($salt.$pass)'),
            HashInfo(name='md5(unicode($pass).$salt)'),
            HashInfo(name='md5($salt.unicode($pass))'),
            HashInfo(name='HMAC-MD5 (key = $pass)'),
            HashInfo(name='HMAC-MD5 (key = $salt)'),
            HashInfo(name='md5(md5($salt).$pass)'),
            HashInfo(name='md5($salt.md5($pass))'),
            HashInfo(name='md5($pass.md5($salt))'),
            HashInfo(name='md5($salt.$pass.$salt)'),
            HashInfo(name='md5(md5($pass).md5($salt))'),
            HashInfo(name='md5($salt.md5($salt.$pass))'),
            HashInfo(name='md5($salt.md5($pass.$salt))'),
            HashInfo(name='md5($username.0.$pass)')]),
    Prototype(
        regex=re.compile(r'^(\$snefru\$)?[a-f0-9]{32}$', re.IGNORECASE),
        modes=[
            HashInfo(name='Snefru-128')]),
    Prototype(
        regex=re.compile(r'^(\$NT\$)?[a-f0-9]{32}$', re.IGNORECASE),
        modes=[
            HashInfo(name='NTLM')]),
    Prototype(
        regex=re.compile(r'^([^\\\/:*?"<>|]{1,20}:)?[a-f0-9]{32}(:[^\\\/:*?"<>|]{1,20})?$', re.IGNORECASE),
        modes=[
            HashInfo(name='Domain Cached Credentials')]),
    Prototype(
        regex=re.compile(r'^([^\\\/:*?"<>|]{1,20}:)?(\$DCC2\$10240#[^\\\/:*?"<>|]{1,20}#)?[a-f0-9]{32}$', re.IGNORECASE),
        modes=[
            HashInfo(name='Domain Cached Credentials 2')]),
    Prototype(
        regex=re.compile(r'^{SHA}[a-z0-9\/+]{27}=$', re.IGNORECASE),
        modes=[
            HashInfo(name='SHA-1(Base64)'),
            HashInfo(name='Netscape LDAP SHA')]),
    Prototype(
        regex=re.compile(r'^\$1\$[a-z0-9\/.]{0,8}\$[a-z0-9\/.]{22}(:.*)?$', re.IGNORECASE),
        modes=[
            HashInfo(name='MD5 Crypt'),
            HashInfo(name='Cisco-IOS(MD5)'),
            HashInfo(name='FreeBSD MD5')]),
    Prototype(
        regex=re.compile(r'^0x[a-f0-9]{32}$', re.IGNORECASE),
        modes=[
            HashInfo(name='Lineage II C4')]),
    Prototype(
        regex=re.compile(r'^\$H\$[a-z0-9\/.]{31}$', re.IGNORECASE),
        modes=[
            HashInfo(name='phpBB v3.x'),
            HashInfo(name='Wordpress v2.6.0/2.6.1'),
            HashInfo(name="PHPass' Portable Hash")]),
    Prototype(
        regex=re.compile(r'^\$P\$[a-z0-9\/.]{31}$', re.IGNORECASE),
        modes=[
            HashInfo(name=u'Wordpress ≥ v2.6.2'),
            HashInfo(name=u'Joomla ≥ v2.5.18'),
            HashInfo(name="PHPass' Portable Hash")]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{32}:[a-z0-9]{2}$', re.IGNORECASE),
        modes=[
            HashInfo(name='osCommerce'),
            HashInfo(name='xt:Commerce')]),
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
        regex=re.compile(r'^[a-f0-9]{32}:[a-f0-9]{32}$', re.IGNORECASE),
        modes=[
            HashInfo(name='WebEdition CMS')]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{32}:.{5}$', re.IGNORECASE),
        modes=[
            HashInfo(name=u'IP.Board ≥ v2+')]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{32}:.{8}$', re.IGNORECASE),
        modes=[
            HashInfo(name=u'MyBB ≥ v1.2+')]),
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
            HashInfo(name='LinkedIn'),
            HashInfo(name='Skein-256(160)'),
            HashInfo(name='Skein-512(160)'),
            HashInfo(name='sha1(sha1(sha1($pass)))'),
            HashInfo(name='sha1(md5($pass))'),
            HashInfo(name='HMAC-SHA1 (key = $pass)')]),
    Prototype(
        regex=re.compile(r'^[a-z0-9]{43}$', re.IGNORECASE),
        modes=[
            HashInfo(name='Cisco-IOS(SHA-256)')]),
    Prototype(
        regex=re.compile(r'^[a-z0-9=]{47}$', re.IGNORECASE),
        modes=[
            HashInfo(name='Fortigate(FortiOS)')]),
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
        regex=re.compile(r'^(S:)?[a-f0-9]{40}(:)?[a-f0-9]{20}$', re.IGNORECASE),
        modes=[
            HashInfo(name='Oracle 11g/12c')]),
    Prototype(
        regex=re.compile(r'^\$bcrypt-sha256\$(2[axy]|2)\,[0-9]+\$[a-z0-9\/.]{22}\$[a-z0-9\/.]{31}$', re.IGNORECASE),
        modes=[
            HashInfo(name='bcrypt(SHA-256)')]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{32}:.{3}$', re.IGNORECASE),
        modes=[
            HashInfo(name='vBulletin < v3.8.5')]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{32}:.{30}$', re.IGNORECASE),
        modes=[
            HashInfo(name=u'vBulletin ≥ v3.8.5')]),
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
            HashInfo(name='sha256($pass.$salt)'),
            HashInfo(name='sha256($salt.$pass)'),
            HashInfo(name='sha256(unicode($pass).$salt)'),
            HashInfo(name='sha256($salt.unicode($pass))'),
            HashInfo(name='HMAC-SHA256 (key = $pass)'),
            HashInfo(name='HMAC-SHA256 (key = $salt)')]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{32}:[a-z0-9]{32}$', re.IGNORECASE),
        modes=[
            HashInfo(name='Joomla < v2.5.18')]),
    Prototype(
        regex=re.compile(r'^[a-f-0-9]{32}:[a-f-0-9]{32}$', re.IGNORECASE),
        modes=[
            HashInfo(name='SAM(LM_Hash:NT_Hash)')]),
    Prototype(
        regex=re.compile(r'^(\$chap\$0\*)?[a-f0-9]{32}[\*:][a-f0-9]{32}(:[0-9]{2})?$', re.IGNORECASE),
        modes=[
            HashInfo(name='MD5(Chap)'),
            HashInfo(name='iSCSI CHAP Authentication')]),
    Prototype(
        regex=re.compile(r'^\$episerver\$\*0\*[a-z0-9\/=+]+\*[a-z0-9\/=+]{27,28}$', re.IGNORECASE),
        modes=[
            HashInfo(name='EPiServer 6.x < v4')]),
    Prototype(
        regex=re.compile(r'^{ssha256}[0-9]{2}\$[a-z0-9$\/.]{60}$', re.IGNORECASE),
        modes=[
            HashInfo(name='AIX(ssha256)')]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{80}$', re.IGNORECASE),
        modes=[
            HashInfo(name='RIPEMD-320')]),
    Prototype(
        regex=re.compile(r'^\$episerver\$\*1\*[a-z0-9\/=+]+\*[a-z0-9\/=+]{42,43}$', re.IGNORECASE),
        modes=[
            HashInfo(name=u'EPiServer 6.x ≥ v4')]),
    Prototype(
        regex=re.compile(r'^0x0100[a-f0-9]{88}$', re.IGNORECASE),
        modes=[
            HashInfo(name='MSSQL(2000)')]),
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
            HashInfo(name='sha512($pass.$salt)'),
            HashInfo(name='sha512($salt.$pass)'),
            HashInfo(name='sha512(unicode($pass).$salt)'),
            HashInfo(name='sha512($salt.unicode($pass))'),
            HashInfo(name='HMAC-SHA512 (key = $pass)'),
            HashInfo(name='HMAC-SHA512 (key = $salt)')]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{136}$', re.IGNORECASE),
        modes=[
            HashInfo(name='OSX v10.7')]),
    Prototype(
        regex=re.compile(r'^0x0200[a-f0-9]{136}$', re.IGNORECASE),
        modes=[
            HashInfo(name='MSSQL(2012)'),
            HashInfo(name='MSSQL(2014)')]),
    Prototype(
        regex=re.compile(r'^\$ml\$[0-9]+\$[a-f0-9]{64}\$[a-f0-9]{128}$', re.IGNORECASE),
        modes=[
            HashInfo(name='OSX v10.8'),
            HashInfo(name='OSX v10.9')]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{256}$', re.IGNORECASE),
        modes=[
            HashInfo(name='Skein-1024')]),
    Prototype(
        regex=re.compile(r'^grub\.pbkdf2\.sha512\.[0-9]+\.([a-f0-9]{128,2048}\.|[0-9]+\.)?[a-f0-9]{128}$', re.IGNORECASE),
        modes=[
            HashInfo(name='GRUB 2')]),
    Prototype(
        regex=re.compile(r'^sha1\$[a-z0-9]+\$[a-f0-9]{40}$', re.IGNORECASE),
        modes=[
            HashInfo(name='Django(SHA-1)')]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{49}$', re.IGNORECASE),
        modes=[
            HashInfo(name='Citrix Netscaler')]),
    Prototype(
        regex=re.compile(r'^\$S\$[a-z0-9\/.]{52}$', re.IGNORECASE),
        modes=[
            HashInfo(name='Drupal > v7.x')]),
    Prototype(
        regex=re.compile(r'^\$5\$(rounds=[0-9]+\$)?[a-z0-9\/.]{0,16}\$[a-z0-9\/.]{43}$', re.IGNORECASE),
        modes=[
            HashInfo(name='SHA-256 Crypt')]),
    Prototype(
        regex=re.compile(r'^0x[a-f0-9]{4}[a-f0-9]{16}[a-f0-9]{64}$', re.IGNORECASE),
        modes=[
            HashInfo(name='Sybase ASE')]),
    Prototype(
        regex=re.compile(r'^\$6\$(rounds=[0-9]+\$)?[a-z0-9\/.]{0,16}\$[a-z0-9\/.]{86}$', re.IGNORECASE),
        modes=[
            HashInfo(name='SHA-512 Crypt')]),
    Prototype(
        regex=re.compile(r'^\$sha\$[a-z0-9]{1,16}\$([a-f0-9]{32}|[a-f0-9]{40}|[a-f0-9]{64}|[a-f0-9]{128}|[a-f0-9]{140})$', re.IGNORECASE),
        modes=[
            HashInfo(name='Minecraft(AuthMe Reloaded)',)]),
    Prototype(
        regex=re.compile(r'^sha256\$[a-z0-9]+\$[a-f0-9]{64}$', re.IGNORECASE),
        modes=[
            HashInfo(name='Django(SHA-256)')]),
    Prototype(
        regex=re.compile(r'^sha384\$[a-z0-9]+\$[a-f0-9]{96}$', re.IGNORECASE),
        modes=[
            HashInfo(name='Django(SHA-384)')]),
    Prototype(
        regex=re.compile(r'^crypt1:[a-z0-9+=]{12}:[a-z0-9+=]{12}$', re.IGNORECASE),
        modes=[
            HashInfo(name='Clavister Secure Gateway')]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{112}$', re.IGNORECASE),
        modes=[
            HashInfo(name='Cisco VPN Client(PCF-File)')]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{1329}$', re.IGNORECASE),
        modes=[
            HashInfo(name='Microsoft MSTSC(RDP-File)')]),
    Prototype(
        regex=re.compile(r'^[^\\\/:*?"<>|]{1,20}[:]{2,3}([^\\\/:*?"<>|]{1,20})?:[a-f0-9]{48}:[a-f0-9]{48}:[a-f0-9]{16}$', re.IGNORECASE),
        modes=[
            HashInfo(name='NetNTLMv1-VANILLA / NetNTLMv1+ESS')]),
    Prototype(
        regex=re.compile(r'^([^\\\/:*?"<>|]{1,20}\\)?[^\\\/:*?"<>|]{1,20}[:]{2,3}([^\\\/:*?"<>|]{1,20}:)?[^\\\/:*?"<>|]{1,20}:[a-f0-9]{32}:[a-f0-9]+$', re.IGNORECASE),
        modes=[
            HashInfo(name='NetNTLMv2')]),
    Prototype(
        regex=re.compile(r'^\$(krb5pa|mskrb5)\$([0-9]{2})?\$.+\$[a-f0-9]{1,}$', re.IGNORECASE),
        modes=[
            HashInfo(name='Kerberos 5 AS-REQ Pre-Auth')]),
    Prototype(
        regex=re.compile(r'^\$scram\$[0-9]+\$[a-z0-9\/.]{16}\$sha-1=[a-z0-9\/.]{27},sha-256=[a-z0-9\/.]{43},sha-512=[a-z0-9\/.]{86}$', re.IGNORECASE),
        modes=[
            HashInfo(name='SCRAM Hash')]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{40}:[a-f0-9]{0,32}$', re.IGNORECASE),
        modes=[
            HashInfo(name='Redmine Project Management Web App')]),
    Prototype(
        regex=re.compile(r'^(.+)?\$[a-f0-9]{16}$', re.IGNORECASE),
        modes=[
            HashInfo(name='SAP CODVN B (BCODE)')]),
    Prototype(
        regex=re.compile(r'^(.+)?\$[a-f0-9]{40}$', re.IGNORECASE),
        modes=[
            HashInfo(name='SAP CODVN F/G (PASSCODE)')]),
    Prototype(
        regex=re.compile(r'^(.+\$)?[a-z0-9\/.+]{30}(:.+)?$', re.IGNORECASE),
        modes=[
            HashInfo(name='Juniper Netscreen/SSG(ScreenOS)')]),
    Prototype(
        regex=re.compile(r'^0x[a-f0-9]{60}\s0x[a-f0-9]{40}$', re.IGNORECASE),
        modes=[
            HashInfo(name='EPi')]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{40}:[^*]{1,25}$', re.IGNORECASE),
        modes=[
            HashInfo(name=u'SMF ≥ v1.1')]),
    Prototype(
        regex=re.compile(r'^(\$wbb3\$\*1\*)?[a-f0-9]{40}[:*][a-f0-9]{40}$', re.IGNORECASE),
        modes=[
            HashInfo(name='Woltlab Burning Board 3.x')]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{130}(:[a-f0-9]{40})?$', re.IGNORECASE),
        modes=[
            HashInfo(name='IPMI2 RAKP HMAC-SHA1')]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{32}:[0-9]+:[a-z0-9_.+-]+@[a-z0-9-]+\.[a-z0-9-.]+$', re.IGNORECASE),
        modes=[
            HashInfo(name='Lastpass')]),
    Prototype(
        regex=re.compile(r'^[a-z0-9\/.]{16}([:$].{1,})?$', re.IGNORECASE),
        modes=[
            HashInfo(name='Cisco-ASA(MD5)')]),
    Prototype(
        regex=re.compile(r'^\$vnc\$\*[a-f0-9]{32}\*[a-f0-9]{32}$', re.IGNORECASE),
        modes=[
            HashInfo(name='VNC')]),
    Prototype(
        regex=re.compile(r'^[a-z0-9]{32}(:([a-z0-9-]+\.)?[a-z0-9-.]+\.[a-z]{2,7}:.+:[0-9]+)?$', re.IGNORECASE),
        modes=[
            HashInfo(name='DNSSEC(NSEC3)')]),
    Prototype(
        regex=re.compile(r'^(user-.+:)?\$racf\$\*.+\*[a-f0-9]{16}$', re.IGNORECASE),
        modes=[
            HashInfo(name='RACF')]),
    Prototype(
        regex=re.compile(r'^\$3\$\$[a-f0-9]{32}$', re.IGNORECASE),
        modes=[
            HashInfo(name='NTHash(FreeBSD Variant)')]),
    Prototype(
        regex=re.compile(r'^\$sha1\$[0-9]+\$[a-z0-9\/.]{0,64}\$[a-z0-9\/.]{28}$', re.IGNORECASE),
        modes=[
            HashInfo(name='SHA-1 Crypt')]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{70}$', re.IGNORECASE),
        modes=[
            HashInfo(name='hMailServer')]),
    Prototype(
        regex=re.compile(r'^[:\$][AB][:\$]([a-f0-9]{1,8}[:\$])?[a-f0-9]{32}$', re.IGNORECASE),
        modes=[
            HashInfo(name='MediaWiki')]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{140}$', re.IGNORECASE),
        modes=[
            HashInfo(name='Minecraft(xAuth)')]),
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
        regex=re.compile(r'^{FSHP[0123]\|[0-9]+\|[0-9]+}[a-z0-9\/+=]+$', re.IGNORECASE),
        modes=[
            HashInfo(name='Fairly Secure Hashed Password')]),
    Prototype(
        regex=re.compile(r'^\$PHPS\$.+\$[a-f0-9]{32}$', re.IGNORECASE),
        modes=[
            HashInfo(name='PHPS')]),
    Prototype(
        regex=re.compile(r'^[0-9]{4}:[a-f0-9]{16}:[a-f0-9]{2080}$', re.IGNORECASE),
        modes=[
            HashInfo(name='1Password(Agile Keychain)')]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{64}:[a-f0-9]{32}:[0-9]{5}:[a-f0-9]{608}$', re.IGNORECASE),
        modes=[
            HashInfo(name='1Password(Cloud Keychain)')]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{256}:[a-f0-9]{256}:[a-f0-9]{16}:[a-f0-9]{16}:[a-f0-9]{320}:[a-f0-9]{16}:[a-f0-9]{40}:[a-f0-9]{40}:[a-f0-9]{32}$', re.IGNORECASE),
        modes=[
            HashInfo(name='IKE-PSK MD5')]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{256}:[a-f0-9]{256}:[a-f0-9]{16}:[a-f0-9]{16}:[a-f0-9]{320}:[a-f0-9]{16}:[a-f0-9]{40}:[a-f0-9]{40}:[a-f0-9]{40}$', re.IGNORECASE),
        modes=[
            HashInfo(name='IKE-PSK SHA1')]),
    Prototype(
        regex=re.compile(r'^[a-z0-9\/+]{27}=$', re.IGNORECASE),
        modes=[
            HashInfo(name='PeopleSoft')]),
    Prototype(
        regex=re.compile(r'^crypt\$[a-f0-9]{5}\$[a-z0-9\/.]{13}$', re.IGNORECASE),
        modes=[
            HashInfo(name='Django(DES Crypt Wrapper)')]),
    Prototype(
        regex=re.compile(r'^(\$django\$\*1\*)?pbkdf2_sha256\$[0-9]+\$[a-z0-9]+\$[a-z0-9\/+=]{44}$', re.IGNORECASE),
        modes=[
            HashInfo(name='Django(PBKDF2-HMAC-SHA256)')]),
    Prototype(
        regex=re.compile(r'^pbkdf2_sha1\$[0-9]+\$[a-z0-9]+\$[a-z0-9\/+=]{28}$', re.IGNORECASE),
        modes=[
            HashInfo(name='Django(PBKDF2-HMAC-SHA1)')]),
    Prototype(
        regex=re.compile(r'^bcrypt(\$2[axy]|\$2)\$[0-9]{2}\$[a-z0-9\/.]{53}$', re.IGNORECASE),
        modes=[
            HashInfo(name='Django(bcrypt)')]),
    Prototype(
        regex=re.compile(r'^md5\$[a-f0-9]+\$[a-f0-9]{32}$', re.IGNORECASE),
        modes=[
            HashInfo(name='Django(MD5)')]),
    Prototype(
        regex=re.compile(r'^\{PKCS5S2\}[a-z0-9\/+]{64}$', re.IGNORECASE),
        modes=[
            HashInfo(name='PBKDF2(Atlassian)')]),
    Prototype(
        regex=re.compile(r'^md5[a-f0-9]{32}$', re.IGNORECASE),
        modes=[
            HashInfo(name='PostgreSQL MD5')]),
    Prototype(
        regex=re.compile(r'^\([a-z0-9\/+]{49}\)$', re.IGNORECASE),
        modes=[
            HashInfo(name='Lotus Notes/Domino 8')]),
    Prototype(
        regex=re.compile(r'^SCRYPT:[0-9]{1,}:[0-9]{1}:[0-9]{1}:[a-z0-9:\/+=]{1,}$', re.IGNORECASE),
        modes=[
            HashInfo(name='scrypt')]),
    Prototype(
        regex=re.compile(r'^\$8\$[a-z0-9\/.]{14}\$[a-z0-9\/.]{43}$', re.IGNORECASE),
        modes=[
            HashInfo(name='Cisco Type 8')]),
    Prototype(
        regex=re.compile(r'^\$9\$[a-z0-9\/.]{14}\$[a-z0-9\/.]{43}$', re.IGNORECASE),
        modes=[
            HashInfo(name='Cisco Type 9')]),
    Prototype(
        regex=re.compile(r'^\$office\$\*2007\*[0-9]{2}\*[0-9]{3}\*[0-9]{2}\*[a-z0-9]{32}\*[a-z0-9]{32}\*[a-z0-9]{40}$', re.IGNORECASE),
        modes=[
            HashInfo(name='Microsoft Office 2007')]),
    Prototype(
        regex=re.compile(r'^\$office\$\*2010\*[0-9]{6}\*[0-9]{3}\*[0-9]{2}\*[a-z0-9]{32}\*[a-z0-9]{32}\*[a-z0-9]{64}$', re.IGNORECASE),
        modes=[
            HashInfo(name='Microsoft Office 2010')]),
    Prototype(
        regex=re.compile(r'^\$office\$\*2013\*[0-9]{6}\*[0-9]{3}\*[0-9]{2}\*[a-z0-9]{32}\*[a-z0-9]{32}\*[a-z0-9]{64}$', re.IGNORECASE),
        modes=[
            HashInfo(name='Microsoft Office 2013')]),
    Prototype(
        regex=re.compile(r'^\$fde\$[0-9]{2}\$[a-f0-9]{32}\$[0-9]{2}\$[a-f0-9]{32}\$[a-f0-9]{3072}$', re.IGNORECASE),
        modes=[
            HashInfo(name=u'Android FDE ≤ 4.3')]),
    Prototype(
        regex=re.compile(r'^\$oldoffice\$[01]\*[a-f0-9]{32}\*[a-f0-9]{32}\*[a-f0-9]{32}$', re.IGNORECASE),
        modes=[
            HashInfo(name=u'Microsoft Office ≤ 2003 (MD5+RC4)'),
            HashInfo(name=u'Microsoft Office ≤ 2003 (MD5+RC4) collider-mode #1'),
            HashInfo(name=u'Microsoft Office ≤ 2003 (MD5+RC4) collider-mode #2')]),
    Prototype(
        regex=re.compile(r'^\$oldoffice\$[34]\*[a-f0-9]{32}\*[a-f0-9]{32}\*[a-f0-9]{40}$', re.IGNORECASE),
        modes=[
            HashInfo(name=u'Microsoft Office ≤ 2003 (SHA1+RC4)'),
            HashInfo(name=u'Microsoft Office ≤ 2003 (SHA1+RC4) collider-mode #1'),
            HashInfo(name=u'Microsoft Office ≤ 2003 (SHA1+RC4) collider-mode #2')]),
    Prototype(
        regex=re.compile(r'^(\$radmin2\$)?[a-f0-9]{32}$', re.IGNORECASE),
        modes=[
            HashInfo(name='RAdmin v2.x')]),
    Prototype(
        regex=re.compile(r'^{x-issha,\s[0-9]{4}}[a-z0-9\/+=]+$', re.IGNORECASE),
        modes=[
            HashInfo(name='SAP CODVN H (PWDSALTEDHASH) iSSHA-1')]),
    Prototype(
        regex=re.compile(r'^\$cram_md5\$[a-z0-9\/+=-]+\$[a-z0-9\/+=-]{52}$', re.IGNORECASE),
        modes=[
            HashInfo(name='CRAM-MD5')]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{16}:2:4:[a-f0-9]{32}$', re.IGNORECASE),
        modes=[
            HashInfo(name='SipHash')]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{4,}$', re.IGNORECASE),
        modes=[
            HashInfo(name='Cisco Type 7')]),
    Prototype(
        regex=re.compile(r'^[a-z0-9\/.]{13,}$', re.IGNORECASE),
        modes=[
            HashInfo(name='BigCrypt')]),
    Prototype(
        regex=re.compile(r'^(\$cisco4\$)?[a-z0-9\/.]{43}$', re.IGNORECASE),
        modes=[
            HashInfo(name='Cisco Type 4')]),
    Prototype(
        regex=re.compile(r'^bcrypt_sha256\$\$(2[axy]|2)\$[0-9]+\$[a-z0-9\/.]{53}$', re.IGNORECASE),
        modes=[
            HashInfo(name='Django(bcrypt-SHA256)')]),
    Prototype(
        regex=re.compile(r'^\$postgres\$.[^\*]+[*:][a-f0-9]{1,32}[*:][a-f0-9]{32}$', re.IGNORECASE),
        modes=[
            HashInfo(name='PostgreSQL Challenge-Response Authentication (MD5)')]),
    Prototype(
        regex=re.compile(r'^\$siemens-s7\$[0-9]{1}\$[a-f0-9]{40}\$[a-f0-9]{40}$', re.IGNORECASE),
        modes=[
            HashInfo(name='Siemens-S7')]),
    Prototype(
        regex=re.compile(r'^(\$pst\$)?[a-f0-9]{8}$', re.IGNORECASE),
        modes=[
            HashInfo(name='Microsoft Outlook PST')]),
    Prototype(
        regex=re.compile(r'^sha256[:$][0-9]+[:$][a-z0-9\/+]+[:$][a-z0-9\/+]{32,128}$', re.IGNORECASE),
        modes=[
            HashInfo(name='PBKDF2-HMAC-SHA256(PHP)')]),
    Prototype(
        regex=re.compile(r'^(\$dahua\$)?[a-z0-9]{8}$', re.IGNORECASE),
        modes=[
            HashInfo(name='Dahua')]),
    Prototype(
        regex=re.compile(r'^\$mysqlna\$[a-f0-9]{40}[:*][a-f0-9]{40}$', re.IGNORECASE),
        modes=[
            HashInfo(name='MySQL Challenge-Response Authentication (SHA1)')]),
    Prototype(
        regex=re.compile(r'^\$pdf\$[24]\*[34]\*128\*[0-9-]{1,5}\*1\*(16|32)\*[a-f0-9]{32,64}\*32\*[a-f0-9]{64}\*(8|16|32)\*[a-f0-9]{16,64}$', re.IGNORECASE),
        modes=[HashInfo(name='PDF 1.4 - 1.6 (Acrobat 5 - 8)')])
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
    usage = "{0} [-h] [-e] [-m] [-j] [-o FILE] INPUT".format(os.path.basename(__file__))

    parser = argparse.ArgumentParser(
        description="Identify the different types of hashes used to encrypt data",
        usage=usage,
        
        add_help=False,
        formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=27)
    )
    parser.add_argument("strings",
                        metavar="INPUT", type=str, nargs="*",
                        help="input to analyze (default: STDIN)")
    group = parser.add_argument_group('options')
    group.add_argument("-e", "--extended",
                       action="store_true",
                       help="list all possible hash algorithms including salted passwords")
    group.add_argument("-o", "--outfile",
                       metavar="FILE", type=str,
                       help="write output to file")
    group.add_argument("-h", "--help",
                       action="help",
                       help="show this help message and exit")
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