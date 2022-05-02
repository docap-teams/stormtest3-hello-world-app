from behave import *
import json

@given(u'micro is setup')
def flask_setup(context):
    assert context.client

@when(u'we call the api without a parameter')
def call_api(context):
    context.response = context.client.get('/api/hello/')
    assert context.response.status_code == 200

@then(u'micro will present Hello World!')
def step_impl(context):
    body = json.loads(str(context.response.data, 'utf8'))
    #print(body)
    assert body['Hello'] == 'World!'

@when(u'we call the api with parameter "{name}"')
def call_api(context, name):
    context.response = context.client.get('/api/hello/' + name)
    #print(context.response)
    assert context.response.status_code == 200

@then(u'micro will present Hello "{name}"')
def step_impl(context, name):
    #print(context.response.data)
    body = json.loads(str(context.response.data, 'utf8'))
    #print(body)
    assert body['Hello'] == name
