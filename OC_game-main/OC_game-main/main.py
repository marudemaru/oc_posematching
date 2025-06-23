import cv2
import setting
from start import show_start_screen
import Game.stage1 as stage1
import Game.stage2 as stage2
import Game.stage3 as stage3
from score import save_score, display_score_screen
import finish_scene
import Music.bgm as bgm
import Countdown.countdown_main as down
import Game.stage1_scene as s1
import Game.stage2_scene as s2
import Game.stage3_scene as s3

# BGMファイルのパス
BGM_MENUE = './Music/free2.mp3'
BGM_GAME = './Music/free1.mp3'
SOUND_EFFECT_FINISH = './Music/Finish_SE.mp3'
SOUND_EFFECT_TRANSITION = './Music/SE1.mp3'
SOUND_EFFECT_TRANSITION2 = './Music/SE2.mp3'

# BGMの初期化
bgm.initialize_bgm()


print(setting.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
print(setting.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

while True:
    # ゲームの初期化
    stage1.initialize_game()

    # スタート画面の表示
    bgm.play_bgm(BGM_MENUE)
    show_start_screen(setting.cap, setting.window_name)
    bgm.play_sound_effect(SOUND_EFFECT_TRANSITION)

    # Countdown画面の表示
    bgm.stop_bgm()
    down.countdown_main(setting.cap, setting.window_name)

    # ゲームループの実行
    bgm.play_bgm(BGM_GAME)
    s1.stage1_scene(setting.cap , setting.window_name)
    stage1.game_loop(setting.cap, setting.window_name)
    score = stage1.get_score()

    stage2.initialize_game()
    s2.stage2_scene(setting.cap , setting.window_name,score)
    stage2.game_loop(setting.cap, setting.window_name,score)
    score = stage2.get_score()

    stage3.initialize_game()
    s3.stage3_scene(setting.cap , setting.window_name,score)
    stage3.game_loop(setting.cap, setting.window_name,score)
    

    # 結果表示(PC)
    score = stage3.get_score()
    print(f'Final Score: {score}')

    # ゲーム終了アニメーションを表示
    bgm.stop_bgm()
    bgm.play_sound_effect(SOUND_EFFECT_FINISH)
    finish_scene.finish_scene(setting.cap, setting.window_name)

    # スコアの保存
    save_score(score)

    # スコア表示画面の表示
    bgm.play_bgm(BGM_MENUE)
    action = display_score_screen(setting.cap, setting.window_name)

    # ユーザーの選択に応じて処理を分岐
    if action == 'quit':
        break  # プログラムを終了
    elif action == 'restart':
        bgm.play_sound_effect(SOUND_EFFECT_TRANSITION2)
        continue  # ループの先頭に戻り、ゲームを再スタート

setting.cap.release()
cv2.destroyAllWindows()
