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

        run = True
        for item in q:
            if item.Name == "beef":
                run = False
                break
        if run:
            food_type = FoodType(
                Name = "beef",
                Carbon = 13300,
                Water = 15415
            )
            food_type.put()
            food_type = FoodType(
                Name = "pork",
                Carbon = 3250,
                Water = 5988
            )
            food_type.put()
            food_type = FoodType(
                Name = "chicken",
                Carbon = 3500,
                Water = 4325
            )
            food_type.put()
            food_type = FoodType(
                Name = "vegetables",
                Carbon = 2000,
                Water = 322
            )
            food_type.put()
            food_type = FoodType(
                Name = "fruits",
                Carbon = 400,
                Water = 962
            )
            food_type.put()
            food_type = FoodType(
                Name = "baked",
                Carbon = 700,
                Water = 4482
            )
            food_type.put()
    def post(self):
        content =  TEMPLATE.get_template('/templates/homepage.html')
        self.response.write(content.render())
        self.response.write("""
        <table style="width:70%">""")

        for item in q:
            self.response.write("""
            <tr>
                <th>"""item.Name"""</th>
                <th>"""item.Carbon""" g CO2 / Kg of Food </th>
                <th>"""item.Water""" L H2O / Kg of FoodItem</th>
            </tr>
            """)

        self.response.write("""
        </table>
        """)
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



class NewItemHandler(webapp2.RequestHandler):
    def get(self):
        print ("Getting new item");

class NewTypeHandler(webapp2.RequestHandler):
    def get(self):
        content = TEMPLATE.get_template('/templates/newType.html')
        self.response.write(content.render())
    def post(self):
        content = TEMPLATE.get_template('/templates/newType.html')
        self.response.write(content.render())
        value = False
        food_type = FoodType(
            Name = self.request.get('foodname'),
            Carbon = float(self.request.get('carbon')),
            Water = float(self.request.get('water'))
        )
        q = FoodType.query().fetch()
        put = True
        for item in q:
            if food_type.Name is item.Name:
                put = False
        if put:
            food_type.put()

        self.redirect('/')


class FoodType(ndb.Model):
    Name = ndb.StringProperty() #name of food type
    # Meat = ndb.BooleanProperty() #meat or non meat
    Carbon = ndb.FloatProperty() #footprint in g CO2 / kg food
    Water = ndb.FloatProperty() #footprint in L water / kg food

class FoodItem(ndb.Model):
    Name = ndb.StringProperty() #name of food
    Ingredients = ndb.StringProperty(repeated = True) #list of ingredients by food type

app = webapp2.WSGIApplication([
  ('/', HomePage),
  ('/login', MainHandler),
  ('/logout', LogoutHandler),
  ('/signIn', LoginHandler),
  ('/newItem', NewItemHandler),
  ('/newType', NewTypeHandler)
], debug=True)
