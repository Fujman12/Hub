from flask import Flask, render_template, url_for
from flask_websub.hub import Hub, SQLite3HubStorage
from celery import Celery

# app & celery
app = Flask(__name__)
app.config['SERVER_NAME'] = 'vanl0057336.online-vm.com'

broker_url = 'sqs://AKIAJDRBIV3D2ZNIMWYA:avqRxeStaIIEPyGEHTT0dexvirz2TJXzhw7Mk+9K@'
celery = Celery('server_example', broker='redis://localhost:6379')

app.config['PUBLISH_SUPPORTED'] = True
# we could also have passed in just PUBLISH_SUPPORTED, but this is probably a
# nice pattern for your app:
hub = Hub(SQLite3HubStorage('/root/Hub/server_data.sqlite3'), celery, **app.config)
app.register_blueprint(hub.build_blueprint(url_prefix='/'))

hub.schedule_cleanup()  # cleanup expired subscriptions once a day, by default

@app.before_first_request
def cleanup():
    # or just cleanup manually at some point
    hub.cleanup_expired_subscriptions.delay()


@app.route('/welcome')
def topic():
    return render_template('server_example.html')


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8000)