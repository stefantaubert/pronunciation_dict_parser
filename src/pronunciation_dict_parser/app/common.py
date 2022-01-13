from argparse import ArgumentParser

from pronunciation_dict_parser.app.globals import (ENCODING, PRONUNCIATION_SEP,
                                                   SYMBOL_SEP, UNK_SYMBOL)


def add_default_output_formatting_arguments(parser: ArgumentParser) -> None:
  parser.add_argument("--include-counter", action="store_true",
                      help="include counter for multiple pronunciations per word")
  parser.add_argument("--only-first-pronunciation", action="store_true",
                      help="include only the first pronunciation")
  parser.add_argument("--symbol-sep", type=str, metavar="CHAR",
                      help="separator of symbols", default=SYMBOL_SEP)
  parser.add_argument("--pronunciation-sep", type=str, metavar="CHAR",
                      help="separator of word and pronunciation", default=PRONUNCIATION_SEP)

  parser.add_argument("--empty-symbol", type=str, metavar="CHAR",
                      help="symbol to use if no pronunciation exist", default=UNK_SYMBOL)
  parser.add_argument("--encoding", type=str, metavar="ENCODING",
                      help="encoding", default=ENCODING)


def add_default_input_formatting_arguments(parser: ArgumentParser) -> None:
  parser.add_argument("--have-counter", action="store_true",
                      help="has counter for multiple pronunciations per word")
  parser.add_argument("--symbol-sep", type=str, metavar="CHAR",
                      help="used separator of symbols", default=SYMBOL_SEP)
  parser.add_argument("--pronunciation-sep", type=str, metavar="CHAR",
                      help="used separator of word and pronunciation", default=PRONUNCIATION_SEP)
  parser.add_argument("--empty-symbol", type=str, metavar="CHAR",
                      help="symbol that indicate that no pronunciation exists", default=UNK_SYMBOL)
  parser.add_argument("--encoding", type=str, metavar="ENCODING",
                      help="used encoding", default=ENCODING)
