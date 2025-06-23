import cv2
import time
import numpy as np
import setting

halfwidth=setting.width//3
halfheight=setting.height//2


def stage3_scene(cap, window_name,score):
    start_time = time.time()
    animation_duration = 3

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 画像を鏡像にし、スコアを描画
        frame = cv2.flip(frame, 1)

        elapsed_time = time.time() - start_time

        if elapsed_time > animation_duration:
            break

        # アニメーションの内容を描画
        alpha = elapsed_time / animation_duration
        overlay = frame.copy()
        cv2.putText(overlay, 'STAGE3', (setting.halfwidth-80,setting.halfheight), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 10, cv2.LINE_AA)
        cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

        # スコアを描画
        cv2.putText(frame, f'Score: {score}', (setting.halfwidth-80, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 0), 3, cv2.LINE_AA)


        cv2.imshow(window_name, frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
