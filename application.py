import web
from settings import render
from filters import truncate_words, truncate_words_with_html, slugify
from extensions import RenderFromPath
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *
from sports import *
from users import *
from profiles import *

urls = (
  '/([^\/]+)', 'redirect',
  '/', 'index',
  #users
  '/u:(\w+)/','users_select',
  '/users/edit/(\d+)', 'users_edit',
  '/users/edit/', 'users_edit',
  '/users/delete/(\d+)', 'users_delete',
  '/users/new/', 'users_new',
  '/users/', 'users',
  #sports
  '/s:(\w+)/','sports_select',
  '/sports/edit/(\d+)', 'sports_edit',
  '/sports/edit/', 'sports_edit',
  '/sports/delete/(\d+)', 'sports_delete',
  '/sports/new/', 'sports_new',
  '/sports/', 'sports',
  '/(.+)/', 'static'
)

#controller code
class redirect:
  def GET(self, path):
    web.seeother('/' + path + '/')

class index:
  def GET(self):
    return render.index()

class static:
  def GET(self, path):
    try:
      static_render = RenderFromPath(render)
      return static_render.load(path)
    except:
      raise web.notfound(render.notfound())

#def internalerror():
#    return web.internalerror(render.servererror())

def load_sqla(handler):
    web.ctx.orm = scoped_session(sessionmaker(bind = engine))
    try:
        return handler()
    except web.HTTPError:
       web.ctx.orm.commit()
       raise
    except:
        web.ctx.orm.rollback()
        raise
    finally:
        web.ctx.orm.commit()
        # If the above alone doesn't work, uncomment 
        # the following line:
        #web.ctx.orm.expunge_all() 

#create application
application = web.application(urls, globals())
#application = web.application(urls, globals(), True)
#application.internalerror = internalerror
application.add_processor(load_sqla)

#run application
if __name__ == "__main__":
    application.run()
