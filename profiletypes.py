import web
from settings import render
from models import ProfileTypes

class profiletypes:
  def GET(self):
    pt = web.ctx.orm.query(ProfileTypes).all()
    return render.profiletypes_listing(pt)

class profiletypes_select:
  def GET(self, id):
    pt = web.ctx.orm.query(ProfileTypes).filter_by(id = id).first()
    return render.profiletypes_view(pt)

class profiletypes_new:
  f = web.form.Form(
      web.form.Checkbox("active", description="active", value="on"),
      web.form.Textbox("name", description="name"),
      web.form.Button("submit", type="submit", description="save")
    )
  f.action = 'new'
  def GET(self):
    return render.profiletypes_form(self.f)
  def POST(self):
    if not self.f.validates():
      return render.users_form(self.f)
    pt = ProfileTypes(
              active = self.f.d.active,
              name = self.f.d.name
            )
    web.ctx.orm.add(pt)
    raise web.seeother('/profiletypes/')

class profiletypes_edit:
  f = web.form.Form(
      web.form.Checkbox("active", description="active", value="on"),
      web.form.Textbox("name", description="name"),
      web.form.Button("submit", type="submit", description="save")
    )
  f.action = 'edit'
  def GET(self, id):
    pt = web.ctx.orm.query(ProfileTypes).filter_by(id = id).first()
    self.f.fill(pt)
    return render.profiletypes_form(self.f)
  def POST(self):
    if not self.f.validates():
      return render.profiletypes_form(self.f)
    pt = web.ctx.orm.query(ProfileTypes).filter_by(id = self.f.d.id).first()
    u.active = self.f.d.active
    u.name = self.f.d.name
    web.ctx.orm.commit()
    raise web.seeother('/profiletypes/')

class profiletypes_delete:
  def GET(self, id):
    pt = web.ctx.orm.query(ProfileTypes).filter_by(id = id).first()
    web.ctx.orm.delete(pt)
    raise web.seeother('/profiletypes/')
