import json
import pandas as pd
from os import listdir, makedirs, rename
from os.path import exists, isdir, isfile, join
from pathlib import Path

import requests

hdr = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
    "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6ImNkODUxOGFlMmVmMDI2NDNiYjgzYTgyZTI2ZGYwMTZlNmM2Yzk5YTNiNGM5NGU3YmU5M2FmNGE2ODZmODAxNmM2ZjgxZGFiZTRiMmJmYjY2In0.eyJhdWQiOiIyIiwianRpIjoiY2Q4NTE4YWUyZWYwMjY0M2JiODNhODJlMjZkZjAxNmU2YzZjOTlhM2I0Yzk0ZTdiZTkzYWY0YTY4NmY4MDE2YzZmODFkYWJlNGIyYmZiNjYiLCJpYXQiOjE2NjQ1NDQyNzAsIm5iZiI6MTY2NDU0NDI3MCwiZXhwIjoxNjc0OTEyMjY3LCJzdWIiOiIiLCJzY29wZXMiOltdfQ.LS04ogwNgH_6YEZrRQNJlP71RpUbLIox0byUPT4f9O6JvRls9SY8lIXsjxn9O7WER98vDRtzfIhn6TN81BZdDCFGJ0ti0Rv58OT378nQUCnStFHsHRwQKTB4JXylbBfVevjfmQT3ks8mJ1URE8DgANTHG2VjClFfLLSbvPKpsEM2B5tOJ___a3V5uNR9i5s45rl1WmIWoSaVFs9-c7cNiHVRfpaObbWeCqNQ04fLQBZCy0Xpiq64HVsF5419paiGvotpDYJEvZeQCSZ0q1iHKQvNO-5T9VjVcy7BV3MJunKdKRldoVHccVRoqkedpTgBx0CheKF8UtKeO5K9vjHTBYR_loIF8Bnu7W7k_qihF3hJYooy6wD4hAhug6g_vqzlVYZMmlPfshetyRDmh_L8HXHlf8LEx4qYK3vton5dPBF9wsziCKSQJIDY3wDi0vJI6ukwIWCaGxtS_rZN2vTM51rvuKXve6Bnj0iDxiTfsurxcl0p_qzWkqSjkiiYBAq0z154O_FUv0iYdOvWMZLjA5gdOK5ovCRi565ChaE_qs6EiSeEPHRxrgav1Lt8oysM2mIm-5OiYYhMe8L7qgkZtnzOhunkDPzpMW9cOj8fgX6NIKIy8Il7Fp_TNTPjOpA1m-zn_pVxQfEfbpooJiiGXF35P5U62lp2VH8rDwU7gME",
    "signature": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2NjcyNDY4MDMsImNsaWVudF90aW1lIjoxNjY3MjQ2ODAzLCJ1cmwiOiIvX2FwaS9pbnNpZGVyL2luc2lkZXJfc3VtbWFyeS9kYXRhIiwic2VydmVyX3RpbWUiOjE2NjcyNDY3NzksImV4cCI6MTY2NzI1MDQwM30.-zmb_oetrMxbdRedv3Wj_PiqK2okk7L-ufSS9x1l-hE"
}

class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

# https://www.marketbeat.com/stocks/NYSE/SKLZ/insider-trades/
# https://www.insidertrades.com/trades/buying/
# https://www.insidertrades.com/trades/selling/
# url="https://www.gurufocus.com/insider/summary"
url = "https://www.gurufocus.com/reader/_api/insider/insider_summary/data"

