# -*- coding: utf-8 -*-
#
# By Pedro Vapi @2015
# This module is responsible for web routing. This is the main web server.
#
from time import time
from datetime import date
import os

from bottle import get
from bottle import post
from bottle import template
from bottle import request
from bottle import run
from bottle import redirect
from bottle import route
from bottle import static_file

from ditic_kanban.rt_summary import get_summary_info
from ditic_kanban.config import DITICConfig
from ditic_kanban.auth import UserAuth
from ditic_kanban.tools import *
from ditic_kanban.rt_api import *
from ditic_kanban.statistics import *


# My first global variable...
user_auth = UserAuth()

# Only used by the URGENT tickets search
my_config = DITICConfig()
system = my_config.get_system()
rt_object = RTApi(system['server'], system['username'], system['password'])

# This part is necessary in order to get access to sound files
# Static dir is in the parent directory
STATIC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../static"))
print STATIC_PATH


def create_default_result():
    # Default header configuration
    result = {
        'title': 'Still testing...'
    }

    # Summary information
    result.update({'summary': get_summary_info()})

    # Mapping email do uer alias
    config = DITICConfig()
    result.update({'alias': config.get_email_to_user()})

    return result


@get('/')
def get_root():
    start_time = time()

    result = create_default_result()
    # Removed to be a display at the TV
    #if request.query.o == '' or not user_auth.check_id(request.query.o):
    #    result.update({'message': ''})
    #    return template('auth', result)
    #result.update({'username': user_auth.get_email_from_id(request.query.o)})
    result.update({'username_id': request.query.o})
    today = date.today().isoformat()
    result.update({'statistics': get_statistics(get_date(30, today), today)})

    # Is there any URGENT ticket?
    result.update({'urgent': get_urgent_tickets(rt_object)})

    result.update({'time_spent': '%0.2f seconds' % (time() - start_time)})
    return template('entrance_summary', result)


@post('/auth')
def auth():
    result = create_default_result()
    result.update({'username': request.forms.get('username'), 'password': request.forms.get('password')})
    if request.forms.get('username') and request.forms.get('password'):
        try:
            if user_auth.check_password(request.forms.get('username'), request.forms.get('password')):
                redirect('/detail/'+ request.forms.get('username') +'?o=' + user_auth.get_email_id(request.forms.get('username')))
            else:
                result.update({'message': 'Password incorrect'})
                return template('auth', result)
        except ValueError as e:
            result.update({'message': str(e)})
            return template('auth', result)
    else:
        result.update({'message': 'Mandatory fields'})
        return template('auth', result)


@get('/done/<id_ticket>/<username_id>/<email>')
def comment(id_ticket,username_id,email):
    result = create_default_result()
    result.update({'comment': request.forms.get('comment'),'id_ticket': id_ticket,'username_id': username_id, 'email':email})
    return template('comment', result)

@get('/description/<id_ticket>')
def ticket_description(id_ticket,):
    result = create_default_result()
    result.update({'ticket': get_ticket_description(user_auth.get_rt_object_from_email(
            user_auth.get_email_from_id(request.query.o)
        ), id_ticket)})
    result.update({'links': get_ticket_links(user_auth.get_rt_object_from_email(
            user_auth.get_email_from_id(request.query.o)
        ), id_ticket)})
    result.update({'history': get_ticket_history(user_auth.get_rt_object_from_email(
            user_auth.get_email_from_id(request.query.o)
        ), id_ticket)})
    result.update({'email': user_auth.get_email_from_id(request.query.o)})
    result.update({'username_id': request.query.o})
    return template('description', result)

@get('/detail/<email>')
def email_detail(email):
    global email_global
    email_global = email

    start_time = time()

    result = create_default_result()
    if request.query.o == '' or not user_auth.check_id(request.query.o):
        result.update({'message': ''})
        return template('auth', result)

    result.update({'username': user_auth.get_email_from_id(request.query.o)})
    result.update({'email': email})
    result.update({'username_id': request.query.o})

    result.update(user_tickets_details(
        user_auth.get_rt_object_from_email(
            user_auth.get_email_from_id(request.query.o)
        ), email))

    # Is there any URGENT ticket?
    result.update({'urgent': get_urgent_tickets(rt_object)})

    result.update({'time_spent': '%0.2f seconds' % (time() - start_time)})
    if email == 'dir' or email == 'dir-inbox' or email == 'unknown':
        return template('ticket_list', result)
    else:
        return template('detail', result)


