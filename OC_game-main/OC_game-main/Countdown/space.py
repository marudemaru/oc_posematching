import cv2
import time
import numpy as np

def space(cap, window_name):
    start_time = time.time()
    animation_duration = 1

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 画像を鏡像にし、スコアを描画
        frame = cv2.flip(frame, 1)

        elapsed_time = time.time() - start_time

        if elapsed_time > animation_duration:
            break

        cv2.imshow(window_name, frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
