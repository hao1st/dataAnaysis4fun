from fun.stock_insider.insider_trading_svc import InsiderTradingService

if __name__ == '__main__':
    insiderTradingSvc = InsiderTradingService()
    insiderTradingSvc.loadData()
    while True:
        symbol = input("Symbol: ")
        if symbol == 'x':
            break
        insiderTradingSvc.symbol = symbol
        insiderTradingSvc.query()

    print("end")
