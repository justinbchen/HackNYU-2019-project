import webapp2
import jinja2
import os
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
        content =  TEMPLATE.get_template('/templates/homepage.html')
        self.response.write(content.render())
        q = FoodType.query().fetch()

        run = False

        for item in q:
            if item.name == "beef":
                run = True
                break
        if run:
            food_type = FoodType(
                Name = "beef",
                Meat = True,
                Carbon = 13300,
                Water = 15415
            )
            food_type.put()
            food_type = FoodType(
                Name = "pork",
                Meat = True,
                Carbon = 3250,
                Water = 5988
            )
            food_type.put()
            food_type = FoodType(
                Name = "chicken",
                Meat = True,
                Carbon = 3500,
                Water = 4325
            )
            food_type.put()
            food_type = FoodType(
                Name = "vegetables",
                Meat = False,
                Carbon = 2000,
                Water = 322
            )
            food_type.put()
            food_type = FoodType(
                Name = "fruits",
                Meat = False,
                Carbon = 400,
                Water = 962
            )
            food_type.put()
            food_type = FoodType(
                Name = "baked",
                Meat = False,
                Carbon = 700,
                Water = 4482
            )
            food_type.put()

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
    Carbon = ndb.FloatProperty() #footprint in g CO2 / kg food
    Water = ndb.FloatProperty() #footprint in L water / kg food

class FoodItem(ndb.Model):
    Name = ndb.StringProperty() #name of food
    Ingredients = ndb.StringProperty(repeated = True) #list of ingredients by food type

app = webapp2.WSGIApplication([
  ('/', HomePage),
  ('/login', MainHandler),
  ('/logout', LogoutHandler),
  ('/signIn', LoginHandler)
], debug=True)
