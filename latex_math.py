"""
Licensed under Public Domain Mark 1.0.
See http://creativecommons.org/publicdomain/mark/1.0/
Author: Justin Bruce Van Horne <justinvh@gmail.com>
"""


"""
Python-Markdown LaTeX Extension

Adds support for $math mode$ and %text mode%. This plugin supports
multiline equations/text.

The actual image generation is done via LaTeX/DVI output.
It encodes data as base64 so there is no need for images directly.
All the work is done in the preprocessor.
"""

import re
import os
import string
import base64
import tempfile
import markdown


from subprocess import call, PIPE


# Defines our basic inline image
IMG_EXPR = "<img class=\"latex-inline math-%s\" alt=\"%s\" id=\"%s\" src=\"data:image/svg+xml,%s\">"


# Base CSS template
IMG_CSS = "<style scoped>img.latex-inline { vertical-align: middle; }</style>\n"


class LaTeXPreprocessor(markdown.preprocessors.Preprocessor):
    # These are our cached expressions that are stored in latex.cache
    cached = {}

    # Basic LaTex Setup as well as our list of expressions to parse
    tex_preamble = r"""\documentclass[]{article}
\usepackage{amsmath}
\usepackage{amsthm}
\usepackage{amssymb}
\usepackage{bm}
\usepackage{relsize}
\usepackage[usenames,dvipsnames]{color}
\pagestyle{empty}
"""

    def __init__(self, configs):
        try:
            cache_file = open('latex.cache', 'r+')
            for line in cache_file.readlines():
                key, val = line.strip("\n").split("$")
                self.cached[key] = val
        except IOError:
            pass

        self.config = {}
        self.config[("general", "preamble")] = ""
        self.config[("dvipng", "args")] = "-q -T tight -bg Transparent -z 9 -D 106"
        self.config[("dvisvgm", "args")] = "--bbox=min --exact --mag=0.7"
        self.config[("delimiters", "text")] = "%"
        self.config[("delimiters", "math")] = "$"
        self.config[("delimiters", "preamble")] = "%%"
        self.config[("delimiters", "equation")] = "$$"

        try:
            import ConfigParser
            cfgfile = ConfigParser.RawConfigParser()
            cfgfile.read('markdown-latex.cfg')

            for sec in cfgfile.sections():
                for opt in cfgfile.options(sec):
                    self.config[(sec, opt)] = cfgfile.get(sec, opt)
        except ConfigParser.NoSectionError:
            pass

        def build_regexp(delim):
            delim = re.escape(delim)
            regexp = r'(?<!\\)' + delim + r'(.+?)(?<!\\)' + delim
            return re.compile(regexp, re.MULTILINE | re.DOTALL)

        # %TEXT% mode which is the default LaTeX mode.
        self.re_textmode = build_regexp(self.config[("delimiters", "text")])
        # $MATH$ mode which is the typical LaTeX math mode.
        self.re_mathmode = build_regexp(self.config[("delimiters", "math")])
        # $$EQUATION$$ mode which is the typical LaTeX equation mode.
        self.re_equationmode = build_regexp(self.config[("delimiters", "equation")])
        # %%PREAMBLE%% text that modifys the LaTeX preamble for the document
        self.re_preamblemode = build_regexp(self.config[("delimiters", "preamble")])

    """The TeX preprocessor has to run prior to all the actual processing
    and can not be parsed in block mode very sanely."""
    def _latex_to_svg(self, tex, mode):
        """Generates a SVG representation of TeX string"""
        # Generate the temporary file
        tempfile.tempdir = ""
        tmp_file_fd, path = tempfile.mkstemp()
        tmp_file = os.fdopen(tmp_file_fd, "w")
        tmp_file.write(self.tex_preamble)

        # Figure out the mode that we're in
        if mode == "math":
            ftex = "\\relscale{1.1}\n$ %s $" % tex
        elif mode == "equation":
            ftex = "\\relscale{1.5}\n\[ %s \]" % tex
        else:
            ftex = "%s" % tex

        tmp_file.write(ftex)
        tmp_file.write('\n\end{document}')
        tmp_file.close()

        # compile LaTeX document. A DVI file is created
        status = call(('pdflatex -halt-on-error -output-format pdf %s' % path).split(), stdout=PIPE)

        # clean up if the above failed
        if status:
            self._cleanup(path, err=True)
            raise Exception("Couldn't compile LaTeX document." +
                "Please read '%s.log' for more detail." % path)

        # Run dvipng on the generated DVI file. Use tight bounding box.
        # Magnification is set to 1200
        dvi = "%s.dvi" % path
        pdf = "%s.pdf" % path
        pdf_crp = "%s-crop.pdf" % path
        png = "%s.png" % path
        svg = "%s.svg" % path
        svgo = "%s-opt.svg" % path

        cmd = "pdfcrop %s" % (pdf)
        status = call(cmd.split(), stdout=PIPE)

        # clean up if we couldn't make the above work
        if status:
            self._cleanup(path, err=True)
            raise Exception("Couldn't crop PDF-LaTeX." +
                    "Please read '%s.log' for more detail." % path)

        cmd = "pdf2svg %s %s" % (pdf_crp, svg)
        status = call(cmd.split(), stdout=PIPE)

        # clean up if we couldn't make the above work
        if status:
            self._cleanup(path, err=True)
            raise Exception("Couldn't convert cropped PDF-LaTeX to SVG." +
                    "Please read '%s.log' for more detail." % path)

        cmd = "svgo %s %s" % (svg, svgo)
        status = call(cmd.split(), stdout=PIPE)

        # clean up if we couldn't make the above work
        if status:
            self._cleanup(path, err=True)
            raise Exception("Couldn't optimize SVG." +
                    "Please read '%s.log' for more detail." % path)

        # Read the png and encode the data
        svg = open(svgo, "rb")
        data = svg.read() \
            .replace('\n', '') \
            .replace('"', "'") \
            .replace('%', '%25') \
            .replace('>', '%3E') \
            .replace('<', '%3C') \
            .replace('#', '%23')
        svg.close()

        self._cleanup(path)

        return data

    def _cleanup(self, path, err=False):
        # don't clean up the log if there's an error
        extensions = ["", ".aux", "-crop.pdf", ".pdf", "-opt.svg", ".svg", ".log"]
        if err:
            extensions.pop()

        # now do the actual cleanup, passing on non-existent files
        for extension in extensions:
            try:
                os.remove("%s%s" % (path, extension))
            except (IOError, OSError):
                pass

    def run(self, lines):
        """Parses the actual page"""
        # Re-creates the entire page so we can parse in a multine env.
        page = "\n".join(lines)

        # Adds a preamble mode
        self.tex_preamble += self.config[("general", "preamble")]
        preambles = self.re_preamblemode.findall(page)
        for preamble in preambles:
            self.tex_preamble += preamble + "\n"
            page = self.re_preamblemode.sub("", page, 1)
        self.tex_preamble += "\n\\begin{document}"

        # Figure out our text strings and math-mode strings
        tex_expr = [(self.re_textmode, "text", x) for x in self.re_textmode.findall(page)]
        tex_expr += [(self.re_equationmode, "equation", x) for x in self.re_equationmode.findall(page)]
        tex_expr += [(self.re_mathmode, "math", x) for x in self.re_mathmode.findall(page) if x[1:] not in [bx[2] for bx in tex_expr]]

        # No sense in doing the extra work
        if not len(tex_expr):
            return page.split("\n")

        # Parse the expressions
        new_cache = {}
        id = 0
        for reg, mode, expr in tex_expr:
            print reg, mode, expr
            b64_expr = base64.b64encode(expr)
            simp_expr = filter(unicode.isalnum, expr)
            if b64_expr in self.cached:
                data = self.cached[b64_expr]
            else:
                data = self._latex_to_svg(expr, mode)
                new_cache[b64_expr] = data
            expr = expr.replace('"', "").replace("'", "")
            id += 1
            img = IMG_EXPR % (
                    'true' if mode in ['math', 'equation'] else 'false',
                    simp_expr,
                    simp_expr[:15] + "_" + str(id),
                    data)
            # print img
            page = reg.sub(img, page, 1)

        # Perform the escaping of delimiters and the backslash per se
        tokens = []
        tokens += [self.config[("delimiters", "preamble")]]
        tokens += [self.config[("delimiters", "text")]]
        tokens += [self.config[("delimiters", "math")]]
        tokens += ['\\']
        for tok in tokens:
            page = page.replace('\\' + tok, tok)

        # Cache our data
        cache_file = open('latex.cache', 'a')
        for key, value in new_cache.items():
            cache_file.write("%s$%s\n" % (key, value))
        cache_file.close()

        # Make sure to resplit the lines
        return page.split("\n")


class LaTeXPostprocessor(markdown.postprocessors.Postprocessor):
        """This post processor extension just allows us to further
        refine, if necessary, the document after it has been parsed."""
        def run(self, text):
            # Inline a style for default behavior
            text = IMG_CSS + text
            return text


class MarkdownLatex(markdown.Extension):
    """Wrapper for LaTeXPreprocessor"""
    def extendMarkdown(self, md, md_globals):
        # Our base LaTeX extension
        md.preprocessors.add('latex',
                LaTeXPreprocessor(self), ">html_block")
        # Our cleanup postprocessing extension
        md.postprocessors.add('latex',
                LaTeXPostprocessor(self), ">amp_substitute")


def makeExtension(*args, **kwargs):
    """Wrapper for a MarkDown extension"""
    return MarkdownLatex(*args, **kwargs)
