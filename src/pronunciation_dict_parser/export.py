from pathlib import Path
from typing import Iterable, List, Optional

from pronunciation_dict_parser.parser import PronunciationDict


def __write_text(file: Path, text: str, encoding: Optional[str]) -> None:
  assert isinstance(file, Path)
  with file.open(encoding=encoding, mode="w") as f:
    return f.write(text)


def export(path: Path, pronunciation_dict: PronunciationDict, word_pronunciation_sep: str = "\t", symbol_sep: str = " ", include_counter: bool = True, encoding="UTF-8") -> None:
  dict_content = ""
  for word, pronunciations in pronunciation_dict.items():
    for counter, pronunciation in enumerate(pronunciations):
      counter_str = f"({counter})" if include_counter and counter > 0 else ""
      pron = symbol_sep.join(pronunciation)
      line = f"{word}{counter_str}{word_pronunciation_sep}{pron}\n"
      dict_content += line
  __write_text(path, dict_content, encoding=encoding)
