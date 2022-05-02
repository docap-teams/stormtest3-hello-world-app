# load our application
from app import app as tested_app

# before a feature 
# get the client and bind it to the context so we can pass it to our tests
def before_feature(context, feature):
    context.client = tested_app.test_client()

# don't do anything after a feature
def after_feature(context, feature):
    pass
