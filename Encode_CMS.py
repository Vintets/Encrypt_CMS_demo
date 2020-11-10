#!/usr/bin/env python
# -*- coding: utf-8 -*-

if 'import':
    import os
    import sys
    import time
    import json
    import random
    PATH_SCRIPT = os.path.dirname(os.path.abspath(unicode(sys.argv[0], 'cp1251')))
    sys.path.append(os.path.join(PATH_SCRIPT, 'Libs'))
    from Libs.Generator import Generator as Generator
    from ini import Ini
    import colorprint as cp
    import clear_consol as cc


class GeneralEncoder():
    def __init__(self, fin='',fout='', fcod='cp1251',
                symbols='', length=3, edging='', delspaces=False, delcomments=False,
                levels=1, console=False, statistics=False):
        self.fin = fin
        self.fout = fout
        self.fcod = fcod
        self.symbols = symbols
        self.length = length
        self.edging = edging
        self.delspace = delspaces
        self.delcomment = delcomments
        self.levels = levels
        self.console = console
        self.stat_freq = statistics
        self.files = self._check_files()
        self.ids = []

    @staticmethod
    def authorship():
        NAME = u'--- Encode_CMS ---'
        AUTHOR = u'master by Vint'
        __version__ = u'0.3.0'
        __copyright__ = u'2017 (c)  bitbucket.org/Vintets/encrypt_cms'
        copyright = __copyright__.center(80, ' ')
        version = ('version %s %s' % (__version__, AUTHOR)).center(80, ' ')
        name_product = NAME.center(80, ' ')
        print u'{0}{1}{2}{0}'.format('*'*80, copyright, version)
        print u'{0}\n'.format(name_product)

    def _check_files(self):
        if len(sys.argv) < 2:
            self.internal_error('nofile')
        files = []
        for file in sys.argv[1:]:
            file = unicode(file, 'cp1251')
            if not os.path.isfile(file):
                self.internal_error('noopen', file)
            files.append(file)
        if self.fout in file:
            self.internal_error('already', file)
        return files

    def internal_error(self, what,  *pars):
        ext_sleep = 0
        if what == 'noopen':
            err = u'13Ошибка открытия файла ^15_%s' % pars[0]
        elif what == 'nofile':
            err = u'13Не передали файл параметром!'
        elif what == 'no_ext':
            err = u'13Не определили расширение файла ^15_%s' % pars[0]
        elif what == 'nogenerator':
            err = u'13Не создан генератор (Generator)'
        elif what == 'no_ids':
            err = u'13Закончились сгенерированные последовательности\n'
            err += u'Увеличьте количество символов для генерации\n'
            err += u'Сейчас сгенерировано ^15_%d ^13_последовательностей' % pars[0]
            ext_sleep = 2
        elif what == 'already':
            err = u'13Файл ^15_%s ^13_уже защищён.\nПовторная защита не допускается.' % pars[0]
            ext_sleep = 1
        else:
            cp.cprint(u'12Неизвестная ошибка!')
        cp.cprint(err)
        # cp.cprint(u'14---------------   ^12_ERROR   ^14_---------------')
        # raw_input('---------------   END   ---------------')
        time.sleep(3 + ext_sleep)
        exit(1)

    def create_ids(self, symbols='hbdp', length=8, edging='q'):
        class_gen = Generator(symbols, length, edging)
        # if not isinstance(class_gen, Generator):
            # self.internal_error('nogenerator')
        class_gen.rand_lgen()
        self.ids = class_gen.get_generate()
        print u'Cгенерировано %d ids' % (len(self.ids))
        # print self.ids[:10]
        pass

    def get_ids(self):
        return self.ids

    def run(self):
        self.create_ids(self.symbols, self.length, self.edging)
        len_ids = len(self.ids)
        for filename in self.files:
            cp.cprint(u'1свободных ids: ^15_%d' % (len(self.ids)))
            print
            cp.cprint(u'1Обрабатываем файл:')
            cp.cprint(u'3_%s \n' % filename)
            class_enc = EncoderCMS(filename, self.fin, self.fout, self.fcod,
                                    self.ids, len_ids, self.console)
            self.ids = class_enc.encode_(self.delspace, self.delcomment, 
                                        self.levels, self.stat_freq)
            if self.console:
                print u'\nВернулось %d шт. ids' % len(self.ids)
                print '\n%s' % ('-'*80)
        cp.cprint(u"3Всего затрачено ^15_%d шт. ^3_'ids'\n" % (len_ids - len(self.ids)))


