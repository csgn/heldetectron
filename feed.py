import cv2
import numpy as np

from flask import Flask, Response, render_template, request
from source import Source
from predict import load_predictor, draw_bboxes, make_predict

app = Flask(__name__)
predictor = load_predictor()

def gen(inference, source):
    while True:
        success, frame = next(source.frames())
        if success:
            if inference > 0:
                result = make_predict(predictor, frame)
                final_frame = np.squeeze(draw_bboxes(frame, result))

            _, encoded_frame = cv2.imencode('.jpg', final_frame)

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + encoded_frame.tobytes() + b'\r\n')

    del source

@app.route('/feed/<inference>/<path:source_url>', methods=['GET'])
def video_feed(inference=0, source_url=0):
    try:
        return Response(gen(int(inference), Source(source_url)), 
                        200,
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    except Exception as e:
        return Response(str(e), 500)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', threaded=True)
