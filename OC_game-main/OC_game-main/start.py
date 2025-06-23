import cv2
import setting
import mediapipe as mp
import numpy as np
import time

# MediaPipe Pose初期化
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

halfwidth = setting.width // 2
halfheight = setting.height // 2
video_path = "c:/Users/81908/Desktop/研究室/OpenCanpus/OC_game/Movie/loading.mp4"  # ここにローディング動画のパスを記載

def show_start_screen(cap, window_name):
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
                cv2.circle(frame, right_hand_pos, setting.point_radius, (0, 0, 0), -1)  # 黒い円
                cv2.circle(frame, left_hand_pos, setting.point_radius, (0, 0, 0), -1)  # 黒い円
                cv2.circle(frame, right_foot_pos, setting.point_radius, (0, 0, 0), -1)  # 黒い円
                cv2.circle(frame, left_foot_pos, setting.point_radius, (0, 0, 0), -1)  # 黒い円

                # 右手または左手が四角形の枠内に入ったかを判定
                if (halfwidth - 20 <= right_hand_pos[0] <= halfwidth + 20 and halfheight + 20 <= right_hand_pos[1] <= halfheight + 60) or \
                   (halfwidth - 20 <= left_hand_pos[0] <= halfwidth + 20 and halfheight + 20 <= left_hand_pos[1] <= halfheight + 60) or \
                   (halfwidth - 20 <= right_foot_pos[0] <= halfwidth + 20 and halfheight + 20 <= right_foot_pos[1] <= halfheight + 60) or \
                   (halfwidth - 20 <= left_foot_pos[0] <= halfwidth + 20 and halfheight + 20 <= left_foot_pos[1] <= halfheight + 60):
                    # ローディング動画を再生
                    #play_loading_video(window_name,frame)
                    break

            # タッチポイントを描画
            cv2.rectangle(frame, (halfwidth - 20, halfheight + 20), (halfwidth + 20, halfheight + 60), (255, 255, 0),thickness=3)
            
            # タッチポイントが出てくる範囲
            cv2.line(frame,(setting.width//4*3,setting.height//5),(setting.width//4*3,setting.height),(0,0,0),thickness = 5,lineType=cv2.LINE_AA)
            cv2.line(frame,(setting.width//4,setting.height//5),(setting.width//4,setting.height),(0,0,0),thickness = 5,lineType=cv2.LINE_AA)
            cv2.line(frame,(setting.width//4,setting.height//5),(setting.width//4*3,setting.height//5),(0,0,0),thickness = 5,lineType=cv2.LINE_AA)


            # textを表示
            cv2.putText(frame, 'Start', (halfwidth-80, halfheight), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3, cv2.LINE_AA)
            
            # 画像を表示
            cv2.imshow(window_name, frame)
            key = cv2.waitKey(1) & 0xFF

            if key == 27:  # "ESC"キーが押されたら終了
                break

            if key == ord('s'):  # "s"キーが押されたらゲームを開始
                return

def play_loading_video(window_name,frame):
    video_cap = cv2.VideoCapture(video_path)
    start_time = time.time()

    while True:
        ret, video_frame = video_cap.read()
        if not ret:
            break

        # 動画フレームをリサイズ
        resized_video_frame = cv2.resize(video_frame, (40, 40))  # サイズを枠のサイズに合わせる

        # 動画フレームを指定したエリアに挿入
        frame[halfheight+20:halfheight+60, halfwidth-20:halfwidth+20] = resized_video_frame

        # ローディング動画をウィンドウに表示
        cv2.imshow(window_name, frame)

        if cv2.waitKey(1) & 0xFF == 27:  # "ESC"キーが押されたら終了
            break

        if time.time() - start_time > 3:  # 3秒後に終了
            break

    video_cap.release()
