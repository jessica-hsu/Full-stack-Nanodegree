import os
import re
from string import letters

import webapp2
import jinja2


from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'template')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

def render_post(response, post):
    response.out.write('<b>' + post.subject + '</b><br>')
    response.out.write(post.content)

def blog_key(name = 'default'):
    return db.Key.from_path('blogs', name)

class BlogHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        return render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

#instance called "ENTRY" (record) with the following "entities" (columns) and data type
class Entry(db.Model):
    title = db.StringProperty(required = True)
    blog_text = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("view-entry.html", p = self)

#Render main page that appears with first page load
class MainPage(BlogHandler):
  def get(self):
      self.render("/index.html")

#Render welcome page after sign in
class Welcome(BlogHandler):
    def get(self):
        username = self.request.get('username')
        if valid_username(username):
            self.render('welcome.html', username = username)
        else:
            self.redirect('/register')

#Render blog's front page
class BlogFront(BlogHandler):
    def get(self):
        username = self.request.get('username')
        if valid_username(username):
            logged = True
        else:
            logged = False
        posts = db.GqlQuery("select * from Entry order by created desc limit 10")
        self.render('front-page.html', posts = posts, is_logged = logged)

#Render something...
class PostPage(BlogHandler):
    def get(self, post_id):
        key = db.Key.from_path('Entry', int(post_id), parent=blog_key())
        post = db.get(key)

        if not post:
            self.error(404)
            return

        self.render("permalink.html", post = post)

#Render page to write new entries
class NewEntry(BlogHandler):
    def get(self):
        self.render("new-entry.html")

    def post(self):
        #grab data from form submit
        title = self.request.get('title')
        blog_text = self.request.get('blog_text')

        #create record and insert to database
        if subject and content:
            p = Entry(parent = blog_key(), title = title, blog_text = blog_text)
            p.put()
            self.redirect('/blog/%s' % str(p.key().id()))
        else:
            error = "subject and content, please!"
            self.render("new-entry.html", title=title, blog_text=blog_text, error=error)



#Render sign up page
class Register(BlogHandler):
    def get(self):
        self.render("register.html")

    def post(self):
        have_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        params = dict(username = username,
                      email = email)

        if not valid_username(username):
            params['error_username'] = "That's not a valid username."
            have_error = True

        if not valid_password(password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True
        elif password != verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not valid_email(email):
            params['error_email'] = "That's not a valid email."
            have_error = True

        if have_error:
            self.render('register.html', **params)
        else:
            self.redirect('/welcome?username=' + username)

#Render login page
class Login(BlogHandler):
    def get(self):
        self.render("sign-in.html")

#Does the logout process
#class Logout(BlogHandler):


app = webapp2.WSGIApplication([('/', MainPage),
                               ('/welcome', Welcome),
                               ('/blog/?', BlogFront),
                               ('/blog/([0-9]+)', PostPage),
                               ('/blog/newentry', NewEntry),
                               ('/register', Register),
                               ('/login', Login)#,
                               #('/logout', Logout)
                               ],
                              debug=True)
