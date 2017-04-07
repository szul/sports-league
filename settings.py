import web
from filters import truncate_words, truncate_words_with_html, slugify

#template directory
#render = web.template.render('templates', base='master', globals={'truncate_words':truncate_words, 'truncate_words_with_html':truncate_words_with_html, 'slugify':slugify})
render = web.template.render(
  'templates',
  globals = {
    'truncate_words':truncate_words,
    'truncate_words_with_html':truncate_words_with_html,
    'slugify':slugify
  }
)
