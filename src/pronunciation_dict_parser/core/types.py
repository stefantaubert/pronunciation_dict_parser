from typing import OrderedDict as OrderedDictType
from typing import Tuple

from ordered_set import OrderedSet

Word = str
Symbol = str
Pronunciation = Tuple[Symbol, ...]
Pronunciations = OrderedSet[Pronunciation]
PronunciationDict = OrderedDictType[Word, Pronunciations]
