#! /usr/bin/env python3

import tornado.ioloop
import tornado.web
import os
import blog

class EntryManager:
    def __init__(self, filename):
        self.filename = filename
        self.entries = []
        self.open()

    def open(self):
        with open(self.filename, "r") as f:
            while True:
                topic = f.readline()
                if len(topic) == 0: # End of File
                    break
                content = f.readline()
                self.entries.append((topic, content))

    def save(self, topic, content):
        self.entries.append((topic, content))
        with open(self.filename, "a") as f:
            f.write(topic)
            f.write(os.linesep)
            f.write(content)
            f.write(os.linesep)

    def getEntries(self):
        return self.entries[::-1] # newest Entry at top

class EntryModule(tornado.web.UIModule):
    def render(self, entry):
        return self.render_string("entry.html", topic=entry[0], content=entry[1])

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

class InternHandler(BaseHandler):
    def get(self):
        if not self.current_user:
                self.redirect("/login")
                return
        self.render("intern.html", title="goto: intern")

    def post(self):
        entryManager.save(self.get_argument("topic"), self.get_argument("content"))
        self.redirect("/")

class LoginHandler(BaseHandler):
    def get(self):
        self.render("login.html", title="goto: login")

    def post(self):
        self.set_secure_cookie("user", self.get_argument("username"))
        self.redirect("/intern")

class MainHandler(tornado.web.RequestHandler):
    def get(self):
#        self.write("Hello, world!")
#        for topic, content in entryManager.getEntries():
#            self.write("<br><b>{0}</b><br>{1}<br>".format(topic, content))
#        self.write('<div align="right"><a href="/intern">Intern</a><div>')
        entries = entryManager.getEntries()
        self.render("blog.html", title="goto: blog", entries=entries)

settings = { 
    "ui_modules": blog,
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "debug": True,
    "cookie_secret": "ß90uihbß0",
    "xsrf_cookies": True,             
}

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/login", LoginHandler),
    (r"/intern", InternHandler),
    ], **settings)

entryManager = EntryManager("entries.txt")

if __name__ == "__main__":
    application.listen(8888) # localhost:8888
    tornado.ioloop.IOLoop.instance().start()
