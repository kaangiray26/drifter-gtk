from gettext import gettext as _
from gi.repository import Gtk, Pango
from bs4 import BeautifulSoup
import mistune
import re

# Note: I've used the \uffff character quite a bit here. This character doesn't
# represent anything, and it's not supposed to be found inside normal text.
# I used it as a custom delimiter for special markdown elements that cannot
# be represented using just pango markup.

HEADER_LEVELS = [
    'xx-large', 'x-large', 'large',
    'medium', 'small', 'x-small', 'xx-small'
]

SUPERSCRIPT_REGEX = re.compile(r'\^\(.+\)|\^[^< ]+')


class PangoRenderer(mistune.Renderer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, escape=True, **kwargs)

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
        if level > len(HEADER_LEVELS):
            level = 0
        return '\n<span size="{0}">{1}</span>\n'.format(
            HEADER_LEVELS[level-1],
            text
        )

class MarkdownView(Gtk.Box):
    def __init__(self, markdown=''):
        super().__init__(
            orientation=Gtk.Orientation.VERTICAL, vexpand=False, hexpand=True
        )
        self.markdown = ''
        self.pango_strings = []
        self.parser = mistune.Markdown(renderer=PangoRenderer())
        self.set_text(markdown)

    def empty(self):
        for child in self.get_children():
            self.remove(child)

    def apply_superscript(self, txt):
        if '^' in txt:
            for match in SUPERSCRIPT_REGEX.findall(txt):
                txt = txt.replace(match, f'''<sup>{
                    match.replace("^", "").replace("(", "").replace(")", "")
                }</sup>''')
        return txt

    def append_label(self, pstr, is_quote=False):
        pstr = str(BeautifulSoup(
            pstr,
            'html.parser'
        ))
        pstr = self.apply_superscript(pstr)
        label = Gtk.Label(
            use_markup=True, selectable=True, wrap=True,
            wrap_mode=Pango.WrapMode.WORD_CHAR,
            justify=Gtk.Justification.FILL, vexpand=False, hexpand=True,
            halign=Gtk.Align.START
        )
        label.set_markup(pstr)
        if is_quote:
            label.get_style_context().add_class('markdown-quote')
        self.add(label)

    def append_quote(self, pstr):
        return self.append_label(pstr, is_quote=True)

    def append_hr(self):
        separator = Gtk.Separator(
            orientation=Gtk.Orientation.HORIZONTAL, vexpand=False, hexpand=True
        )
        separator.get_style_context().add_class('separator-hr')
        self.add(separator)

    def set_text(self, markdown):
        self.empty()
        self.markdown = markdown
        if markdown == '':
            return
        self.pango_strings = self.parser(self.markdown).split('\uffff\uffff')
        for pstr in self.pango_strings:
            if pstr == '##HR##':
                self.append_hr()
            elif '##BLOCKQUOTE##' in pstr:
                self.append_quote(
                    pstr.replace('##BLOCKQUOTE##', '').strip()
                )
            else:
                self.append_label(pstr.strip())
        self.show()