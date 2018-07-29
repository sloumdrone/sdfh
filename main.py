from bottle import route, run, template, static_file, post, request, get, redirect, response, error
import os.path, os, hashlib, datetime, sqlite3, time, json, re, random, urllib2
from cgi import escape as sanitize
from slack_paths import slack_url, site_base_url
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
def main_index():
    if request.get_cookie('user_ident') != None:
        ident = request.get_cookie('user_ident')
        udata = select_user(ident)
        if ident == udata['user_ident']:
            if udata['session_id'] == request.get_cookie('session'):
                redirect('/recent/show/all')
    else:
        ident = ''

    status = str(request.query.statusCode)
    return template('index', loginissue=status, user=ident, page_title='index')
##---**
##---**
@route('/recent/<action>/<filter>') # still in progress
def recent(action,filter):
    is_logged_in()
    ident = request.get_cookie('user_ident')
    page_title = 'recent : ' + action + ' : ' + filter
    if action == 'show':
        if filter == 'all':
            recents = retrieve_recents()
            return template('recents',data=recents,page_title=page_title,user=ident)

    redirect('/recent/show/all')
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
            attendees = retrieve_attendees(event_id)
            # attendees = ['person','cesca']
            error = False
            code = str(request.query.error)
            if code == '1':
                error = True
            return template('event_listing', event=event_data, user=ident, page_title=page_title, comments=comment_data, error=error, event_id=event_id, attendees=attendees)
    elif action == 'edit':
        if event_id != 'all':
            error = False
            code = str(request.query.error)
            if code == '1':
                error = True
            event_data = retrieve_event(event_id)
            return template('edit_event', event=event_data, user=ident, page_title=page_title, error=error, event_id=event_id)
    elif action == 'delete':
        event_data = retrieve_event(event_id)[0]
        if ident == event_data['creator']:
            delete_event(event_id)
            return redirect('/events/show/all')
        return redirect('/events/show/' + event_id + '?error=1')
    elif action == 'join':
        join_event(ident,event_id)
        redirect('/events/show/'+event_id)
    elif action == 'leave':
        leave_event(ident,event_id)
        redirect('/events/show/'+event_id)

    return redirect('/events/show/all')
##---**
##---**
@route('/signup', method='POST')
def sign_up():
    username = request.forms.get('ident')
    if not re.match(r"^[A-Za-z0-9_!]{3,30}$",username):
        return redirect('/addusr?error=regexissue')
    password = request.forms.get('pass')

    if not select_user(username):
        ts = datetime.datetime.now()+datetime.timedelta(days=1)
        pwhash = hashlib.md5()
        pwhash.update(password)
        session_id = hashlib.md5()
        session_id.update(str(ts))
        new_user(username,pwhash.hexdigest(),session_id.hexdigest())
        user_info_to_db(user_ident=username,create=True)
        return redirect('/addusr?error=none&success=true')
    else:
        return redirect('/addusr?error=misc')
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
    error = False
    code = str(request.query.error)
    if code == '1':
        error = True
    if action == 'show':
        if user_ident == 'all':
            user_list = retrieve_users()
            return template('directory', user=ident, page_title=page_title, user_list=user_list, user_query=user_ident)
        else:
            user_info = retrieve_user_info(user_ident)
            comments = retrieve_comments('directory',user_ident)

            return template('directory_listing', user=ident, page_title=page_title, usr=user_info, error=error, comments=comments,page_ident=user_ident)
    elif action == 'edit' and user_ident != 'all':
        if ident == user_ident:
            user_info = retrieve_user_info(user_ident)
            return template('edit_directory_listing', user=ident, page_title=page_title, usr=user_info,error=error)
        else:
            return redirect('/directory/show/'+user_ident)
