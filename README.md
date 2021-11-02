# video-timestamp-uploader

A simple uploader application which can POST both video files and timestamps contained within the video duration to a server.

The uploader is divided into `client` and `server` applications:

- The `client` consists of an upload form built with [Quasar](https://quasar.dev/), which loads video files and allows the user to define timestamps within the video duration. It also performs validation.
- The `server` application is a simple [Flask](https://flask.palletsprojects.com/en/2.0.x/) API for demonstrational purposes. It receives POST requests from the `client` application and responds with a little bit of information about the received file and timestamps.

Installation and usage instructions can be found on the README files provided in each application directory.
