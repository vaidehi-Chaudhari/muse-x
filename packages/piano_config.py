# Config file for final DSP project

screen_size = (1300, 650)
background_image = 'resources/white.png'
background_size = None
width_or_height_first = True
piano_image = 'resources/piano.png'
piano_size = None
message_color = (0, 0, 0, 255)
fonts_size = 23
label1_place = (300, 400)
label2_place = (300, 350)
label3_place = (300, 450)
label_anchor_x = 'left'
label_anchor_y = 'center'
fonts = 'Consolas'
bold = True
go_back_image = 'resources/go_back_1.png'
go_back_place = 50, 550
nyu_image = 'resources/nyu_image.png'
nyu_place = 1100, 550
self_play_image = 'resources/play_1.png'
self_play_place = 50, 480
button_resize_num = 2.3
fps = 60

key_settings = {
    'z': 'A#1',
    'x': 'B1',
    'c': 'C2',
    'v': 'C#2',
    'b': 'D2',
    'n': 'D#2',
    'm': 'E2',
    ',': 'F2',
    '.': 'F#2',
    '/': 'G2',
    'a': 'G#2',
    's': 'A2',
    'd': 'A#2',
    'f': 'B2',
    'g': 'C3',
    'h': 'C#3',
    'j': 'D3',
    'k': 'D#3',
    'l': 'E3',
    ';': 'F3',
    "'": 'F#3',
    'enter': 'G3',
    'tab': 'G#3',
    'q': 'A3',
    'w': 'A#3',
    'e': 'B3',
    'r': 'C4',
    't': 'C#4',
    'y': 'D4',
    'u': 'D#4',
    'i': 'E4',
    'o': 'F4',
    'p': 'F#4',
    '[': 'G4',
    ']': 'G#4',
    '\\': 'A4',
    '`': 'A#4',
    '1': 'B4',
    '2': 'C5',
    '3': 'C#5',
    '4': 'D5',
    '5': 'D#5',
    '6': 'E5',
    '7': 'F5',
    '8': 'F#5',
    '9': 'G5',
    '0': 'G#5',
    '-': 'A5',
    '=': 'A#5',
    'backspace': 'B5',
    'f1': 'C6',
    'f2': 'C#6',
    'f3': 'D6',
    'f4': 'D#6',
    'f5': 'E6',
    'f6': 'F6',
    'f7': 'F#6',
    'f8': 'G6',
    'f9': 'G#6',
    'f10': 'A6',
    'f11': 'A#6',
    'f12': 'B6'
}

midi_device_id = 1
device_info_num = 10

pause_key = 'space'
repeat_key = 'ctrl'
unpause_key = 'enter'
pause_key_clear_notes = False

frequency = 44100
size = -16
channel = 2
buffer = 1024
max_num_channels = 100
global_volume = 0.6

# if delay is set to True, when you are self playing, the sounds will
delay = True
delay_time = 3
fadeout_ms = 100

# touch interval is when the sound is still on delay

touch_interval = 0.1

# if this parameter is set to True,

delay_only_read_current = True

# the suffix of the sound files
sound_format = 'wav'

# the path of the sounds folder
sound_path = 'resources/sounds'

show_delay_time = 1

# these are the parameters for chord types detections
detect_mode = 'chord'
inv_num = False
change_from_first = True
original_first = True
same_note_special = False
whole_detect = True
return_fromchord = False
poly_chord_first = False
root_position_return_first = True
alter_notes_show_degree = True

# if  True, then it enables the config key during pyaling
config_enable = True

config_key = 'lctrl'

# volume change keys
volume_up = '='
volume_down = '-'

volume_change_unit = 0.01

change_delay = 'd'
change_read_current = 'c'
change_pause_key_clear_notes = 'x'

