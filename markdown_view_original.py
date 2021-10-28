#!/usr/bin/python
#-*- encoding:utf-8 -*-

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango
import mistune

class PangoRenderer(mistune.Renderer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, escape=True, **kwargs)
        self.HEADER_LEVELS = [
            'xx-large', 'x-large', 'large',
            'medium', 'small', 'x-small', 'xx-small'
        ]

    def text(self, text):
        return mistune.escape(
            text.replace(
                '\n', '\ufafa'
            ).replace(
                '\ufafa\ufafa', '\n\n'
            ).replace(
                '\ufafa', ' '
            )
        )

    def link(self, link, title, text):
        return super().link(link, None, text)

    def image(self, src, alt='', title=None):
        return self.link(
            src,
            None,
            _('Image: ')+alt if isinstance(alt, str) else _('[Image]')
        )

    def emphasis(self, text):
        return f'<i>{text}</i>'

    def double_emphasis(self, text):
        return f'<b>{text}</b>'

    def codespan(self, text):
        return (
            '<tt>{0}</tt>'
        ).format(mistune.escape(text.rstrip(), smart_amp=False))

    def block_code(self, code, lang=None):
        return f'\n<tt>{mistune.escape(code)}</tt>\n'

    def newline(self):
        return '\n'

    def list(self, body, ordered=True):
        return '\n'.join([
            li.replace('\u2022', f'{i+1}.') for i, li in
            enumerate(body.split('\n'))
        ]) if ordered else body

    def list_item(self, text):
        # u2022 is a bullet sign
        return f'\u2022 {text}\n'

    def paragraph(self, text):
        return f'{text}\n\n'

    def strikethrough(self, text):
        return f'<span strikethrough="true">{text}</span>'

    def linebreak(self):
        return '\n'

    def hrule(self):
        return '\n\uffff\uffff##HR##\uffff\uffff\n'

    def block_quote(self, text):
        # return mistune.escape('> '+text)
        return f'\n\uffff\uffff##BLOCKQUOTE##\n{text}\uffff\uffff'

    def table(self, header, body):
        return (
            f'\n{header}\n{body}\n'
        )

    def table_row(self, content):
        return f'{content}\n'

    def table_cell(self, content, **flags):
        return content + '\t\t\t'

    def header(self, text, level, raw=None):
        if level > len(self.HEADER_LEVELS):
            level = 0
        return '\n<span size="{0}">{1}</span>\n'.format(
            self.HEADER_LEVELS[level-1],
            text
        )

class MarkdownRenderer:
    def __init__(self, text):
        self.text       = text
        self.parser     = mistune.Markdown(renderer=PangoRenderer())

    def get_text(self):
        self.pango_strings = self.parser(self.text).split('\uffff\uffff')
        for pstr in self.pango_strings:
            print (pstr)
        return self.pango_strings
