import logging
import re
from collections import OrderedDict
from logging import getLogger
from pathlib import Path
from typing import List, Optional, Set, Tuple
from urllib.request import urlopen

from ordered_set import OrderedSet
from tqdm import tqdm

from pronunciation_dict_parser.parser import _read_lines, parse_lines
from pronunciation_dict_parser.types import (Pronunciation, PronunciationDict,
                                             Symbol, Word)


def parse_dictionary_from_txt(path: Path, encoding: str) -> PronunciationDict:
  logger = getLogger(__name__)
  if path is None or not path.exists():
    raise Exception()
  logger.info("Loading dictionary file...")
  lines = _read_lines(path, encoding)
  logger.info("Parsing file...")
  resulting_dict = parse_lines(lines)
  logger.info("Done.")
  logger.info(f"# Dictionary entries: {len(resulting_dict)}")
  return resulting_dict
