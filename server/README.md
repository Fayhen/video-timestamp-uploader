# video-uploader-sample-server

This is a minimal API created with [Flask](https://flask.palletsprojects.com/en/2.0.x/) to receive POST requests from the `client` application. It performs no functions other than logging data to the console and sending back responses with sample data.

## Installation

Please ensure you have Python 3 installed on your system, then set up and activate a virtual environment:

```
python -m venv venv
. ./venv/bin/activate
```

With the virtual environment activated, use `pip` to install this application's requirements:

```
pip install -r requirements.txt
```

Finally, execute either `run.sh` or `run.bat` depending on your operating system. Otherwise, manually set the environment variable `FLASK_APP=api` and then execute `flask run` on your terminal.
