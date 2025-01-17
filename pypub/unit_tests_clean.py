import re

import unittest

from bs4 import BeautifulSoup

from pypub.compat import *
from pypub.clean import clean, condense, create_html_from_fragment, html_to_xhtml

"""
TODO html and body with out head my_first_chapter = pypub.create_chapter_from_string('<html><body><p>Hello World</p></body></html>', title='Hello Body Chapter')
TODO mdash (etc.) Unicode characters, see:
 * https://github.com/wcember/pypub/issues/18 - xmlprettify can cause mangled output
 * https://github.com/wcember/pypub/issues/26 - mdash / ndash not supported
 * https://github.com/wcember/pypub/issues/20 - Problem with diacritic sign.
 * epubcheck error FATAL(RSC-016)
"""

class CleanTests(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_condense(self):
        pass

    def test_clean_empty_img(self):
        s = u'''
                <!DOCTYPE html>
                <html>
                 <head>
                 </head>
                 <body>
                  <img src=""></img>
                 </body>
                </html>
                '''
        s1 = u'''
                <!DOCTYPE html>
                <html>
                 <head>
                 </head>
                 <body>
                  <img src=""></img>
                  <img></img>
                  <img/>
                 </body>
                </html>
                '''
        self.assertEqual(condense(clean(s1)), condense(clean(s)))

    def test_clean_with_article(self):
        s = '<html><head><title>test title</title></head><body><article>Hello! I am a test</article></body></html>'
        s1 = '<html><head><title>test title</title></head><body><div>dsfasfadfasdfasdf</div><article>Hello! I am a test</article></body></html>'
        s2 = '<html><head><title>test title</title></head><body><article><video></video>Hello! I am a test</article></body></html>'
        self.assertEqual(condense(clean(s)), condense(s))
        self.assertEqual(condense(clean(s1)), condense(s))
        self.assertEqual(condense(clean(s2)), condense(s))

    def test_clean_tags_full_html(self):
        s = u'''
                <!DOCTYPE html>
                <html>
                 <head>
                    <title>test title</title>
                 </head>
                 <body>
                  <div>Hello </div>
                 </body>
                </html>
                '''
        s1 = u'''
                <!DOCTYPE html>
                <html>
                 <head>
                    <title>test title</title>
                 </head>
                 <body>
                  <div>Hello </div>
                  <script>Uh oh...it's an evil script!</script>
                 </body>
                </html>
                '''
        s2 = u'''
                <!DOCTYPE html>
                <html>
                 <head>
                    <title>test title</title>
                 </head>
                 <body>
                  <div>Hello </div>
                 </body>
                 <script>Uh oh...it's an evil script again!</script>
                </html>
                '''
        s3 = u'''
                <!DOCTYPE html>
                <html>
                 <head>
                    <title>test title</title>
                 </head>
                 <body>
                  <div>Hello </div>
                 </body>
                 <video>Play me!</video>
                </html>
                '''
        s4 = u'''
                <!DOCTYPE html>
                <html>
                 <head>
                    <title>test title</title>
                 </head>
                 <body>
                  <video>
                   <div>Hello </div>
                  </video>
                 </body>
                 <video>Play me!</video>
                </html>
                '''

        s5 = u'''
        <!DOCTYPE html>
        <html>
         <head>
                    <title>test title</title>
         </head>
         <body>
          <video>
           <div>Hello&nbsp;</div>
          </video>
         </body>
         <video>Play me!</video>
        </html>
        '''
        self.assertEqual(condense(clean(s)), condense(s))
        self.assertEqual(condense(clean(s1)), condense(s))
        self.assertEqual(condense(clean(s2)), condense(s))
        self.assertEqual(condense(clean(s3)), condense(s))
        self.assertEqual(condense(clean(s4)), condense(s))
        self.assertEqual(condense(clean(s5)), condense(s))

    def test_html_to_xhtml(self):
        s = u'<!DOCTYPE html><html xmlns="http://www.w3.org/1999/xhtml"><head><title>xhtml test title</title></head><body><div id="Test">Hello</div><br /><br /></body></html>'
        s1 = u'''
                <!DOCTYPE html>
                <html>
                 <head>
                 <title>xhtml test title</title>
                 </head>
                 <body>
                  <DIV ID="Test">Hello</div>
                  <br>
                  <br>
                 </body>
                </html>
                '''
        self.assertEqual(condense(html_to_xhtml(clean(s1))), s)

    def test_html_to_xhtml_no_title(self):
        s = u'<!DOCTYPE html><html xmlns="http://www.w3.org/1999/xhtml"><head><title>Ebook Chapter</title></head><body><div id="Test">Hello</div><br /><br /></body></html>'
        s1 = u'''
                <!DOCTYPE html>
                <html>
                 <head>
                 </head>
                 <body>
                  <DIV ID="Test">Hello</div>
                  <br>
                  <br>
                 </body>
                </html>
                '''
        self.assertEqual(condense(html_to_xhtml(clean(s1))), s)

    def test_create_html_from_fragment(self):
        test_tag1 = BeautifulSoup('<div></div>', 'html.parser').div
        test_tree1 = create_html_from_fragment(test_tag1)
        self.assertEqual(unicode(test_tree1), '<html><head></head><body><div></div></body></html>')
        self.assertRaises(TypeError, create_html_from_fragment, '')
        self.assertRaises(ValueError, create_html_from_fragment, test_tree1)


if __name__ == '__main__':
    unittest.main()
