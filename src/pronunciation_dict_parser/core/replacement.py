
from typing import List, Optional

from pronunciation_dict_parser.core.types import PronunciationDict, Symbol


def replace_symbols(dictionary: PronunciationDict, symbols: List[Symbol], replace_with: Optional[Symbol], in_words: bool, in_pronunciations: bool, empty_symbol: Symbol) -> None:
  assert in_words or in_pronunciations
  for entry in dictionary.items():
    pass
