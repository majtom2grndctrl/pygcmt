import sys, os, sqlite3, datetime, bottle, pytz, logging
#sys.path.insert(0,'/home/dhiester/webapps/pygtmt/lib/python2.7')

from bottle import route, default_app, run, template, static_file, request, post, get
from beaker.middleware import SessionMiddleware
from cork import Cork
from pytz import timezone

#Global blog preferences
class gcmt:
    path = '/home/dhiester/Sites/pygcmt/'
    timezone = 'US/Eastern'
    timeformat = "%Y-%m-%d @ %I:%M%p"
    utcformat = "%Y-%m-%d %H:%M:%S:%f"
    site_title = 'Your New Site'

logging.basicConfig(format='localhost - - [%(asctime)s] %(message)s', level=logging.DEBUG)
log = logging.getLogger(__name__)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

aaa = Cork(gcmt.path + 'cork_conf', email_sender='spammagnet001@distantlyyours.com', smtp_url = 'smtp://smtp.webfaction.com')

app = bottle.app()

session_opts = {
    'session.type': 'cookie',
    'session.validate_key': True,
    'session.cookie_expires': True,
    'session.timeout': 3600 * 24, #1 day
    'session.encrypt_key': 'secret',
}

app = SessionMiddleware(app, session_opts)

def postd():
    return bottle.request.forms

def post_get(name, default=''):
    return bottle.request.POST.get(name, default).strip()

bottle.debug(True)
bottle.TEMPLATE_PATH.append(gcmt.path +'views')

