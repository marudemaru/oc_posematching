import Countdown.countdown1 as cd1
import Countdown.countdown2 as cd2
import Countdown.countdown3 as cd3
import Countdown.countdown_start as cd_s
import Countdown.space as space
import Music.bgm as bgm

SOUND_EFFECT_countdown = './Music/countdown.mp3'

def countdown_main(cap, window_name):
    space.space(cap,window_name)

    bgm.play_sound_effect(SOUND_EFFECT_countdown)
    cd3.countdown3(cap,window_name)
    cd2.countdown2(cap,window_name)
    cd1.countdown1(cap,window_name)
    cd_s.countdown_start(cap,window_name)
    