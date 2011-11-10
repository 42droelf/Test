#! /usr/bin/env python3
import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        if self.get_secure_cookie("mycookie"):
            self.write("Your secure cookie was set!")
            items = ["Item 1", "Item 2", "Item 3", "SECURE Cookie was set!"]
        else:
            self.set_secure_cookie("mycookie", "myvalue")
            self.write("Your SECURE cookie was not set!")
            items = ["Item 1", "Item 2", "Item 3", "SECURE Cookie was not set!"]
        self.render("template.html", title="My title", items=items)

application = tornado.web.Application([
    (r"/", MainHandler),
], cookie_secret="deimudda")

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
