# app-skeleton

Skeleton of a Flask application which can be used in production.

###Contents

 - Flask application template in `app/app.py`.
 - Input form with different input types examples `app/templates/input.html`.
 - Class wrapper to extend the Flask application using Gunicorn `app/resources/gunicorn_wrapper.py`.
 - Example class which handles the form submission `app/resources/form_submitter.py`.
 - Function handling Gunicorn command line arguments `app/run_app.py`.
 - Folder with all necessary files for putting the application into a Docker container.
 - Basic example of running a model based in user inputs and showing results in a pandas DataFrame as html.
 
### Run application
To run the application execute the command
```bash
python run_app.py [Options]
```
where `Options` are a few of Gunicorn's possible optional settings. To see which settings can be specified execute `python app/run_app.py --help`. Except for the `--debug` argument (more in the **Run in debug mode** section), all others have a one-to-one relationship with a Gunicorn setting.

By default if running without options `python run_app.py`, `loglevel` will be set to `info`, `workers` and `threads` to `1`, and the application will be hosted in `localhost` under `port` `5000`.

[Here](http://docs.gunicorn.org/en/stable/settings.html) is a list of all Gunicorn's settings, including the default values.

### Run in debug mode
In short, by running in debug mode you will use a single process, log level will be set to debug and process will restart when code or html changes.

You can run in debug mode by executing
```bash
python run_app.py --debug
```
this will ovewrite the following Gunicorn settings:

 -  `loglevel = 'debug'`
 - `reload = True`
 - `threads = 1`
 - `workers = 1`
 - `worker_class = 'sync'`
 
 In addition it will overwrite some Flask configuration settings
  
  - `app.jinja_env.auto_reload = True`
  - `app.config['TEMPLATES_AUTO_RELOAD'] = True`

## Run as native Flask application

If you still want to run the application as a native Flask application without gunicorn you can do that by executing

```bash
export FLASK_APP=app/app.py; flask run [Options]
```

more information can be found [here](http://flask.pocoo.org/docs/0.12/quickstart/).

### Docker


### Model prediction example 