@post('/createticket')
def create_ticket():
    result = create_default_result()
    result.update(create_new_ticket(rt_object, request.forms.get('requestor'), request.forms.get('subject')))
    redirect('/')


@get('/newticket')
def new_ticket():
    result = create_default_result()
    result.update({'requestor': request.forms.get('requestor'), 'subject': request.forms.get('subject')})
    return template('new_ticket', result)
    


@get('/closed/<email>')
def email_detail(email):
    start_time = time()

    result = create_default_result()
    if request.query.o == '' or not user_auth.check_id(request.query.o):
        result.update({'message': ''})
        return template('auth', result)

    result.update({'username': user_auth.get_email_from_id(request.query.o)})
    result.update({'email': email})
    result.update({'username_id': request.query.o})

    result.update(user_closed_tickets(
        user_auth.get_rt_object_from_email(
            user_auth.get_email_from_id(request.query.o)
        ), email))

    # Is there any URGENT ticket?
    result.update({'urgent': get_urgent_tickets(rt_object)})

    result.update({'time_spent': '%0.2f seconds' % (time() - start_time)})
    return template('ticket_list', result)


@post('/search')
def search():
    start_time = time()

    result = create_default_result()
    if request.query.o == '' or not user_auth.check_id(request.query.o):
        result.update({'message': ''})
        return template('auth', result)

    if not request.forms.get('search'):
        redirect('/?o=%s' % request.query.o)
    search = request.forms.get('search')

    result.update({'username': user_auth.get_email_from_id(request.query.o)})
    result.update({'email': search})
    result.update({'username_id': request.query.o})

    result.update(search_tickets(
        user_auth.get_rt_object_from_email(
            user_auth.get_email_from_id(request.query.o)
        ), search))

    # Is there any URGENT ticket?
    result.update({'urgent': get_urgent_tickets(rt_object)})

    result.update({'time_spent': '%0.2f seconds' % (time() - start_time)})
    return template('search', result)


@route('/ticket/<ticket_id>/action/<action>')
@post('/ticket/<ticket_id>/action/<action>')
def ticket_action(ticket_id, action):
    ticket_action_2(ticket_id, action, request.forms.get('comment'))
    redirect("/detail/" + request.query.email + "?o=" + request.query.o)


def ticket_action_2(ticket_id, action, commentary):
    start_time = time()

    result = create_default_result()
    if request.query.o == '' or not user_auth.check_id(request.query.o):
        result.update({'message': ''})
        return template('auth', result)

    # Apply the action to the ticket
    result.update(ticket_actions(
        user_auth.get_rt_object_from_email(
            user_auth.get_email_from_id(request.query.o)
        ),
        ticket_id,
        action,
        commentary,
        request.query.email, user_auth.get_email_from_id(request.query.o)
    ))

    # Update table for this user
    result.update(user_tickets_details(
        user_auth.get_rt_object_from_email(
            user_auth.get_email_from_id(request.query.o)
        ), request.query.email))

    result.update({'username': user_auth.get_email_from_id(request.query.o)})
    result.update({'email': request.query.email})
    result.update({'username_id': request.query.o})

    # Is there any URGENT ticket?
    result.update({'urgent': get_urgent_tickets(rt_object)})

    result.update({'time_spent': '%0.2f seconds' % (time() - start_time)})
    if request.query.email == 'dir' or request.query.email == 'dir-inbox' or request.query.email == 'unknown':
        return template('ticket_list', result)
    else:
        return template('detail', result)


@route("/static/<filepath:path>", name="static")
def static(filepath):
    return static_file(filepath, root=STATIC_PATH)


def start_server():
    run(server='paste', host='0.0.0.0', debug=True)

if __name__ == "__main__":
    start_server()
