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
        if spider.name == 'bj1':
            self.parser_rules = [
                DateParserRule(pattern=u'决定自[0-9]{4}年([0-9]{1,2}月)?([0-9]{1,2}日)?起，',
                               start_pos=3, end_pos=-2, target='start'),
                DateParserRule(pattern=u'[0-9]{4}年[0-9]{1,2}月[0-9]{1,2}日(起)?至([0-9]{4}年)?([0-9]{1,2}月)?([0-9]{1,2}日)?',
                               start_pos=0, end_pos=10, target='start'),
                DateParserRule(pattern=u'[0-9]{4}年[0-9]{1,2}月[0-9]{1,2}日(起)?至([0-9]{4}年)?([0-9]{1,2}月)?([0-9]{1,2}日)?',
                               start_pos=10, end_pos=-1, target='end'),

            ]
        return self.parser_rules

    def check_fill_st(self, test):
        import re

        utest = unicode(test, 'utf8')
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
        return start_datetime

    def check_fill_ed(self, test):
        import re
        end_datetime = ''
        utest = unicode(test, 'utf8')
        lst_datetime = []
        for rule in [r for r in self.parser_rules if r.target == 'end']:
            p = re.compile(rule.pattern)
            for result in p.finditer(utest):
                t = result.group()
                rule.end_pos = len(t)
                t = t[rule.start_pos:rule.end_pos]
                lst_datetime.append(t)

        lst_datetime = list(set(lst_datetime))
        end_datetime = ';'.join(lst_datetime)  # consider one announcement contains 2+ records
        return end_datetime


class ExportOptions:
    def __init__(self):
        pass
