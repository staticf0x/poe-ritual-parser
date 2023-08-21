import re

from loguru import logger
from pydantic import ValidationError

from poe_ritual_parser.models import Item

VERSION_REGEX = re.compile(r"Created with RitualReaderv(\d+\.\d+\.\d+)")
COST_REGEX = re.compile(r"Cost: (\d*)")
CLASS_REGEX = re.compile(r"Item Class: ([\w ]*)")
RARITY_REGEX = re.compile(r"Rarity: ([\w]*)")

FilterT = str | None


class RitualLogParser:
    """Parser for Ritual logs."""

    def __init__(self, file: str) -> None:
        self.file = file
        self.items: list[Item] = []
        self.version_str: str = "undefined"
        self.parse()

    def parse(self) -> None:
        """Parse the provided log file into Items."""
        self.items = []

        with open(self.file, encoding="cp1250") as fread:
            item_dict: dict[str, str | int] = {}

            for n, line in enumerate(fread.readlines(), 1):
                if line.startswith("Pos:"):
                    # New item
                    try:
                        item = Item(**item_dict)
                        self.items.append(item)
                        logger.debug("Successfully parsed item")
                    except ValidationError:
                        logger.error("Cannot fully parse item")

                    item_dict = {}

                if m := VERSION_REGEX.search(line):
                    # Log version
                    self.version_str = m.group(1)
                    logger.info("Log version: {}", self.version_str)

                if m := COST_REGEX.search(line):
                    # Item cost
                    try:
                        item_dict["cost"] = int(m.group(1))
                    except ValueError:
                        logger.error(
                            "Cannot parse cost: '{}' on line {}",
                            m.group(1),
                            n,
                        )
                        continue

                if m := CLASS_REGEX.search(line):
                    item_dict["item_class"] = m.group(1)

                if m := RARITY_REGEX.search(line):
                    item_dict["rarity"] = m.group(1)

        logger.success("Loaded {} items", len(self.items))

    def filter(self, item_class: FilterT = None, rarity: FilterT = None) -> list[Item]:
        """Filter found items by class and/or rarity."""
        filtered: list[Item] = self.items[:]

        if item_class is not None:
            filtered = filter(lambda item: item.item_class.lower() == item_class.lower(), filtered)

        if rarity is not None:
            filtered = filter(lambda item: item.rarity.lower() == rarity.lower(), filtered)

        return filtered
