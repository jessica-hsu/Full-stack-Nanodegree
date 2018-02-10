import os
import re
from string import letters

import webapp2
import jinja2


from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'template')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

secret = "shamidaigee" # taiwanese for "what is this?". Used to hash passwords

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

def render_post(response, post):
    response.out.write('<b>' + post.subject + '</b><br>')
    response.out.write(post.content)

def blog_key(name = 'default'):
    return db.Key.from_path('blogs', name)

# for securing values for registration
def make_secure_val(val):
    return "%s|%s" % (val, hmac.new(secret, val).hexigest())

# making sure secure value is valid
def check_secure_val(secure_val):
    val = secure_val.split("|")[0]
    if secure_val == make_secure_val(val):
        return val

# functions for hashing passwords
# make salt, a random string with x letters
def make_salt(length=5):
    return ''.join(random.choice(letters) for x in xrange(length))

# hash the password
def hash_password(name, pd, salt=None):
    if not salt:
        salt = make_salt()
    hashed_pd = hashlib.sha256(name+pd+salt).hexdigest()
    return '%s, %s' % (salt, hashed_pd) # return salt and the hased name+pass_salt. store in db later

# check if password is valid
def valid_password(name, password, hashed_pd):
    the_salt = hashed_pd.split(',')[0]
    if (hashed_pd == hash_password(name, password, the_salt)):
        return True
    else:
        return False

class BlogHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        return render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    # cookie setting
    def set_cookie(self, name, val):
        cookie_value = make_secure_val(val)
        self.response.headers.add_header(
            "Set-Cookie",
            "%s=%s; Path=/" % (name, cookie_value)
        )

    # read cookie. Check to see if exists
    def read_cookie(self, name):
        cookie_value = self.request.cookies.get(name) # get cookie according to name
        if (check_secure_val(cookie_value)): # return cookie if cookie exists and is secure
            return cookie_value

    # set cookie during login for user
    def login():
        self.set_cookie('user_id', str(user.key().id()))

    # check to see if user is logged in
    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_cookie("user_id")
        self.user = uid and User.by_id(int(uid))

# create User objects to store different users. Also have methods for this class objects
class User (db.Model):
    # object properties
    name = db.StringProperty(required = True)
    hashed_pw = db.StringProperty(required = True)
    email = db.StringProperty()

    # class method: method to look up a user by ID
    @classmethod
    def getById(cls, uid):
        return User.getUserById(uid, parent = users_key())

    # class method: look up a user by names
    @classmethod
    def getByName(cls, name):
        user = User.all().filter('name =', name).get()  # database lookup. select * from user where name = name
        return user

    # creates new user and adds to database
    @classmethod
    def register(cls, name, password, email = None):
        hashed_pw = make_pw_hash(name, password)     # hash the password
        # create new user object and return it
        u = User(parent = users_key(),
                 name = name,
                 hashed_pw = hashed_pw,
                 email = email)
        return u

    # logs user in
    @classmethod
    def login(cls, name, password):
        user = getByName(name)
        valid = valid_password(name, password, user.hashed_pw)
        if (user and valid):    # user must exist and password must be valid
            return user



# instance called "ENTRY" (record) with the following "entities" (columns) and data type
class Entry(db.Model):
    title = db.StringProperty(required = True)
    blog_text = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("view-entry.html", p = self)

# Render main page that appears with first page load
class MainPage(BlogHandler):
  def get(self):
      self.render("/index.html")

# Render welcome page after sign in
class Welcome(BlogHandler):
    def get(self):
        username = self.request.get('username')
        if valid_username(username):
            self.render('welcome.html', username = username)
        else:
            self.redirect('/register')

# Render blog's front page
class BlogFront(BlogHandler):
    def get(self):
        username = self.request.get('username')
        if valid_username(username):
            logged = True
        else:
            logged = False
        posts = db.GqlQuery("select * from Entry order by created desc limit 10")
        self.render('front-page.html', posts = posts, is_logged = logged)

# Render something...
class PostPage(BlogHandler):
    def get(self, post_id):
        key = db.Key.from_path('Entry', int(post_id), parent=blog_key())
        post = db.get(key)

        if not post:
            self.error(404)
            return

        self.render("permalink.html", post = post)

# Render page to write new entries
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



# Render sign up page
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

    # if registration was successful
    def done(self):

# Render login page
class Login(BlogHandler):
    def get(self):
        self.render("sign-in.html")

    # get username and password and authenticate
    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        user = User.login(username, password)
        if (user):  #redirect to welcome page if login successful
            self.login(user)
            self.redirect('/welcome')
        else:   # login failed, display error message
            message = "Username or password invalid."
            self.render("sign-in.html", error_message = message)

# Does the logout process
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