class InsiderTradingService():
    def __init__(self, fromDate=None, toDate=None, symbol=None):
        self.fromDate = fromDate
        self.toDate = toDate
        self.symbol = symbol
        self.dtBuyAll = None
        self.dtSellAll = None

    def startDownload(self):
        with requests.Session() as s:
            for page in range(21, 22):
                reqJosn = {
                    "filters": [],
                    "insider_filters": [
                        {
                            "left": "trans_share",
                            "operator": ">=",
                            "right": "100"
                        },
                        {
                            "left": "date",
                            "operator": ">",
                            "right": self.fromDate
                        },
                        {
                            "left": "date",
                            "operator": "<",
                            "right": self.toDate
                        }
                    ],
                    "guru_filters": [],
                    "inst_holding_filters": [],
                    "page": page,
                    "sort": "date|desc",
                    "per_page": 40,
                    "exchanges": [
                        "AMEX",
                        "ARCA",
                        "BATS",
                        "GREY",
                        "IEXG",
                        "NAS",
                        "NYSE",
                        "OTCBB",
                        "OTCPK"
                    ]
                }
                download = s.post(url, headers=hdr, json=reqJosn)
                content = download.content.decode('utf-8')
                print(content)

                folderpath = '{0}/stock/insiders/{1}'.format(Path.home(), self.fromDate)
                if not exists(folderpath):
                    makedirs(folderpath)
                filepath = '{0}/{1}.json'.format(folderpath, page)
                if not exists(filepath):
                    with open(filepath, 'w') as f:
                        f.write(content)

    def rename(self):
        folderpath = '{0}/stock/insiders/{1}'.format(Path.home(), self.fromDate)
        files = [f for f in listdir(folderpath) if f.endswith('.json') and isfile(join(folderpath, f))]
        for f in files:
            oldfile = '{0}/stock/insiders/{1}/{2}'.format(Path.home(), self.fromDate, f)
            newfile = '{0}/stock/insiders/{1}/{2}'.format(Path.home(), self.fromDate, f[11:])
            rename(oldfile, newfile)

    def writeBuySellResults(self):
        dtCurr = None
        for page in range(1, 22):
            folderpath = '{0}/stock/insiders/{1}'.format(Path.home(), self.fromDate)
            filepath = '{0}/{1}.json'.format(folderpath, page)
            if exists(filepath):
                tmpJson = json.load(open(filepath))
                data = tmpJson['data']
                dfTmp = pd.json_normalize(data)
                if dtCurr is None:
                    dtCurr = dfTmp
                else:
                    dtCurr = dtCurr.append(dfTmp)
                # print(dtCurr)
                # if dtPrev is not None:
                #     dtCurr = pd.concat([dtPrev, dtCurr], ignore_index=True)
                # dtPrev = dtCurr
        # print(dtCurr)
        dtNew = dtCurr.filter(
            items=['symbol', 'company', 'name', 'position', 'date', 'type', 'trans_share', 'trade_price',
                   'final_share'])
        dtNew = dtNew.sort_values(by=['symbol', 'date'], axis=0, ascending=[True, True], inplace=False,
                                  kind='quicksort', ignore_index=True, key=None)

        buyDF = dtNew.loc[dtNew['type'] == 'P']
        buyDF = buyDF.filter(
            items=['symbol', 'company', 'name', 'position', 'date', 'trans_share', 'trade_price', 'final_share'])
        sellDF = dtNew.loc[dtNew['type'] == 'S']
        sellDF = sellDF.filter(
            items=['symbol', 'company', 'name', 'position', 'date', 'trans_share', 'trade_price', 'final_share'])
        # result = dtCurr.to_json(orient='records')
        # parsed = json.loads(result)
        # print(json.dumps(parsed, indent=2))
        buyCsvFile = '{0}/insiderBuy.csv'.format(folderpath, page)
        ret = buyDF.to_csv(buyCsvFile, index=False)

        sellCsvFile = '{0}/insiderSell.csv'.format(folderpath, page)
        ret = sellDF.to_csv(sellCsvFile, index=False)
        print(ret)

    def loadData(self):
        folderpath = '{0}/stock/insiders'.format(Path.home())
        subfolders = [f for f in listdir(folderpath) if isdir(join(folderpath, f))]
        subfolders.sort()
        for d in subfolders:
            buyfile = '{0}/stock/insiders/{1}/insiderBuy.csv'.format(Path.home(), d)
            if exists(buyfile):
                dfBuy = pd.read_csv(buyfile)
                if self.dtBuyAll is None:
                    self.dtBuyAll = dfBuy
                else:
                    self.dtBuyAll = self.dtBuyAll.append(dfBuy)

            sellfile = '{0}/stock/insiders/{1}/insiderSell.csv'.format(Path.home(), d)
            if exists(sellfile):
                dfSell = pd.read_csv(sellfile)
                if self.dtSellAll is None:
                    self.dtSellAll = dfSell
                else:
                    self.dtSellAll = self.dtSellAll.append(dfSell)

        self.dtBuyAll = self.dtBuyAll.sort_values(by=['symbol', 'date'], axis=0, ascending=[True, True], inplace=False,
                                                  kind='quicksort', ignore_index=True, key=None)

    def query(self):
        buyRes = self.dtBuyAll.query('symbol==@self.symbol')
        # buyRes = buyRes.sort_values(by=['date'], axis=0, ascending=[True], inplace=False,
        #                             kind='quicksort', ignore_index=True, key=None)
        #print("%s" % self.symbol)
        if buyRes.empty:
            print(color.BOLD + "NO BOUGHT" + color.END)
        else:
            print(color.BOLD + color.GREEN + "BOUGHT" + color.END)
            # The scope of these changes made to
            # pandas settings are local to with statement.
            # with pd.option_context('display.max_rows', None,
            #                        'display.max_columns', None,
            #                        'display.precision', 3,
            #                        ):
            print(buyRes.to_string(index=False))


        # self.dtSellAll = self.dtSellAll.sort_values(by=['date'], axis=0, ascending=[True], inplace=False,
        #                                 kind='quicksort', ignore_index=True, key=None)

        sellRes = self.dtSellAll.query('symbol==@self.symbol')
        if sellRes.empty:
            print(color.BOLD + "NO SOLD" + color.END)
        else:
            print(color.BOLD + color.RED + "SOLD" +  color.END)
            print(sellRes.to_string(index=False))