class EncoderCMS(GeneralEncoder):
    def __init__(self, full_filename, fin, fout, fcod, ids, len_ids, console=False):
        self.full_filename = full_filename
        self.del_suffix = fin
        self.fout = fout
        self.fcod = fcod
        self.ids = ids
        self.len_ids = len_ids
        self.console = console
        self.filename_parts = self.get_filename_parts(self.full_filename)
        self.defs = []
        self.percent = [
                {'len':3, 'step':[]},
                {'len':14, 'step':[(42, 75)]},
                {'len':31, 'step':[(18, 35), (58, 85)]},
                {'len':63, 'step':[(10, 18), (28, 40), (55, 65), (80, 90)]},
                {'len':81, 'step':[(7, 15), (25, 37), (47, 57), (67, 77), (85, 95)]}
                ]
        self.dummy = u'FOR(WHILE(GOTOBREAKELSEEND_CYCEND_IFIF(INC(WAIT(WAITMS(ANDORXORPXL(PXLXOR(PXLCRC(PXLCOUNTRND(RNDFROM(FROMCLIP(DIST(HGETTEXT(HGET(SIN(COS(ARCSIN(ARCCOS(SQRT(ROUND(POW(ABS(LCLICK(LDOWN(LUP(RCLICK(RDOWN(RUP(MDOWN(MUP(MCLICK(MOVE(MOVER(DBLCLICK(WHEELDOWN(WHEELUP(KEYDOWN(KEYPRESS(KEYSTRING(KEYUP(IF_KEYDOWN(DEFINE(GETSCREENCOLORMODEHALTIF_PIXEL_IN(IF_PICTURE_IN(EXECUTE(TOCLIP(UNDEFINE(SUBEND_SUBSTRFILTER(STRCUT(STRCUT2(STRPOS(STRLEN(STRCONCAT(STRREPLACE(STRREADLN(STRWRITELN(STRMD5(INT(GETKBLAYOUT(SETKBLAYOUT(TFREADARR(TFWRITEARR(STRSEPARATE(THREAD(END_THREADSETTHREAD(WNDFIND(WNDSIZE(WNDPOS(WNDSTATE(WNDGETINFO(WNDSETINFO(WNDBUMP(POSTMESSAGE(SENDMESSAGE(TFCLEAR(TFREAD(TFWRITE(TFCOUNT(TFDELETE(ISKEYDOWN(INPUTBOX(HTTPGET(HTTPPOST(HINTPOPUP(INIREAD(INIWRITE(SWITCH(END_SWITCHCASE(DEFAULTARRSIZE(ARRPUSH(ARRPOP(SCANPXL(SCANPICTURE(DIALOGBOX('

    def get_filename_parts(self, full_filename):
        file_orig = os.path.split(full_filename)
        path = file_orig[0]
        spl = os.path.splitext(file_orig[1])
        if len(spl) < 2:
            self.internal_error('no_ext', file_orig[1])
            return None
        name = spl[0]
        if name.endswith(self.del_suffix):
            name = name[:-7]
        filename_parts = {
                        'path':path,
                        'name':name,
                        'ext':spl[1]
                        }
        print 'path =', filename_parts['path']
        print 'name =', filename_parts['name']
        print 'ext = ', filename_parts['ext']
        print
        return filename_parts

    def read_file(self):
        with open(self.full_filename, 'r') as fr:
            r_text = fr.read()
        try:
            all_text = textbase = r_text.decode('cp1251')
        except UnicodeDecodeError:
            all_text = textbase = r_text.decode('utf-8')
        except:
            internal_error('noopen', self.full_filename)
        return all_text

    def breaking(self, all_text):
        text_list = all_text.split(u'\n')
        dir_h = [u'#name', u'#ps2_keyboard', u'#ps2_mouse', u'#logfile', u'#autorun']
        h2 = [u'author', u'version', u'автор', u'версия']
        # dir_m = [u'#include', u'#define']

        end_head = -1
        for i, st in enumerate(text_list[:15]):
            # print i, st
            st = st.lstrip(u' \t')
            st = st.lower()
            for directive in dir_h:
                if st.startswith(directive):
                    end_head = i
                    # print 'END_HEAD', i, directive
                    break
            if st.startswith('//'):
                if (end_head >= 0) and i - 1 == end_head:
                    end_head = i
                    # print 'no_space', i
                st = st.lstrip(u'/ \t')
                for start_word in h2:
                    if st.startswith(start_word):
                        end_head = i
                        # print 'END_HEAD', i, start_word
                        break

        # print u'ИТОГ', end_head
        end_head += 1
        if end_head > 0:
            header = text_list[:end_head]
            raw_text = text_list[end_head:]
            # print len(header)
            # for i in header:
                # print i
            # print raw_text[:3]
        else:
            header = []
            raw_text = text_list
        raw_text = map(lambda st: st.lstrip(u' \t'), raw_text)
        return header, raw_text

    def excluding(self, raw_text, delspace, delcomment):
        if not (delspace or delcomment): return raw_text
        correct_text = []
        for st in raw_text:
            st = st.lstrip(u' \t')
            if delcomment and u'//' in st:
                st = EncoderCMS.replace_comment(st)
            st = st.rstrip(u' \t')
            if delspace and st == u'': continue
            correct_text.append(st)
        return correct_text

    @staticmethod
    def replace_comment(st):
        test = False
        comment = None
        start = 0
        while True:
            pos_comment = st.find(u'//', start)
            if test: print 'pos_comment =', pos_comment
            if pos_comment == -1: break
            quotes = st.count(u'"', 0, pos_comment)
            if test: print 'quotes', quotes
            if quotes % 2 == 0:
                comment = pos_comment
                break
            start = pos_comment + 2
        if test: print 'comment', comment
        if comment is None:
            return st
        else:
            return st[:comment]
        if test and False:
            print replace_comment('$mouse = 5 stroke')
            print replace_comment('$mouse = 5//stroke')
            print replace_comment('$mouse = "5" nnn "//stroke"')
            print replace_comment('$mouse = "5" nnn //stroke')
            print replace_comment('$mouse = "5//" nnn //stroke  kkk//')

    def statistics(self, raw_text, delspace=False, delcomment=False):
        min_key = 1000
        max_key = 0
        sum = 0
        counter = {}
        for i in raw_text:
            l = len(i)
            if l < min_key: min_key = l
            if l > max_key: max_key = l
            sum += l
            counter[l] = counter.get(l, 0) + 1
        print u'строк       %d' % len(raw_text)
        print u'min len     %d'% min_key
        print u'max len     %d'% max_key
        print u'average len %.3f' % (float(sum) / len(raw_text))
        # print counter, u'\n'
        # print list(counter.items())
        self.print_stat_table(counter, max_key)
        
    def print_stat_table(self, counter, max_key):
        values = [val for key, val in counter.items()]
        if not values: return
        values.sort(reverse=True)
        max_val = values[0]
        print 'max count  ', max_val
        # print counter

        cp.cprint2(u'5\n%s' % (u'График количества строк по длине строки'.center(80)))
        cp.cprint2(u'8%s' % ('-'*80))
        over80 = 0
        for line in range(max_val, -1, -1):
            sp = []
            for i in range(max_key + 1):
                val = counter.get(i, 0)
                if i > 79 and val > line:
                    over80 += 1
                if i % 3 == 0:
                    color = 2
                elif (i-1) % 3 == 0:
                    color = 3
                else:
                    color = 6
                if val > line:
                    if sp:
                        sp.append('^%d_'% color)
                    else:
                        sp.append(str(color))
                    sp.append('I')
                else: sp.append(' ')
            cp.cprint2(u'%s\r' % (''.join(sp)))

        s1 = [str(n) for n in range(0, 10, 3)]
        s1b = [str(n) for n in range(12, 79, 3)]
        s2 = [str(n) for n in range(1, 10, 3)]
        s2b = [str(n) for n in range(10, 79, 3)]
        s3 = [str(n) for n in range(2, 10, 3)]
        s3b = [str(n) for n in range(11, 79, 3)]
        cp.cprint2(u'8%s\r' % ('-'*80))
        cp.cprint2(u'2_%s  %s' % ('  '.join(s1), ' '.join(s1b)))
        cp.cprint2(u'3_ %s  %s\n' % ('  '.join(s2), ' '.join(s2b)))
        cp.cprint(u'6_  %s  %s\n' % ('  '.join(s3), ' '.join(s3b)))
        if over80:
            cp.cprint(u'5Строк длиной 80 символов и более ^15_%d ^5_шт.' % over80)

    def encode_(self, delspace=False, delcomment=False, levels=1, stat_freq=False):
        all_text = self.read_file()
        header, raw_text = self.breaking(all_text)
        raw_text = self.excluding(raw_text, delspace, delcomment)
        if stat_freq:
            self.statistics(raw_text, delspace, delcomment)
        for i in range(levels):
            raw_text = self.passing_level(raw_text)
        # print ('\n'.join(raw_text)).encode('cp866', 'ignore')
        out_text = self.assembly_file(header, raw_text)
        self.write_file(out_text)
        return self.ids

    def percent2steps(self, st):
        steps = []
        length = len(st)
        for tab in self.percent:
            if length < tab['len']:
                start = 0
                for col, p in enumerate(tab['step']):
                    p1 = int(p[0] * length / 100)
                    p2 = int(p[1] * length / 100)
                    if p1 < 2: p1 = 2
                    if length - p2 < 1: p2 = length - 1
                    steps.append((p1, p2))
                break
        else:
            iter = int(length/12)
            for i in range(1, iter+1):
                p1 = 12*i - 5
                p2 = 12*i + 1
                if p2 >= length: p2 = length - 2
                steps.append((p1, p2))
        return steps

    def print_colored_steps(self, st, steps, pos):
        length = len(st)
        # print 'length', length
        # print steps, '\n', pos
        if not steps:
            cp.cprint2(u'1_%s\n' % ('8'*length))
            return
        has = 0
        for col, par in enumerate(steps):
            if col > 4: col += 1
            cp.cprint2(u'1_%s^%d_%s' % ('8'*(par[0]-has-1), col+2, '8'*(par[1]-par[0]+1)))
            has = par[1]
        cp.cprint2(u'1_%s\n' % ('8'*(length - has)))
        # print st
        pass

    def print_colored_divide(self, divide_s):
        if not self.console: return
        for col, ss in enumerate(divide_s):
            if col > 4: col += 1
            cp.cprint2(u'%d_%s' % (col+2, ss))
        print

    def steps2pos_random(self, steps):
        pos = []
        for par in steps:
            pos.append(random.randint(par[0], par[1]))
        return pos

    @staticmethod
    def get_position_symbol(st, symb):
        _positions = []
        _start = 0
        while symb in st[_start:]:
            ps = st[_start:].find(symb)
            _start += ps
            _positions.append(_start)
            _start += 1
        return _positions

    @staticmethod
    def check_comment(st, positions, pos_comments):
        for pc in pos_comments:
            quote = st.count('"', 0, pc)
            if quote % 2 == 0:
                # print u'Начало коммента', pc
                positions = filter(lambda x: x <= pc, positions)
                break
        return positions

    @staticmethod
    def check_comments_divide(st, positions, pos_comments):
        # st = u'Длинное начало "aa//bb" // два //"'
        # positions = [4, 17, 19, 23, 24, 25, 32]
        for pc in pos_comments:
            if st[pc + 1:].startswith('/'):
                try:
                    positions.remove(pc+1)
                    # print u'позиция разрывает', pc+1
                except ValueError: pass
        _pos = positions[:]
        start = 0
        _pos.append(len(st))
        for end in _pos:
            ss = st[start:end]
            # print '-' + ss + '-'
            if start > 0 and ('//' in ss) and \
                    ss.lstrip(u' \t').startswith('//') and \
                    (st.count('"', 0, start) % 2 == 0):
                positions.remove(start)
                # print u'диапазон начинается с коммента', start
            start = end

    @staticmethod
    def check_quotes_divide(st, positions, pos_quotes):
        _pos = positions[:]
        for qu in pos_quotes:
            for posit in _pos:
                if qu[0] < posit <= qu[1]:
                    positions.remove(posit)

    @staticmethod
    def filter_pos(st, positions):
        pos_comments = EncoderCMS.get_position_symbol(st, '//')
        pos_quotes_by_one = EncoderCMS.get_position_symbol(st, '"')
        # print 'pos_quotes_by_one ', pos_quotes_by_one
        pos_quotes = []
        if len(pos_quotes_by_one) % 2 != 0:
            pos_quotes_by_one.append(len(st))
        for i in range(0, len(pos_quotes_by_one), 2):
            pos_quotes.append((pos_quotes_by_one[i], pos_quotes_by_one[i+1]))

        # print 'pos_quotes ', pos_quotes
        # print 'pos_comments ', pos_comments
        # print 'positions ', positions
        positions = EncoderCMS.check_comment(st, positions, pos_comments)
        # print 'positions ', positions
        EncoderCMS.check_comments_divide(st, positions, pos_comments)
        # print 'positions ', positions
        EncoderCMS.check_quotes_divide(st, positions, pos_quotes)
        # print 'positions ', positions
        return positions

    def divide_string(self, st, pos): # @staticmethod
        if st.startswith('empty=0//'):
            return [st]
        # print pos,
        _pos = pos[:]
        _positions = EncoderCMS.filter_pos(st, _pos)
        # print _positions
        start = 0
        result = []
        _positions.append(len(st))
        for end in _positions:
            result.append(st[start:end])
            start = end
        return result

    def passing_level(self, raw_text):
        dir_h = [u'#name', u'#include', u'#logfile', u'#autorun',
                u'#ps2_keyboard', u'#ps2_mouse', u'#define']
        defs_level = []
        for num_str, st in enumerate(raw_text):
            if not st: continue
            if st.startswith('//'):
                st = 'empty=0' + st
            for directive in dir_h:
                if st.startswith(directive):
                    print st
                    break
            else:
                steps = self.percent2steps(st)
                pos = self.steps2pos_random(steps)
                divide_s = self.divide_string(st, pos)
                # self.print_colored_steps(st, steps, pos)
                self.print_colored_divide(divide_s)
                # if len(st) > 5:
                    # raw_input('---- END   ----')
                    # exit()
                current_st = []
                for ss in divide_s:
                    if ss.startswith('//'): # если подстрока начинается с //
                        current_st.append(ss)
                        continue
                    ids = self.get_ids()
                    defs_level.append((ids, ss))
                    current_st.append(ids)
                raw_text[num_str] = ''.join(current_st)
                if random.randint(0, 10) == 0:
                    ids = self.get_ids()
                    fals_start = random.randint(0, len(self.dummy) - 13)
                    fals_end = fals_start + random.randint(5, 12)
                    fals = self.dummy[fals_start:]
                    defs_level.append((ids, self.dummy[fals_start:fals_end]))
        random.shuffle(defs_level)
        if defs_level:
            self.defs = defs_level + self.defs
        # print self.defs
        # print len(self.defs)
        return raw_text

    def get_ids(self):
        if not self.ids: # закончились ли ids
            self.internal_error('no_ids', self.len_ids)
        return self.ids.pop()

    def assembly_file(self, header, raw_text):
        all_defs = []
        for i in self.defs:
            all_defs.append('#define ' + i[0] + ':' + i[1])
        out_text = '\n'.join(header + all_defs + raw_text)
        return out_text

    def write_file(self, out_text):
        out_name = self.filename_parts['name'] + self.fout + self.filename_parts['ext']
        with open(os.path.join(self.filename_parts['path'], out_name), 'w') as f:
            f.write(out_text.encode(self.fcod))


