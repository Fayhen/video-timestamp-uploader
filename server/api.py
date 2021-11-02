from flask import Flask, request, make_response
from flask_cors import CORS
import time


app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def home():
    msg = 'Hello. Please direct your video transcription requests to the "/video" route.'
    return make_response({ 'message': msg }, 200)

@app.route('/video', methods=['POST'])
def transcription():
    # Get the necessary data from the request data: start time, end time and video file
    startTime = request.form.get('startTime', None)
    endTime = request.form.get('endTime', None)
    videoFile = request.files.get('videoFile', None)

    # Print data to console for viewing
    print(f'startTime: {startTime}')
    print(f'endTime: {endTime}')
    print(f'videoFile: {videoFile}')
    
    # Print some file data to console for viewing
    # Note: The file is stored as a werkzeug.FileStorage class instance
    print(type(videoFile))
    print(videoFile.__dict__)
    print(videoFile.filename)
    print(videoFile.content_type)
    print(videoFile.stream)


    # Simulate time spent generating a transcription
    time.sleep(10)
    sample_transcription = 'This is a sample transcription.'

    return make_response({ 'transcription': sample_transcription }, 201)

