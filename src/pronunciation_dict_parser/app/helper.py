from logging import getLogger
from pathlib import Path

from pronunciation_dict_parser.core.export import to_text
from pronunciation_dict_parser.core.types import PronunciationDict, Symbol


def write_text(path: Path, text: str, encoding: str) -> None:
  assert isinstance(path, Path)
  path.parent.mkdir(parents=True, exist_ok=True)
  with path.open(encoding=encoding, mode="w") as file:
    return file.write(text)


def save_dictionary_as_txt(pronunciation_dict: PronunciationDict, path: Path, encoding: str, word_pronunciation_sep: Symbol, symbol_sep: Symbol, include_counter: bool, only_first_pronunciation: bool, empty_symbol: Symbol) -> None:
  dict_content = to_text(pronunciation_dict, word_pronunciation_sep,
                         symbol_sep, include_counter, only_first_pronunciation, empty_symbol)
  write_text(path, dict_content, encoding)
  logger = getLogger(__name__)
  logger.info(f"Written dictionary to: {path}")
