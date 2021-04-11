from quart import Quart, request, send_file
from cmyui import log
from pathlib import Path
from objects import glob

import os.path
import secrets
import orjson
import cmyui

app = Quart(__name__)

@app.before_serving
async def connections():
    glob.db = cmyui.AsyncSQLPool()
    await glob.db.connect(glob.config.mysql)

@app.route('/upload', methods=['GET', 'POST'])
async def upload_file():
    files = await request.files
    form = await request.form
    upload = (files.get('file'))
    filename = (form.get('name'))
    ext = os.path.splitext(filename)[1]
    rnd = secrets.token_urlsafe(4)
    upload.save(fr'D:\Dev\uploader-v2\uploads\{rnd}{ext}')
    return orjson.dumps({"filename": rnd, "extension": ext}), 200

@app.route('/upload/<secret>/<upload>')
async def get_file(secret, upload):
    UPLOADS = Path.cwd() / 'uploads'
    path = UPLOADS / upload
    if not path.exists():
        return 'File not found', 400
    else:
        return await send_file(path)

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__))) # set cwd for consistency
    app.run(port=9292, debug=False)