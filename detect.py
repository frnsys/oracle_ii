import cv2
import util
import pygame
import imutils
import numpy as np
import pygame.camera
from pygame.locals import KEYDOWN, K_q

DEBUG = True

# calibrate this for camera position
MIN_CARD_AREA = 250000.0/3


def detect(on_detect):
    dim = (800,600)
    pygame.camera.init()
    cams = pygame.camera.list_cameras()
    cam = pygame.camera.Camera(cams[-1], dim)
    cam.start()

    pygame.init()
    display = pygame.display.set_mode(dim, 0)
    capture = True
    while capture:
        img = cam.get_image()
        img = pygame.transform.scale(img, dim)
        img = util.pygame_to_cv2(img)

        # preprocess image
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        gray = cv2.bilateralFilter(gray, 11, 17, 17) # calibrate
        ret, gray = cv2.threshold(gray, 100,160,0)   # calibrate
        edges = imutils.auto_canny(gray)

        # extract contours
        _, cnts, _ = cv2.findContours(edges.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = [c for c in cnts if cv2.contourArea(c) >= MIN_CARD_AREA]

        c, card = None, None
        if cnts:
            # get largest contour
            c = sorted(cnts, key=cv2.contourArea, reverse=True)[0]

            # approximate the contour
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.05 * peri, True)
            pts = np.float32(approx)

            x,y,w,h = cv2.boundingRect(c)

            # Find center point of card by taking x and y average of the four corners.
            # average = np.sum(pts, axis=0)/len(pts)
            # cent_x = int(average[0][0])
            # cent_y = int(average[0][1])
            # center = [cent_x, cent_y]

            # Warp card into 200x300 flattened image using perspective transform
            card = util.flattener(img, pts, w, h)
            card = util.cv2_to_pil(card).rotate(180)

        # display
        if card is not None:
            on_detect(card)
            cv2.drawContours(img, [c], -1, (0, 0, 255), 3)
        img = util.cv2_to_pygame(img)
        display.blit(img, (0,0))

        # for debugging
        if DEBUG:
            for layer in [gray, edges]:
                layer = cv2.cvtColor(layer, cv2.COLOR_GRAY2RGB)
                layer = util.cv2_to_pygame(layer)
                layer.set_alpha(100)
                display.blit(layer, (0,0))
        pygame.display.flip()

        # q to quit
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_q:
                capture = False

    cam.stop()
    pygame.quit()