from quart import Quart, request, send_file, render_template
from cmyui import log, Ansi, Version
from pathlib import Path
from objects import glob
from datetime import datetime

import os.path
import secrets
import orjson
import cmyui
import shutil

app = Quart(__name__)

glob.version = cmyui.Version(0, 1, 0)

@app.before_serving
async def connections():
    # SHAMELESS COPY PASTE FROM MY DISCORD BOT BELOW

    # check user has a config, if not, attempt to clone the sample config and prompt the user to edit & restart
    if not (Path.cwd() / 'config.py').exists():
        if not (Path.cwd() / 'ext/config.sample.py').exists():
            log('You are missing a config file and there is also no sample config file. Please reclone from GitHub and try again!', Ansi.LRED)
            exit()
        
        # no config but they have a sample config, clone the sample config and prompt user to edit & restart
        shutil.copy((Path.cwd() / 'ext/config.sample.py'), (Path.cwd() / 'config.py'))
        log('Config generated. Please edit the config file and try again!', Ansi.LRED)
        exit()
    
    if not (Path.cwd() / 'uploads').exists():
        os.mkdir(Path.cwd() / 'uploads')

    # connect uploader to db
    try:
        glob.db = cmyui.AsyncSQLPool()
        await glob.db.connect(glob.config.mysql)
        if glob.config.debug:
            log('Connected to MySQL.', Ansi.GREEN)
    except:
        log('Error connecting to MySQL. Please check your config and ensure MySQL is running and try again!', Ansi.LRED)
        exit()
    
    # uploader has started up without any issues
    log(f'==== Katagami v{glob.version} started ====', Ansi.GREEN)

_app_name = glob.config.AppName
@app.before_serving
@app.template_global()
def appName() -> str:
    return _app_name

""" home """
@app.route('/')
async def home():
    return await render_template('home.html')

""" upload stuff """
@app.route('/upload', methods=['GET', 'POST'])
async def upload_file():
    files = await request.files
    #form = request.headers
    upload = (files.get('file'))
    #filename = (form.get('name'))

    # authentication
    token = (form.get('token'))
    log(files)
    log(token)
    log(filename)
     user = await glob.db.fetch('SELECT name FROM users WHERE token = %s', [token])
     if not user:
         return 'Invalid token', 401
     username = user['name']

     ext = os.path.splitext(filename)[1]
     rnd = secrets.token_urlsafe(4)
     upload.save(fr'{os.getcwd()}/uploads/{username}/{rnd}{ext}')
     return orjson.dumps({"filename": rnd, "extension": ext, "username": username}), 200

@app.route('/uploads/<username>/<upload>')
async def get_file(username, upload):
    UPLOADS = Path.cwd() / f'uploads/{username}'
    path = UPLOADS / upload
    if not path.exists():
        return 'File not found', 400
    else:
        return await send_file(path)


""" dashboard """
@app.route('/dashboard')
async def dashboard():
    return await render_template('dashboard/dashboard.html')

""" login, register """
@app.route('/auth/login')
async def login():
    return await render_template('auth/login.html')

@app.route('/auth/register')
async def reg():
    return await render_template('auth/register.html')


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__))) # set cwd for consistency
    app.run(port=glob.config.port, debug=glob.config.debug)
