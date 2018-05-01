from flask import Blueprint, render_template

from datetime import datetime, timedelta

now_time = datetime.now()
begin_time = now_time + timedelta(days=-7)

vd = Blueprint('vd', __name__, url_prefix='')
param_location = ('json', )


@vd.route('/')
def index():

    return render_template('index.html')