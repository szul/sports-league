import web
from settings import render
from models import Sports

class sports:
  def GET(self):
    s = web.ctx.orm.query(Sports).all()
    return render.sports_listing(s)

class sports_select:
  def GET(self, sport):
    s = web.ctx.orm.query(Sports).filter_by(name = sport).first()
    return render.sports_view(s)

class sports_new:
  f = web.form.Form(
      web.form.Checkbox("active", description="active", value="on"),
      web.form.Textbox("name", web.form.notnull, description="name"),
      web.form.Button("submit", type="submit", description="save")
    )
  f.action = 'new'
  def GET(self):
    return render.sports_form(self.f)
  def POST(self):
    if not self.f.validates():
      return render.sports_form(self.f)
    s = Sports(
              active = self.f.d.active,
              name = self.f.d.name
            )
    web.ctx.orm.add(s)
    raise web.seeother('/sports/')

class sports_edit:
  f = web.form.Form(
      web.form.Hidden("id", description="hidden"),
      web.form.Checkbox("active", description="active", value="on"),
      web.form.Textbox("name", web.form.notnull, description="name"),
      web.form.Button("submit", type="submit", description="save")
    )
  f.action = 'edit'
  def GET(self, id):
    s = web.ctx.orm.query(Sports).filter_by(id = id).first()
    self.f.fill(s)
    return render.sports_form(self.f)
  def POST(self):
    if not self.f.validates():
      return render.sports_form(self.f)
    s = web.ctx.orm.query(Sports).filter_by(id = self.f.d.id).first()
    s.active = self.f.d.active
    s.name = self.f.d.name
    web.ctx.orm.commit()
    raise web.seeother('/sports/')

class sports_delete:
  def GET(self, id):
    s = web.ctx.orm.query(Sports).filter_by(id = id).first()
    web.ctx.orm.delete(s)
    raise web.seeother('/sports/')
