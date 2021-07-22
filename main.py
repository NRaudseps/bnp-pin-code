from base64 import b64decode
from os import listdir
from os.path import isfile, join

import cv2
import flask
import numpy as np


def read64(base64_string):
    np_arr = np.frombuffer(b64decode(base64_string), np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_UNCHANGED)
    return img


class BNPCodeOrder:
    def __init__(self, screen_image):
        self.screen_image = screen_image
        self.number_images = sorted([f for f in listdir('img') if isfile(join('img', f))])
        self.code = [7, 8, 5, 1, 4, 9]

    def get_pin_code_order(self):
        positions = dict()
        for index, image in enumerate(self.number_images):
            number_image = cv2.imread(f'img/{image}', cv2.IMREAD_UNCHANGED)

            # This method finds the position of the number in the image
            result = cv2.matchTemplate(self.screen_image, number_image, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            position = round(max_loc[0], -1), round(max_loc[1], -1)
            positions[index] = position

        positions = self.sort_sequence(positions)

        code_order = []
        for index in self.code:
            code_order.append(positions.index(index))
        return code_order

    @staticmethod
    def sort_sequence(number_sequence):
        row_y_axis = [420, 500]
        rows = []
        for y_axis in row_y_axis:
            # Separate by Y axis
            row = {k: v for k, v in number_sequence.items() if v[1] == y_axis}
            # Sort by X axis
            row = sorted(row.items(), key=lambda x_axis: x_axis[1][0])
            # Turn dict to array
            row = [v[0] for v in row]
            rows += row
        return rows


app = flask.Flask(__name__)


@app.route('/', methods=['POST'])
def home():
    file = read64(flask.request.files['media'].read())
    pin_code_order = BNPCodeOrder(file).get_pin_code_order()

    return {
        'order': pin_code_order
    }


if __name__ == '__main__':
    app.run()
