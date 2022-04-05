import logging
import re
from collections import OrderedDict
from logging import getLogger
from pathlib import Path
from typing import List, Optional, Set, Tuple
from urllib.request import urlopen

from ordered_set import OrderedSet
from tqdm import tqdm

from pronunciation_dict_parser.types import (Pronunciation, PronunciationDict,
                                             Symbol, Word)

alternative_pronunciation_indicator_pattern = re.compile(r"\([0-9]+\)")
word_pronunciation_pattern = re.compile(r"([^\s]+)\s+(.+)")
symbol_separator_pattern = re.compile(r"\s+")


def parse_url(url: str, encoding: str) -> PronunciationDict:
  logger = getLogger(__name__)
  logger.info("Downloading dictionary content...")
  lines = _read_url_lines(url, encoding)
  logger.info("Parsing content...")
  resulting_dict = parse_lines(lines)
  logger.info("Done.")
  logger.info(f"Dictionary entries: {len(resulting_dict)}")
  return resulting_dict


def parse_dictionary_from_txt(path: Path, encoding: str, pronunciation_sep: str = None, symbol_sep: str = None, have_counter: bool = None, empty_symbol: Symbol = None) -> PronunciationDict:
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


def get_occurring_symbols(dictionary: PronunciationDict) -> OrderedSet[Symbol]:
  assert isinstance(dictionary, dict)
  all_symbols: Set[Symbol] = OrderedSet(sorted({
    symbol
      for pronunciations in dictionary.values()
      for pronunciation in pronunciations
      for symbol in pronunciation
  }))
  return all_symbols


def _read_url_lines(url: str, encoding: str) -> List[str]:
  with urlopen(url) as url_content:
    result = [line.decode(encoding) for line in url_content]
  return result


def _read_lines(file: Path, encoding: Optional[str]) -> List[str]:
  assert isinstance(file, Path)
  with file.open(encoding=encoding, mode="r") as f:
    return f.readlines()


def parse_lines(lines: List[str]) -> PronunciationDict:
  result: PronunciationDict = OrderedDict()
  logger = getLogger(__name__)
  use_tqdm = logger.level <= logging.INFO
  data = tqdm(lines) if use_tqdm else lines
  for line_nr, line in enumerate(data, start=1):
    line_should_be_processed = __should_line_be_processed(line, line_nr)

    if line_should_be_processed:
      _process_line(line, result, line_nr)

  return result


def sort_after_words(dictionary: PronunciationDict) -> PronunciationDict:
  result = OrderedDict({k: dictionary[k] for k in sorted(dictionary.keys())})
  return result


def _process_line(line: str, dictionary: PronunciationDict, line_nr: int) -> None:
  logger = getLogger(__name__)
  splitting_result = __try_get_word_and_pronunciation(line)
  if splitting_result is None:
    logger = getLogger(__name__)
    logger.warning(f"Line {line_nr}: Couldn't parse \"{line}\".")
    return None

  word, pronunciation_arpa = splitting_result
  word_upper = word.upper()

  if word_upper not in dictionary:
    dictionary[word_upper] = OrderedSet()

  already_contained = pronunciation_arpa in dictionary[word_upper]
  if already_contained:
    logger.warning(
      f"Line {line_nr}: For word \"{word}\" the same pronunciation \"{' '.join(list(pronunciation_arpa))}\" exists multiple times!")
  else:
    dictionary[word_upper].add(pronunciation_arpa)

  return None


def __try_get_word_and_pronunciation(line: str) -> Optional[Tuple[Word, Pronunciation]]:
  line = line.strip()
  splitting_result = __try_split_word_pronunciation(line)
  if splitting_result is None:
    return None
  word_str, pronunciation_str = splitting_result
  word_str = __remove_double_indicators(word_str)
  pronunciation: Pronunciation = tuple(re.split(symbol_separator_pattern, pronunciation_str))
  return word_str, pronunciation


def __try_split_word_pronunciation(line: str) -> Optional[Tuple[Word, str]]:
  res = re.match(word_pronunciation_pattern, line)
  if res is None:
    return None

  word = res.group(1)
  pronunciation_str = res.group(2)
  return word, pronunciation_str


def __remove_double_indicators(word: Word) -> Word:
  ''' example: ABBE(1) => ABBE '''
  result = re.sub(alternative_pronunciation_indicator_pattern, '', word)

  return result


def __should_line_be_processed(line: str, line_nr: int) -> bool:
  logger = getLogger(__name__)
  is_empty = len(line) == 0
  if is_empty:
    logger.info(f"Line {line_nr}: Ignoring empty line.")
    return False

  is_comment = line.startswith(";;;")
  if is_comment:
    stripped_line = line.strip("\n")
    logger.info(f"Line {line_nr}: Ignoring comment -> \"{stripped_line}\".")
    return False

  return True
