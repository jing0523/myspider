from scrapy import cmdline
import datetime,time
cmd = ''
tmptime = datetime.date.today().strftime('%Y%m%d')
# cmd += 'scrapy crawl bj1 -o bj_data_'+tmptime + '.csv'
cmd += 'scrapy crawl bj2 -o bj_data2_'+tmptime + '.csv'
# cmd += 'scrapy crawl sz1 -o sz_data_'+tmptime + '.csv'

cmdline.execute(cmd.split())

# cmdline.execute('scrapy crawl sz1 -o sz_data_'+tmptime + '.csv')