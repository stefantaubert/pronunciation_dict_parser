from pronunciation_dict_parser.parser import PronunciationDict, parse_url


def parse_cmu() -> PronunciationDict:
  return parse_url(
    url="http://svn.code.sf.net/p/cmusphinx/code/trunk/cmudict/cmudict-0.7b",
    encoding="ISO-8859-1",
  )


def parse_librispeech() -> PronunciationDict:
  return parse_url(
    url="https://www.openslr.org/resources/11/librispeech-lexicon.txt",
    encoding="UTF-8",
  )
