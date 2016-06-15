# What

**html-pkgr** converts a web page into a single, standalone HTML file. All linked resources are embedded within [data URIs](https://en.wikipedia.org/wiki/Data_URI_scheme). This project was inspired by the forgotten [standalone-html](https://github.com/jgm/standalone-html).

# How

**html-pkgr** scans the HTML document for `img`, `link`, `script`, and `iframe` tags, fetches the requisite resources, and replaces `href`/`scr` attributes with a data URIs. It also scans CSS files, replacing `url`s with data URIs.

# Caveats

 - Requires Python 3+
 - Requires [BeautifulSoup4](https://pypi.python.org/pypi/beautifulsoup4)
 - Converts URLs, not files (workaround: Python's SimpleHTTPServer)
 - Was written in an afternoon for one specific task; YMMV

# Todo

 - Case-insensitive tags and attributes
 - Use `referer` header when requesting resources

# Usage

python3 pack.py &lt;*URL*&gt; [&gt; *outfile*]

For example:
````bash
python3 pack.py "http://undefinedx.com" > undefinedx.html
````

See also the example folder.