##---**
##---**
@route('/thread/<action>/<user_ident>/<time_ident>')
def thread(action,user_ident,time_ident):
    is_logged_in()
    ident = request.get_cookie('user_ident')
    page_title = 'thread : ' + action + ' : ' + user_ident + ' : ' + time_ident
    error = False
    code = str(request.query.error)
    if code == '1':
        error = True
    if action == 'show':
        sayings = [
        'see something, say something',
        'spit it out already',
        'all the cool kids post comments',
        'what do you think?',
        'brave words from the brightest minds of sdfh',
        "'tis the privilege of friendship to talk nonsense",
        "i love to talk about nothing, it's the only thing i know anything about",
        "board the cows! we've come to enslave your marigolds",
        'saying nothing... sometimes says the most',
        'tell the truth, but tell it slant',
        'little by little, one travels far',
        'your absence has gone through me'
        ]

        saying = random.choice(sayings)
        comment = retrieve_comments('directory',user_ident,time_ident)[0]
        threads = retrieve_threads(user_ident,time_ident)
        return template('comment_listing', user=ident, page_title=page_title, error=error, comment=comment,threads=threads,saying=saying)
    elif action == 'delete' and user_ident == ident:
        delete_comments_and_threads(ident,time_ident)
        return redirect('/directory/show/'+ident)
    return redirect('/')
##---**
##---**
@route('/new_event', method='POST')
def handle_new_event_add():
    is_logged_in()
    user = request.get_cookie('user_ident')
    title = request.forms.get('event_title')
    location = request.forms.get('event_location')
    date = request.forms.get('event_date')
    description = request.forms.get('event_description')
    description = strip_html_tags(description)
    date = int(datetime.datetime.strptime(date,'%m-%d-%Y').strftime('%s'))

    post_id = post_event_to_db(user, title, location, date, description)
    join_event(user,post_id)
    if post_id:
        event_url = site_base_url + 'events/show/' + str(post_id)
        send_slack_update('event',event_url,user,title)
        return redirect('/events/show/all')

    return redirect('/add_event?error=1')
##---**
##---**
@route('/edit_event', method='POST')
def handle_event_edit():
    is_logged_in()
    user = request.get_cookie('user_ident')
    title = request.forms.get('event_title')
    location = request.forms.get('event_location')
    date = request.forms.get('event_date')
    description = request.forms.get('event_description')
    description = strip_html_tags(description)
    date = int(datetime.datetime.strptime(date,'%m-%d-%Y').strftime('%s'))
    event_id = int(request.forms.get('event_id'))

    if update_event_db(user, title, location, date, description,event_id):
        return redirect('/events/show/' + str(event_id))

    return redirect('/event/edit/' + str(event_id) + '?error=1')
##---**
##---**
@route('/edit_directory_listing', method='POST')
def handle_event_edit():
    is_logged_in()
    user = request.get_cookie('user_ident')
    bio = request.forms.get('bio')
    tools = request.forms.get('tools')
    skills = request.forms.get('skills')

    if user_info_to_db(user, bio, tools, skills):
        return redirect('/directory/show/' + user)

    return redirect('/directory/edit/' + user + '?error=1')
##---**
##---**
@route('/add_comment/<page_type>/<item_id>',method='POST')
def add_event(page_type,item_id):
    is_logged_in()
    user = request.get_cookie('user_ident')
    comment = request.forms.get('comment')
    comment = strip_html_tags(comment)
    currenttime = int(time.time())
    if post_comment_to_db(user, currenttime, comment, page_type, item_id):
        if page_type != 'thread':
            link_url = site_base_url + page_type + '/show/' + item_id
            send_slack_update('comment',link_url,user,comment)
            return redirect('/' + page_type + '/show/' + item_id)

    return redirect('/' + page_type + '/show/' + item_id + '?error=1')
