import csv
import os
import re
from datetime import datetime
from os import path
from pathlib import Path

import requests

from fun.ark.ark_action import BaseService

hdr = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}

urlTable = [['https://ark-funds.com/wp-content/uploads/funds-etf-csv/ARK_AUTONOMOUS_TECH._&_ROBOTICS_ETF_ARKQ_HOLDINGS.csv', 'ARKQ'],
       ['https://ark-funds.com/wp-content/uploads/funds-etf-csv/ARK_INNOVATION_ETF_ARKK_HOLDINGS.csv', 'ARKK'],
       ['https://ark-funds.com/wp-content/uploads/funds-etf-csv/ARK_FINTECH_INNOVATION_ETF_ARKF_HOLDINGS.csv', 'ARKF'],
       ['https://ark-funds.com/wp-content/uploads/funds-etf-csv/ARK_NEXT_GENERATION_INTERNET_ETF_ARKW_HOLDINGS.csv', 'ARKW'],
       ['https://ark-funds.com/wp-content/uploads/funds-etf-csv/ARK_GENOMIC_REVOLUTION_ETF_ARKG_HOLDINGS.csv', 'ARKG'],
       ['https://ark-funds.com/wp-content/uploads/funds-etf-csv/ARK_SPACE_EXPLORATION_&_INNOVATION_ETF_ARKX_HOLDINGS.csv', 'ARKX']]

class DownloadService(BaseService):
    def startDownload(self):
        with requests.Session() as s:
            for url in urlTable:
                fundnm = url[1]
                download = s.get(url[0], headers=hdr) #, verify = "/Users/hliu/Documents/CloudflareIncECCCA-3.crt")
                content = download.content.decode('utf-8')
                print(content)

                rows = content.split('\n')
                print(len(rows))

                if len(rows) > 1:
                    currdate = rows[1].split(',')[0]
                    dt = datetime.strptime(currdate, '%m/%d/%Y')
                    dateStr = dt.strftime('%Y-%m-%d')
                    today = datetime.today()
                    if (today.strftime('%Y-%m-%d') != dateStr):
                        print("no download since date mismatch!")
                        return False
                else:
                    continue
                print(dateStr)

                data = []
                for i in range(len(rows) - 2):
                    if i == 0:
                        tmpheader = rows[0].split(',')
                        header = [s.strip('"') for s in tmpheader]
                    else:
                        tmprow = re.split(r',(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)', rows[i])
                        row = [s.strip('"') for s in tmprow]
                        data.append(row)

                folderpath = '{0}/ark/{1}'.format(Path.home(), dateStr)
                if not path.exists(folderpath):
                    os.makedirs(folderpath)
                filepath = '{0}/{1}.csv'.format(folderpath, fundnm)
                with open(filepath, 'w', encoding='UTF8') as f:
                    # create the csv writer
                    writer = csv.writer(f)
                    # write a row to the csv file
                    writer.writerow(header)
                    writer.writerows(data)
            return True