note_place = [
    (-5.0, 50), (10, 102), (19.6, 50), (44.2, 50), (59.0, 102), (68.8, 50),
    (83.6, 102), (93.4, 50), (118.0, 50), (132.8, 102), (142.6, 50),
    (157.4, 102), (167.2, 50), (182.0, 102), (191.8, 50), (216.4, 50),
    (231.2, 102), (241.0, 50), (255.8, 102), (265.6, 50), (290.2, 50),
    (305.0, 102), (314.8, 50), (329.6, 102), (339.4, 50), (354.2, 102),
    (364.0, 50), (388.6, 50), (403.4, 102), (413.2, 50), (428.0, 102),
    (437.8, 50), (462.4, 50), (477.2, 102), (487.0, 50), (501.8, 102),
    (511.6, 50), (526.4, 102), (536.2, 50), (560.8, 50), (575.6, 102),
    (585.4, 50), (600.2, 102), (610.0, 50), (634.6, 50), (649.4, 102),
    (659.2, 50), (674.0, 102), (683.8, 50), (698.6, 102), (708.4, 50),
    (733.0, 50), (747.8, 102), (757.6, 50), (772.4, 102), (782.2, 50),
    (806.8, 50), (821.6, 102), (831.4, 50), (846.2, 102), (856.0, 50),
    (870.8, 102), (880.6, 50), (905.2, 50), (920.0, 102), (929.8, 50),
    (944.6, 102), (954.4, 50), (979.0, 50), (993.8, 102), (1003.6, 50),
    (1018.4, 102), (1028.2, 50), (1043.0, 102), (1052.8, 50), (1077.4, 50),
    (1092.2, 102), (1102.0, 50), (1116.8, 102), (1126.6, 50), (1151.2, 50),
    (1166.0, 102), (1175.8, 50), (1190.6, 102), (1200.4, 50), (1215.2, 102),
    (1225.0, 50), (1249.6, 50)
]

load_sound = True

# show_key set to True will show what keyboard keys you are pressing
show_key = False

# detect chord types when the current notes change
show_chord = True
show_notes = True

# the parameters of the function split_melody
melody_tol = 10
chord_tol = 9
get_off_overlap_notes = False
average_degree_length = 8
melody_degree_tol = 'B4'

# notes showing mode: choose one from 'dots' and 'bars' and 'bars drop',
note_mode = 'bars drop'
bar_width = 14
bar_height = 20
#bar_color = (124, 252, 0)
bar_color = (148,0,211)
#sustain_bar_color = (124, 200, 0)
sustain_bar_color = (148, 0, 211)
bar_y = 178
bar_offset_x = 6
dots_offset_x = 10
bar_opacity = 160
opacity_change_by_velocity = True
# color mode: choose one from 'normal' and 'rainbow'
color_mode = 'rainbow'
bar_steps = 6
bar_unit = 400
bar_hold_increase = 5
bars_drop_interval = 2
bars_drop_place = 173
adjust_ratio = 62
bar_border = 5
bar_border_color = (100, 100, 100)
get_off_drums = True
sort_invisible = False
play_as_midi = True
draw_piano_keys = True
white_key_width = 23
white_key_height = 138
white_key_interval = 25
white_key_y = 37
white_keys_number = 52
white_key_start_x = 0
white_key_color = (255, 255, 255)

black_key_width = 15
black_key_height = 90
black_key_y = 85
black_key_first_x = 18
black_key_start_x = 64.467
black_key_color = (0, 0, 0)

black_keys_set = [0, 30, 43.85, 28.67, 28.48]
black_keys_set_interval = 43.75
black_keys_set_num = 7

piano_key_border = 0
piano_key_border_color = (100, 100, 100)

piano_background_image = 'resources/piano_background.png'

show_music_analysis = False
music_analysis_file = None
music_analysis_place = (250, 500)
key_header = 'current key: '
music_analysis_width = 1300
music_analysis_fonts_size = 20

use_track_colors = True
tracks_colors = [(0, 255, 0), (255, 255, 0), (0, 0, 255), (0, 255, 255),
                 (255, 0, 255), (0, 128, 0), (0, 191, 255), (0, 255, 127),
                 (0, 128, 128), (0, 0, 128), (255, 215, 0), (255, 165, 0),
                 (124, 252, 0), (238, 130, 238), (218, 112, 214),
                 (255, 20, 147)]
use_default_tracks_colors = True
pitch_range = ('A0', 'C8')

use_soundfont = False
play_use_soundfont = False
sf2_path = 'resources/gm.sf2'
bank = 0
preset = 0
sf2_duration = 6
sf2_decay = 1
sf2_volume = 100

soft_pedal_volume = 0.2

render_as_audio = False

language = 'English'
