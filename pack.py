# built-in
import argparse
from base64 import b64encode
import mimetypes
import re
import sys
import urllib.parse
import urllib.request
# external
from bs4 import BeautifulSoup


# init
mimetypes.init()


# main export
class Pack:

  @staticmethod
  def get_prefix(url, typ=None):
    if typ is None:
      typ, enc = mimetypes.guess_type(url)
      if typ is None:
        typ = 'application/octet-stream'
    return 'data:%s;base64,' % typ

  @staticmethod
  def should_datafy(url):
    return url is not None and url[:5].lower() != 'data:'

  @staticmethod
  def fetch(url):
    try:
      return urllib.request.urlopen(url).read()
    except Exception as ex:
      sys.stderr.write('Unable to fetch URL [%s]\n' % url)
      raise ex

  @staticmethod
  def datafy(url, data=None, mime=None):
    if data is None:
      data = Pack.fetch(url)
    return Pack.get_prefix(url, mime) + urllib.parse.quote_plus(b64encode(data))

  @staticmethod
  def datafy_css(url):
    content = Pack.fetch(url)
    css = str(content, 'utf-8')
    if 'url(' in css:
      pattern = '^.*:.*url\((.*?)\).*;.*$'
      lines = []
      for line in css.split('\n'):
        match = re.match(pattern, line)
        if match is None:
          lines.append(line)
        else:
          link = match.group(1)
          data = Pack.datafy(link)
          lines.append(re.sub('url\((.*?)\)', 'url(%s)' % data, line))
      content = '\n'.join(lines).encode('utf-8')
    return Pack.datafy(url, content, 'text/css')

  @staticmethod
  def pack(url):
    content = Pack.fetch(url)
    soup = BeautifulSoup(content, 'lxml')
    for tag in soup.find_all('link'):
      rel, href = tag.get('rel'), tag.get('href')
      if not Pack.should_datafy(href):
        continue
      if rel is not None and type(rel) is list and len(rel) == 1 and rel[0].lower() == 'stylesheet':
        tag['href'] = Pack.datafy_css(urllib.parse.urljoin(url, href))
      else:
        tag['href'] = Pack.datafy(urllib.parse.urljoin(url, href))
    for tag in soup.find_all('script') + soup.find_all('img'):
      src = tag.get('src')
      if not Pack.should_datafy(src):
        continue
      tag['src'] = Pack.datafy(urllib.parse.urljoin(url, src))
    return str(soup)


if __name__ == '__main__':
  # args and usage
  parser = argparse.ArgumentParser()
  parser.add_argument('url', type=str, help='url to pack')
  args = parser.parse_args()

  # pack
  html = Pack.pack(args.url)

  # write result to stdout
  print(html)