@route('/')
@route('/blogposts/<page>')
def index(page=0):
    tz_utc = pytz.timezone('UTC')

    offset = page * 10
    conn = sqlite3.connect(gcmt.path + 'gcmt.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute('SELECT * FROM blogpost ORDER BY published DESC LIMIT 10 OFFSET ' + str(offset))
    results = c.fetchall()

	#Change time from UTC to Site timezone
    for result in results:
        utctime = tz_utc.localize(datetime.datetime.fromtimestamp(result['published']))
        result['date'] = utctime.astimezone(timezone(gcmt.timezone)).strftime(gcmt.timeformat)

    c.close()
    return template('index', blogposts=results, site_title = gcmt.site_title)

@route('/manage')
def manage():
    aaa.require(role='admin', fail_redirect='/manage/login')
    return template('manage.content', title = "Manage content for " + gcmt.site_title)

@route('/manage/login', method='GET')
def login_form():
    return template('login', site_title = gcmt.site_title)

@route('/manage/login', method='POST')
def login():
    username = post_get('username')
    password = post_get('password')
    aaa.login(username, password, success_redirect='/manage', fail_redirect='/manage/login')

@route('/manage/logout')
def logout():
    aaa.logout(success_redirect='/manage/login')

@route('/manage/blogposts/json')
@route('/manage/blogposts/json/<page>')
def json(page=0):
    aaa.require(role='admin', fail_redirect='/manage/login')

    offset = page * 10
    conn = sqlite3.connect(gcmt.path + 'gcmt.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute('SELECT id, title, published FROM blogpost ORDER BY published DESC LIMIT 10 OFFSET ' + str(offset))
    results = c.fetchall()

	#Change time from UTC to Site timezone
    for result in results:
        tz_utc = pytz.timezone('UTC')
        utctime = tz_utc.localize(datetime.datetime.fromtimestamp(result['published']))
        result['date'] = utctime.astimezone(timezone(gcmt.timezone)).strftime('%m/%d/%Y')

    c.close()

    if not results:
        return {'Blogpost':'No blog posts!'}
    else:
        return {'blogposts': results }

@route('/manage/blogposts/editor')
def blogpost_editor():
    aaa.require(role='admin', fail_redirect='/manage/login')

    return template('manage.editor')

@route('/manage/blogposts/edit/<id>')
def blogpost_edit(id):
    aaa.require(role='admin', fail_redirect='/manage/login')

    conn = sqlite3.connect(gcmt.path + 'gcmt.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute('SELECT * FROM blogpost WHERE id IS ' + id)
    result = c.fetchone()

    c.close()

    #Change time from UTC to Site timezone
    tz_utc = pytz.timezone('UTC')
    utctime = tz_utc.localize(datetime.datetime.fromtimestamp(result['published']))
    result['date'] = utctime.astimezone(timezone(gcmt.timezone)).strftime('%m/%d/%Y')

    return template('manage.blogposts.edit', post=result)
#    return str(result)

@route('/manage/blogposts/save', method='POST')
def save_new_blogpost():
    aaa.require(role='admin', fail_redirect='/manage/login')
    try:
        var_now = datetime.datetime.now(timezone('UTC'))
        conn = sqlite3.connect(gcmt.path + 'gcmt.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        conn.execute("INSERT INTO blogpost VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (None, post_get('title'), 'Published', 1, var_now.strftime('%s'), None, post_get('content'), post_get('excerpt')))
        conn.commit()

        conn.close()
        return "Success?"
    except Exception, e:
        return "Oops"

@route('/manage/blogposts/save/<id>', method='POST')
def save_edited_blogpost(id):
    aaa.require(role='admin', fail_redirect='/manage/login')
#    try:
    var_now = datetime.datetime.now(timezone('UTC'))
    conn = sqlite3.connect(gcmt.path + 'gcmt.db')
    c = conn.cursor()
    c.execute("UPDATE blogpost SET title = '"+str(post_get('title'))+"', content='"+post_get('content')+"', excerpt='"+post_get('excerpt')+"' WHERE id = "+id+";")
    conn.commit()

#        conn.close()
    return "Success?"
#    except Exception, e:
#        return "Oops" + post_get('title') + post_get('content')



@route('/manage/users')
def manage_accounts():
    aaa.require(role='admin', fail_redirect='/manage/login')
    return template('manage.accounts', current_user = aaa.current_user, users = aaa.list_users(), roles = aaa.list_roles())

@route('/manage/users/new', method='POST')
def new_user():
    try:
        aaa.create_user(postd().username, postd().role, postd().password)
        return dict(ok=True, msg='')
    except Exception, e:
        return dict(ok=False, msg=e.message)

@route('/manage/users/delete', method='POST')
def delete_user():
    try:
        aaa.delete_user(post_get('username'))
        return dict(ok=True, msg='User deleted')
    except Exception, e:
        print repr(e)
        return dict(ok=False, msg=e.message)

@bottle.route('/manage/change_password/:reset_code')
@bottle.view('password_changE_form')
def change_password(reset_code):
    return dict(reset_code=reset_code)

@route('/hello')
@route('/hello/<name>')
def hello(name='World'):
    return template('hello', name=name)

@route('/now')
def now():
    utc_now = datetime.datetime.now(timezone('UTC'))
    unix_int = int(utc_now.strftime('%s'))
    tz_utc = pytz.timezone('UTC')
    unix_datetime = tz_utc.localize(datetime.datetime.fromtimestamp(unix_int))
    return unix_datetime.astimezone(timezone(gcmt.timezone)).strftime(gcmt.timeformat) + '<br /><br />' + gcmt.timezone

#More or less a diagnostic method; delete later
@route('/posts')
def posts():
    conn = sqlite3.connect(gcmt.path + 'gcmt.db')
    c = conn.cursor()
    c.execute('SELECT * FROM blogpost')
    result = c.fetchall()
    c.close()

    return str(result)

@route('/javascripts/<filepath:path>')
def javascripts(filepath):
    return static_file(filepath, root='/home/dhiester/Sites/pygcmt/javascripts')

@route('/stylesheets/<filename>')
def scripts(filename):
    return static_file(filename, root='/home/dhiester/Sites/pygcmt/stylesheets')

#application = app # Use this line for mod_wsgi

run(app, host='localhost', port=8080) # use this line for built-in server