# ------------------------------------------------------------------------------

def to_bool(s):
    if s.lower() in ['true', 'on', '1']:
        return True
    return False

def read_settings(filename_config):
    params = {}
    fileini = os.path.join(PATH_SCRIPT, filename_config)
    if not os.path.isfile(fileini):
        cp.cprint(u'13Ошибка открытия файла ^15_%s' % filename_config)
        time.sleep(3 + ext_sleep)
        exit(1)
    settings = Ini(fileini)

    settings.set_name_section('Global')
    sec_param = settings.get_allparam()
    sec_param = {i[0]:i[1]  for i in sec_param}
    params['fin'] = sec_param.get('suffix_decode', u'').decode('utf-8')
    params['fout'] = sec_param.get('suffix_protection', u'').decode('utf-8')
    params['fcod'] = sec_param.get('code', 'cp1251').decode('utf-8')

    settings.set_name_section('Encoder')
    sec_param = settings.get_allparam()
    sec_param = {i[0]:i[1]  for i in sec_param}
    # print sec_param
    params['symbols'] = sec_param.get('symbols', u'hbdp').decode('utf-8')
    params['length'] = int(sec_param.get('length', 8))
    params['edging'] = sec_param.get('edging', u'q').decode('utf-8')
    params['delspaces'] = to_bool(sec_param.get('del_spaces', 'False').decode('utf-8'))
    params['delcomments'] = to_bool(sec_param.get('del_comments', 'False').decode('utf-8'))
    params['levels'] = int(sec_param.get('levels', 1))
    params['console'] = to_bool(sec_param.get('console', 'False').decode('utf-8'))
    params['statistics'] = to_bool(sec_param.get('statistics', 'False').decode('utf-8'))
    # print params
    return params

