import webapp2
import jinja2
import os
from books import *
from google.appengine.api import users
from google.appengine.ext import ndb
import logging
from time import sleep



TEMPLATE = jinja2.Environment(
	loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions = ['jinja2.ext.autoescape'],
	autoescape = True
)



class HomePage(webapp2.RequestHandler):

	def get(self):
		books = Books.query().fetch()
		if len(books) == 0:
			BookLoader()
		content = TEMPLATE.get_template('/templates/home.html')

		if self.request.cookies.get("logged_in") == "True":
			self.response.write(content.render(active = True))
		else:
			self.response.write(content.render(login = True))


class CssiUser(ndb.Model):

  	first_name = ndb.StringProperty()
  	last_name = ndb.StringProperty()
	username = ndb.StringProperty()
	email = ndb.StringProperty()
	password = ndb.StringProperty()
	confirm_password = ndb.StringProperty()
	location = ndb.StringProperty()
	user_library = ndb.StringProperty(repeated = True)

class PersonalLibrary(webapp2.RequestHandler):
	def get(self):
		print "At Library"
		# content = TEMPLATE.get_template('/templates/library.html')
		content = TEMPLATE.get_template('/templates/book.html')

		self.response.write("""
		<html lang="en" dir="ltr">
		  <head>
		    <link rel="image_src" href="back-end/faveicon.ico">
			<link href="/css/bootstrap.min.css" rel="stylesheet">
		    <link href="https://fonts.googleapis.com/css?family=Orbitron|Russo+One" rel="stylesheet">
		    <link href="https://fonts.googleapis.com/css?family=Ubuntu" rel="stylesheet">
			<link rel="stylesheet" type="text/css" href="css/main.css">
		    <link href="/css/cover.css" rel="stylesheet">
		    <title>readSmart</title>
		    <link rel="shortcut icon" type="image/x-icon" href="/img/logo2.png"/>
		  </head>
		  <body>
		    <div class="cover-container d-flex w-100 h-100 p-3 mx-auto flex-column">
		      <header class="masthead mb-auto">
		        <div class="inner">
				<a href="/"> <img class= "masthead-brand" style = "width: 220px; height: 60px;" src="/img/logo.png" alt="Logo"> </a>
				<nav class="nav nav-masthead justify-content-right">
					<a class="nav-link" style = "font-size: 24px;" href="/login">Home</a>
					<a class="nav-link" style = "font-size: 24px;" href="/booklist">Books</a>
					<a class="nav-link active" style = "font-size: 24px;" href = "/library">Library</a>
					<a class="nav-link" style = "font-size: 24px;" href = "/logout">Logout</a>
				</nav>
		          </nav>
		        </div>
		      </header>
			  <div id = book_container">
		""")

		q = CssiUser.query().fetch()
		books = Books.query().fetch()
		user = self.request.cookies.get("user")
		for item in q:
			if item.username == user:
				for value in item.user_library:
					for book in books:
						if value == book.title:
							if book.user_created == "yes":
								print "Item Created By User"
								s = str(book.image_file).encode('base64')
								print s
								self.response.write(content.render(title = book.title, s = s, author = book.author, user = True, code = False, library = True))
							else:
								print "Item hardcoded"
								self.response.write(content.render(title = book.title, id = book.id, author = book.author, code = True, user = False, library = True))
				self.response.write("""
					</div>
					<footer class="mastfoot mt-auto">
					<div class="inner">
					<p>readSmart&copy; Federick Gonzalez, Casey Mook, and Jaylen Patterson</p>
					</div>
					</footer>
				""")
				return
	def post(self):
		print "Post method called"
		q = CssiUser.query().fetch()
		user = self.request.cookies.get("user")
		for item in q:
			print item
			if item.username == user:
				print item
				book = self.request.get("book")
				print book
				if book in item.user_library:
					sleep(.5)
					self.redirect('/library')
				else:
					item.user_library.append(book)
					item.put()
					sleep(.5)

					self.redirect('/library')


