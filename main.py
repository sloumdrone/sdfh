from bottle import route, run, template, static_file, post, request, get, redirect, response, error
import os.path, os, hashlib, datetime, sqlite3, time, json, re
from cgi import escape as sanitize
##---**
##---**
##################################################################################
####--------------------------------Globals---------------------------------#####
################################################################################
##---**
##---**
db = './resources/sdfh.sqlite'
##---**
##---**
##################################################################################
####--------------------Routing for Pages/API Endpoints---------------------#####
################################################################################
##---**
##---**
@route('/')
def main_blog():
    if request.get_cookie('user_ident') != None:
        ident = request.get_cookie('user_ident')
        udata = select_user(ident)
        if ident == udata['user_ident']:
            if udata['session_id'] == request.get_cookie('session'):
                redirect('/events/show/all')

    status = str(request.query.statusCode)
    return template('index', loginissue=status, user=ident, page_title='index')
##---**
##---**
@route('/events/<action>/<event_id>')
def events(action,event_id):
    is_logged_in()
    ident = request.get_cookie('user_ident')
    page_title = 'events : ' + action + ' : ' + event_id
    if action == 'show':
        if event_id == 'all':
            event_list = retrieve_events()
            return template('events',event_list=event_list,user=ident,page_title=page_title)
        else:
            event_data = retrieve_event(event_id)
            comment_data = retrieve_comments('events',event_id)
            error = False
            code = str(request.query.error)
            if code == '1':
                error = True
            return template('event_listing', event=event_data, user=ident, page_title=page_title, comments=comment_data, error=error, event_id=event_id)
    elif action == 'edit':
        if event_id != 'all':
            error = False
            code = str(request.query.error)
            if code == '1':
                error = True
            event_data = retrieve_event(event_id)
            return template('edit_event', event=event_data, user=ident, page_title=page_title, error=error, event_id=event_id)

    return redirect('/events/show/all')
##---**
##---**
@route('/add_event')
def add_event():
    is_logged_in()
    ident = request.get_cookie('user_ident')
    page_title = 'events : create : new'
    error = False
    code = str(request.query.error)
    if code == '1':
        error = True
    return template('add_event',user=ident,page_title=page_title,error=error)
##---**
##---**
@route('/directory/<action>/<user_ident>')
def directory(action,user_ident):
    is_logged_in()
    ident = request.get_cookie('user_ident')
    page_title = 'directory : ' + action + ' : ' + user_ident
    if action == 'show':
        if user_ident == 'all':
            user_list = retrieve_users()
            return template('directory',user=ident,page_title=page_title,user_list=user_list,user_query=user_ident)
        else:
            return template('directory_listing',user=ident,user_query=user_ident,page_title=page_title)
    elif action == 'edit':
        return redirect('/events/show/all')
##---**
##---**
@route('/new_event', method='POST')
def handle_new_event_add():
    is_logged_in()
    user = request.forms.get('event_creator')
    title = request.forms.get('event_title')
    location = request.forms.get('event_location')
    date = request.forms.get('event_date')
    description = request.forms.get('event_description')
    date = int(datetime.datetime.strptime(date,'%m-%d-%Y').strftime('%s'))

    if post_event_to_db(user, title, location, date, description):
        return redirect('/events')

    return redirect('/add_event?error=1')
##---**
##---**
@route('/edit_event', method='POST')
def handle_event_edit():
    is_logged_in()
    user = request.forms.get('event_creator')
    title = request.forms.get('event_title')
    location = request.forms.get('event_location')
    date = request.forms.get('event_date')
    description = request.forms.get('event_description')
    date = int(datetime.datetime.strptime(date,'%m-%d-%Y').strftime('%s'))
    event_id = int(request.forms.get('event_id'))

    if update_event_db(user, title, location, date, description,event_id):
        return redirect('/events/show/' + str(event_id))

    return redirect('/event/edit/' + str(event_id) + '?error=1')
##---**
##---**
@route('/add_comment/<page_type>/<item_id>',method='POST')
def add_event(page_type,item_id):
    is_logged_in()
    user = request.get_cookie('user_ident')
    comment = request.forms.get('comment')
    currenttime = int(time.time())
    if post_comment_to_db(user, currenttime, comment, page_type, item_id):
        return redirect('/' + page_type + '/show/' + item_id)

    return redirect('/' + page_type + '/show/' + item_id + '?error=1')
##---**
##---**
@route('/addusr')
def add_usr():
    return template('addusr')
