import re, unicodedata

def truncate_words(s, num, end_text='...'):
  length = int(num)
  words = s.split()
  if len(words) > length:
    words = words[:length]
    if not words[-1].endswith(end_text):
      words.append(end_text)
  return u' '.join(words)

def truncate_words_with_html(s, num, end_text='...'):
  length = int(num)
  if length <= 0:
    return u''
  html4_singlets = ('br', 'col', 'link', 'base', 'img', 'param', 'area', 'hr', 'input')
  re_words = re.compile(r'&.*?;|<.*?>|(\w[\w-]*)', re.U)
  re_tag = re.compile(r'<(/)?([^ ]+?)(?: (/)| .*?)?>')
  pos = 0
  end_text_pos = 0
  words = 0
  open_tags = []
  while words <= length:
    m = re_words.search(s, pos)
    if not m:
      break
    pos = m.end(0)
    if m.group(1):
      words += 1
      if words == length:
        end_text_pos = pos
      continue
    tag = re_tag.match(m.group(0))
    if not tag or end_text_pos:
      continue
    closing_tag, tagname, self_closing = tag.groups()
    tagname = tagname.lower()
    if self_closing or tagname in html4_singlets:
      pass
    elif closing_tag:
      try:
        i = open_tags.index(tagname)
      except ValueError:
        pass
      else:
        open_tags = open_tags[i+1:]
    else:
      open_tags.insert(0, tagname)
  if words <= length:
    return s
  out = s[:end_text_pos]
  if end_text:
    out += ' ' + end_text
  for tag in open_tags:
    out += '</%s>' % tag
  return out

def slugify(value):
  value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
  value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
  return re.sub('[-\s]+', '-', value)
