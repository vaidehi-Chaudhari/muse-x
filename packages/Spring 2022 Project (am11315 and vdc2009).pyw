import random

if sys.platform == 'darwin':
    piano_field = tk.Tk()
    piano_field.withdraw()
    piano_field.destroy()

if piano_config.language == 'English':
    from languages.en import language_patch
elif piano_config.language == 'hindi':
    from languages.cn import language_patch
    mp.detect = language_patch.detect

if (piano_config.play_as_midi
        and piano_config.use_soundfont) or piano_config.play_use_soundfont:
    import sf2_loader as rs

key = pyglet.window.key


def get_off_sort(a):
    piano = language_patch.am11vdc2009_language_dict['sort']
    amvc_nyu = a.split('/')
    for i in range(len(amvc_nyu)):
        current = amvc_nyu[i]
        if piano in current:
            current = current[:current.index(piano) - 1]
            if current[0] == '[':
                current += ']'
            amvc_nyu[i] = current
    return '/'.join(amvc_nyu)


def load(dic, path, file_format, volume):
    wavedict = {
        i: pygame.mixer.Sound(f'{path}/{dic[i]}.{file_format}')
        for i in dic
    }
    if volume != None:
        [wavedict[x].set_volume(volume) for x in wavedict]
    return wavedict


def SoundFont(dic, sf2, volume):
    wavedict = {
        i: pygame.mixer.Sound(
            buffer=sf2.export_note(dic[i],
                                   duration=piano_config.sf2_duration,
                                   decay=piano_config.sf2_decay,
                                   volume=piano_config.sf2_volume,
                                   get_audio=True).raw_data)
        for i in dic
    }
    if volume != None:
        [wavedict[x].set_volume(volume) for x in wavedict]
    return wavedict


def image_vdc(img):
    return pyglet.image.load(img).get_texture()


def update(dt):
    pass


class amvc_dsp_button:

    def __init__(self, img, x, y):
        self.img = image_vdc(img).get_transform()
        self.img.width /= piano_config.button_resize_num
        self.img.height /= piano_config.button_resize_num
        self.x = x
        self.y = y
        self.button = pyglet.sprite.Sprite(self.img, x=self.x, y=self.y)
        self.ranges = [self.x, self.x + self.img.width
                       ], [self.y, self.y + self.img.height]

    def get_range(self):
        height, width = self.img.height, self.img.width
        return [self.x, self.x + width], [self.y, self.y + height]

    def inside(self, pos_mouse):
        range_of_x, range_of_y = self.ranges
        return range_of_x[0] <= pos_mouse[0] <= range_of_x[1] and range_of_y[
            0] <= pos_mouse[1] <= range_of_y[1]

    def draw(self):
        self.button.draw()


