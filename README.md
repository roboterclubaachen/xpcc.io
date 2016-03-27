# xpcc.io website and documentation

This repo contains the website, user guide and reference manual for the xpcc microcontroller framework.

This documentation is written in Markdown and uses MkDocs to generate HTML documents.
To get a live preview of the website while your editing, execute `mkdocs serve` and then point your browser to http://127.0.0.1:8000.

To build the website, execute `mkdocs build`, then `xpcc_doxygen.sh` to build and move the xpcc doxygen documentation into place.

The `site` folder contains the entire website and is all that is required to host xpcc.io.

The theme is [Material for MkDocs](http://squidfunk.github.io/mkdocs-material/), which is modified to replace the download button with a forks button.

### Markdown extensions

A couple of canonical extensions are enabled, like `tables` and `admonition`.

Two custom extensions are used to render both LaTeX and Markdeep into statically hosted, inlined SVG, which removes the need to include client-side Javascript rendering for either.
It makes the site load faster and works for browser not having Javascript enabled.
It also makes this site not require fetching some third party JS library, which might disappear in the future.

Note: These plugins were adapted without much love and are therefore very hacked together. We're here to write documentation, not plugins. Please feel free to make them nice.

#### LaTeX

Adapted from [here](https://github.com/justinvh/Markdown-LaTeX). It renders the LaTeX formula into inlined SVG.
Use $formula$ for math mode, or $$formula$$ for equations.
Note that a `latex.cache` file is used to not have to render everything again.

Required `pdflatex`, `pdfcrop`, `pdf2svg` and `svgo` command line tools installed.

#### Markdeep

To create beautiful geometric diagrams, this plugin renders markdeep diagrams into inline SVG.
You need to have Selenium install for it (`pip install selenium`).
Wrap the diagram in `<markdeep-diagram> </markdeep-diagram>` html tags.
