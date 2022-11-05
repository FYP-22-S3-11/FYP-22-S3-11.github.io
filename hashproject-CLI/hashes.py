#!/usr/bin/python3

import io
import os
import sys
import argparse
import requests
import hashID


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
    url = "https://crytop.appsndevs.com/api/coinDetail/coin/"
    r = requests.get(url + coin)

    outfile.write("Name: " + r.json().get('data').get('name') + "\n")
    outfile.write("Symbol: " + r.json().get('data').get('symbol') + "\n")
    outfile.write("Type of hash: " + r.json().get('data').get('hash') + "\n")
    outfile.write("Last update date: " + r.json().get('data').get('last_update_date') + "\n")
    outfile.write("=====================================================\n")
    outfile.write("Proceed to identify the hash type?\n")
    outfile.write("Press [ENTER] to continue or [CTRL + C] to exit\n")

    if write_out:
        print("Name: " + r.json().get('data').get('name'))
        print("Symbol: " + r.json().get('data').get('symbol'))
        print("Type of hash: " + r.json().get('data').get('hash'))
        print("Last update date: " + r.json().get('data').get('last_update_date'))
        print("=====================================================")
        print("Proceed to identify the hash type?")
        print("Press [ENTER] to continue or [CTRL + C] to exit")

    value = sys.stdin.readline()

    return value == ""

def identify_hash(outfile, HID):
    while True:
        line = input("Hash: ")
        if not line:
            break
        outfile.write(f"Analyzing '{line.strip()}'\n\n")
        write_result(HID.identify_hash(line), outfile)
        sys.stdout.flush()


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
    write_out = False


    if not args.outfile:
        outfile = sys.stdout
    else:
        try:
            write_out = True
        except EnvironmentError:
            parser.error(f"Could not open {args.output}")

    if not args.strings or args.strings[0] == "-":
        if args.coin and not write_out:
            to_identify = get_coin(outfile, args.coin, write_out)

            if to_identify != "":
                identify_hash(outfile, HID)

        elif args.coin and write_out:
            try:
                outfile = io.open(args.outfile, "w", encoding="utf-8")
                to_identify = get_coin(outfile, args.coin, write_out)
                identify_hash(outfile, HID)
                outfile.close()
            except KeyboardInterrupt:
                outfile.close()
                sys.exit(0)
            except EnvironmentError:
                parser.error(f"Could not open {args.output}")

    else:
        for string in args.strings:
            if write_out:
                try:
                    outfile = io.open(args.outfile, "w", encoding="utf-8")
                    line = input("Hash: ")
                    
                    if not line:
                        break
                    
                    outfile.write(f"Analyzing '{line.strip()}'\n\n")
                    write_result(HID.identify_hash(line), outfile)
                    sys.stdout.flush()
                    outfile.close()
                except KeyboardInterrupt:
                    outfile.close()
                    sys.exit(0)
                except EnvironmentError:
                    parser.error(f"Could not open {args.output}")
            else:
                outfile.write(f"\nAnalyzing '{string.strip()}'\n")
                write_result(HID.identify_hash(string), outfile)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
