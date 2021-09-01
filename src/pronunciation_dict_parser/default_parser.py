from enum import Enum

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


def parse_public_dict(public_dict: PublicDictType) -> PronunciationDict:
  return parse_url(
    url=public_dict.get_url(),
    encoding=public_dict.get_encoding(),
  )
