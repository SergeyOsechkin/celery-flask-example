from flask import Flask
from celery import Celery, group
from celery.result import allow_join_result
import time

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://redis:6379'
app.config['CELERY_RESULT_BACKEND'] = 'redis://redis:6379'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


@celery.task
def wait_func():
    old = time.monotonic()
    jobs = group(subtask.s(item) for item in range(10))
    result = jobs.apply_async()
    with allow_join_result():   # disable the warning and exceptions
        return str(result.get()) + str(time.monotonic() - old)


@celery.task
def subtask(i):
    n = 0
    for _ in range(100000000):
        n += 1
    return i


@app.route('/', methods=['GET', 'POST'])
def index():
    j = wait_func.delay()
    return j.get()
