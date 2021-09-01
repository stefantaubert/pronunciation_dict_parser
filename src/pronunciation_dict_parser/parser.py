import logging
import re
from collections import OrderedDict
from logging import getLogger
from pathlib import Path
from typing import Dict, List, Optional
from typing import OrderedDict as OrderedDictType
from typing import Set, Tuple
from urllib.request import urlopen

from ordered_set import OrderedSet
from tqdm import tqdm

Word = str
Symbol = str
Pronunciation = Tuple[Symbol, ...]
Pronunciations = OrderedSet[Pronunciation]
PronunciationDict = OrderedDictType[Word, Pronunciations]

alternative_pronunciation_indicator_pattern = re.compile(r"\([0-9]+\)")
word_pronunciation_pattern = re.compile(r"([^\s]*)\s*(.*)")
symbol_separator_pattern = re.compile(r"\s")


def parse_url(url: str, encoding: str = "UTF-8") -> PronunciationDict:
  logger = getLogger(__name__)
  logger.info("Downloading dictionary content...")
  lines = _read_url_lines(url, encoding)
  logger.info("Parsing content...")
  resulting_dict = parse_lines(lines)
  logger.info("Done.")
  logger.info(f"Dictionary entries: {len(resulting_dict)}")
  return resulting_dict


def parse_file(path: Path, encoding: Optional[str] = "UTF-8") -> PronunciationDict:
  logger = getLogger(__name__)
  if path is None or not path.exists():
    raise Exception()
  logger.info("Loading dictionary file...")
  lines = _read_lines(path, encoding)
  logger.info("Parsing file...")
  resulting_dict = parse_lines(lines)
  logger.info("Done.")
  logger.info(f"Dictionary entries: {len(resulting_dict)}")
  return resulting_dict


def get_occurring_symbols(dictionary: PronunciationDict) -> Set[Symbol]:
  assert isinstance(dictionary, dict)
  all_symbols: Set[Symbol] = {
    symbol
      for pronunciations in dictionary.values()
      for pronunciation in pronunciations
      for symbol in pronunciation
  }
  return all_symbols


def _read_url_lines(url: str, encoding: str):
  url_content: List[bytes] = urlopen(url)
  result = [line.decode(encoding) for line in url_content]
  return result


def _read_lines(file: Path, encoding: Optional[str]) -> List[str]:
  with file.open(encoding=encoding) as f:
    return f.readlines()


def parse_lines(lines: List[str]) -> PronunciationDict:
  result: PronunciationDict = OrderedDict()
  logger = getLogger(__name__)
  use_tqdm = logger.level <= logging.INFO
  data = tqdm(lines) if use_tqdm else lines
  for line_nr, line in enumerate(data, start=1):
    line_should_be_processed = _line_should_be_processed(line, line_nr)

    if line_should_be_processed:
      _process_line(line, result, line_nr)

  return result


def _process_line(line: str, dictionary: PronunciationDict, line_nr: int) -> None:
  logger = getLogger(__name__)
  word, pronunciation_arpa = _get_word_and_pronunciation(line)
  word_upper = word.upper()

  if word_upper not in dictionary:
    dictionary[word_upper] = OrderedSet()

  already_contained = pronunciation_arpa in dictionary[word_upper]
  if already_contained:
    logger.warning(
      f"Line {line_nr}: For word \"{word}\" the same pronunciation \"{' '.join(list(pronunciation_arpa))}\" exists multiple times!")
  else:
    dictionary[word_upper].add(pronunciation_arpa)


def _get_word_and_pronunciation(line: str) -> Tuple[Word, Pronunciation]:
  line = line.strip()
  word_str, pronunciation_str = split_word_pronunciation(line)
  word_str = _remove_double_indicators(word_str)
  pronunciation: Pronunciation = tuple(re.split(symbol_separator_pattern, pronunciation_str))

  return word_str, pronunciation


def split_word_pronunciation(line: str) -> Tuple[Word, str]:
  res = re.match(word_pronunciation_pattern, line)
  if res is None:
    raise Exception()

  word = res.group(1)
  pronunciation_str = res.group(2)
  return word, pronunciation_str


def _remove_double_indicators(word: Word) -> Word:
  ''' example: ABBE(1) => ABBE '''
  result = re.sub(alternative_pronunciation_indicator_pattern, '', word)

  return result


def _line_should_be_processed(line: str, line_nr: int) -> bool:
  logger = getLogger(__name__)
  is_empty = len(line) == 0
  if is_empty:
    logger.info(f"Line {line_nr}: Ignoring empty line.")
    return False

  is_comment = line.startswith(";;;")
  if is_comment:
    stripped_line = line.strip("\n")
    logger.info(f"Line {line_nr}: Ignoring comment -> \"{stripped_line}\"")
    return False

  return True
