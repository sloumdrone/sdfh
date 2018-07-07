from bottle import route, run, template, static_file, post, request, get, redirect, response, error
import os.path, os, hashlib, datetime, sqlite3, time, json, re
from PIL import Image
from shutil import copyfile
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
                redirect('/events')

    status = str(request.query.statusCode)
    return template('index', loginissue=status, user=ident)
##---**
##---**
@route('/events')
def home():
    is_logged_in()
    ident = request.get_cookie('user_ident')
    event_list = retrieve_events()
    page_title = 'events: show : all'
    return template('events',event_list=event_list,user=ident,page_title=page_title)
##---**
##---**
@route('/directory/<user_ident>')
def profile(user_ident):
    is_logged_in()
    ident = request.get_cookie('user')
    page_title = 'directory : show : ' + user_ident
    return template('profile',user=ident,dir_user=user_ident,page_title=page_title)
##---**
##---**
@route('/directory')
def profile(user_ident):
    is_logged_in()
    ident = request.get_cookie('user')
    page_title = 'directory : show : all'
    user_list = '' #function to generate a user list
    return template('profile',user=ident,page_title=page_title)
##---**
##---**
@route('/post', method='POST')
def handle_post():
    username = request.get_cookie('user')
    message = request.forms.get('message')
    message = message + ' '
    regex = r'@{1}\w*(?=[\W!?\s]{1})'

    for name in re.findall(regex,message):
        validity = select_user(str(name[1:]).rstrip())
        if not validity:
            message = str.replace(message,name,name[1:])
        else:
            message = str.replace(message,name,'@'+str(validity['username']))

    length = len(message)

    if length > 1 and length <= 200:
        message = re.sub('<[^<]+?>', '', message)
        message = sanitize(message, True)
        post_to_db(username,message)
    return redirect('/home')
##---**
##---**
@route('/addusr')
def add_usr():
    return template('addusr')
##---**
##---**
@route('/signup', method='POST')
def sign_up():
    username = request.forms.get('ident')
    if not re.match(r"^[A-Za-z0-9]{4,15}$",username):
        return redirect('/?statusCode=223')
    password = request.forms.get('pass')

    if not select_user(username):
        ts = datetime.datetime.now()+datetime.timedelta(days=1)
        pwhash = hashlib.md5()
        pwhash.update(password)
        session_id = hashlib.md5()
        session_id.update(str(ts))
        new_user(username,pwhash.hexdigest(),session_id.hexdigest())
        return redirect('/')
    else:
        return redirect('/')
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
    if request.get_cookie("user") != None:
        un = request.get_cookie("user")
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

        c.execute("CREATE TABLE events (event_name text NOT NULL, eventdatetime integer NOT NULL, location text NOT NULL, user_id integer NOT NULL, event_description text)")

        c.execute("CREATE TABLE conversations (conversation_type text NOT NULL, conversation_ident integer NOT NULL, comment text NOT NULL, conversation_time integer NOT NULL, user_id integer NOT NULL)")

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
def post_conversation_to_db(user, message, type):
    current_time = time.time()
    message = message.strip()
    db_conn = sqlite3.connect(db)
    c = db_conn.cursor()
    c.execute('''INSERT INTO posts(user_id,post_body,post_time) VALUES(?,?,?)''',(user,message,current_time))
    db_conn.commit()
    lastid = c.lastrowid
    db_conn.close()
    if lastid:
        return True
    return False
##---**
##---**
def retrieve_events():
    db_conn = sqlite3.connect(db)
    c = db_conn.cursor()
    c.execute('''SELECT event_name, location, eventdatetime FROM events ORDER BY eventdatetime DESC''')
    output = []
    for row in c:
        output.append({'event_title':row[0],'event_location':row[1],'event_date':row[2]})
    db_conn.commit()
    db_conn.close()
    return output
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
