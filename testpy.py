domain_bj = "http://www.stc.gov.cn/./201606/t20160603_55739.html"
basic_url = 'http://www.stc.gov.cn/ZWGK/TZGG/GGJG/index'
lastpage = 5
start_urls = [basic_url+ '.html']
for p in range(1, lastpage + 1,1):
    start_urls.append(basic_url + str(p) + '.html')

print basic_url.replace('/index','/')