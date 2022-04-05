import re
from collections import OrderedDict
from functools import partial
from logging import getLogger
from multiprocessing.pool import Pool
from pathlib import Path
from typing import List, Optional, Set, Tuple
from urllib.request import urlopen

from ordered_set import OrderedSet
from tqdm import tqdm

from pronunciation_dict_parser.types import (Pronunciation, PronunciationDict,
                                             Symbol, Word)


def get_dict_from_file(path: Path, encoding: str, consider_comments: bool, consider_word_nrs: bool, consider_pronunciation_comments: bool, n_jobs, maxtasksperchild: Optional[int], chunksize: int) -> PronunciationDict:
  lines = read_lines_from_file(path, encoding)
  result = get_dict_from_lines(lines, consider_comments, consider_word_nrs,
                               consider_pronunciation_comments, n_jobs, maxtasksperchild, chunksize)
  return result


def get_dict_from_url(url: Path, encoding: str, consider_comments: bool, consider_word_nrs: bool, consider_pronunciation_comments: bool, n_jobs, maxtasksperchild: Optional[int], chunksize: int) -> PronunciationDict:
  lines = read_lines_from_url(url, encoding)
  result = get_dict_from_lines(lines, consider_comments, consider_word_nrs,
                               consider_pronunciation_comments, n_jobs, maxtasksperchild, chunksize)
  return result


def read_lines_from_url(url: str, encoding: str) -> Optional[List[str]]:
  try:
    with urlopen(url) as url_content:
      result = [line.decode(encoding) for line in url_content]
  except Exception as ex:
    logger = getLogger(__name__)
    logger.error("Url couldn't be loaded!")
    return None
  return result


def read_lines_from_file(path: Path, encoding: str) -> Optional[List[str]]:
  try:
    text = path.read_text(encoding)
  except Exception as ex:
    logger = getLogger(__name__)
    logger.error("File couldn't be loaded!")
    return None
  result = text.splitlines()
  return result


word_pronunciation_pattern = re.compile(r"([^\s]+)\s+(.+)")
word_alternative_pattern = re.compile(r"(\S+)\([0-9]+\)")
pronunciation_comment_pattern = re.compile(r"(.*\S+)\s+(#.*)")
symbol_separator_pattern = re.compile(r"\s+")


def get_dict_from_lines(lines: List[str], consider_comments: bool, consider_word_nrs: bool, consider_pronunciation_comments: bool, n_jobs, maxtasksperchild: Optional[int], chunksize: int) -> PronunciationDict:
  logger = getLogger(__name__)

  process_method = partial(
    process_get_pronunciation,
    consider_comments=consider_comments,
    consider_pronunciation_comments=consider_pronunciation_comments,
    consider_word_nrs=consider_word_nrs,
  )

  with Pool(
    processes=n_jobs,
    initializer=__init_pool_prepare_cache_mp,
    initargs=(lines,),
    maxtasksperchild=maxtasksperchild,
  ) as pool:
    entries = range(len(lines))
    iterator = pool.imap(process_method, entries, chunksize)
    result = dict(tqdm(iterator, total=len(entries), unit="lines"))

  pronunciation_dict: PronunciationDict = OrderedDict()

  for line_i in range(len(lines)):
    line_nr = line_i + 1
    assert line_i in result
    word, pronunciation, message = result[line_i]
    if message is not None:
      logger.info(f"Line {line_nr}: {message}")
      continue
    assert word is not None
    assert pronunciation is not None
    if word in pronunciation_dict:
      if pronunciation in pronunciation_dict[word]:
        logger.info(
          f"Line {line_nr}: Ignored line because for word \"{word}\" the pronunciation \"{' '.join(pronunciation)}\" was already assigned previously.")
        continue
      pronunciation_dict[word].add(pronunciation)
    else:
      pronunciation_dict[word] = OrderedSet((pronunciation,))

  return pronunciation_dict


process_lines: List[str] = None


def __init_pool_prepare_cache_mp(lines: List[str]) -> None:
  global process_lines
  process_lines = lines


def process_get_pronunciation(line_i: int, consider_comments: bool, consider_word_nrs: bool, consider_pronunciation_comments: bool) -> Tuple[int, Tuple[Optional[Word], Optional[Pronunciation], Optional[str]]]:
  global process_lines
  assert 0 <= line_i < len(process_lines)
  line = process_lines[line_i]

  line = line.strip()
  line_is_empty = line == ""
  if line_is_empty:
    return line_i, None, None, "Ignored empty line."

  if consider_comments:
    is_comment = line.startswith(";;;")
    if is_comment:
      return line_i, None, None, f"Ignored comment -> \"{line}\""

  word_pronun_match = re.fullmatch(word_pronunciation_pattern, line)
  is_invalid_line = word_pronun_match is None
  if is_invalid_line:
    return line_i, None, None, f"Ignored invalid line -> \"{line}\""

  word = word_pronun_match.group(1)
  pronunciation = word_pronun_match.group(2)

  if consider_word_nrs:
    word_nr_match = re.fullmatch(word_alternative_pattern, word)
    has_word_nr = word_nr_match is not None
    if has_word_nr:
      word = word_nr_match.group(1)

  if consider_pronunciation_comments:
    comment_match = re.fullmatch(pronunciation_comment_pattern, pronunciation)
    has_comment = comment_match is not None
    if has_comment:
      pronunciation = comment_match.group(1)

  symbols = re.split(symbol_separator_pattern, pronunciation)
  pronunciation = tuple(symbols)

  return line_i, (word, pronunciation, None)
