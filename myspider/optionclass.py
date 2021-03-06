# -*- coding: utf-8 -*-
class DateParserRule(object):
    def __init__(self, pattern, start_pos, end_pos, target):
        '''
        Attributes：-
        pattern                      -str            regex pattern that will be used to find start or end date
        start_pos                    -int            parse position for extract date 'string
        end_pos                      -int            parse position for extract date 'string
        target                       -const          START or END, states that will be used for which fieldname
        '''
        self.pattern = pattern
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.target = target


class DataParser(object):
    '''
        Attributes：-
        parser_rules                 -list<obj>      list of rule object

        Method: -
        setRules                     -obj            return the rules for the specific spider
        check_fill_st                -str            use regex to fiter all event-end datetime
        check_fill_ed                -str            use regex to fiter all event-end datetime

        '''

    def __init__(self):
        self.parser_rules = []

    def setRules(self, spider):
        self.name = spider.name
        if not spider.name:
            return None
        if spider.name in ['bj1', 'sz1', 'nj1']:  # 目前支持通告分析
            self.parser_rules = [
                DateParserRule(pattern=u'决定自[0-9]{4}年([0-9]{1,2}月)?([0-9]{1,2}日)?起，',
                               start_pos=3, end_pos=-2, target='start'),
                DateParserRule(pattern=u'[0-9]{4}年[0-9]{1,2}月[0-9]{1,2}日(起)?至([0-9]{4}年)?([0-9]{1,2}月)?([0-9]{1,2}日)?',
                               start_pos=0, end_pos=9, target='start'),
                DateParserRule(pattern=u'[0-9]{4}年[0-9]{1,2}月[0-9]{1,2}日(起)?至([0-9]{4}年)?([0-9]{1,2}月)?([0-9]{1,2}日)?',
                               start_pos=10, end_pos=-1, target='end'),

            ]
        elif spider.name == 'zjHWApp':
            self.parser_rules = [
                DateParserRule(pattern=u'预计在[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}\s[0-9]{2}\:[0-9]{2}(\:[0-9]{2})?',
                               start_pos=3, end_pos=-2, target='end'),
            ]
        elif spider.name == 'bjevent2':
            self.parser_rules = [
                DateParserRule(pattern=u'预计恢复时间[0-9]{4}年[0-9]{1,2}月[0-9]{1,2}日',
                               start_pos=6, end_pos=-2, target='end'),
            ]

        return self.parser_rules

    def check_fill_st(self, test):
        import re

        if (type(test) is str):
            utest = unicode(test, 'utf8')
        else:
            utest = test
        start_datetime = ''
        lst_datetime = []
        for rule in [r for r in self.parser_rules if r.target == 'start']:
            p = re.compile(rule.pattern)
            for result in p.finditer(utest):
                t = result.group()
                t = t[rule.start_pos:rule.end_pos]
                lst_datetime.append(t)

        lst_datetime = list(set(lst_datetime))
        start_datetime = ';'.join(lst_datetime)
        return start_datetime.encode('utf-8')

    def check_fill_ed(self, test):
        import re
        end_datetime = ''
        if (type(test) is str):
            utest = unicode(test, 'utf8')
        else:
            utest = test
        lst_datetime = []
        for rule in [r for r in self.parser_rules if r.target == 'end']:
            p = re.compile(rule.pattern)
            for result in p.finditer(utest):
                t = result.group()
                rule.end_pos = len(t)
                t = t[rule.start_pos:]
                lst_datetime.append(t)

        lst_datetime = list(set(lst_datetime))
        end_datetime = ';'.join(lst_datetime)  # consider one announcement contains 2+ records
        return end_datetime.encode('utf-8')


class ExportOptions(object):
    '''
        Attributes：-
        activeparser                 -<obj,bool>     default true, will return active flag by comparing occurTime and endTime
        eventType                    -str
        datetimeparser               -<obj,bool>     bool:use parser (start_date?end_date),list of object: DataParser
        hasImg                       -bool           contains supporting doc image or not
        Method: -
        Open_ImgDownload_Channel     -               open imagedownloader to download gif/png/jpeg

        '''
    def __init__(self):
        self.activeparser = None
        self.eventType = ''
        self.datetimeparser = None
        self.hasImg = False

    def Open_ImgDownload_Channel(self):
        self.hasImg = True
        # initialize image downloader

    def Write_Over_End_Date(self):
        # self.datetimeparser =
        pass
