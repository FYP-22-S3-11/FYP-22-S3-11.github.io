#!/usr/bin/python3

import io
import os
import sys
import argparse
from urllib.parse import quote

import requests
import hashID


COIN_API_URL = "https://crytop.appsndevs.com/api/coinDetail/coin/"
COIN_API_TIMEOUT = 15


def write_result(identified_modes, outfile):
    count = 0
    hash_types = ""

    for mode in identified_modes:
        count += 1
        hash_types += f"[+] {mode.name}\n"
    outfile.write(hash_types)

    if count == 0:
        outfile.write("[!] Unknown hash\n")
    return count > 0


def get_coin(outfile, coin, write_out=False):
    # quote() the coin: it is appended straight onto the URL, so an
    # unencoded value such as '../../admin' would address a different
    # endpoint than the one intended.
    url = COIN_API_URL + quote(coin, safe="")

    try:
        r = requests.get(url, timeout=COIN_API_TIMEOUT)
        r.raise_for_status()
        data = r.json().get("data")
    except requests.exceptions.RequestException as err:
        sys.stderr.write(f"[!] Could not reach the coin API: {err}\n")
        return False
    except ValueError:
        sys.stderr.write("[!] Coin API did not return valid JSON\n")
        return False

    if not data:
        sys.stderr.write(f"[!] No coin found for '{coin}'\n")
        return False

    details = (
        "Name: " + str(data.get("name")) + "\n"
        "Symbol: " + str(data.get("symbol")) + "\n"
        "Type of hash: " + str(data.get("hash")) + "\n"
        "Last update date: " + str(data.get("last_update_date")) + "\n"
        "=====================================================\n"
    )
    outfile.write(details)

    if write_out:
        # the details went to the output file, so mirror them to the terminal
        sys.stdout.write(details)

    return True


def identify_hash(outfile, HID):
    while True:
        try:
            line = input("Hash: ")
        except EOFError:
            break
        if not line:
            break
        outfile.write(f"Analyzing '{line.strip()}'\n\n")
        write_result(HID.identify_hash(line), outfile)
        sys.stdout.flush()


def identify_strings(strings, outfile, HID):
    for string in strings:
        outfile.write(f"\nAnalyzing '{string.strip()}'\n")
        write_result(HID.identify_hash(string), outfile)


def main():
    usage = f"{os.path.basename(__file__)} [-h] [-o FILE] [-c COIN] \'INPUT\'"

    parser = argparse.ArgumentParser(
        description="Identify the different types of hashes. Default mode ONLY identifies the hash type and write to stdout",
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
                       help="Type of cryptocurrency coin to search for, returns relevant information about the coin")

    group.add_argument("-h", "--help",
                       action="help",
                       help="Show this help message and exit")

    args = parser.parse_args()
    HID = hashID.HashID()
    write_out = bool(args.outfile)

    if write_out:
        # opened once, not once per input, so several INPUTs no longer
        # truncate each other's results
        try:
            outfile = io.open(args.outfile, "w", encoding="utf-8")
        except EnvironmentError:
            parser.error(f"Could not open {args.outfile}")
    else:
        outfile = sys.stdout

    try:
        if args.coin:
            if not get_coin(outfile, args.coin, write_out):
                return 1
            print("Proceed to identify the hash type?")
            print("Press [ENTER] to continue or [CTRL + C] to exit")
            sys.stdin.readline()

        if args.strings and args.strings[0] != "-":
            identify_strings(args.strings, outfile, HID)
        else:
            identify_hash(outfile, HID)
    except KeyboardInterrupt:
        return 0
    finally:
        if outfile is not sys.stdout:
            outfile.close()

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        pass
