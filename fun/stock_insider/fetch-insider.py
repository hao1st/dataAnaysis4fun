import argparse

from fun.stock_insider.insider_trading_svc import InsiderTradingService

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--FromDate", help = "From date (YYYY-MM-dd)")
    parser.add_argument("-t", "--ToDate", help = "To date (YYYY-MM-dd)")
    args = parser.parse_args()
    # fromDate = "2019-09-30"
    # toDate = '2020-03-31'
    #fromDate = "2022-09-31"
    #toDate = '2022-10-08'
    #fromDate='2022-10-07'
    #toDate = '2022-10-18'
    fromDate='2022-10-17'
    toDate = '2022-11-01'

    if args.FromDate:
        fromDate = args.FromDate
    print("from date: %s" % fromDate)
    if args.ToDate:
        toDate = args.ToDate
    print("To date: %s" % toDate)

    # df5 = pd.DataFrame([1], index=['a'])
    # print(df5)
    # df6 = pd.DataFrame([2], index=['a'])
    # print(df6)
    # print(pd.concat([df5, df6]))
    # print(pd.concat([df5, df6], verify_integrity=True))

    insiderTradingSvc = InsiderTradingService(fromDate, toDate)
    insiderTradingSvc.startDownload()
    #insiderTradingSvc.writeBuySellResults()

    print("end")