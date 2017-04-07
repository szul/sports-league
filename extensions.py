from web.template import Template

class RenderFromPath(object):
  def __init__(self, obj):
    self.obj = obj
  def load(self, path):
    t = self.obj._template(path)
    if self.obj._base and isinstance(t, Template):
        def template(*a, **kw):
            return self.obj._base(t(*a, **kw))
        return template()
    else:
        return self.obj._template(path)
  def __getattr__(self, attr):
    return getattr(self.obj, attr)