##---**
##---**
@post('/login', method='POST')
def log_me_in():
    user_ident = request.forms.get('ident')
    user_pass = request.forms.get('pass')
    pwhash = hashlib.md5()
    pwhash.update(user_pass)
    validity = verify_login(user_ident,pwhash.hexdigest())
    if validity:
        ts = datetime.datetime.now()+datetime.timedelta(days=14)
        session_id = hashlib.md5()
        session_id.update(str(ts))
        create_session_db(validity['user_ident'],session_id.hexdigest())
        response.set_cookie('user_ident',validity['user_ident'],expires=ts)
        response.set_cookie('session',session_id.hexdigest(),expires=ts)
        response.set_cookie('user_id',str(validity['user_id']),expires=ts)
        redirect('/events')
    else:
        redirect('/')
##---**
##---**
@route('/logout')
def logout():
    username = request.get_cookie("user")

    logout_user_db(username)

    response.delete_cookie("user")
    response.delete_cookie("session")
    redirect('/')
##---**
##---**
@route('/images/<path:path>')
def serve_pictures(path):
    return static_file(path, root='./resources/images/')
##---**
##---**
@route('/library/<lib>')
def serve_libs(lib):
    return static_file(lib, root='./resources/lib/')
##---**
##---**
@error(404)
@error(500)
def catch_errors(error):
    return '''<!DOCTYPE html>
    <html>
        <head>
            <meta charset="utf-8">
            <title>sdfh: the sky is falling!</title>
            <link rel="stylesheet" href="/library/error.css">
        </head>
        <body>
            <div class="container">
                <div class="image"></div><div class="title">sdfh</div>
                <p>something has gone awry</p>
                <p>
                    <a href="/">index</a>
                </p>
            </div>
        </body>
    </html>'''
##---**
##---**
@route('/delete_account', method='POST')
def delete_account():
    is_logged_in()
    user = request.get_cookie('user')
    pwd = request.forms.get('pwd')
    pwhash = hashlib.md5()
    pwhash.update(pwd)
    if verify_login(user,pwhash.hexdigest()):
        if delete_account(user):
            response.delete_cookie("user")
            response.delete_cookie("session")
            return json.dumps({'success':True, 'error':None})
        else:
            return json.dumps({'success':False,'error':'SQL error'})
    return json.dumps({'success':False,'error':'Passwords do not match.'})
##---**
##---**
@route('/about')
def about():
    return template('aboutpage', username=' ')
##---xx
##---xx
##################################################################################
####----------------------Routes Above/Functions Below----------------------#####
################################################################################
##---**
##---**
def is_logged_in():
    if request.get_cookie("user_ident") != None:
        un = request.get_cookie("user_ident")
        udata = select_user(un)
        if un == udata["user_ident"]:
            if udata["session_id"] != request.get_cookie("session"):
                redirect('/')
        else:
            redirect('/')
    else:
        redirect('/')
##---**
##---**
def verify_login(un,pw):
    udata = select_user(un)
    if udata:
        if pw == udata['user_pass']:
            return udata
    return False
##---**
##---**
def check_and_build_db():
    if not os.path.isfile(db):
        db_conn = sqlite3.connect(db)
        c = db_conn.cursor()

        c.execute("CREATE TABLE users (user_ident text NOT NULL PRIMARY KEY, user_pass text NOT NULL,session_id text DEFAULT null)")

        c.execute("CREATE TABLE events (event_name text NOT NULL, eventdatetime integer NOT NULL, location text NOT NULL, user_ident integer NOT NULL, event_description text)")

        c.execute("CREATE TABLE conversations (conversation_type text NOT NULL, page_ident integer NOT NULL, comment text NOT NULL, conversation_time integer NOT NULL, user_ident text NOT NULL)")

        db_conn.commit()
        db_conn.close()
    ##---**
    ##---**
def select_user(user):
    db_conn = sqlite3.connect(db)
    c = db_conn.cursor()
    c.execute('''SELECT user_ident, user_pass, session_id, rowid FROM users WHERE lower(user_ident)=lower(?)''',(user,))
    row_data = c.fetchone()
    db_conn.close()
    if row_data is None:
        return False
    user_data = {"user_ident":row_data[0],"user_pass":row_data[1],"session_id":row_data[2],"user_id":row_data[3]}

    return user_data
##---**
##---**
def logout_user_db(user):
    db_conn = sqlite3.connect(db)
    c = db_conn.cursor()
    c.execute('''UPDATE users SET session_id = 'Invalid1Session1Id1' WHERE user_ident=?''',(user,))
    db_conn.commit()
    db_conn.close()
