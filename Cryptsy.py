import requests
import time
import hmac,hashlib
import logging
import urllib

logging.getLogger("requests").setLevel(logging.NOTSET)

class Cryptsy:
    def __init__(self, PublicKey, PrivateKey, domain="api.cryptsy.com"):
        self.domain = domain
        self.PublicKey = PublicKey
        self.PrivateKey = PrivateKey

    def _query(self, method, id=None, action=None, query=[], get_method="GET"):

        route = "/api/v2/" + method
        if(id != None):
            route = route + "/" + str(id)
            if(action != None):
                route = route + "/" + str(action)

        query.append(('nonce', time.time()))
        queryStr = urllib.urlencode(query)
        link = 'https://' + self.domain + route
        sign = hmac.new(self.PrivateKey.encode('utf-8'),
                        queryStr,
                        hashlib.sha512).hexdigest()
        headers = {'Sign': sign, 'Key': self.PublicKey.encode('utf-8')}

        if(get_method == "PUT"):
            ret = requests.put(link,
                               params=query,
                               headers=headers,
                               verify=False)
        elif(get_method == "DELETE"):
            ret = requests.delete(link,
                                  params=query,
                                  headers=headers,
                                  verify=False)
        elif(get_method == "POST"):
            ret = requests.post(link,
                                params=query,
                                headers=headers,
                                verify=False)
        else:
            ret = requests.get(link,
                               params=query,
                               headers=headers,
                               verify=False)
        print ret.text
        try:
            jsonRet = ret.json()
            return jsonRet
        except ValueError:
            return {"success": False,
                    "error": {"ValueError": ["Could not load json string."]}}


    # Markets
    def markets(self):
        return self._query(method="markets")

    def market(self, id):
        return self._query(method="markets", id=id)

    def market_orderbook(self, id, limit=100, otype="both", mine=False):
        return self._query(method="markets", id=id, action="orderbook",
            query=[("limit", limit), ("type", otype), ("mine", mine)])

    def market_tradehistory(self, id, limit=100, mine=False):
        return self._query(method="markets", id=id, action="tradehistory",
            query=[("limit", limit), ("mine", mine)])

    def market_triggers(self, id, limit=100):
        return self._query(method="markets", id=id, action="triggers",
            query=[("limit", limit)])

    def market_ohlc(self, id, start=0, stop=time.time(),
                                            interval="minute", limit=100):
        intervals = ["minute", "hour", "day"]
        if(interval not in intervals):
            interval = intervals[0]
        return self._query(method="markets",
                           id=id,
                           action="ohlc",
                           query=[("start", start),
                                  ("stop", stop),
                                  ("interval", interval),
                                  ("limit", limit)])


    # Currencies
    def currencies(self):
        return self._query(method="currencies")

    def currency(self, id):
        return self._query(method="currencies", id=id)

    def currency_markets(self, id):
        return self._query(method="currencies", id=id, action="markets")


    # User
    def balances(self, btype="all"):
        return self._query(method="balances", query=[("type", btype)])

    def balance(self, id, btype="all"):
        return self._query(method="balances", id=id, query=[("type", btype)])

    def deposits(self, id=0, limit=100):
        if(id != 0):
            return self._query(method="deposits",
                               id=id,
                               query=[("limit", limit)])
        return self._query(method="deposits", query=[("limit", limit)])

    def withdrawals(self, id=0, limit=100):
        if(id != 0):
            return self._query(method="withdrawals",
                               id=id,
                               query=[("limit", limit)])
        return self._query(method="withdrawals", query=[("limit", limit)])

    def addresses(self):
        return self._query(method="addresses")

    def address(self, id):
        return self._query(method="addresses", id=id)

    def transfers(self, limit=100):
        return self._query(method="transfers", query=[("limit", limit)])


    # Orders
    def order(self, id):
        return self._query(method="order", id=id)

    def order_create(self, marketid, quantity, ordertype, price):
        return self._query(method="order", query=[("quantity", quantity),
                                                    ("ordertype", ordertype),
                                                    ("price", price),
                                                    ("marketid", marketid)],
                                            get_method="POST")

    def order_remove(self, id):
        return self._query(method="order", id=id, get_method="DELETE")


    # Triggers
    def trigger(self, id):
        return self._query(method="trigger", id=id)

    def trigger_create(self, marketid, ordertype, quantity,
                                   comparison, price, orderprice, expires=''):
        return self._query(method="trigger",
                           query=[("marketid", marketid),
                                  ("type", ordertype),
                                  ("quantity", quantity),
                                  ("comparison", comparison),
                                  ("price", price),
                                  ("orderprice", orderprice),
                                  ("expires", expires)],
                           get_method="POST")

    def trigger_remove(self, id):
        return self._query(method="trigger", id=id, get_method="DELETE")


    # Converter
    def convert(self, id):
        return self._query(method="converter", id=id)

    def convert_create(self, fromcurrency, tocurrency, sendingamount=0.0,
                            receivingamount=0.0, tradekey="", feepercent=0.0):
        return self._query(method="converter",
                           query=[("fromcurrency", fromcurrency),
                                  ("tocurrency", tocurrency),
                                  ("sendingamount", sendingamount),
                                  ("receivingamount", receivingamount),
                                  ("tradekey", tradekey),
                                  ("feepercent", feepercent)],
                           get_method="POST")
