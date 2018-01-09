import unittest

import os

from man_parser import ManParser


class ManParserTests(unittest.TestCase):
    def out_file_testing(self, out, expected):
        self.assertTrue(os.path.isfile(out))
        with open(out, 'r') as html:
            self.assertEqual(expected, html.read())

    def test_empty_file(self):
        with self.assertRaises(TypeError):
            ManParser('test_files/empty_test.txt')

    def test_strange_file(self):
        with self.assertRaises(TypeError):
            ManParser('test_files/strange_test_file.txt')

    def test_no_name_section(self):
        with self.assertRaises(TypeError):
            ManParser('test_files/no_name_section.txt')

    def test_structure(self):
        m2h = ManParser('test_files/structure.txt', 'test_files/structure.html')
        m2h.parse_file()
        expected = ('<html>\n  <header>\n    <title>test man page</title>\n' +
                    '  </header>\n  <body>\n    <p>TEST(1)</p>\n\n    <h3>NAME</h3>\n' +
                    '      <p>&emsp;smth</p>\n    <h3>LOL</h3>\n      <p>&emsp;kek</p>\n' +
                    '      <p>&emsp;cheburek</p>\n    <h3>OPTIONS</h3>\n' +
                    '      <p>&emsp;-meow</p>\n      <p>&emsp;&emsp;cats are cool</p>\n' +
                    '  </body>\n</html>')
        self.out_file_testing('test_files/structure.html',expected)

    def test_one_font(self):
        m2h = ManParser('test_files/one_font.txt', 'test_files/one_font.html')
        m2h.parse_file()
        expected = ('<html>\n  <header>\n    <title>font man page</title>\n' +
                    '  </header>\n  <body>\n    <p>Font(1)</p>\n\n' +
                    '    <h3>NAME</h3>\n      <p>&emsp;<b>bold</b></p>\n' +
                    '  </body>\n</html>')
        self.out_file_testing('test_files/one_font.html', expected)

    def test_all_fonts(self):
        m2h = ManParser('test_files/many_fonts_test.txt', 'test_files/fonts_test.html')
        m2h.parse_file()
        expected = ('<html>\n  <header>\n    <title>fonts man page</title>\n' +
                    '  </header>\n  <body>\n    <p>FONTS(0)</p>\n\n' +
                    '    <h3>NAME</h3>\n      <p>&emsp;<b>bold</b> <i>italic</i>' +
                    ' <i>italic</i> <b>bold</b>  <i>italic</i> roman  <b>bold</b>' +
                    ' <i>italic</i>  <b>bold</b> roman' +
                    '  roman <b>bold</b>  roman <i>italic</i> </p>\n' +
                    '      <p>&emsp;<small>small</small> <small>small</small> <b>bold</b>  </p>\n' +
                    '  </body>\n</html>')
        self.assertTrue(os.path.isfile('test_files/fonts_test.html'))
        self.out_file_testing('test_files/fonts_test.html', expected)

    def test_another_type_of_font_tags(self):
        m2h = ManParser('test_files/other_type_fonts.txt', 'test_files/fonts_test_2.html')
        m2h.parse_file()
        expected = ('<html>\n  <header>\n    <title>font man page</title>\n' +
                    '  </header>\n  <body>\n    <p>FONT(2)</p>\n\n' +
                    '    <h3>NAME</h3>\n      <p>&emsp;<b>bold</b> <i>italic</i></p>\n' +
                    '  </body>\n</html>')
        self.out_file_testing('test_files/fonts_test_2.html', expected)

    def test_full(self):
        m2h = ManParser('test_files/full_test.txt', 'test_files/full_test.html')
        m2h.parse_file()
        expected = ('<html>\n  <header>\n    <title>corrupt man page</title>\n' +
                    '  </header>\n  <body>\n    <p>CORRUPT(1)</p>\n\n' +
                    '    <h3>NAME</h3>\n      <p>&emsp;corrupt - modify files by randomly changing bits</p>\n' +
                    '    <h3>SYNOPSIS</h3>\n      <p>&emsp;<b>corrupt</b> [<b>-n</b> <i>BITS</i>]' +
                    ' [<b>--bits</b> <i>BITS</i>] <i>file</i> ... </p>\n' +
                    '    <h3>DESCRIPTION</h3>\n      <p>&emsp;<b>corrupt</b> modifies files by' +
                    ' toggling a randomly chosen bit.</p>\n    <h3>OPTIONS</h3>\n' +
                    '      <p>&emsp;<b>-n,</b> --bits <b>=<i>BITS</i></b> </p>\n' +
                    '      <p>&emsp;&emsp;Set the number of bits to modify.' +
                    ' Default is one bit</p>\n  </body>\n</html>')
        self.out_file_testing('test_files/full_test.html', expected)
