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
import hashlib
from selenium import webdriver

from subprocess import call, PIPE


# Defines our basic inline image
DIAGRAM_EXPR = "<center class=\"md\">{}</center>"

# Base CSS template
DIAGRAM_CSS = "<style scoped>svg.diagram{display:block;font-family:'Ubuntu Mono';font-size:14px;text-align:center;stroke-linecap:round;stroke-width:1.5px;}.md</style>"


class MarkdeepDiagramPreprocessor(markdown.preprocessors.Preprocessor):
    # These are our cached expressions that are stored in latex.cache
    cached = {}

    # Basic markdeep setup
    markdeep_preamble = r"""
<!DOCTYPE html>
<html>
<body>

<diagram>
{}
</diagram>

<script>window.markdeepOptions = {{mode: 'html'}};</script>
<script src="https://casual-effects.com/markdeep/latest/markdeep.min.js"></script>

</body>
</html>
"""

    def __init__(self, configs):
        try:
            cache_file = open('markdeep.cache', 'r+')
            for line in cache_file.readlines():
                key, val = line.strip("\n").split("$")
                self.cached[key] = val
        except IOError:
            pass

        self.re_diagram = re.compile(r'<markdeep-diagram>[\n\r]*(?P<code>.*?)[\n\r]*</markdeep-diagram>', re.MULTILINE | re.DOTALL)


    def _diagram_to_svg(self, markdeep):
        """Generates a SVG representation of Diagram string"""
        import urlparse, urllib
        def path2url(path):
            return urlparse.urljoin(
              'file:', urllib.pathname2url(os.path.abspath(path)))

        # Generate the temporary file
        tempfile.tempdir = ""
        tmp_file_fd, path = tempfile.mkstemp()
        with open(path + ".html", "w") as fd:
            fd.write(self.markdeep_preamble.format(markdeep + " "))

        driver = webdriver.PhantomJS() # or add to your PATH
        driver.set_window_size(1024*2, 768*2) # optional
        driver.get(path2url(path + ".html"))
        ps = driver.page_source
        driver.quit()

        re_svg = re.compile("<svg.*?</svg>", re.MULTILINE | re.DOTALL)
        svg = re_svg.findall(ps)[0]

        fsvg = "%s.svg" % path
        fsvgo = "%s-opt.svg" % path

        with open(fsvg, "w") as f:
        	f.write(svg)

        cmd = "svgo --multipass %s %s" % (fsvg, fsvgo)
        status = call(cmd.split(), stdout=PIPE)

        # Read the png and encode the data
        svg = open(fsvgo, "rb")
        data = svg.read()
        svg.close()

        self._cleanup(path)

        return data

    def _cleanup(self, path, err=False):
        # don't clean up the log if there's an error
        extensions = ["", "-opt.svg", ".svg", ".html"]
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

        # Figure out our text strings and math-mode strings
        tex_expr = [(self.re_diagram, x) for x in self.re_diagram.findall(page)]

        # No sense in doing the extra work
        if not len(tex_expr):
            return page.split("\n")

        # Parse the expressions
        new_cache = {}
        id = 0
        for reg, expr in tex_expr:
            # print reg, mode, expr
            hash_expr = hashlib.sha1(expr).hexdigest()
            if hash_expr in self.cached:
                data = self.cached[hash_expr]
            else:
                print expr
                data = self._diagram_to_svg(expr)
                new_cache[hash_expr] = data
            id += 1
            diagram = DIAGRAM_EXPR.format(data)
            page = reg.sub(diagram, page, 1)

        # Cache our data
        cache_file = open('markdeep.cache', 'a')
        for key, value in new_cache.items():
            cache_file.write("%s$%s\n" % (key, value))
        cache_file.close()

        # Make sure to resplit the lines
        return page.split("\n")


class MarkdeepDiagramPostprocessor(markdown.postprocessors.Postprocessor):
        """This post processor extension just allows us to further
        refine, if necessary, the document after it has been parsed."""
        def run(self, text):
            # Inline a style for default behavior
            text = DIAGRAM_CSS + text
            return text


class MarkdeepDiagram(markdown.Extension):
    """Wrapper for LaTeXPreprocessor"""
    def extendMarkdown(self, md, md_globals):
        # Our base LaTeX extension
        md.preprocessors.add('markdeep',
                MarkdeepDiagramPreprocessor(self), ">html_block")
        # Our cleanup postprocessing extension
        md.postprocessors.add('markdeep',
                MarkdeepDiagramPostprocessor(self), ">amp_substitute")


def makeExtension(*args, **kwargs):
    """Wrapper for a MarkDeep extension"""
    return MarkdeepDiagram(*args, **kwargs)
