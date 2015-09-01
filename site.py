#! /usr/bin/env python2
# coding: utf8
from functools import partial
import bottle
from bottle import request, get
from bottle import jinja2_view, static_file

import mongo

navitems = ('/', 'Home')

view = partial(jinja2_view, navitems=navitems, request=request)
@get('/')
@view("index.jinja2")
def index():
    events = mongo.get_events()

    return {'events': events}
    
@get('/static/<filename>')
def getstaticfile(filename):
    return static_file(filename, root="static/")



application = bottle.app()
    
if __name__ == '__main__':
    bottle.run(app=application, host='0.0.0.0', port=8088, debug=True, reloader=True)