##---**
##---**
@route('/add_thread/<parent_user>/<parent_time>',method='POST')
def add_thread(parent_user,parent_time):
    is_logged_in()
    user = request.get_cookie('user_ident')
    comment = request.forms.get('comment')
    comment = strip_html_tags(comment)
    currenttime = int(time.time())
    if post_thread_to_db(parent_user, parent_time, user, comment, currenttime):
        thread_url = site_base_url + 'thread/show/' + parent_user + '/' + parent_time
        send_slack_update('comment',thread_url,user,comment)
        return redirect('/thread/show/' + parent_user + '/' + parent_time)

    return redirect('/thread/show/' + parent_user + '/' + parent_time + '?error=1')
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
            <link rel="stylesheet" href="/library/main.css">
        </head>
        <body>
            <header><a href="/" id="page_title_link">super dev friends huzzah!</a></header>
                <p>something has gone awry</p>
                <p><a href="/">index</a></p>
            </div>
        </body>
    </html>'''
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
        db_conn = sqlite3.connect('./resources/sdfh.sqlite')
        c = db_conn.cursor()

        c.execute("CREATE TABLE users (user_ident text NOT NULL PRIMARY KEY, user_pass text NOT NULL,session_id text DEFAULT null)")

        c.execute("CREATE TABLE events (event_name text NOT NULL, eventdatetime integer NOT NULL, location text NOT NULL, user_ident integer NOT NULL, event_description text)")

        c.execute("CREATE TABLE conversations (conversation_type text NOT NULL, page_ident text NOT NULL, comment text NOT NULL, conversation_time integer NOT NULL, user_ident text NOT NULL)")

        c.execute("CREATE TABLE user_info (user_ident text NOT NULL, bio text, tools text, skills text)")

        c.execute("CREATE TABLE threads (parent_page text NOT NULL, parent_time integer NOT NULL, thread_user text NOT NULL, thread_comment text NOT NULL, thread_time integer NOT NULL)")

        c.execute("CREATE TABLE attendees (user_ident text NOT NULL, event_id integer NOT NULL)")

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
def user_info_to_db(user_ident, bio='', tools='', skills='',create=False):
    bio = bio.lower().strip()
    skills = skills.strip().lower()
    tools = tools.strip().lower()
    db_conn = sqlite3.connect(db)
    c = db_conn.cursor()
    if create:
        c.execute('''INSERT INTO user_info(user_ident,bio,tools,skills) VALUES(?,?,?,?)''',(user_ident, bio, tools, skills))
        db_conn.commit()
        lastid = c.lastrowid
    else:
        result = c.execute('''UPDATE user_info SET bio = ?, tools = ?, skills = ? WHERE user_ident = ?''',(bio, tools, skills, user_ident))
        db_conn.commit()
        if result.rowcount > 0:
            lastid = True
        else:
            lastid = False
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
        return lastid
    return False
##---**
##---**
def update_event_db(user_ident, title, location, date, description,event_id):
    description = description.strip().lower()
    title = sanitize(title.lower())
    location = sanitize(location.lower())
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
def update_user_info_db(user_ident, bio, tools, skills):
    bio = bio.strip().lower()
    tools = sanitize(tools.lower())
    skills = sanitize(skills.lower())
    db_conn = sqlite3.connect(db)
    c = db_conn.cursor()
    result = c.execute('''UPDATE user_info SET bio = ?, tools = ?, skills = ? WHERE user_ident = ?''', (bio,tools,skills,user_ident))
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
def retrieve_attendees(event_id):
    db_conn = sqlite3.connect(db)
    c = db_conn.cursor()
    c.execute('''SELECT DISTINCT user_ident FROM attendees WHERE event_id = ? ORDER BY user_ident ASC''',(event_id,))
    output = []
    for row in c:
        output.append(row[0])
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
def retrieve_user_info(user_ident):
    db_conn = sqlite3.connect(db)
    c = db_conn.cursor()
    c.execute('''SELECT user_ident, bio, tools, skills FROM user_info WHERE user_ident = ?''',(user_ident,))
    output = []
    for row in c:
        output.append({'user_ident':row[0], 'bio':row[1], 'tools':row[2], 'skills':row[3]})
    db_conn.commit()
    db_conn.close()
    if len(output) > 0:
        return output[0]
    return {'user_ident':user_ident, 'bio':'', 'tools':'', 'skills':''}
##---**
##---**
def retrieve_comments(type,id,time='%'):
    db_conn = sqlite3.connect(db)
    c = db_conn.cursor()
    c.execute('''SELECT user_ident, comment, conversation_time FROM conversations WHERE conversation_type = ? and page_ident = ? and conversation_time like ? ORDER BY conversation_time ASC''',(type,id,time))
    output = []
    for row in c:
        output.append({'user':row[0],'comment':row[1],'time':row[2]})
    db_conn.commit()
    db_conn.close()
    return output
##---**
##---**
def delete_comments_and_threads(user,time_id):
    db_conn = sqlite3.connect(db)
    c = db_conn.cursor()
    c.execute('''DELETE FROM conversations WHERE conversation_type = 'directory' and page_ident = ? and conversation_time = ?''',(user,time_id))
    c.execute('''DELETE FROM threads WHERE parent_page = ? and parent_time = ?''',(user,time_id))
    db_conn.commit()
    db_conn.close()
    return True
##---**
##---**
def delete_event(id):
    db_conn = sqlite3.connect(db)
    c = db_conn.cursor()
    c.execute('''DELETE FROM attendees WHERE event_id = ?''',(id,))
    c.execute('''DELETE FROM events WHERE rowid = ?''',(id,))
    db_conn.commit()
    db_conn.close()
    return True
##---**
##---**
def retrieve_threads(user,time):
    db_conn = sqlite3.connect(db)
    c = db_conn.cursor()
    c.execute('''SELECT thread_user, thread_comment, thread_time FROM threads WHERE parent_page = ? and parent_time = ? ORDER BY thread_time ASC''',(user,time))
    output = []
    for row in c:
        output.append({'user':row[0],'comment':row[1],'time':row[2]})
    db_conn.commit()
    db_conn.close()
    return output
##---**
##---**
def retrieve_recents():
    db_conn = sqlite3.connect(db)
    c = db_conn.cursor()
    # c2 = db_conn.cursor()
    # c3 = db_conn.cursor()
    output = {'events':[],'user_posts':[],'users':[],'threads':[]}
    c.execute('''SELECT DISTINCT conversations.page_ident, conversations.comment, conversations.conversation_time FROM conversations INNER JOIN threads ON threads.parent_time = conversations.conversation_time WHERE conversations.conversation_type = 'directory' ORDER BY threads.thread_time DESC LIMIT 5''')
    for row in c:
        output['threads'].append({'user':row[0],'comment':row[1],'thread_id':row[2]})
    c.execute('''SELECT event_name, rowid FROM events ORDER BY rowid DESC LIMIT 5''')
    for row in c:
        output['events'].append({'title':row[0],'event_id':row[1]})
    c.execute('''SELECT user_ident FROM users ORDER BY rowid DESC LIMIT 5''')
    for row in c:
        output['users'].append({'user':row[0]})
    c.execute('''SELECT DISTINCT comment, user_ident FROM conversations WHERE conversation_type = 'directory' ORDER BY conversation_time DESC LIMIT 5''')
    for row in c:
        output['user_posts'].append({'comment':row[0],'user':row[1]})
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
##---**
##---**
def post_thread_to_db(parent_page, parent_time, thread_user, thread_comment, thread_time):
    thread_comment = thread_comment.strip().lower()

    db_conn = sqlite3.connect(db)
    c = db_conn.cursor()
    c.execute('''INSERT INTO threads(parent_page,parent_time,thread_user,thread_comment,thread_time) VALUES(?,?,?,?,?)''',(parent_page, parent_time, thread_user, thread_comment, thread_time))
    db_conn.commit()
    lastid = c.lastrowid
    db_conn.close()
    if lastid:
        return True
    return False
##---**
##---**
def join_event(user,event):
    db_conn = sqlite3.connect(db)
    c = db_conn.cursor()
    c.execute('''INSERT INTO attendees(user_ident,event_id) VALUES(?,?)''',(user,event))
    db_conn.commit()
    lastid = c.lastrowid
    db_conn.close()
    if lastid:
        return True
    return False
##---**
##---**
def leave_event(user,event):
    db_conn = sqlite3.connect(db)
    c = db_conn.cursor()
    c.execute('''DELETE FROM attendees WHERE user_ident = ? and event_id = ?''',(user,event))
    db_conn.commit()
    lastid = c.lastrowid
    db_conn.close()
    if lastid:
        return True
    return False
##---**
##---**
def strip_html_tags(string):
    tags_to_strip = ['script','iframe','form','textarea']
    for tag in tags_to_strip:
        tag_count = string.count('<'+tag)
        if tag_count > 0:
            for x in range(tag_count):
                start = string.find('<'+tag)
                end = string.find('</'+tag, start+1) + 4 + len(tag)
                string = string.replace(string[start:end],'')
    string = string.replace('"','&quot;').replace("'",'&apos;')
    return string
##---**
##---**
def send_slack_update(type, url, user, comment=''):
    textstring = 'A new <' + url + '|' + type + '> has been posted on <' + url + '|' + 'sdfh.space> by ' + '<' + site_base_url + 'directory/show/' + user + '|' + user + '>: "' + comment + '".'
    data = {
            'text': textstring
    }

    req = urllib2.Request(slack_url)
    req.add_header('Content-Type', 'application/json')

    response = urllib2.urlopen(req, json.dumps(data))
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
