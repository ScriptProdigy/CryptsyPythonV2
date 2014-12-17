CryptsyPythonV2
===============

Python Library for Cryptsy's V2 API


Requirements
============
* Tested in Python 2.7
* requests lib. (http://docs.python-requests.org/en/latest/)

Examples
========
Print Last Hours Worth of OHLC
```python
from Cryptsy import Cryptsy
from pprint import pprint
import time

c = Cryptsy("", "")
ohlc = c.market_ohlc(132, start=0, stop=time.time(), interval="minute", limit=60)
pprint(ohlc)
```


List Currencies
```python
from Cryptsy import Cryptsy
from pprint import pprint

c = Cryptsy("", "")
currencies = c.currencies()
pprint(currencies)
```


Create Converter Quote with 2% fee.
```python
from Cryptsy import Cryptsy
from pprint import pprint

c = Cryptsy("", "")
quote = c.convert_create(3, 132, sendingamount=1, tradekey="", feepercent=2)
pprint(quote)
```
