# -*- coding: utf-8 -*-

import urllib2
import json, codecs, csv
import datetime
import os, sys

reload(sys)

domain_sh = "http://map.shlzj.sh.cn"
basic_url = 'http://map.shlzj.sh.cn/LuZhengMap/mapwork/queryAllZD?_='

token = '1465354229719'

_url = basic_url + token
_req = urllib2.Request(_url, data=json.dumps([1, 2, 3]), headers={
    'Content-Type': 'application/json'
})
opener = urllib2.build_opener()
f = opener.open(_req)

data = json.loads(f.read())

strn = datetime.datetime.today().strftime('%Y-%m-%d')
outpath = 'output/'
outfile = outpath + 'sh1_roadevent_' + strn + '.csv'
if not os.path.exists(outpath):
    os.mkdir('output')
perpage = 9
fieldnames = ['ID', 'COLLECTDATE', 'EVENTTYPE', 'ROADNAME'
    , 'DIRECTION', 'START_TIME', 'END_TIME', 'CONTENT', 'TITLE', 'REF', 'POSTDATE', 'POSTFROM'
    , '_STATUS']


def calc_page_pos(pageInd):
    return str(pageInd / perpage + 1)


# set rules 2 filter news captured from websites
class content_filter_rules(self):
    def check_status(postdate, plandate):
        from datetime import datetime
        td = datetime.today()
        dt2 = datetime.strptime(postdate, '%Y-%m-%d %H:%M')
        dt3 = datetime.strptime(plandate, '%Y-%m-%d %H:%M')

        if (dt2 < td and dt3 > td):
            return 'ACTIVE'
        return 'OVERDUE'

        # def text_filter(text):
        #     return True


with open(outfile, 'w') as csvf:
    csvwriter = csv.DictWriter(csvf, fieldnames=fieldnames, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csvwriter.writeheader()
    # csvwriter.writerow(fieldnames)
    pdata = data['rows']

    for i in range(0, len(pdata), 1):
        dl = pdata[i]

        rowdict = {el: '' for el in fieldnames}
        # start mapping data

        str_postdate = dl[u'detectionTimeDis']
        str_plandate = dl[u'planTimeDis']

        rowdict['ID'] = dl['id']
        rowdict['COLLECTDATE'] = strn
        rowdict['EVENTTYPE'] = dl[u'stopreason']
        rowdict['ROADNAME'] = dl[u'roadName']
        rowdict['DIRECTION'] = (dl[u'position'] + '_' + dl[u'directionTypeDis']).strip('\r\n\t')
        rowdict['START_TIME'] = ''
        # 发生时间 from describe
        rowdict['END_TIME'] = str_plandate
        rowdict['CONTENT'] = dl[u'describe'].strip().replace('\n', '').replace('\r', '')
        rowdict['TITLE'] = dl[u'title'].strip().replace('\n', '').replace('\r', '')
        # for QC to open to url
        # rowdict['REF'] =  'Navigate to ' + calc_page_pos(i) +  '    page'
        rowdict['REF'] = str(calc_page_pos(i))
        rowdict['POSTDATE'] = str_postdate
        rowdict['POSTFROM'] = u'上海市路政局'
        rowdict['_STATUS'] = content_filter_rules.check_status(str_postdate, str_plandate)

        for key in rowdict:
            rowdict[key] = rowdict[key].encode('utf-8')
            key = key.encode('utf-8')
        # End mapping data and export them to csv

        csvwriter.writerow(rowdict)

print 'Exported'
csvf.close()
