import argparse
import os
import sys

from loguru import logger

from poe_ritual_parser.parser import RitualLogParser

ITEM_TYPES: list[str] = [
    "rare",
    "unique",
]


def print_found(found: list) -> None:
    # TODO: Implement this
    pass


def main() -> None:
    logger.remove()
    logger.add(
        sys.stdout,
        format="{time:YYYY-MM-DD HH:mm:ss} | <level>{level:7s}</level> | {message}",
        level="DEBUG",
        colorize=True,
    )

    parser = argparse.ArgumentParser()
    parser.add_argument("--log", "-l", type=str, help="Path to the log file")
    parser.add_argument(
        "--class",
        "-c",
        dest="item_class",
        type=str,
        help="Item class to display",
    )
    parser.add_argument(
        "--rarity", "-r", type=str, help="Item rarity to display", choices=ITEM_TYPES
    )

    args = parser.parse_args()

    if not os.path.exists(args.log):
        print("File '{args.log}' doesn't exist")
        return

    log_parser = RitualLogParser(args.log)
    found = log_parser.filter(args.item_class, args.rarity)
    print_found(found)


if __name__ == "__main__":
    main()
