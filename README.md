# pronunciation_dict_parser

## Usage

```py
import logging
from pronunciation_dict_parser import parse_public_dict, PublicDictType, get_occurring_symbols

# adjust log level (optional)
logging.basicConfig()
logging.getLogger("pronunciation_dict_parser.parser").setLevel(logging.INFO)

pronunciations = parse_public_dict(PublicDictType.CMU_ARPA)
pronunciations = parse_public_dict(PublicDictType.LIBRISPEECH_ARPA)
pronunciations = parse_public_dict(PublicDictType.MFA_ARPA)
pronunciations = parse_public_dict(PublicDictType.MFA_EN_UK_IPA)
pronunciations = parse_public_dict(PublicDictType.MFA_EN_US_IPA)

symbols = get_occurring_symbols(pronunciations)
```

## Methods

- Download public dictionary
- Format file
- Replace symbols from words/pronunciations (removing is possible)
- Print statistics
  - Occurring symbols
  - Words count
- Remove alternative pronunciations
- Get pronunciations for word
- Merge dictionaries into one (all need to have the same format)
