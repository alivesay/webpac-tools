"""Provides RESTful web service interface to WebPACSession."""

__author__ = "Andrew Livesay <andrewl@multco.us>"
__license__ = "Public Domain"

from bottle import abort, request, response, route, run
import json
import os
from WebPACSession import WebPACSession


CATALOG_URL = 'https://catalog.example.com'


@route('/change_pin', method='PUT')
def change_pin():
  data = request.body.readline()
 
  if not data:
    response.status = 400
    return { 'error': 'no data found' }
 
  entity = json.loads(data)
  
  if not set(('code', 'pin', 'new_pin')) <= set(entity):
    response.status = 400
    return { 'error': 'missing required keys' }

  try:
    wbsession = WebPACSession(CATALOG_URL)
    wbsession.login(entity['code'], entity['pin'])
    wbsession.change_pin(entity['pin'], entity['new_pin'])

  except Exception as e:
    if str(e) == 'login failed':
      response.status = 401
    else:
      response.status = 400
    return { 'error': str(e) }


@route('/modify_contact_info', method='PUT')
def modify_contact_info():
  data = request.body.readline()
 
  if not data:
    response.status = 400
    return { 'error': 'no data found' }
 
  entity = json.loads(data)
  
  if not set(('code', 'pin', 'address_line_1', 'address_line_2', 'telephone', 'email', 'location_code')) <= set(entity):
    response.status = 400
    return { 'error': 'missing required keys' }

  try:
    wbsession = WebPACSession(CATALOG_URL)
    wbsession.login(entity['code'], entity['pin'])
    wbsession.modify_contact_info(entity['address_line_1'], entity['address_line_2'],
                                  entity['telephone'], entity['email'], entity['location_code'])

  except Exception as e:
    if str(e) == 'login failed':
      response.status = 401
    else:
      response.status = 400
    return { 'error': str(e) }


@route('/register', method='PUT')
def register():
  data = request.body.readline()
 
  if not data:
    response.status = 400
    return { 'error': 'no data found' }
 
  entity = json.loads(data)
  
  if not set(('first_name', 'middle_name', 'last_name',
              'mailing_address_line_1', 'mailing_address_line_2', 
              'street_address_line_1, 'street_address_line_2',
              'telephone', 'email', 'birthdate')) <= set(entity):
    response.status = 400
    return { 'error': 'missing required keys' }

  try:
    wbsession = WebPACSession(CATALOG_URL)
    wbsession.register(entity['first_name'], entity['middle_name'], entity['last_name'],
                       entity['mailing_address_line_1'], entity['mailing_address_line_2'],
                       entity['street_address_line_1'], entity['street_address_line_2'],
                       entity['telephone'], entity['email'], entity['birthdate'])

  except Exception as e:
    if str(e) == 'login failed':
      response.status = 401
    else:
      response.status = 400
    return { 'error': str(e) }


@route('/contact_info', method='GET')
def contact_info():
  code = request.query.get('code')
  pin = request.query.get('pin')

  try:
    wbsession = WebPACSession(CATALOG_URL)
    wbsession.login(code, pin)
    contact_info = wbsession.get_contact_info()
    
    return contact_info

  except Exception as e:
    if str(e) == 'login failed':
      response.status = 401
    else:
      response.status = 400
 
    return { 'error': str(e) }


run(host='localhost', port=9000, debug=True)