class piano_nyu(pyglet.window.Window):

    def __init__(self):
        self.init_window()
        self.init_mtsp()
        self.init_key_map()
        self.init_keys()
        self.init_sreecn()
        self.init_layers()
        self.init_buttons()
        self.init_our_piano_keys()
        self.init_note_mode()
        self.init_sreecn_labels()
        self.init_music_analysis()

    def init_window(self):
        super(piano_nyu, self).__init__(*piano_config.screen_size,
                                           caption='Spring 2022 Project ( am11315 and vdc2009 )',
                                           resizable=True,
                                           file_drops=True)
        self.icon = pyglet.image.load('resources/piano.ico')
        self.set_icon(self.icon)
        self.handles_keys = key.KeyStateHandler()
        self.push_handlers(self.handles_keys)

    def init_key_map(self):
        self.map_key_dict = {
            each.lower().lstrip('_'): value
            for each, value in key.__dict__.items() if isinstance(value, int)
        }
        self.can_rever = {
            j: i
            for i, j in self.map_key_dict.items()
        }
        self.can_rever[59] = ';'
        self.can_rever[39] = "'"
        self.can_rever[44] = ","
        self.can_rever[46] = "."
        self.can_rever[47] = '/'
        self.can_rever[91] = '['
        self.can_rever[93] = ']'
        self.can_rever[92] = '\\'
        self.can_rever[96] = '`'
        self.can_rever[45] = '-'
        self.can_rever[61] = '='
        self.can_rever[65288] = 'backspace'
        self.dicts_gapping = {
            j: i
            for i, j in self.can_rever.items()
        }

    def init_keys(self):
        self.pause_key = self.map_key_dict.setdefault(piano_config.pause_key,
                                                      key.SPACE)
        self.repeat_key = self.map_key_dict.setdefault(piano_config.repeat_key,
                                                       key.LCTRL)
        self.unpause_key = self.map_key_dict.setdefault(
            piano_config.unpause_key, key.ENTER)
        self.config_key = self.map_key_dict.setdefault(piano_config.config_key,
                                                       key.LALT)

  
    def init_sreecn(self):
        self.screen_width, self.screen_height = piano_config.screen_size
        self.show_delay_time = int(piano_config.show_delay_time * 1000)
        pygame.mixer.init(piano_config.frequency, piano_config.size,
                          piano_config.channel, piano_config.buffer)
        pygame.mixer.set_num_channels(piano_config.max_num_channels)
        try:
            background = image_vdc(piano_config.background_image)
        except:
            background = image_vdc('resources/white.png')
        if not piano_config.background_size:
            if piano_config.width_or_height_first:
                ratio_background = self.screen_width / background.width
                background.width = self.screen_width
                background.height *= ratio_background
            else:
                ratio_background = self.screen_height / background.height
                background.height = self.screen_height
                background.width *= ratio_background
        else:
            background.width, background.height = piano_config.background_size
        self.background = background

    def init_layers(self):
        self.batch = pyglet.graphics.Batch()
        self.bottom_group = pyglet.graphics.OrderedGroup(0)
        self.piano_bg = pyglet.graphics.OrderedGroup(1)
        self.piano_key = pyglet.graphics.OrderedGroup(2)
        self.play_highlight = pyglet.graphics.OrderedGroup(3)

    def init_note_mode(self):
        if not piano_config.draw_piano_keys:
            self.bar_offset_x = 9
            image = image_vdc(piano_config.piano_image)
            if not piano_config.piano_size:
                ratio = self.screen_width / image.width
                image.width = self.screen_width
                image.height *= ratio
            else:
                image.width, image.height = piano_config.piano_size
            self.image_show = pyglet.sprite.Sprite(image,
                                                   x=0,
                                                   y=0,
                                                   batch=self.batch,
                                                   group=self.piano_bg)

        piano_eng.plays = []
        if piano_config.note_mode == 'bars drop':
            piano_eng.br_dr = []
            distances = self.screen_height - self.piano_height
            self.bars_drop_interval = piano_config.bars_drop_interval
            self.bar_steps = (distances / self.bars_drop_interval
                              ) / piano_config.adjust_ratio
        else:
            self.bar_steps = piano_config.bar_steps
            self.bars_drop_interval = 0

    def init_buttons(self):
        if piano_config.language == 'hindi':
            piano_config.go_back_image = 'packages/languages/cn/go_back.png'
            piano_config.self_play_image = 'packages/languages/cn/play.png'
           
        self.backwrd_but = amvc_dsp_button(piano_config.go_back_image,
                                                 *piano_config.go_back_place)
        self.self_play_button = amvc_dsp_button(
            piano_config.self_play_image, *piano_config.self_play_place)
        
        self.nyu_image_button = amvc_dsp_button(
            piano_config.nyu_image, *piano_config.nyu_place)

    def init_sreecn_labels(self):
        self.label = pyglet.text.Label('',
                                       font_name=piano_config.fonts,
                                       font_size=piano_config.fonts_size,
                                       bold=piano_config.bold,
                                       x=piano_config.label1_place[0],
                                       y=piano_config.label1_place[1],
                                       color=piano_config.message_color,
                                       anchor_x=piano_config.label_anchor_x,
                                       anchor_y=piano_config.label_anchor_y,
                                       multiline=True,
                                       width=1000)
        self.label2 = pyglet.text.Label('',
                                        font_name=piano_config.fonts,
                                        font_size=piano_config.fonts_size,
                                        bold=piano_config.bold,
                                        x=piano_config.label2_place[0],
                                        y=piano_config.label2_place[1],
                                        color=piano_config.message_color,
                                        anchor_x=piano_config.label_anchor_x,
                                        anchor_y=piano_config.label_anchor_y)
        self.label3 = pyglet.text.Label('',
                                        font_name=piano_config.fonts,
                                        font_size=piano_config.fonts_size,
                                        bold=piano_config.bold,
                                        x=piano_config.label3_place[0],
                                        y=piano_config.label3_place[1],
                                        color=piano_config.message_color,
                                        anchor_x=piano_config.label_anchor_x,
                                        anchor_y=piano_config.label_anchor_y)

        self.le_mid = pyglet.text.Label(
            '',
            font_name=piano_config.fonts,
            font_size=15,
            bold=piano_config.bold,
            x=250,
            y=400,
            color=piano_config.message_color,
            anchor_x=piano_config.label_anchor_x,
            anchor_y=piano_config.label_anchor_y,
            multiline=True,
            width=1000)

    def init_music_analysis(self):
        if piano_config.show_music_analysis:
            self.music_analysis_label = pyglet.text.Label(
                '',
                font_name=piano_config.fonts,
                font_size=piano_config.music_analysis_fonts_size,
                bold=piano_config.bold,
                x=piano_config.music_analysis_place[0],
                y=piano_config.music_analysis_place[1],
                color=piano_config.message_color,
                anchor_x=piano_config.label_anchor_x,
                anchor_y=piano_config.label_anchor_y,
                multiline=True,
                width=piano_config.music_analysis_width)
            if piano_config.music_analysis_file:
                with open(piano_config.music_analysis_file,
                          encoding='utf-8-sig') as f:
                    data = f.read()
                    lines = [i for i in data.split('\n\n') if i]
                    self.music_analysis_list = []
                    self.current_key = None
                    bar_counter = 0
                    for each in lines:
                        if each:
                            if each[:3] != 'key':
                                current = each.split('\n')
                                current_bar = current[0]
                                if current_bar[0] == '+':
                                    bar_counter += eval(current_bar[1:])
                                else:
                                    bar_counter = eval(current_bar) - 1
                                current_chords = '\n'.join(current[1:])
                                if self.current_key:
                                    current_chords = f'{piano_config.key_header}{self.current_key}\n' + current_chords
                                self.music_analysis_list.append(
                                    [bar_counter, current_chords])
                            else:
                                self.current_key = each.split('key: ')[1]

    def init_our_piano_keys(self):
        self.piano_height = piano_config.white_key_y + piano_config.white_key_height
        self.piano_keys = []
        self.dsp_colours = []
        if piano_config.draw_piano_keys:
            piano_background = image_vdc(piano_config.piano_background_image)
            if not piano_config.piano_size:
                ratio = self.screen_width / piano_background.width
                piano_background.width = self.screen_width
                piano_background.height *= ratio
            else:
                piano_background.width, piano_background.height = piano_config.piano_size
            self.piano_background_show = pyglet.sprite.Sprite(
                piano_background,
                x=0,
                y=0,
                batch=self.batch,
                group=self.piano_bg)
            for i in range(piano_config.white_keys_number):
                current_piano_key = pyglet.shapes.BorderedRectangle(
                    x=piano_config.white_key_start_x +
                    piano_config.white_key_interval * i,
                    y=piano_config.white_key_y,
                    width=piano_config.white_key_width,
                    height=piano_config.white_key_height,
                    color=piano_config.white_key_color,
                    batch=self.batch,
                    group=self.piano_key,
                    border=piano_config.piano_key_border,
                    border_color=piano_config.piano_key_border_color)
                current_piano_key.current_color = None
                self.piano_keys.append(current_piano_key)
                self.dsp_colours.append(
                    (current_piano_key.x, piano_config.white_key_color))
            first_black_key = pyglet.shapes.BorderedRectangle(
                x=piano_config.black_key_first_x,
                y=piano_config.black_key_y,
                width=piano_config.black_key_width,
                height=piano_config.black_key_height,
                color=piano_config.black_key_color,
                batch=self.batch,
                group=self.piano_key,
                border=piano_config.piano_key_border,
                border_color=piano_config.piano_key_border_color)
            first_black_key.current_color = None
            self.piano_keys.append(first_black_key)
            self.dsp_colours.append(
                (first_black_key.x, piano_config.black_key_color))
            current_start = piano_config.black_key_start_x
            for j in range(piano_config.black_keys_set_num):
                for k in piano_config.black_keys_set:
                    current_start += k
                    current_piano_key = pyglet.shapes.BorderedRectangle(
                        x=current_start,
                        y=piano_config.black_key_y,
                        width=piano_config.black_key_width,
                        height=piano_config.black_key_height,
                        color=piano_config.black_key_color,
                        batch=self.batch,
                        group=self.piano_key,
                        border=piano_config.piano_key_border,
                        border_color=piano_config.piano_key_border_color)
                    current_piano_key.current_color = None
                    self.piano_keys.append(current_piano_key)
                    self.dsp_colours.append(
                        (current_start, piano_config.black_key_color))
                current_start += piano_config.black_keys_set_interval
            self.piano_keys.sort(key=lambda s: s.x)
            self.dsp_colours.sort(key=lambda s: s[0])
            self.dsp_colours = [t[1] for t in self.dsp_colours]
            self.note_place = [(each.x, each.y) for each in self.piano_keys]
            self.bar_offset_x = 0

    def init_mtsp(self):
        self.mouse_left = 1
        self.pos_mouse = 0, 0
        self.first_time = True
        self.message_label = False
        self.is_click = False
        self.mode_num = None
        self.func = None
        self.click_mode = None
        self.bar_offset_x = piano_config.bar_offset_x
        self.open_browse_window = False

    def init_language(self):
        global language_patch
        if piano_config.language == 'English':
            from languages.en import language_patch
            importlib.reload(mp)
        elif piano_config.language == 'hindi':
            from languages.cn import language_patch
            mp.detect = language_patch.detect
        piano_eng.current_midi_device = language_patch.am11vdc2009_language_dict[
            'current_midi_device']

    def init_mtsp(self):
        self.mouse_left = 1
        self.pos_mouse = 0, 0
        self.first_time = True
        self.message_label = False
        self.is_click = False
        self.mode_num = None
        self.func = None
        self.click_mode = None
        self.bar_offset_x = piano_config.bar_offset_x
        self.open_browse_window = False

    def on_file_drop(self, x, y, paths):
        if paths:
            current_path = paths[0]
            import mimetypes
            type_cur = mimetypes.guess_type(current_path)[0]
            if type_cur:
                type_cur, type_name = type_cur.split('/')
                if type_cur == 'image':
                    piano_config.background_image = current_path
                    self.init_sreecn()
                elif type_name == 'mid':
                    if self.click_mode is None:
                        init_result = piano_eng.init_midi_show(
                            current_path)
                        self.click_mode = 2
                        self.mode_num = 2
                        if init_result == 'back':
                            self.mode_num = 4
                        else:
                            self.func = piano_eng.mode_midi_show
                            self.not_first()
                            pyglet.clock.schedule_interval(
                                self.func, 1 / piano_config.fps)

    def on_mouse_motion(self, x, y, dx, dy):
        self.pos_mouse = x, y

    def on_mouse_press(self, x, y, button, modifiers):
        if self.backwrd_but.inside(
                self.pos_mouse
        ) & button & self.mouse_left and not self.first_time:
            pygame.mixer.stop()
            pygame.mixer.music.stop()
            if self.mode_num in [0, 1, 2]:
                pyglet.clock.unschedule(self.func)
                if piano_eng.plays:
                    piano_eng.plays.clear()
                if self.mode_num == 0:
                    if piano_eng.yet_hold_r:
                        piano_eng.yet_hold_r.clear()
                elif self.mode_num == 1:
                    piano_config.delay_only_read_current = True
                elif self.mode_num == 2:
                    pyglet.clock.unschedule(
                        piano_eng.midi_file_play)
                    if piano_config.show_music_analysis:
                        self.music_analysis_label.text = ''
                    if piano_config.play_as_midi:
                        if piano_config.use_soundfont and not piano_config.render_as_audio:
                            if self.now_sf2.playing:
                                self.now_sf2.stop()
                    if piano_eng.playls:
                        piano_eng.playls.clear()
            self.is_click = True
            self.click_mode = None
            if piano_config.note_mode == 'bars' or piano_config.note_mode == 'bars drop':
                piano_eng.still_hold.clear()
                if piano_config.note_mode == 'bars drop':
                    piano_eng.br_dr.clear()
            if piano_config.draw_piano_keys:
                for k in range(len(self.piano_keys)):
                    self.piano_keys[k].color = self.dsp_colours[k]
            self.label3.text = ''

        if self.self_play_button.inside(
                self.pos_mouse) & button & self.mouse_left and self.first_time:
            self.click_mode = 0
      


    def _draw_window_first_time(self):
        self.self_play_button.draw()
        self.nyu_image_button.draw()
        if self.mode_num is None:
            self.main_wins()
        else:
            self._main_window_enter_mode()

    def main_wins(self):
        if self.handles_keys[key.LSHIFT]:
            self.le_mid.text = piano_eng.current_midi_device
        if self.handles_keys[key.LCTRL]:
            self.le_mid.text = ''
        if self.handles_keys[self.config_key] and self.handles_keys[
                key.S]:
            self.open_settings()
        if self.handles_keys[self.config_key] and self.handles_keys[
                key.R]:
            self.label.text = language_patch.am11vdc2009_language_dict[
                'reload']
            self.label.draw()
            self.flip()
            self.reload_settings()
        if self.click_mode == 0:
            self.mode_num = 0
            self.label.text = language_patch.am11vdc2009_language_dict['load']
            self.label.draw()
        elif self.click_mode == 1:
            self.mode_num = 1
            self.label.text = language_patch.am11vdc2009_language_dict['load']
            self.label.draw()
        elif self.click_mode == 2:
            self.mode_num = 2

    def on_draw(self):
        self.clear()
        self.background.blit(0, 0)
        if not piano_config.draw_piano_keys:
            self.image_show.draw()
        if self.batch:
            self.batch.draw()
        self.backwrd_but.draw()
        self.le_mid.draw()
        if self.first_time:
            self._draw_window_first_time()
        else:
            self._draw_window()

    def _main_window_enter_mode(self):
        if self.mode_num == 0:
            piano_eng.slef_pin()
            self.label.text = language_patch.am11vdc2009_language_dict[
                'finished']
            self.label.draw()
            self.func = piano_eng.mode_self_pc
            self.not_first()
            pyglet.clock.schedule_interval(self.func, 1 / piano_config.fps)
        elif self.mode_num == 1:
            try:
                piano_eng.init_self_midi()
                if not piano_eng.device:
                    self.label.text = language_patch.am11vdc2009_language_dict[
                        'no MIDI input']
                    self.mode_num = 3
                    self.reset_click_mode()
                    self.label.draw()
                else:
                    self.label.text = language_patch.am11vdc2009_language_dict[
                        'finished']
                    self.label.draw()
                    self.func = piano_eng.mode_self_midi
                    self.not_first()
                    pyglet.clock.schedule_interval(self.func,
                                                   1 / piano_config.fps)
            except Exception as e:
                piano_eng.has_load(False)
                pygame.midi.quit()
                piano_eng.current_midi_device += f'\n{language_patch.am11vdc2009_language_dict["error message"]}: {e}'
                self.label.text = language_patch.am11vdc2009_language_dict[
                    'no MIDI input']
                self.mode_num = 3
                self.reset_click_mode()
                self.label.draw()
        elif self.mode_num == 2:
            if not self.open_browse_window:
                init_result = piano_eng.init_midi_show()
                if init_result == 'back':
                    self.mode_num = 4
                else:
                    self.func = piano_eng.mode_midi_show
                    self.not_first()
                    pyglet.clock.schedule_interval(self.func,
                                                   1 / piano_config.fps)
        elif self.mode_num == 3:
            time.sleep(1)
            self.label.text = ''
            self.mode_num = None
        elif self.mode_num == 4:
            self.label.text = ''
            self.mode_num = None
            self.reset_click_mode()



    def redraw(self):
        self.clear()
        self.background.blit(0, 0)
        if not piano_config.draw_piano_keys:
            self.image_show.draw()
        if self.batch:
            self.batch.draw()
        self.backwrd_but.draw()
        self.le_mid.draw()
        self.label2.draw()
        if self.message_label:
            self.label3.draw()
        if piano_config.show_music_analysis:
            self.music_analysis_label.draw()

    def reset_click_mode(self):
        self.click_mode = None

    def not_first(self):
        self.first_time = not self.first_time

    def open_settings(self):
        self.handles_keys[self.config_key] = False
        self.handles_keys[key.S] = False
        os.chdir(abs_path)
        current_config_window = config_window()
        current_config_window.mainloop()
        self.reload_settings()

    def _draw_window(self):
        if self.is_click:
            self.is_click = False
            self.not_first()
            self.label.text = ''
            self.label2.text = ''

            pyglet.clock.unschedule(self.func)
            self.mode_num = None
        self.label.draw()
        self.label2.draw()
        if self.message_label:
            self.label3.draw()
        if piano_config.show_music_analysis:
            self.music_analysis_label.draw()

    def reload_settings(self):
        importlib.reload(piano_config)
        self.init_mtsp()
        self.init_language()
        self.init_keys()
        self.init_sreecn()
        self.init_layers()
        self.init_buttons()
        self.init_our_piano_keys()
        self.init_note_mode()
        self.init_sreecn_labels()
        self.init_music_analysis()


