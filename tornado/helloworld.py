#! /usr/bin/env python3

import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('<html><body>Dein Name: <form action="/" method="post">'
                   '<input type="text" name="message">'
                   '<input type="submit" value="Submit"'
                   '</form></body></html>')
    def post(self):
        self.redirect('/story/21')
#        self.set_header("Content-Type", "text/plain")
#        self.write("You wrote {0}".format(self.get_argument("message")))

class StoryHandler(tornado.web.RequestHandler):
    def get(self, story_id):
        self.write("You requested the story {0}".format(story_id))

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/story/([0-9]+)", StoryHandler)
])

if __name__ == "__main__":
   application.listen(8888)
   tornado.ioloop.IOLoop.instance().start()
