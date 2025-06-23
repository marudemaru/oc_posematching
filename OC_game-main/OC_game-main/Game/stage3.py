import cv2
import mediapipe as mp
import numpy as np
import random
import time
import Game.avater as avater
import setting


# MediaPipe Pose初期化
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# グローバル変数の定義
game_duration = 30  # ゲームの長さ（秒）
target_radius = 15  # 円の半径
target_color_1 = (0, 0, 255)  # 赤
target_color_2 = (255, 0, 0)  # 青
golden_color = (0, 215, 255)  # 金
target_pos = None
rand = random.randint(1, 5)  # 初期化（1,2: 赤, 3,4: 青, 5: 金）
last_target_time = None  # ターゲット生成時間

def initialize_game():
    global target_pos, rand, last_target_time
    rand = random.randint(1, 5)
    target_pos = (random.randint(target_radius+setting.width//4, 3*setting.width//4 - target_radius), random.randint(target_radius+setting.height//5, setting.height - target_radius))
    last_target_time = time.time()

def get_score():
    global score
    return score

def game_loop(cap, window_name, s2_score):
    global score, target_pos, rand, last_target_time
    score = s2_score
    start_time = time.time()
    initialize_game()  # ゲーム開始時にターゲットを初期化

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # 画像を鏡像にし、BGRからRGBに変換
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # 姿勢推定
            results = pose.process(rgb_frame)

            # 結果を描画
            if results.pose_landmarks:
                avater.draw_avatar(frame, results.pose_landmarks.landmark)

                # 手の位置を取得
                left_hand = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_INDEX]
                right_hand = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_INDEX]
                left_hand_pos = (int(left_hand.x * setting.width), int(left_hand.y * setting.height))
                right_hand_pos = (int(right_hand.x * setting.width), int(right_hand.y * setting.height))

                # 足の位置を取得
                left_foot = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE]
                right_foot = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE]
                left_foot_pos = (int(left_foot.x * setting.width), int(left_foot.y * setting.height))
                right_foot_pos = (int(right_foot.x * setting.width), int(right_foot.y * setting.height))


                # 当たり判定のエリアを描画
                cv2.circle(frame, right_hand_pos, setting.point_radius, target_color_1, -1)  # 赤い円
                cv2.circle(frame, left_hand_pos, setting.point_radius, target_color_2, -1)  # 青い円
                cv2.circle(frame, right_foot_pos, setting.point_radius, target_color_2, -1)  # 青い円
                cv2.circle(frame, left_foot_pos, setting.point_radius, target_color_1, -1)  # 赤い円


                # タッチの判定
                if (rand in [1, 2] and np.linalg.norm(np.array(right_hand_pos) - np.array(target_pos)) < target_radius + setting.point_radius) or \
                   (rand in [1, 2] and np.linalg.norm(np.array(left_foot_pos) - np.array(target_pos)) < target_radius + setting.point_radius):
                    score += 5
                    initialize_game()  # 新しいターゲットを生成
                elif (rand in [3, 4] and np.linalg.norm(np.array(left_hand_pos) - np.array(target_pos)) < target_radius + setting.point_radius) or \
                     (rand in [3, 4] and np.linalg.norm(np.array(right_foot_pos) - np.array(target_pos)) < target_radius + setting.point_radius):
                    score += 5
                    initialize_game()  # 新しいターゲットを生成
                elif rand == 5 and ((np.linalg.norm(np.array(right_hand_pos) - np.array(target_pos)) < target_radius + setting.point_radius) or \
                                   (np.linalg.norm(np.array(left_hand_pos) - np.array(target_pos)) < target_radius + setting.point_radius) or \
                                   (np.linalg.norm(np.array(right_foot_pos) - np.array(target_pos)) < target_radius + setting.point_radius) or \
                                   (np.linalg.norm(np.array(left_foot_pos) - np.array(target_pos)) < target_radius + setting.point_radius)):
                    score += 3
                    initialize_game()  # 新しいターゲットを生成

            # タッチポイントを描画
            elapsed_target_time = time.time() - last_target_time
            if elapsed_target_time > 2:  # ターゲットが表示されてから2秒経過した場合
                initialize_game()

            if rand in [1, 2]:
                cv2.circle(frame, target_pos, target_radius, target_color_1, -1)  # 赤いターゲット
            elif rand in [3, 4]:
                cv2.circle(frame, target_pos, target_radius, target_color_2, -1)  # 青いターゲット
            elif rand == 5:
                cv2.circle(frame, target_pos, target_radius, golden_color, -1)  # 金のターゲット

            # 経過時間を描画
            elapsed_time = time.time() - start_time
            cv2.putText(frame, f'Time: {int(game_duration - elapsed_time)}', (setting.halfwidth+200, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 0), 3, cv2.LINE_AA)

            # スコアを描画
            if elapsed_time <= game_duration / 2:
                cv2.putText(frame, f'Score: {score}', (setting.halfwidth-400, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 0), 3, cv2.LINE_AA)
            else:
                cv2.putText(frame, 'Score: ???', (setting.halfwidth-400, 100), cv2.FONT_HERSHEY_SIMPLEX,3, (0, 0, 0), 3, cv2.LINE_AA)

            # ゲーム終了判定
            if elapsed_time > game_duration:
                break

            # 画像を表示
            cv2.imshow(window_name, frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break
