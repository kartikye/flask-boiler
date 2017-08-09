from flask import Flask, Blueprint
import config
import json
import time
app = Flask(__name__, static_url_path="/static")

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

app.times = {}
def timeme(method):
    def wrapper(*args, **kw):
        startTime = int(round(time.time() * 1000))
        result = method(*args, **kw)
        endTime = int(round(time.time() * 1000))
        app.times[method.__name__] = endTime - startTime
        json.dump(app.times, open('log/times.json', 'w'))
        return result

    return wrapper

app.timeme = timeme

#Blueprints
#from app.verifier.verifier import verifier as verify
#app.register_blueprint(verify)

#from app.validator.validator import validator
#app.register_blueprint(validator)
    