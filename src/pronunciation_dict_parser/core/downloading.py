from logging import getLogger

from pronunciation_dict_parser.core.default_parser import (PublicDictType,
                                                           parse_public_dict)
from pronunciation_dict_parser.core.types import PronunciationDict


def download(dictionary: PublicDictType) -> PronunciationDict:
  logger = getLogger(__name__)
  logger.info(f"Downloading {str(dictionary)}...")
  pronunciation_dict = parse_public_dict(dictionary)
  return pronunciation_dict
