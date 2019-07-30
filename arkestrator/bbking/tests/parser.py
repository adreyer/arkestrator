from django.test import TestCase

import bbking.tags
from bbking import parser

__all__ = ['ParserTestCase', 'MalformedCodeTestCase']

class ParserTestCase(TestCase):
    def test_parse_basic(self):
        parsed = parser.parser.parse("[i]This text is italian.[/i]")

        self.assertEqual(len(parsed), 1)
        tag = parsed[0]
        self.assertEqual(type(tag), parser.Tagged)
        self.assertEqual(tag.name, 'i')
        self.assertEqual(tag.contents, ["This text is italian."])
        self.assertEqual(tag.raw, "[i]This text is italian.[/i]")

    def test_parse_with_arg(self):
        parsed = parser.parser.parse("[url=http://www.example.com/]An Example Site[/url]")

        self.assertEqual(len(parsed), 1)
        tag = parsed[0]
        self.assertEqual(type(tag), parser.Tagged)
        self.assertEqual(tag.name, 'url')

        self.assertEqual(tag.arg, "http://www.example.com/")
        self.assertEqual(tag.kwargs, {})
        self.assertEqual(tag.contents, ["An Example Site"])
        self.assertEqual(tag.raw, "[url=http://www.example.com/]An Example Site[/url]")

    def test_parse_with_kwargs(self):
        parsed = parser.parser.parse("[img width=640 height=480]http://www.example.com/goatse.jpg[/img]")
        
        self.assertEqual(len(parsed), 1)
        tag = parsed[0]
        self.assertEqual(type(tag), parser.Tagged)
        self.assertEqual(tag.name, 'img')
        self.assertEqual(tag.arg, None)
        self.assertEqual(tag.kwargs, {'width' : '640', 'height' : '480'})
        self.assertEqual(tag.contents, ["http://www.example.com/goatse.jpg"])
        self.assertEqual(tag.raw, "[img width=640 height=480]http://www.example.com/goatse.jpg[/img]")

    def test_parse_multiple_tags(self):
        parsed = parser.parser.parse("""[quote=Rev. Johnny Healey]
            [i]this is a quote[/i] is not the proper way to quote someone.
[/quote]
I am aggree.
        """)

        self.assertEqual(len(parsed), 2)

        self.assertEqual(type(parsed[0]), parser.Tagged)
        tag = parsed[0]
        self.assertEqual(tag.name, 'quote')
        self.assertEqual(tag.arg, 'Rev. Johnny Healey')
        self.assertEqual(len(tag.contents), 3)
        self.assertEqual(type(tag.contents[1]), parser.Tagged)
        self.assertEqual(tag.contents[1].name, 'i')
        self.assertEqual(len(tag.contents[1].contents), 1)
        self.assertEqual(tag.contents[1].contents[0], "this is a quote")

        self.assertEqual(type(parsed[1]), str)
        self.assertEqual(parsed[1].strip(), 'I am aggree.')

    def test_parse_url_with_eq(self):
        parsed = parser.parser.parse("[url=http://www.example.com/this=a_test]An Example Site[/url]")
        self.assertEqual(len(parsed), 1)
        tag = parsed[0]
        self.assertEqual(type(tag), parser.Tagged)
        self.assertEqual(tag.name, 'url')

        self.assertEqual(tag.arg, "http://www.example.com/this=a_test")

    def test_infamous_footnote_bracket_bug(self):
        parsed = parser.parser.parse("[quote]According to the NYT[2] you are a douche[/quote]")
        self.assertEqual(len(parsed), 1)
        tag = parsed[0]
        self.assertEqual(type(tag), parser.Tagged)
        self.assertEqual(tag.name, 'quote')
        
        self.assertEqual(len(tag.contents), 1)
        self.assertEqual(tag.contents[0], 'According to the NYT[2] you are a douche')

class MalformedCodeTestCase(TestCase):
    def test_parse_unclosed(self):
        parsed = parser.parser.parse("[img]http://www.example.com/goatse.jpg")

        self.assertEqual(len(parsed), 1)
        self.assertEqual(parsed[0], "[img]http://www.example.com/goatse.jpg")

    def test_parse_unmatched(self):
        parsed = parser.parser.parse("[img]http://www.example.com/goatse.jpg[/url]")

        self.assertEqual(len(parsed), 1)
        self.assertEqual(parsed[0], "[img]http://www.example.com/goatse.jpg[/url]")
        
    def test_parse_missing_bracket(self):
        parsed = parser.parser.parse("[img http://www.example.com/goatse.jpg[/img]")

        self.assertEqual(len(parsed), 1)
        self.assertEqual(parsed[0], "[img http://www.example.com/goatse.jpg[/img]")

    def test_parse_missing_bracket_with_arg(self):
        parsed = parser.parser.parse("[url=http://www.example.com/ this is a test.[/url]")

        self.assertEqual(len(parsed), 1)
        self.assertEqual(parsed[0], "[url=http://www.example.com/ this is a test.[/url]")

    def test_parse_malformed_close_tag(self):
        parsed = parser.parser.parse("[url=http://www.example.com/]this is a test.[/url malformed]")

        self.assertEqual(len(parsed), 1)
        self.assertEqual(parsed[0],"[url=http://www.example.com/]this is a test.[/url malformed]")
    
    def test_bad_tag_name(self):
        parsed = parser.parser.parse("[noparse][b]test[/b][/noparse]")
        self.assertEqual(len(parsed), 3)

    def test_brainfuck(self):
        parsed = parser.parser.parse("[brainfuck]>---->-->+>++++>++>+>+>+>+>-->->->>>>->-->-->-->-->->>+>-->->>>>>>+>--->++>>>>>>++>->>>>>>>>>>>>>>>+>>>>++>->>>>+>--->++>--->--->--->++>+>+>-->->->->++++>+>>+>+>>++>->->-->->>>>>+>>++>>>>>>-->-->+>+>>->->>++>->>>+>++>->>++++>>>+>+>-->->->>>>>>>>>>>+>+>--->++>>>>>>>->->-->+>++>+>+>-->->-->->++>--->+>+>>++>>++>--->->->>>>>->-->>>>>+>-->+>+>+>>->->->>++>++>>>>++++[[+>>>+<<<]<++++]>++++>>-[+[+<<-[>]>]<<[<]>>++++++[-<<++++++++++>>]<<++.+>[<++>[+>>+<<]]+++++[+<++++>]>>[+<<+<.>>>]<<[---[-<+++>[+++<++++++++++++++>[+++++[-<+++++>]<+>]]]]>+++>>]<<<<[.<][/brainfuck]")
        self.assertEqual(len(parsed), 1)


class CompiledTagsTestCase(TestCase):
    def test_literal_len(self):
        lt = bbking.tags.LiteralTag("abcdefg")
        self.assertEqual(len(lt), 7)

    def test_bbtag_len(self):
        tag = get_tag("b")
        bbtag = tag("abcdefg")
        self.assertEqual(len(bbtag), 7)

    def test_block_len(self):
        lt = bbking.tags.LiteralTag("abcdefg")
        tag = get_tag("b")
        bbtag = tag("abcdefg")
        btag = bbking.tags.BlockTag([lt,tag])

        self.assertEqual(len(btag), 14)
