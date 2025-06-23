import cv2
import os
import mediapipe as mp
import numpy as np
import setting

# MediaPipe Pose初期化
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

halfwidth = setting.width // 2
halfheight = setting.height // 2

# スコアを保存するファイルのパス
SCORE_FILE = 'scores.txt'

def save_score(score):
    with open(SCORE_FILE, 'a') as file:
        file.write(f'{score}\n')

def get_high_scores():
    if not os.path.exists(SCORE_FILE):
        return []
    with open(SCORE_FILE, 'r') as file:
        scores = file.readlines()
    scores = [int(score.strip()) for score in scores]
    scores.sort(reverse=True)
    return scores

def get_last_scores():
    with open(SCORE_FILE, 'r') as file:
        scores = file.readlines()
    last_score = scores[-1].strip()
    return last_score

def display_score_screen(cap, window_name):
    high_scores = get_high_scores()
    last_score = get_last_scores()
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # 画像を鏡像にし、スコアを描画
            frame = cv2.flip(frame, 1)
            cv2.putText(frame, 'High Scores:', (halfwidth-400, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2, cv2.LINE_AA)
            cv2.putText(frame, 'Your Scores:', (halfwidth+200, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2, cv2.LINE_AA)
            cv2.putText(frame, f'{last_score}', (halfwidth+200, 110), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2, cv2.LINE_AA)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # 姿勢推定
            results = pose.process(rgb_frame)

            for i, score in enumerate(high_scores[:5], start=1):
                cv2.putText(frame, f'{i}. {score}', (halfwidth-400, 50 + i * 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2, cv2.LINE_AA)

            # 結果を描画
            if results.pose_landmarks:

                # 手の位置を取得
                left_hand = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_INDEX]
                right_hand = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_INDEX]
                left_hand_pos = (int(left_hand.x * setting.width), int(left_hand.y * setting.height))
                right_hand_pos = (int(right_hand.x * setting.width), int(right_hand.y * setting.height))

                # 当たり判定のエリアを描画
                cv2.circle(frame, right_hand_pos, setting.point_radius, (0, 0, 0), -1)  # 黒い円
                cv2.circle(frame, left_hand_pos, setting.point_radius, (0, 0, 0), -1)  # 黒い円

                # 右手または左手がReStartの枠内に入ったかを判定
                if (halfwidth - 150 <= right_hand_pos[0] <= halfwidth - 110 and halfheight + 100 <= right_hand_pos[1] <= halfheight + 140) or \
                   (halfwidth - 150 <= left_hand_pos[0] <= halfwidth - 110 and halfheight + 100 <= left_hand_pos[1] <= halfheight + 140):
                    return 'restart'  # 再スタート
                
                # 右手または左手がfinishの枠内に入ったかを判定
                if (halfwidth + 110 <= right_hand_pos[0] <= halfwidth + 150 and halfheight + 100 <= right_hand_pos[1] <= halfheight + 140) or \
                   (halfwidth + 110 <= left_hand_pos[0] <= halfwidth + 150 and halfheight + 100 <= left_hand_pos[1] <= halfheight + 140):
                    return 'quit'  # 終了

            # タッチポイントを描画
            cv2.rectangle(frame, (halfwidth - 150, halfheight + 100), (halfwidth - 110, halfheight + 140), (255, 255, 0),thickness=3)

            # タッチポイントを描画
            cv2.rectangle(frame, (halfwidth + 110, halfheight + 100), (halfwidth + 150, halfheight + 140), (255, 255, 0),thickness=3)

            # textを表示
            cv2.putText(frame, 'ReStart', (halfwidth-230, halfheight+80), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3, cv2.LINE_AA)

            # textを表示
            cv2.putText(frame, 'Finish', (halfwidth+50, halfheight+80), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3, cv2.LINE_AA)
            
            # 画像を表示
            cv2.imshow(window_name, frame)
            key = cv2.waitKey(1) & 0xFF

            if key == ord('q'):
                return 'quit'  # 終了
            elif key == ord('r'):
                return 'restart'  # 再スタート
            if cv2.waitKey(1) & 0xFF == 27:
                return 'quit' 

