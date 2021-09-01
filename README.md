# pronunciation_dict_parser

```py
import logging
from pronunciation_dict_parser import parse_cmu

# adjust loglevel (optional)
logging.basicConfig()
logging.getLogger("pronunciation_dict_parser.parser").setLevel(logging.INFO)

cmudict = parse_cmu()
```
