import requests
import numpy as np
from detect import detect


def on_detect(card_image):
    image = np.array(card_image).tolist()
    resp = requests.post('http://localhost:8888', json={'image': image})
    print(resp.json())


if __name__ == '__main__':
    detect(on_detect)

