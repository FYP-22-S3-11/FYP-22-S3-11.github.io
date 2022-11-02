#!/usr/bin/python3

import io
import os
import sys
import argparse
import requests
import hashID


def write_result(identified_modes, outfile):
    """
    Write human-readable output from identify_hash
    """
    count = 0
    hash_types = ""
    for mode in identified_modes:
        count += 1
        hash_types += f"[+] {mode.name}\n"
    outfile.write(hash_types + "\n")
    if count == 0:
        outfile.write("[+] Unknown hash\n")
    return count > 0


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
                       help="Type of cryptocurrency coin to search for, returns [ID], [Name], [Hash Type]")

    group.add_argument("-h", "--help",
                       action="help",
                       help="Show this help message and exit")

    args = parser.parse_args()
    HID = hashID.HashID()

    if not args.outfile:
        outfile = sys.stdout
    else:
        try:
            outfile = io.open(args.outfile, "w", encoding="utf-8")
        except EnvironmentError:
            parser.error(f"Could not open {args.output}")

    if not args.strings or args.strings[0] == "-":
        if args.coin:
            url = "https://crytop.appsndevs.com/api/coinDetail/coin/"
            r = requests.get(url + args.coin)
            print("Id: " + str(r.json().get('data').get('id')))
            print("Name: " + r.json().get('data').get('name'))
            print("Hash: " + r.json().get('data').get('hash'))
            print("=====================================================\n")

        outfile.write("Proceed to identify the hash type?\n")
        outfile.write("Press [ENTER] to continue or [CTRL + C] to exit\n")
        
        if input() == "":
            while True:
                line = input("Hash: ")
                if not line:
                    break
                outfile.write(f"Analyzing '{line.strip()}'\n")
                write_result(HID.identify_hash(line), outfile)
                sys.stdout.flush()
        
    else:
        for string in args.strings:
            if os.path.isfile(string):
                try:
                    with io.open(string, "r", encoding="utf-8") as infile:
                        for line in infile:
                            if line.strip():
                                outfile.write(f"Analyzing '{line.strip()}'\n")
                                write_result(HID.identify_hash(line), outfile)
                except (EnvironmentError, UnicodeDecodeError):
                    sys.stdout.write(f"Could not open {string}")
            else:
                outfile.write(f"Analyzing '{string.strip()}'\n")
                write_result(HID.identify_hash(string), outfile)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
