# pronunciation_dict_parser

## Features

### Parsing

- Parsing a dictionary from an URL or File
- Ignore line comments in style `;;; {comment}`
- Ignore pronunciation comments in style `{word} {pronunciation} # {comment}`
- Ignore duplicate pronunciations for the same word
- Ignore empty and invalid lines
- Support for weights in style `{word} {weight} {pronunciation}`
- Ignore pronunciations with a weight of zero
- Support for all whitespace separated pronunciations, e.g., `\t`, `␣`, `␣␣` between word and pronunciation, and between symbols in a pronunciation.
- Support for multiprocessing

## Usage

```py
import logging
from pronunciation_dict_parser import parse_public_dict, PublicDictType, get_occurring_symbols

# adjust log level (optional)
logging.basicConfig()
logging.getLogger("pronunciation_dict_parser.parser").setLevel(logging.INFO)
```
