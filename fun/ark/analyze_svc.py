# https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html
import pandas as pd

from fun.ark.download_svc import DownloadService, urlTable

class AnalyzeService(DownloadService):
    def compareData(self):
        print("fromDate: %s, toDate: %s" % (self.fromDate, self.toDate))
        currPath = '{0}/{1}'.format(self.srcHomePath, self.toDate)
        prevPath = '{0}/{1}'.format(self.srcHomePath, self.fromDate)
        cols = ['company','ticker','shares','market value ($)','weight (%)']
        colNames = ['ticker', 'shares0','market value 0 ($)','weight 0 (%)']
        for url in urlTable:
            print("Fund %s:" % url)
            currfile = '{0}/{1}.csv'.format(currPath, url[1])
            currDF = pd.read_csv(currfile, index_col=0, usecols=cols)
            prevfile = '{0}/{1}.csv'.format(prevPath, url[1])
            prevDF = pd.read_csv(prevfile, index_col=0, usecols=cols)

            currDF = currDF.rename(columns={currDF.columns[0]: 't', currDF.columns[1]: 's', currDF.columns[2]: 'm', currDF.columns[3]: 'w'},  errors="raise")
            prevDF = prevDF.rename(columns={prevDF.columns[0]: 't0', prevDF.columns[1]: 's0', prevDF.columns[2]: 'm0', prevDF.columns[3]: 'w0'},  errors="raise")
            #currDF = currDF[cols]
            #prevDF = prevDF[cols]
            df = [currDF, prevDF]
            mergedDF = pd.concat(df, axis=1)

            companies = []
            symbols = []
            deltas = []
            shares = []
            prices = []
            for i, row in mergedDF.iterrows():
                currT = row['t']
                prevT = row['t0']
                currS = 0 if pd.isna(row['s']) else int(row['s'].replace(',', ''))
                prevS = 0 if pd.isna(row['s0']) else int(row['s0'].replace(',', ''))
                sdiff = currS - prevS
                currM = 0 if pd.isna(row['m']) else float(row['m'].replace(',', '').replace('$', ''))
                prevM = 0 if pd.isna(row['m0']) else float(row['m0'].replace(',', '').replace('$', ''))
                pricePerShare = 0 if currS <= 0 else currM / currS
                companies.append(i)
                symbols.append(currT)
                deltas.append(sdiff)
                shares.append(currS)
                prices.append(pricePerShare)

                #print("%s: diff: %d, share: %d, price per share: %f" % (i, sdiff, currS, pricePerShare))

            myDF = pd.DataFrame({'symbol': symbols, 'delta': deltas, 'share': shares, 'price': prices})
            myDF = myDF.sort_values(by=['delta', 'symbol'], axis=0, ascending=[False, True], inplace=False,
                             kind='quicksort', ignore_index=True, key=None)

            print(myDF)
            print("pause")
