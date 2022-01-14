from argparse import ArgumentParser
from logging import getLogger
from pathlib import Path
from tempfile import gettempdir

from pronunciation_dict_parser.app.common import \
    add_default_output_formatting_arguments
from pronunciation_dict_parser.app.helper import save_dictionary_as_txt
from pronunciation_dict_parser.core.downloading import download
from pronunciation_dict_parser.core.public_dicts import PublicDictType
from pronunciation_dict_parser.core.types import Symbol


def get_downloading_parser(parser: ArgumentParser):
  parser.description = ""
  default_path = Path(gettempdir()) / "pronunciations.dict"
  parser.add_argument("--path", metavar='PATH', type=Path,
                      help="file where to output pronunciation dictionary", default=default_path)
  parser.add_argument("--dictionary", metavar='TYPE', choices=PublicDictType,
                      type=PublicDictType.__getitem__, default=PublicDictType.MFA_ARPA, help="pronunciation dictionary")
  add_default_output_formatting_arguments(parser)
  parser.add_argument("-o", "--overwrite", action="store_true",
                      help="overwrite file if it exists")
  return app_download


def app_download(path: Path, dictionary: PublicDictType, pronunciation_sep: Symbol, symbol_sep: Symbol, include_counter: bool, only_first_pronunciation: bool, encoding: str, empty_symbol: Symbol, overwrite: bool):
  if not overwrite and path.exists():
    logger = getLogger(__name__)
    logger.error("File already exists!")
    return

  pronunciation_dict = download(dictionary)

  save_dictionary_as_txt(pronunciation_dict, path, encoding, pronunciation_sep,
                         symbol_sep, include_counter, only_first_pronunciation, empty_symbol)

  logger = getLogger(__name__)
  logger.info(f"Written dictionary to: {path}")