def percent2sep_viewer():
    percent = [
            {'len':3, 'step':[]},
            {'len':14, 'step':[(42, 75)]},
            {'len':31, 'step':[(18, 35), (58, 85)]},
            {'len':63, 'step':[(10, 18), (28, 40), (55, 65), (80, 90)]},
            {'len':81, 'step':[(7, 15), (25, 37), (47, 57), (67, 77), (85, 95)]}
            ]

    for s in range(79, 101):
    # for s in [16, 17, 28, 40, 62, 80]:
        st = '8'*s
        steps = []
        length = len(st)
        for tab in percent:
            if length < tab['len']:
                start = 0
                for col, p in enumerate(tab['step']):
                    p1 = int(p[0] * length / 100)
                    p2 = int(p[1] * length / 100)
                    if p1 < 2: p1 = 2
                    if length - p2 < 1: p2 = length - 1
                    steps.append((p1, p2))
                break
        else:
            iter = int(length/12)
            for i in range(1, iter+1):
                p1 = 12*i - 5
                p2 = 12*i + 1
                if p2 >= length: p2 = length - 2
                steps.append((p1, p2))

        if not steps:
            cp.cprint2(u'1_%s\n' % ('8'*length))
            continue

        # выводим на печать
        print 'length', length
        print steps
        has = 0
        for col, par in enumerate(steps):
            if col > 4: col += 1
            cp.cprint2(u'1_%s^%d_%s' % ('8'*(par[0]-has-1), col+2, '8'*(par[1]-par[0]+1)))
            has = par[1]
        cp.cprint2(u'1_%s\n' % ('8'*(length - has)))
    raw_input()
    exit()

