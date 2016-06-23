import os, datetime, time

os.chdir('/Users/lijing211574/PycharmProjects/myspider/myspider/Request/output')
strn = datetime.datetime.now().strftime('%Y-%m-%d_%H_%M')
# command0 = "scrapy crawl zjHWApp -o zjHWApp_" + strn + ".csv"
# return_code0 = os.system(command0)
# print 'Exported Spider: zjHWApp results in CSV'
# print '=======================>'


command1 = "scrapy crawl bjevent -o bjevent_" + strn + ".csv"
return_code1 = os.system(command1)
print 'Exported Spider: bjevent results in CSV'
print '=======================>'

command2 = "scrapy crawl bjevent2 -o bjevent2_" + strn + ".csv"
return_code2 = os.system(command2)
print 'Exported Spider: bjevent2 results in CSV'
print '=======================>'
