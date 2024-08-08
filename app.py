import logging

from apscheduler.schedulers.background import BackgroundScheduler
from flasgger import Swagger
from flask import Flask
from flask_cors import CORS

from src import cron
from src.consts import GETLOGS, TIMEOUT
from src.core import limiter
from src.exceptions import (
    forbidden,
    gateway_timeout,
    internal_server_error,
    page_not_found,
    )
from src.routes import admin, index, monitors

if GETLOGS:
    logging.basicConfig(filename='logs.log', level=logging.INFO)

# scheduler
scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(cron.job, 'interval', minutes=TIMEOUT)
scheduler.start()

# app
app = Flask(__name__)
CORS(app)
limiter.init_app(app)
swagger = Swagger(app, template_file='src/swagger.yaml')

# error handling
app.register_error_handler(403, forbidden)
app.register_error_handler(404, page_not_found)
app.register_error_handler(500, internal_server_error)
app.register_error_handler(504, gateway_timeout)

# routes
app.register_blueprint(index.route)
app.register_blueprint(monitors.route)
app.register_blueprint(admin.route)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
    scheduler.shutdown()
