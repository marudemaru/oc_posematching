import cv2
import mediapipe as mp
import numpy as np
import random
import setting

# MediaPipe Pose初期化
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def draw_avatar(frame, landmarks):
    # 体の各部位を線でつなぐ
    connections = [
        (mp_pose.PoseLandmark.LEFT_SHOULDER, mp_pose.PoseLandmark.RIGHT_SHOULDER),
        (mp_pose.PoseLandmark.LEFT_SHOULDER, mp_pose.PoseLandmark.LEFT_ELBOW),
        (mp_pose.PoseLandmark.LEFT_ELBOW, mp_pose.PoseLandmark.LEFT_WRIST),
        (mp_pose.PoseLandmark.RIGHT_SHOULDER, mp_pose.PoseLandmark.RIGHT_ELBOW),
        (mp_pose.PoseLandmark.RIGHT_ELBOW, mp_pose.PoseLandmark.RIGHT_WRIST),
        (mp_pose.PoseLandmark.LEFT_HIP, mp_pose.PoseLandmark.RIGHT_HIP),
        (mp_pose.PoseLandmark.LEFT_HIP, mp_pose.PoseLandmark.LEFT_KNEE),
        (mp_pose.PoseLandmark.LEFT_KNEE, mp_pose.PoseLandmark.LEFT_ANKLE),
        (mp_pose.PoseLandmark.RIGHT_HIP, mp_pose.PoseLandmark.RIGHT_KNEE),
        (mp_pose.PoseLandmark.RIGHT_KNEE, mp_pose.PoseLandmark.RIGHT_ANKLE)
    ]

    for connection in connections:
        point1 = (int(landmarks[connection[0]].x * setting.width), int(landmarks[connection[0]].y * setting.height))
        point2 = (int(landmarks[connection[1]].x * setting.width), int(landmarks[connection[1]].y * setting.height))
        cv2.line(frame, point1, point2, (255, 255, 255), 5)

    

