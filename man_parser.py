class ManParser:
    def __init__(self, input_file_name, output_file_name='out.html'):
        self.man_file = self.open_file(input_file_name)
        self.html_file = open(output_file_name, 'w')
        self.fonts = {'B': self.bold, 'I': self.italic, 'BR': self.bold_roman,
                      'BI': self.bold_italic, 'IR': self.italic_roman,
                      'IB': self.italic_bold, 'RB': self.roman_bold,
                      'RI': self.roman_italic, 'SM': self.small,
                      'SB': self.small_bold}
        self.paragraphs = []

    def open_file(self, file):
        man_file = open(file, 'r')
        first_line = man_file.readline()
        second_line = man_file.readline()
        if first_line == '' or not first_line.startswith('.TH') \
                or not second_line.startswith('.SH NAME'):
            man_file.close()
            raise TypeError()
        else:
            man_file.seek(0)
            return man_file

    def parse_file(self):
        self.html_file.write('<html>\n')
        self.split_to_paragraphs()
        self.man_file.seek(0)
        paragraph_index = 0
        more_paragraphs = False
        for line in self.man_file:
            if line.startswith('.TH'):
                self.write_main_title(line[4:-1])
            elif line.startswith('.SH'):
                self.write_section_title(line[4:-1])
                more_paragraphs = True
            elif more_paragraphs:
                par = '      {}'.format(self.paragraphs[paragraph_index][0])
                self.html_file.write(par)
                more_paragraphs = self.paragraphs[paragraph_index][1]
                paragraph_index += 1
        self.html_file.writelines(['  </body>\n', '</html>'])
        self.man_file.close()
        self.html_file.close()

    def split_to_paragraphs(self):
        paragraph = ''
        tp_flag = False
        tabs_count = 1
        for line in self.man_file:
            if line.startswith('.SH') and paragraph != '':
                par = '<p>{0}{1}</p>\n'.format('&emsp;' * tabs_count,
                                               paragraph)
                self.paragraphs.append((par, False))
                paragraph = ''
                if tabs_count == 2:
                    tabs_count = 1
            elif (line.startswith('.P') or line.startswith('.LP') or
                    tp_flag) and paragraph != '':
                par = '<p>{0}{1}</p>\n'.format('&emsp;' * tabs_count,
                                               paragraph)
                self.paragraphs.append((par, True))
                paragraph = self.parse_line(line[:-1]) if tp_flag else ''
                if tp_flag:
                    tabs_count = 2
                    tp_flag = False
                elif tabs_count == 2:
                    tabs_count = 1
            elif line.startswith('.TP'):
                tp_flag = True
            elif len(paragraph) >= 150:
                par = '<p>{0}{1}</p>\n'.format('&emsp;' * tabs_count,
                                               paragraph)
                self.paragraphs.append((par, True))
                paragraph = self.parse_line(line[:-1])
            elif not line.startswith('.TH') and not line.startswith('.SH'):
                if paragraph != '':
                    paragraph += ' '
                paragraph += self.parse_line(line[:-1])
        self.paragraphs.append(('<p>{0}{1}</p>\n'.format('&emsp;' * tabs_count,
                                                         paragraph), False))

    def parse_line(self, line):
        new_line = ''
        i = 0
        while i < len(line):
            if not (line[i] == '\\' or line[i] == ' ' and line[i + 1] == '"'):
                new_line += line[i]
            elif line[i] == ' ' and line[i + 1] == '"':
                i += 1
            elif line[i + 1] == 'f':
                if line[i + 2] in self.fonts.keys():
                    line_to_tag = self.find_tagged_part(line[i + 3:])
                    new_line += self.fonts[line[i + 2]](line_to_tag[0])
                    i += 5 + line_to_tag[1]
            i += 1
        if new_line.startswith('.'):
            if new_line[1] in self.fonts.keys() and new_line[2] == ' ':
                new_line = self.fonts[new_line[1]](new_line[3:])
            elif new_line[1:3] in self.fonts.keys():
                new_line = self.fonts[new_line[1:3]](new_line[4:])
        return new_line

    def find_tagged_part(self, line):
        line_to_tag = ''
        for i in range(len(line)):
            if line[i] == '\\':
                if line[i + 1] == 'f':
                    return line_to_tag, i
            else:
                line_to_tag += line[i]

    def write_main_title(self, title):
        self.html_file.write('  <header>\n')
        title_word = title.lower().split()[0]
        tagged_title = '    <title>{} man page</title>\n'.format(title_word)
        self.html_file.write(tagged_title)
        self.html_file.write('  </header>\n')
        self.html_file.write('  <body>\n')
        splitted_title = title.split()
        self.html_file.write('    <p>{0}({1})</p>\n\n'.format(splitted_title[0],
                             splitted_title[1]))

    def write_section_title(self, title):
        self.html_file.write('    <h3>{}</h3>\n'.format(title))

    @staticmethod
    def bold(line):
        return '<b>{}</b>'.format(line)

    @staticmethod
    def italic(line):
        return '<i>{}</i>'.format(line)

    @staticmethod
    def alternate_fonts(line, font1=None, font2=None):
        new_line = ''
        splitted_line = line.split()
        first_words = splitted_line[0::2]
        for word in splitted_line:
            if word in first_words:
                if font1 is None:
                    new_line += word + ' '
                else:
                    new_line += font1(word) + ' '
            else:
                if font2 is None:
                    new_line += word + ' '
                else:
                    new_line += font2(word) + ' '
        return new_line

    def bold_roman(self, line):
        return self.alternate_fonts(line, self.bold)

    def bold_italic(self, line):
        return self.alternate_fonts(line, self.bold, self.italic)

    def italic_roman(self, line):
        return self.alternate_fonts(line, self.italic)

    def italic_bold(self, line):
        return self.alternate_fonts(line, self.italic, self.bold)

    def roman_bold(self, line):
        return self.alternate_fonts(line, font2=self.bold)

    def roman_italic(self, line):
        return self.alternate_fonts(line, font2=self.italic)

    @staticmethod
    def small(line):
        return '<small>{}</small>'.format(line)

    def small_bold(self, line):
        return self.alternate_fonts(line, self.small, self.bold)
