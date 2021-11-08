import pickle
import tempfile
from enum import Enum
from pathlib import Path

from pronunciation_dict_parser.parser import PronunciationDict, parse_url


class PublicDictType(Enum):
  CMU_ARPA = 0
  LIBRISPEECH_ARPA = 1
  MFA_ARPA = 2
  MFA_EN_UK_IPA = 3
  MFA_EN_US_IPA = 4
  PROSODYLAB_ARPA = 5

  def get_url(self) -> str:
    if self == PublicDictType.CMU_ARPA:
      return "http://svn.code.sf.net/p/cmusphinx/code/trunk/cmudict/cmudict-0.7b"
    if self == PublicDictType.LIBRISPEECH_ARPA:
      return "https://www.openslr.org/resources/11/librispeech-lexicon.txt"
    if self == PublicDictType.MFA_ARPA:
      return "https://raw.githubusercontent.com/MontrealCorpusTools/mfa-models/main/dictionary/english.dict"
    if self == PublicDictType.MFA_EN_UK_IPA:
      return "https://raw.githubusercontent.com/MontrealCorpusTools/mfa-models/main/dictionary/english_uk_ipa.dict"
    if self == PublicDictType.MFA_EN_US_IPA:
      return "https://raw.githubusercontent.com/MontrealCorpusTools/mfa-models/main/dictionary/english_us_ipa.dict"
    if self == PublicDictType.PROSODYLAB_ARPA:
      return "https://raw.githubusercontent.com/prosodylab/Prosodylab-Aligner/master/eng.dict"
    assert False

  def get_encoding(self) -> str:
    if self == PublicDictType.CMU_ARPA:
      return "ISO-8859-1"
    if self == PublicDictType.LIBRISPEECH_ARPA:
      return "UTF-8"
    if self == PublicDictType.MFA_ARPA:
      return "UTF-8"
    if self == PublicDictType.MFA_EN_UK_IPA:
      return "UTF-8"
    if self == PublicDictType.MFA_EN_US_IPA:
      return "UTF-8"
    if self == PublicDictType.PROSODYLAB_ARPA:
      return "UTF-8"

    assert False


def parse_public_dict(dict_type: PublicDictType) -> PronunciationDict:
  if __dict_is_saved_in_tmp(dict_type):
    return __load_from_temp(dict_type)
  result = __parse_public_dict_from_url(dict_type)
  __save_to_temp(result, dict_type)
  return result


def __parse_public_dict_from_url(public_dict: PublicDictType) -> PronunciationDict:
  return parse_url(
    url=public_dict.get_url(),
    encoding=public_dict.get_encoding(),
  )


def __get_tmp_path(dict_type: PublicDictType) -> Path:
  result = Path(tempfile.gettempdir()) / f"{str(dict_type)}.pkl"
  return result


def __dict_is_saved_in_tmp(dict_type: PublicDictType) -> bool:
  path = __get_tmp_path(dict_type)
  return path.is_file()


def __save_to_temp(pronunciations: PronunciationDict, dict_type: PublicDictType) -> None:
  path = __get_tmp_path(dict_type)
  with open(path, mode="w") as file:
    pickle.dump(pronunciations, file)


def __load_from_temp(dict_type: PublicDictType) -> PronunciationDict:
  path = __get_tmp_path(dict_type)
  assert path.is_file()
  with open(path, mode="r") as file:
    return pickle.load(file)
