#!/usr/bin/python3
"""Known-answer tests for the hash identifier.

Run with:  python3 -m unittest test_hashes -v
"""

import unittest

import hashID


class IdentifyHashTest(unittest.TestCase):

    def setUp(self):
        self.hid = hashID.HashID()

    def modes(self, value):
        return [mode.name for mode in self.hid.identify_hash(value)]

    def assertIdentifies(self, value, expected):
        modes = self.modes(value)
        self.assertTrue(
            any(expected.lower() in mode.lower() for mode in modes),
            f"expected {expected!r} among the types reported for {value!r}, got {modes}")

    def assertUnknown(self, value):
        self.assertEqual([], self.modes(value), f"{value!r} should not match any prototype")

    # --- classic digests -------------------------------------------------

    def test_md5(self):
        self.assertIdentifies("5f4dcc3b5aa765d61d8327deb882cf99", "MD5")

    def test_ntlm(self):
        self.assertIdentifies("8846f7eaee8fb117ad06bdd830b7586c", "NTLM")

    def test_sha1(self):
        self.assertIdentifies("5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8", "SHA-1")

    def test_sha256(self):
        self.assertIdentifies(
            "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8", "SHA-256")

    def test_sha512(self):
        self.assertIdentifies(
            "b109f3bbbc244eb82441917ed06d618b9008dd09b3befd1b5e07394c706a8bb9"
            "80b1d7785e5976ec049b46df5f1326af5a2ea6d103fd07c95385ffab0cacbc86", "SHA-512")

    def test_uppercase_hex_is_accepted(self):
        self.assertIdentifies("5F4DCC3B5AA765D61D8327DEB882CF99", "MD5")

    # --- password hashing schemes ---------------------------------------

    def test_bcrypt_2a(self):
        self.assertIdentifies(
            "$2a$12$GhvMmNVjRW29ulnudl.LbuAnUtN/LRfe1JsBm1Xu6LE3059z5Tr8m", "bcrypt")

    def test_bcrypt_2b(self):
        # $2b$ is the current bcrypt version prefix
        self.assertIdentifies(
            "$2b$12$GhvMmNVjRW29ulnudl.LbuAnUtN/LRfe1JsBm1Xu6LE3059z5Tr8m", "bcrypt")

    def test_sha256_crypt(self):
        self.assertIdentifies(
            "$5$rounds=5000$usesomesillystri$KqJWpanXZHKq2BOB43TSaYhEWsQ1Lr5QNyPCDH/Tp.6",
            "SHA-256 Crypt")

    def test_sha512_crypt(self):
        # the default /etc/shadow format on most Linux distributions
        self.assertIdentifies(
            "$6$rounds=5000$usesomesillystri$D4IrlHR5ynUwBQZjZHqZ7yrUJqTZPZ5zdqJLRnJ4"
            "KMvCkzPtqOfmLMbHCqXMuOFNBrqZ9ZfZKMhOmRnJmGBLI0", "SHA-512 Crypt")

    def test_argon2id(self):
        self.assertIdentifies(
            "$argon2id$v=19$m=65536,t=3,p=4$c29tZXNhbHQ$RdescudvJCsgt3ub+b+dWRWJTmaaJObG",
            "Argon2")

    def test_django_pbkdf2(self):
        self.assertIdentifies(
            "pbkdf2_sha256$260000$abcdefghij$hQ3o3oJ0i4l5gHk8s4hBqL7R1LPr0W8sEPTJFYBoYIQ=",
            "Django")

    # --- blockchain encodings -------------------------------------------

    def test_bitcoin_p2pkh_address(self):
        self.assertIdentifies("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa", "Bitcoin Address")

    def test_bitcoin_bech32_address(self):
        self.assertIdentifies("bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t4", "Bech32")

    def test_ethereum_address(self):
        self.assertIdentifies("0x5aAeb6053F3E94C9b9A09f33669435E7Ef1BeAed", "Ethereum")

    def test_wif_private_key_uncompressed(self):
        self.assertIdentifies(
            "5HueCGU8rMjxEXxiPuD5BDku4MkFqeZyd4dZ1jvhTVqvbTLvyTJ", "uncompressed")

    def test_wif_private_key_compressed(self):
        self.assertIdentifies(
            "L4rK1yDtCWekvXuE6oXD9jCYfFNV2cWQpVMa3J1zMBRwFo2iLwvE", "compressed")

    def test_bip32_extended_key(self):
        self.assertIdentifies(
            "xpub661MyMwAqRbcFtXgS5sYJABqqG9YLmC4Q1Rdap9gSE8NqtwybGhePY2gZ29ESFjqJoCu1"
            "Rupje8YtGqsefD265TMg7usUDFdp6W1EGMcet8", "BIP32")

    # --- inputs that must NOT be identified ------------------------------

    def test_base58_excludes_zero(self):
        # Base58 has no 0, O, I or l, so this cannot be an address
        self.assertUnknown("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfN0")

    def test_garbage_is_unknown(self):
        self.assertUnknown("hello-world-this-is-not-a-hash")

    def test_empty_is_unknown(self):
        self.assertUnknown("")

    def test_bigcrypt_is_not_reported_for_every_long_hash(self):
        # BigCrypt hashes are 13 + 11n characters; before this was bounded it
        # matched any long alphanumeric string and so was reported for nearly
        # every hash the tool identified
        for value in ("5f4dcc3b5aa765d61d8327deb882cf99",
                      "5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8",
                      "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"):
            self.assertNotIn("BigCrypt", self.modes(value))

    def test_bigcrypt_still_matches_a_real_bigcrypt_hash(self):
        self.assertIdentifies("QRD5eLLCFPhAkzOuruJ2op9G", "BigCrypt")


if __name__ == "__main__":
    unittest.main()
