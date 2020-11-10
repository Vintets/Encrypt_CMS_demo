#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import os.path
import ConfigParser


# работа с файлами ini
class Ini():
    def __init__(self, filename):
        self.filename = filename
        self.rewrite = False
        self.parser = ConfigParser.RawConfigParser()
        self.read_ini()
        time.sleep(0.06)

    def new_ini(self):
        with open(self.filename, 'w') as f:
            text = u''
            # text = u'[default]\n\n'
            f.write(text.encode('UTF-8'))
        time.sleep(0.06)

    def read_ini(self):
        if not os.path.isfile(self.filename):
            self.new_ini()
        # while (time.time() - os.path.getatime(self.filename)) < 0.06:
            # time.sleep(0.02)
            # print u'Файл {} занят! {:.17}'.format(self.filename, time.time() - os.path.getatime(self.filename))
        # with open(self.filename, 'r') as f:
            # f.read()
        self.parser.read(self.filename)
        self.rewrite = False

    def set_name_section(self, section):
        if self.parser.has_section(section):
            self.sect = section
            return True
        return False

    def set_name_section_or_add(self, section):
        self.sect = section
        if not self.parser.has_section(section):
            self.add_section(section)

    def work_section(self):
        return self.sect

    def get_sections(self):
        return self.parser.sections()

    def get_param(self, param):
        if param in self.parser.options(self.sect):
            return self.parser.get(self.sect, param).decode('utf-8')
        return None

    def get_boolean_param(self, param):
        if param in self.parser.options(self.sect):
            return self.parser.getboolean(self.sect, param)
        return None

    def get_allparam(self):
        return self.parser.items(self.sect)

    def set_param(self, param, value):
        self.parser.set(self.sect, param, value.encode('utf-8'))
        self.rewrite = True

    def set_param_dict(self, dict):
        for key in dict.keys():
            dat = self.get_param(key)
            if dat and (dat == str(dict[key])): continue
            self.rewrite = True
            self.parser.set(self.sect, key, dict[key])

    def add_section(self, param):
        try:
            self.parser.add_section(param)
            self.rewrite = True
        except ConfigParser.DuplicateSectionError:
            # print u"Секция '%s' уже есть" % param
            pass
        except:
            print u"Не смог записать секцию '%s' в файл" % param

    def remove_option(self, param):
        self.parser.remove_option(self.sect, param)
        self.rewrite = True

    def remove_section(self, param):
        self.parser.remove_section(self.sect, param)
        self.rewrite = True

    def save(self):
        if self.rewrite:
            with open(self.filename, 'w') as fp:
                self.parser.write(fp)
            self.rewrite = False

    def print_ini(self):
        for sec in self.get_sections():
            self.set_name_section(sec)
            print sec
            print self.get_allparam()


if __name__ == '__main__':
    actor_1 = Ini() # инициация класса

    # raw_input('---------------   END   ---------------')

    # filter(lambda s: s != 'global_settings', self.parser.sections())

    # try:
    # except ConfigParser.NoOptionError:
    # except ConfigParser.NoSectionError:
    # except ConfigParser.DuplicateSectionError

    # .getfloat
    # .getint
    # .getboolean