# ==============================================================================

if __name__ == '__main__':
    os.system('color 71')
    cc.clearConsol()  # очищаем консоль
    GeneralEncoder.authorship()
    # percent2sep_viewer()  # визуальный просмотр деления на зоны

    # st = u'100500 // раз "'
    # st = u'Длинное начало "aa//bb" // два //"'
    # positions = [4, 17, 19, 23, 24, 25, 32]
    # print st
    # EncoderCMS.filter_pos(st, positions)
    # position_comments = EncoderCMS.get_position_symbol(st, '//')
    # position_quotes = EncoderCMS.get_position_symbol(st, '"')
    # exit()

    filename_config = u'settings_encrypt.ini'
    params = read_settings(filename_config)

    # fin =     u'_decode'        # суффикс входного файла
    # fout =    u'_protection'    # суффикс выходного файла
    # fcod =    'cp1251'          # кодировка выходного файла
    # symbols = 'hbdp'            # набор символов для генерации последовательности
    # length =  8                 # длина основной части последовательности
    # edging =  'q'               # символы обрамления
    # delspaces = False           # удалять пустые строки
    # delcomments = False         # удалять комментарии
    # levels = 1                  # количество проходов кодирования
    # console = True              # показывать процесс
    # statistics = False          # статистика количества строк по длине строки

    GeneralEncoder(**params).run()

    # time.sleep(1)
    # raw_input('---------------   END   ---------------')
    cp.cprint(u'2------------   Скрипт защищён   ----------\n')
    raw_input()

# ------------------------------------------------------------------------------
# chdir /D D:\Яндекс Диск\_Python\A_Python\Encrypt_CMS
# python "D:\Яндекс Диск\_Python\A_Python\Encrypt_CMS\Encode_CMS.py" My_encr_011_decode.cms
# python "D:\Яндекс Диск\_Python\A_Python\Encrypt_CMS\Encode_CMS.py" Test_script.cms My_encr_011_decode.cms
# python "D:\Яндекс Диск\_Python\A_Python\Encrypt_CMS\Encode_CMS.py" Luhn_check_small.cms
