# pronunciation_dict_parser

## Usage

```py
import logging
from pronunciation_dict_parser import parse_public_dict, PublicDictType

# adjust log level (optional)
logging.basicConfig()
logging.getLogger("pronunciation_dict_parser.parser").setLevel(logging.INFO)

pronunciations = parse_public_dict(PublicDictType.CMU_ARPA)
pronunciations = parse_public_dict(PublicDictType.LIBRISPEECH_ARPA)
pronunciations = parse_public_dict(PublicDictType.MFA_ARPA)
pronunciations = parse_public_dict(PublicDictType.MFA_EN_UK_IPA)
pronunciations = parse_public_dict(PublicDictType.MFA_EN_US_IPA)
```
