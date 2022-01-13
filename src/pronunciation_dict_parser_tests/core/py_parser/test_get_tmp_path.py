from pathlib import Path

from pronunciation_dict_parser.core.default_parser import (PublicDictType,
                                                           __get_tmp_path)


def test_get_tmp_path_cmu_arpa__returns_correct_path():
  result = __get_tmp_path(PublicDictType.CMU_ARPA)

  assert result == Path("/tmp/PublicDictType.CMU_ARPA.pkl")