##---**
##---**
def create_session_db(user,session):
    db_conn = sqlite3.connect(db)
    c = db_conn.cursor()
    c.execute('''UPDATE users SET session_id=? WHERE user_ident=?''',(session,user))
    db_conn.commit()
    db_conn.close()
##---**
##---**
def new_user(un,pw,sid):
    db_conn = sqlite3.connect(db)
    c = db_conn.cursor()
    c.execute('''INSERT INTO users(user_ident,user_pass,session_id) VALUES(?,?,?)''',(un,pw,sid))
    lastid = c.lastrowid
    db_conn.commit()
    db_conn.close()
    if lastid:
        return True
    return False
##---**
##---**
def post_event_to_db(user_ident, title, location, date, description):
    description = description.strip().lower()
    title = sanitize(title.lower())
    location = sanitize(location)
    db_conn = sqlite3.connect(db)
    c = db_conn.cursor()
    c.execute('''INSERT INTO events(user_ident,event_name,location,event_description,eventdatetime) VALUES(?,?,?,?,?)''',(user_ident,title,location,description,date))
    db_conn.commit()
    lastid = c.lastrowid
    db_conn.close()
    if lastid:
        return True
    return False
##---**
##---**
def update_event_db(user_ident, title, location, date, description,event_id):
    description = description.strip().lower()
    title = sanitize(title.lower())
    location = sanitize(location)
    db_conn = sqlite3.connect(db)
    c = db_conn.cursor()
    result = c.execute('''UPDATE events SET user_ident = ?, event_name = ?, location = ?, event_description = ?, eventdatetime = ? WHERE rowid = ?''',(user_ident,title,location,description,date,event_id))
    db_conn.commit()
    db_conn.close()
    if result.rowcount > 0:
        return True
    return False
##---**
##---**
def retrieve_events():
    db_conn = sqlite3.connect(db)
    c = db_conn.cursor()
    c.execute('''SELECT event_name, location, eventdatetime, rowid FROM events ORDER BY eventdatetime DESC''')
    output = []
    for row in c:
        output.append({'event_title':row[0],'event_location':row[1],'event_date':row[2],'event_id':row[3]})
    db_conn.commit()
    db_conn.close()
    return output
##---**
##---**
def retrieve_event(id):
    db_conn = sqlite3.connect(db)
    c = db_conn.cursor()
    c.execute('''SELECT event_name, location, eventdatetime, event_description, user_ident FROM events WHERE rowid = ?''',(id,))
    output = []
    for row in c:
        output.append({'title':row[0],'location':row[1],'date':row[2],'description':row[3],'creator':row[4]})
    db_conn.commit()
    db_conn.close()
    return output
##---**
##---**
def retrieve_users():
    db_conn = sqlite3.connect(db)
    c = db_conn.cursor()
    c.execute('''SELECT user_ident FROM users ORDER BY user_ident ASC''')
    output = []
    for row in c:
        output.append(row[0])
    db_conn.commit()
    db_conn.close()
    return output
##---**
##---**
def retrieve_comments(type,id):
    db_conn = sqlite3.connect(db)
    c = db_conn.cursor()
    c.execute('''SELECT user_ident, comment FROM conversations WHERE conversation_type = ? and page_ident = ? ORDER BY conversation_time DESC''',(type,id))
    output = []
    for row in c:
        output.append({'user':row[0],'comment':row[1]})
    db_conn.commit()
    db_conn.close()
    return output
##---**
##---**
def post_comment_to_db(user_ident, current_time, comment_text, conversation_type, page_id):
    comment_text = comment_text.strip().lower()

    db_conn = sqlite3.connect(db)
    c = db_conn.cursor()
    c.execute('''INSERT INTO conversations(conversation_type,page_ident,comment,conversation_time,user_ident) VALUES(?,?,?,?,?)''',(conversation_type,page_id,comment_text,current_time,user_ident))
    db_conn.commit()
    lastid = c.lastrowid
    db_conn.close()
    if lastid:
        return True
    return False

    #conversations (conversation_type text NOT NULL, page_ident integer NOT NULL, comment text NOT NULL, conversation_time integer NOT NULL, user_ident text NOT NULL
##---xx
##---xx
##################################################################################
#####---------------------------Run-the-server-----------------------------######
################################################################################
##---**
##---**
if __name__ == '__main__':
    check_and_build_db()
    run(host='localhost', port=8080)
##---xx
##---xx
