from __future__ import print_function
import re
import os
import json
import base64
import uuid
import subprocess
import redis
from flask import Flask, request
from flask import render_template
from celery import Celery
from rdkit.Chem import AllChem


app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379/0',
    CELERY_RESULT_BACKEND='redis://localhost:6379/1',
    CACHE_SETTING={
        "host": "127.0.0.1",
        "port": 6379,
    },
    BASE_DIR=os.getcwd(),
)


def make_celery(app):
    celery = Celery(app.import_name,  # 此处官网使用app.import_name，因为这里将所有代码写在同一个文件flask_celery.py,所以直接写名字。
                    broker=app.config['CELERY_BROKER_URL'],
                    backend=app.config['CELERY_RESULT_BACKEND']
                    )
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


celery = make_celery(app)
CACHE = redis.Redis(**app.config.get("CACHE_SETTING"))


class OrsaTask(object):
    INITIAL = 0
    FINISHED = 1
    mol_text = ""

    # TODO Wrong logic of arguments
    def __init__(self, pk=None, img_data=None, upload_path='uploads/'):
        if pk is None:
            self.pk = str(uuid.uuid4())
            # TODO Should get file type, base64 data at one regx
            ft, suffix = re.search('(image)/(\w+)', img_data).groups()
            self.fp = "".join((upload_path, self.pk, '.', suffix))
            os.chdir(os.path.dirname(__file__))
            with open(self.fp, 'wb') as f:
                img_base64 = img_data[img_data.find('base64,') + 7:]
                data = base64.b64decode(img_base64)
                f.write(data)
            self._save()
            self.osra(self)
        else:
            self.pk = pk

    @celery.task
    def osra(self):
        osra_fp = os.path.join(app.config["BASE_DIR"], "osra/osra.bat")
        args = ['-f sdf', self.fp]
        command = ' '.join([osra_fp]+args)
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        if not stderr:
            self.mol_text = stdout.decode('u8')
            self._save()
        else:
            raise ValueError(stderr)

    def _save(self):
        CACHE.hmset(self.pk,
                    {'fp': self.fp,
                     'mol_text': self.mol_text}
                    )

    def get_moltext(self):
        mol_text = CACHE.hget(self.pk, 'mol_text')
        return mol_text


@app.route('/')
def main_page():
    return render_template("index.html")


@app.route('/upload/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        img_data = request.form['image_file']
        task = OrsaTask(img_data=img_data)
        j = {
            'status': 'success',
            'pk': task.pk
        }
        return json.dumps(j)


@app.route('/get_moltext/<pk>', methods=["GET", ])
def get_moltext(pk=None):
    if request.method == 'GET':
        task = OrsaTask(pk=pk)
        mol_text = task.get_moltext().decode('u8')
        j = {'mol_text': mol_text}
        if mol_text:
            j['status'] = 'success'
        else:
            j['status'] = 'fail'
        return json.dumps(j)


@app.route('/clean/', methods=['POST'])
def clean():
    if request.method == 'POST':
        mol_text = request.form.get('mol_text', "")
        m = AllChem.MolFromMolBlock(mol_text)
        if m:
            t = AllChem.Compute2DCoords(m)
            mol_text = AllChem.MolToMolBlock(m)
        j = {'mol_text': mol_text}
        return json.dumps(j)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
