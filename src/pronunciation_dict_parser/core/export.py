from pronunciation_dict_parser.core.parser import PronunciationDict
from pronunciation_dict_parser.core.types import Symbol


def to_text(pronunciation_dict: PronunciationDict, word_pronunciation_sep: Symbol, symbol_sep: Symbol, include_counter: bool, only_first_pronunciation: bool, empty_symbol: Symbol) -> None:
  dict_content = ""
  for word, pronunciations in pronunciation_dict.items():
    for counter, pronunciation in enumerate(pronunciations):
      if len(pronunciation) == 0 and len(empty_symbol) > 0:
        pronunciation = tuple(empty_symbol)
      counter_str = f"({counter})" if include_counter and counter > 0 else ""
      pron = symbol_sep.join(pronunciation)
      line = f"{word}{counter_str}{word_pronunciation_sep}{pron}\n"
      dict_content += line
      if only_first_pronunciation:
        break
  return dict_content