class piano_engine:

    def __init__(self):
        self.init_mtsp()

    def init_mtsp(self):
        self.notedic = piano_config.key_settings
        self.chrd_no = mp.chord([])
        self.playnotes = []
        self.yet_hold_r = []
        self.still_hold = []
        self.paused = False
        self.pause_start = 0
        self.playls = []
        self.br_dr = []
        self.plays = []
        self.mid_leb = False
        self.current_midi_device = language_patch.am11vdc2009_language_dict[
            'current_midi_device']
        self.device = None
        #self.play_midi_file = False
        self.auto_ikn = False
        self.soft_vols = 1

    def has_load(self, change):
        self.mid_leb = change

    def key_c(self, current_key):
        return current_piano_nyu.handles_keys[
            current_piano_nyu.
            config_key] and current_piano_nyu.handles_keys[
                current_piano_nyu.dicts_gapping[current_key]]

    def configshow(self, content):
        current_piano_nyu.label.text = str(content)


    def detect_config(self):
        if self.key_c(piano_config.volume_up):
            if piano_config.global_volume + piano_config.volume_change_unit <= 1:
                piano_config.global_volume += piano_config.volume_change_unit
            else:
                piano_config.global_volume = 1
            [
                self.wavdic[j].set_volume(piano_config.global_volume)
                for j in self.wavdic
            ]
            self.configshow(
                f'volume up to {int(piano_config.global_volume*100)}%')
        if self.key_c(piano_config.volume_down):
            if piano_config.global_volume - piano_config.volume_change_unit >= 0:
                piano_config.global_volume -= piano_config.volume_change_unit
            else:
                piano_config.global_volume = 0
            [
                self.wavdic[j].set_volume(piano_config.global_volume)
                for j in self.wavdic
            ]
            self.configshow(
                f'volume down to {int(piano_config.global_volume*100)}%')
        self.sockets(piano_config.change_delay, 'delay')
        self.sockets(piano_config.change_read_current,
                     'delay_only_read_current')
        self.sockets(piano_config.change_pause_key_clear_notes,
                     'pause_key_clear_notes')
        if piano_config.play_use_soundfont:
            self.sfont2_c()

    def sockets(self, current_key, name):
        if self.key_c(current_key):
            setattr(piano_config, name, not getattr(piano_config, name))
            self.configshow(
                f'{name} {language_patch.am11vdc2009_language_dict["changes"]} {getattr(piano_config, name)}'
            )


    def sfont2_c(self, mode=0):
        current_sf2 = current_piano_nyu.current_sf2
        if self.key_c('1'):
            if current_sf2.current_preset != 0:
                self.sfont2_tab(-1, audio_mode=mode)
        if self.key_c('2'):
            self.sfont2_tab(1, audio_mode=mode)
        if self.key_c('3'):
            if current_sf2.current_bank != 0:
                self.sfont2_tab(-1, 1, audio_mode=mode)
        if self.key_c('4'):
            self.sfont2_tab(1, 1, audio_mode=mode)

    def sfont2_tab(self, step, mode=0, audio_mode=0):
        current_sf2 = current_piano_nyu.current_sf2
        if mode == 0:
            current_change = current_sf2.change(
                preset=current_sf2.current_preset + step, correct=False)
            current_preset = f'{current_sf2.current_preset} {current_sf2.get_current_instrument()}' if current_change != -1 else f'{current_sf2.current_preset} No preset'
            current_piano_nyu.redraw()
            current_piano_nyu.label.text = f'Change SoundFont preset to {current_preset}'
            current_piano_nyu.label.draw()
            current_piano_nyu.flip()
            if current_change != -1:
                if audio_mode == 0:
                    self.wavdic = SoundFont(self.notedic, current_sf2,
                                           piano_config.global_volume)
                else:
                    notenames = os.listdir(piano_config.sound_path)
                    notenames = [x[:x.index('.')] for x in notenames]
                    self.wavdic = SoundFont({i: i
                                            for i in notenames}, current_sf2,
                                           piano_config.global_volume)
        else:
            current_sf2.change_bank(current_sf2.current_bank + step)
            current_piano_nyu.redraw()
            current_piano_nyu.label.text = f'Change SoundFont bank to {current_sf2.current_bank}'
            current_piano_nyu.label.draw()
            current_piano_nyu.flip()


    def piano_key_reset(self, dt, each):
        current_piano_nyu.piano_keys[
            each.degree -
            21].color = current_piano_nyu.dsp_colours[each.degree - 21]

    def _detect_chord(self, current_chord):
        return mp.detect(
            current_chord, piano_config.detect_mode, piano_config.inv_num,
            piano_config.change_from_first, piano_config.original_first,
            piano_config.root_position_return_first,
             piano_config.same_note_special, piano_config.whole_detect,
            piano_config.return_fromchord, piano_config.poly_chord_first,
            piano_config.alter_notes_show_degree)

    def slef_pin(self):
        if not piano_config.play_use_soundfont:
            self.wavdic = load(self.notedic, piano_config.sound_path,
                               piano_config.sound_format,
                               piano_config.global_volume)
        else:
            self.wavdic = SoundFont(self.notedic,
                                   current_piano_nyu.current_sf2,
                                   piano_config.global_volume)
        self.last = []
        self.changed = False
        if piano_config.delay:
            self.stillplay = []
        self.end_gm = None


    def init_midi_show(self, file_name=None):
        current_piano_nyu.open_browse_window = True
        current_setup = browse.setup(language_patch.browse_language_dict,
                                     file_name=file_name)
        current_piano_nyu.open_browse_window = False
        self.path = current_setup.file_path
        self.action = current_setup.action
        read_result = current_setup.read_result
        self.suit = current_setup.suit
        set_bpm = current_setup.set_bpm
        self.off_melody = current_setup.off_melody
        self.if_merge = current_setup.if_merge
        play_interval = current_setup.interval
        if self.action == 1:
            self.action = 0
            return 'back'
        if self.path and read_result:
            if read_result != 'error':
                self.bpm, self.musicsheet, start_time = read_result
                self.musicsheet, new_start_time = self.musicsheet.pitch_filter(
                    *piano_config.pitch_range)
                start_time += new_start_time
                self.suit = len(self.musicsheet)
                if set_bpm:
                    self.bpm = float(set_bpm)
            else:
                return 'back'
        else:
            return 'back'

        if self.off_melody:
            self.musicsheet = mp.split_chord(
                self.musicsheet, 'hold', piano_config.melody_tol,
                piano_config.chord_tol, piano_config.get_off_overlap_notes,
                piano_config.average_degree_length,
                piano_config.melody_degree_tol)
            self.suit = len(self.musicsheet)
        if play_interval is not None:
            play_start, play_stop = int(
                self.suit * (play_interval[0] / 100)), int(
                    self.suit * (play_interval[1] / 100))
            self.musicsheet = self.musicsheet[play_start:play_stop]
            self.suit = play_stop + 1 - play_start
        if self.suit == 0:
            return 'back'
        pygame.mixer.set_num_channels(self.suit)
        self.wholenotes = self.musicsheet.notes
        self.unit_time = 4 * 60 / self.bpm

        
        self.musicsheet.start_time = start_time
        self.playls = self._midi_show_init(self.musicsheet, self.unit_time,
                                           start_time)
        if piano_config.show_music_analysis:
            self.disply_music = [[
                mp.add_to_last_index(self.musicsheet.interval, each[0]),
                each[1]
            ] for each in current_piano_nyu.music_analysis_list]
            self.default_disply_music = copy(
                self.disply_music)
        self.startplay = time.time()
        self.end_gm = None
        self.finished = False
        self.paused = False


    def mode_self_pc(self, dt):
        self.key_brd_spc_k()
        self.red_k_pss()
        self.playcont()
        if piano_config.note_mode == 'bars' or piano_config.note_mode == 'bars drop':
            self._pc_move_note_bar()
        if self.changed:
            self._pc_update_notes()

    def key_brd_spc_k(self):
        if piano_config.config_enable:
            self.detect_config()
        if current_piano_nyu.handles_keys[
                current_piano_nyu.pause_key]:
            pygame.mixer.stop()
            if piano_config.pause_key_clear_notes:
                if piano_config.delay:
                    self.stillplay = []

    def red_k_pss(self):
        self.current = [
            current_piano_nyu.can_rever[i]
            for i, j in current_piano_nyu.handles_keys.items()
            if j and i in current_piano_nyu.can_rever
        ]
        self.current = [i for i in self.current if i in self.wavdic]
        if piano_config.delay:
            self.contplay_obj = [x[0] for x in self.stillplay]
            self.truecurrent = self.current.copy()
        for each in self.current:
            if piano_config.delay:
                if each in self.contplay_obj:
                    inds = self.contplay_obj.index(each)
                    if not self.stillplay[inds][2] and time.time(
                    ) - self.stillplay[inds][1] > piano_config.touch_interval:
                        self.wavdic[each].fadeout(piano_config.fadeout_ms)
                        self.stillplay.pop(inds)
                        self.contplay_obj.pop(inds)
                else:
                    self.changed = True
                    self.wavdic[each].play()
                    self.stillplay.append([each, time.time(), True])
                    self.contplay_obj.append(each)
                    if piano_config.note_mode == 'bars' or piano_config.note_mode == 'bars drop':
                        current_bar = self._pc_draw_note_bar(each)
                    else:
                        current_bar = None
                    if piano_config.draw_piano_keys:
                        self._pc_set_piano_key_color(each, current_bar)
            else:
                if each not in self.last:
                    self.changed = True
                    self.wavdic[each].play()
                    if piano_config.note_mode == 'bars' or piano_config.note_mode == 'bars drop':
                        current_bar = self._pc_draw_note_bar(each)
                    else:
                        current_bar = None
                    if piano_config.draw_piano_keys:
                        self._pc_set_piano_key_color(each, current_bar)

    def _pc_draw_note_bar(self, each):
        current_note = mp.toNote(self.notedic[each])
        places = current_piano_nyu.note_place[current_note.degree - 21]
        current_bar = pyglet.shapes.BorderedRectangle(
            x=places[0] + current_piano_nyu.bar_offset_x,
            y=piano_config.bar_y,
            width=piano_config.bar_width,
            height=piano_config.bar_height,
            color=piano_config.bar_color if piano_config.color_mode == 'normal'
            else (random.randint(0, 255), random.randint(0, 255),
                  random.randint(0, 255)),
            batch=current_piano_nyu.batch,
            group=current_piano_nyu.play_highlight,
            border=piano_config.bar_border,
            border_color=piano_config.bar_border_color)
        current_bar.opacity = piano_config.bar_opacity
        self.yet_hold_r.append([each, current_bar])
        return current_bar

    def _pc_set_piano_key_color(self, each, current_bar=None):
        current_note = mp.toNote(self.notedic[each])
        current_piano_key = current_piano_nyu.piano_keys[current_note.degree
                                                            - 21]
        if piano_config.color_mode == 'normal':
            current_piano_key.color = piano_config.bar_color
        else:
            if piano_config.note_mode == 'bars' or piano_config.note_mode == 'bars drop':
                current_piano_key.color = current_bar.color
            else:
                current_piano_key.color = (random.randint(0, 255),
                                           random.randint(0, 255),
                                           random.randint(0, 255))
        current_piano_key.current_color = current_piano_key.color

    def playcont(self):
        for j in self.last:
            if j not in self.current:
                if piano_config.delay:
                    if j in self.contplay_obj:
                        ind = self.contplay_obj.index(j)
                        stillobj = self.stillplay[ind]
                        if time.time() - stillobj[1] > piano_config.delay_time:
                            self.changed = True
                            self.wavdic[j].fadeout(piano_config.fadeout_ms)
                            self.stillplay.pop(ind)
                            self.contplay_obj.pop(ind)
                        else:
                            self.stillplay[ind][2] = False
                            self.current.append(j)
                    else:
                        self.changed = True
                        self.wavdic[j].fadeout(piano_config.fadeout_ms)
                else:
                    self.changed = True
                    self.wavdic[j].fadeout(piano_config.fadeout_ms)
        self.last = self.current

    def _pc_move_note_bar(self):
        i = 0
        while i < len(self.plays):
            each = self.plays[i]
            each.y += piano_config.bar_steps
            if each.y >= current_piano_nyu.screen_height:
                each.batch = None
                del self.plays[i]
                continue
            i += 1
        for k in self.yet_hold_r:
            current_hold_note, current_bar = k
            if current_hold_note in self.truecurrent:
                current_bar.height += piano_config.bar_hold_increase
            else:
                self.plays.append(current_bar)
                self.yet_hold_r.remove(k)

    def _pc_update_notes(self):
        self.changed = False
        if piano_config.delay:
            if piano_config.delay_only_read_current:
                notels = [self.notedic[t] for t in self.truecurrent]
            else:
                notels = [self.notedic[t] for t in self.contplay_obj]
        else:
            notels = [self.notedic[t] for t in self.last]
        if piano_config.draw_piano_keys:
            if self.end_gm:
                for t in self.end_gm:
                    current_piano_nyu.piano_keys[
                        t.degree -
                        21].color = current_piano_nyu.dsp_colours[
                            t.degree - 21]
        if notels:
            self.chrd_no = mp.chord(notels)
            for k in self.chrd_no:
                if piano_config.draw_piano_keys:
                    current_piano_key = current_piano_nyu.piano_keys[
                        k.degree - 21]
                    current_piano_key.color = piano_config.bar_color if piano_config.color_mode == 'normal' else current_piano_key.current_color
            self.chrd_no.notes.sort(key=lambda x: x.degree)
            if self.chrd_no != self.end_gm:
                self.end_gm = self.chrd_no
                current_piano_nyu.label.text = str(self.chrd_no.notes)
                if piano_config.show_chord and any(
                        type(t) == mp.note for t in self.chrd_no):
                    chordtype = self._detect_chord(self.chrd_no)

                    current_piano_nyu.label2.text = str(
                        chordtype
                    ) if not piano_config.sort_invisible else get_off_sort(
                        str(chordtype))
        else:
            self.end_gm = notels
            current_piano_nyu.label.text = str(notels)
            current_piano_nyu.label2.text = ''
        if piano_config.show_key:
            current_piano_nyu.label.text = str(self.truecurrent)


piano_eng = piano_engine()
current_piano_nyu = piano_nyu()
pyglet.clock.schedule_interval(update, 1 / piano_config.fps)
pyglet.app.run()
