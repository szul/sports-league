import web
from settings import render
from models import Users
from validation import VEMAIL

class users:
  def GET(self):
    u = web.ctx.orm.query(Users).all()
    return render.users_listing(u)

class users_select:
  def GET(self, user):
    u = web.ctx.orm.query(Users).filter_by(username = user).first()
    return render.users_view(u)

class users_new:
  f = web.form.Form(
      web.form.Checkbox("active", description="active", value="on"),
      web.form.Textbox("firstname", description="firstname"),
      web.form.Textbox("lastname", description="lastname"),
      web.form.Textbox("username", description="username"),
      web.form.Textbox("email", VEMAIL, description="email"),
      web.form.Password("password", description="password"),
      web.form.Password("password_confirm", description="confirm"),
      web.form.Button("submit", type="submit", description="save"),
      validators = [
        web.form.Validator("Passwords didn't match.", lambda i: i.password == i.password_confirm)
      ]
    )
  f.action = 'new'
  def GET(self):
    return render.users_form(self.f)
  def POST(self):
    if not self.f.validates():
      return render.users_form(self.f)
    u = Users(
              active = self.f.d.active,
              firstname = self.f.d.firstname,
              lastname = self.f.d.lastname,
              username = self.f.d.username,
              email = self.f.d.email,
              password = self.f.d.password
            )
    web.ctx.orm.add(u)
    raise web.seeother('/users/')

class users_edit:
  f = web.form.Form(
      web.form.Hidden("id", description="hidden"),
      web.form.Checkbox("active", description="active", value="on"),
      web.form.Textbox("firstname", description="firstname"),
      web.form.Textbox("lastname", description="lastname"),
      web.form.Textbox("username", description="username"),
      web.form.Textbox("email", VEMAIL, description="email"),
      web.form.Password("password", description="password"),
      web.form.Password("password_confirm", description="confirm"),
      web.form.Button("submit", type="submit", description="save"),
      validators = [
        web.form.Validator("Passwords didn't match.", lambda i: i.password == i.password_confirm)
      ]
    )
  f.action = 'edit'
  def GET(self, id):
    u = web.ctx.orm.query(Users).filter_by(id = id).first()
    u.password = ''
    self.f.fill(u)
    return render.users_form(self.f)
  def POST(self):
    if not self.f.validates():
      return render.users_form(self.f)
    u = web.ctx.orm.query(Users).filter_by(id = self.f.d.id).first()
    u.active = self.f.d.active
    u.firstname = self.f.d.firstname
    u.lastname = self.f.d.lastname
    u.username = self.f.d.username
    u.email = self.f.d.email
    u.password = self.f.d.password
    web.ctx.orm.commit()
    raise web.seeother('/users/')

class users_delete:
  def GET(self, id):
    u = web.ctx.orm.query(Users).filter_by(id = id).first()
    web.ctx.orm.delete(u)
    raise web.seeother('/users/')