class MainHandler(webapp2.RequestHandler):
	def get(self):
    # user = users.get_current_user()
		content = TEMPLATE.get_template('/templates/signup.html')
		if self.request.get('error') == 'True':
			self.response.write(content.render(failure = True, passwords_do_not_match = True))
			return
		else:
			if self.request.cookies.get("logged_in") == "True":
				self.response.write(content.render(success = True, user = self.request.cookies.get("user")))
			else:
				self.response.write(content.render(failure = True))


 	def post(self):
		# logged_in = True
		content = TEMPLATE.get_template('/templates/signup.html')
	  	cssi_user = CssiUser(
	       	first_name=self.request.get('firstname'),
	       	last_name=self.request.get('lastname'),
			username = self.request.get('Username'),
		    email = self.request.get('Email'),
			confirm_password = self.request.get('Confirm password'),
		    password = self.request.get('Password'),
		    location = self.request.get('location'))
		print cssi_user.confirm_password
		print cssi_user.password
		if cssi_user.confirm_password == cssi_user.password:
			cssi_user.put()
			self.response.set_cookie("logged_in", "True")
			self.response.set_cookie("user", cssi_user.username)
			self.response.write(content.render(success = True, user = cssi_user.first_name))
			return
		else:
			self.redirect('/login?error=True')

class LoginHandler(webapp2.RequestHandler):
	def get(self):
		content = TEMPLATE.get_template('/templates/signIn.html')
		self.response.write(content.render(start = True, error=False))

	def post(self):
		username = self.request.get("Username")
		password = self.request.get("Password")
		#content = TEMPLATE.get_template('/templates/signup.html')

		# user_key =  CssiUser.all()
		user_signed_in = False
		q = CssiUser.query().fetch()
		for user in q:
			if (user.username == username and user.password == password) or (user.email == username and user.password == password):
				# logged_in = True
				self.response.set_cookie("logged_in", "True")
				self.response.set_cookie("user", user.username)
				self.response.clear()
				user_signed_in = True
				break
				# self.response.write(content.render(success = True, user = user.first_name))
				# return
			if user.username != username or user.password != password or user.email != username:
				user_signed_in = False
				self.response.delete_cookie("logged_in")
				self.response.delete_cookie("user")


		if not user_signed_in:
			content = TEMPLATE.get_template('/templates/signIn.html')
			self.response.write(content.render(start = True, error = True, Username = username, Password = password))
		else:
			self.redirect("/login")

		# ndb.Query()
		# q.filter("username = ", self.response.get("Username"))
		# print q

class LogoutHandler(webapp2.RequestHandler):
	def get(self):
		self.response.delete_cookie("logged_in")
		self.response.delete_cookie("user")

		self.redirect('/')




class UserInput(webapp2.RequestHandler):
	def get(self):
		content = TEMPLATE.get_template('/templates/UserInput.html')
		self.response.write(content.render(title = "book variable"))
		# print "Class is functional"



def average(persons_input, title):
	b = Books.query().fetch()
	for book in b:
		if b.title == title:
			book_length = persons_input
			book_length = int(book_length)
			b.bookindex.append(book_length)

class RemoveBookHandler(webapp2.RequestHandler):
	def post(self):
		book = self.request.get("booktitle")
		username = self.request.cookies.get("user")
		q = CssiUser.query().filter(CssiUser.username == username).get()
		self.response.write(book)
		q.user_library.remove(book)
		q.put()
		sleep(.5)
		self.redirect('/library')

app = webapp2.WSGIApplication([
  ('/', HomePage),
  ('/login', MainHandler),
  ('/logout', LogoutHandler),
  ('/signIn', LoginHandler),
  ('/input', UserInput),
  ('/booklist', BookHandler),
  ('/bookview', BookView),
  ('/library', PersonalLibrary),
  ('/addBooks', AddBookHandler),
  ('/removebooks', RemoveBookHandler)
], debug=True)
