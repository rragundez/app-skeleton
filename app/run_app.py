import click
import logging
import os

from werkzeug.debug import DebuggedApplication

from app import app
from resources.gunicorn_app import GunicornApp


@click.command(
    context_settings={
        'allow_extra_args': True,
        'ignore_unknown_options': True,
        'allow_interspersed_args': True,
    }
)
@click.option(
    '-h', '--host',
    default='127.0.0.1',
    help=("The hostname to listen on. Set this to '0.0.0.0' to have the "
          "application available eternally. Defaults to '127.0.0.1'")
)
@click.option(
    '-p', '--port',
    default=5000,
    help="The port of the application. Defaults to '5000'."
)
@click.option(
    '--debug', is_flag=True,
    help=("Set reload=True, loglevel=debug, workers=1, threads=1 "
          "and worker_class='sync'")
)
@click.option(
    '-w', '--workers',
    default=1,
    help="Number of workers to use. Defaults to 1 worker."
)
@click.option(
    '-k', '--worker-class', 'worker_class',
    default='sync',
    help="The type of workers to use. Defaults to `sync` type."
)
@click.option(
    '--threads',
    default=1,
    help=("Run each worker with this number of threads. If more than 1, "
          "workerclass='gthread'. Defaults to 1 thread.")
)
@click.option(
    '--log-level', 'loglevel',
    default='info',
    help="The granularity of error log outputs. By default it uses the "
         "python logging module. Defaults to 'info'."
)
@click.option(
    '--access-logfile', 'accesslog',
    help=("File to write information about all requests to the application. "
          "'-' logs to stdout. Defaults to None.")
)
@click.option(
    '--error-logfile', 'errorlog',
    default='-',
    help=("File to write error logs to. '-' logs to stderr. Defaults to '-'.")
)
@click.option(
    '-n', '--name', 'proc_name',
    help=("Base name for naming the running processes. Affects things like "
          "ps and top. Defaults to 'gunicorn'.")
)
@click.option(
    '--pythonpath',
    help="A comma-separated list of directories to add to the Python path."
)
@click.option(
    '-u', '--user',
    help=("Switch worker processes to run as this user. Can be a valid "
          "user id or the name of a user. Defaults to current user.")
)
@click.option(
    '-D', '--daemon', is_flag=True,
    help="Demonize the application. Runs the application in the background."
)
@click.option(
    '--forwarded-allow-ips',
    default='127.0.0.1',
    help=("Front-end’s IPs from which allowed to handle set secure headers "
          "(comma separate). Set * to disable checking of Front-end IPs. "
          "Defaults to '127.0.0.1'.")
)
def run_gunicorn_app(host, port, debug, **settings):
    """Serve Flask application using Gunicorn.

    The Flask application and respective resources and endpoints should
    defined in `app.py` in this same directory.
    """

    logging.basicConfig(level='DEBUG' if debug else 'INFO')

    # Set a global flag that indicates that we were invoked from the
    # command line interface provided server command.  This is detected
    # by Flask.run to make the call into a no-op.  This is necessary to
    # avoid ugly errors when the script that is loaded here also attempts
    # to start a server.
    os.environ['FLASK_RUN_FROM_CLI_SERVER'] = '1'

    settings['bind'] = '{}:{}'.format(host, port)

    if debug:
        app.jinja_env.auto_reload = True
        app.config['TEMPLATES_AUTO_RELOAD'] = True
        settings.update({'loglevel': 'debug',
                         'reload': True,
                         'threads': 1,
                         'workers': 1,
                         'worker_class': 'sync'})
        app.wsgi_app = DebuggedApplication(app.wsgi_app, True)
        logging.info(" * Launching in Debug mode.")
        logging.info(" * Serving application using a single worker.")
    else:
        logging.info(" * Launching in Production Mode.")
        logging.info(" * Serving application with {} worker(s)."
                     .format(settings["workers"]))

    server = GunicornApp(app, settings=settings)
    server.run()


if __name__ == '__main__':
    run_gunicorn_app()
