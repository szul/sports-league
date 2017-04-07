import web

VEMAIL = web.form.regexp(r".*@.*", "must be a valid email address")
