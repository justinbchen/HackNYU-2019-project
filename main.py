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
		print ("Here")

class User(ndb.Model):
	first_name = ndb.StringProperty()
	last_name = ndb.StringProperty()
	username = ndb.StringProperty()
	email = ndb.StringProperty()
	password = ndb.StringProperty()
	confirm_password = ndb.StringProperty()
	location = ndb.StringProperty()
	user_library = ndb.StringProperty(repeated = True)

class MainHandler(webapp2.RequestHandler):
	def get(self):
		print ("Here")
	def post(self):
		print ("Here")

class LoginHandler(webapp2.RequestHandler):
	def get(self):
		content = TEMPLATE.get_template('') # This set the template for the page
		self.response.write(content.render())

	def post(self):
		print ("Here")

class LogoutHandler(webapp2.RequestHandler):
	def get(self):
		print ("Here")



class UserInput(webapp2.RequestHandler):
	def get(self):
		content = TEMPLATE.get_template('/templates/UserInput.html')
		self.response.write(content.render(title = "book variable"))
		# print "Class is functional"


class FoodType(ndb.Model):
    Name = ndb.StringProperty() #name of food type
    Meat = ndb.BooleanProperty() #meat or non meat
	Carbon = nbd.FloatProperty() #footprint in g CO2 / kg food
	Water = nbd.FloatProperty() #footprint in L water / kg food

class FoodItem(ndb.Model):
    Name = ndb.StringProperty() #name of food
    Ingredients = nbd.ListProperty(FoodType) #list of ingredients by food type

app = webapp2.WSGIApplication([
  ('/', HomePage),
  ('/login', MainHandler),
  ('/logout', LogoutHandler),
  ('/signIn', LoginHandler)
], debug=True)
