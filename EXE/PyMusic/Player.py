import glob
import sqlite3
from myplayer import Ui_Player
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QTableWidgetItem, QHeaderView, QStyle, QTableWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from PyQt5.QtGui import QPalette, QLinearGradient, QBrush, QColor
from PyQt5.QtCore import QUrl
from Setting import Settings
from Playlist import PlayList


class Player(QMainWindow):
    """Основное окно"""

    def __init__(self):
        super(Player, self).__init__()
        self.mediaPlayer = QMediaPlayer()
        self.ui = Ui_Player()
        self.ui.setupUi(self)  # подключаем интерфейс
        self.init_ui()  # Нужно объяснять?)

    def init_ui(self):
        """Основная инициализация"""
        self.setWindowTitle('Player')
        # прикольная кнопка плей is activated
        self.ui.playButton.setIcon(
            self.style().standardIcon(QStyle.SP_MediaPlay))
        # словарь для преобразования в update_base()
        self.forms = {'mp3': '1',
                      'wav': '2'}
        # флажки
        self.playing = False
        self.player_changing = False

        self.update_base()  # обновляем базу
        self.open_settings_txt()  # вытаскиваем настройки
        self.set_color()  # ставим цвет фона
        self.update_player()  # обновляем плейлист в QMediaPlayer
        self.get_queue_in_table()  # вставляет список очереди в таблицу

        # если изменилось состояние (play/stop)
        self.mediaPlayer.stateChanged.connect(self.mediastate_changed)
        # если музыка проигралась одну секунду (двигает ползунок)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        # если изменился трек, подгоняется длинна ползунка
        self.mediaPlayer.durationChanged.connect(self.duration_changed)

        self.ui.horizontalSlider.valueChanged.connect(self.set_position)  # если ползунок подвигали
        self.ui.volume.valueChanged.connect(self.change_volume)
        # кнопки
        self.ui.openAudio.clicked.connect(self.open_file)
        self.ui.openAudio.setDisabled(1)
        self.ui.playlist.triggered.connect(self.open_playlists)
        self.ui.win_options.triggered.connect(self.open_parametr)
        self.ui.playButton.clicked.connect(self.pause_music)

        self.ui.next_button.clicked.connect(self.next_track)  # трек вперёд
        self.ui.previous_button.clicked.connect(self.previous_track)  # трек назад
        self.ui.update_button.clicked.connect(self.update_player)  # обновить очередь треков после изменений

    def get_queue_in_table(self):
        """Вставляет список очереди в таблицу"""
        queue = open('queue.txt', 'r').read().split('\n')
        while self.ui.list_queue.rowCount() > 0:  # Удаляем старые строки
            self.ui.list_queue.removeRow(0)
        for i, elem in enumerate(queue):  # Добавляем новые строки
            self.ui.list_queue.setRowCount(
                self.ui.list_queue.rowCount() + 1)
            self.ui.list_queue.setItem(
                i, 0, QTableWidgetItem(str(elem)))

        self.ui.list_queue.setEditTriggers(QTableWidget.NoEditTriggers)  # Нельзя изменить ячейку
        # Нельзя изменить ширину столбца и строки
        self.ui.list_queue.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.ui.list_queue.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    def change_volume(self, volume):
        """Изменяет громкость"""
        self.mediaPlayer.setVolume(int(volume))
        setting_volume = open('settings.txt', 'r').read().split('\n')
        setting_volume[11] = str(volume)
        txt = open('settings.txt', 'w')
        txt.write('\n'.join(setting_volume))
        txt.close()

    def update_player(self):
        """Обновляет вручную очередь в плеере"""
        playlist = QMediaPlaylist(self.mediaPlayer)
        txt_queue = open('queue.txt', 'r').read().split('\n')
        for i in txt_queue:
            print(f"tracks/{i}")
            url = QUrl.fromLocalFile(f"tracks/{i}")
            playlist.addMedia(QMediaContent(url))
        self.mediaPlayer.setPlaylist(playlist)
        self.mediaPlayer.playlist().setCurrentIndex(0)
        self.get_queue_in_table()

    def set_position(self, position):
        """Двигаем плеер в зависимости от позиции ползунка"""
        if not self.player_changing:  # если это делает пользователь
            self.mediaPlayer.setPosition(position)

    def mediastate_changed(self):
        """Меняет иконку кнопки play"""
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.ui.playButton.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause))

        else:
            self.ui.playButton.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay))

    def position_changed(self, position):
        """Плеер двигает ползунок"""
        # была проблема, когда проигрыватель двигает ползунок, а потом ползунок двигал проигрыватель.
        # этот флажок чинит эту проблему
        self.player_changing = True
        self.ui.horizontalSlider.setValue(position)
        self.player_changing = False

    def duration_changed(self, duration):
        """Изменяет длинну ползунка в зависимости от длинны трека"""
        self.ui.horizontalSlider.setRange(0, duration)

    def open_parametr(self):
        """Открывает окно с настройками"""
        self.wpar = Settings()
        self.wpar.show()

    def open_playlists(self):
        """Открывает окно с библиотекой треков"""
        self.wplay = PlayList(self.mediaPlayer)
        self.wplay.show()

    def update_base(self):
        """Добавляет/Удаляет треки из базы данных"""
        con = sqlite3.connect('base.sqlite')
        cur = con.cursor()
        result1 = cur.execute("""SELECT
                            songs.name FROM songs""").fetchall()
        result = list(map(lambda x: x[0], result1))
        tracks = check_new_tracks()
        for track in tracks:
            name = track[:-4]
            form = self.forms[track[-3:]]
            if name not in result:
                print(f"Трек добавился в базу: {name}\n")
                cur.execute("""INSERT INTO songs(name, format) VALUES(?, ?)""", (name, form))
        con.commit()

        data = cur.execute("""SELECT 
                    songs.name,
                    format.format
                    FROM songs
                    LEFT JOIN format
                        ON songs.format = format.id""").fetchall()
        for track in data:
            name = '.'.join(track)
            if name not in tracks:
                print(f"Трек удалился из базы: {name}\n")
                cur.execute("""DELETE from songs
                            where name = ?""", (track[0],))

        con.commit()
        con.close()

    def open_settings_txt(self):
        """Открытие файла с сохранёнными настройками"""
        setting_txt = open("settings.txt").read().split('\n')
        self.red = int(setting_txt[0][4:])
        self.green = int(setting_txt[1][6:])
        self.blue = int(setting_txt[2][5:])
        self.red2 = int(setting_txt[3][5:])
        self.green2 = int(setting_txt[4][7:])
        self.blue2 = int(setting_txt[5][6:])
        self.red3 = int(setting_txt[6][5:])
        self.green3 = int(setting_txt[7][7:])
        self.blue3 = int(setting_txt[8][6:])
        self.folder = setting_txt[9][7:]
        self.variant = int(setting_txt[10][8:])

    def set_color(self):
        """Выставляет цвет фона у окна"""
        variant = self.variant
        p = QPalette()
        gradient = QLinearGradient(0, 0, 0, 400)

        if variant == 0:  # одноцветный
            gradient.setColorAt(0.0, QColor(self.red, self.green, self.blue))
        elif variant == 1:  # двухцветный
            gradient.setColorAt(0.0, QColor(self.red, self.green, self.blue))
            gradient.setColorAt(1.0, QColor(self.red2, self.green2, self.blue2))
        elif variant == 2:  # трёхцветный
            gradient.setColorAt(0.0, QColor(self.red, self.green, self.blue))
            gradient.setColorAt(0.5, QColor(self.red2, self.green2, self.blue2))
            gradient.setColorAt(1, QColor(self.red3, self.green3, self.blue3))

        p.setBrush(QPalette.Window, QBrush(gradient))
        self.setAutoFillBackground(True)
        self.setPalette(p)

    def pause_music(self):
        """Остановить или воспроизвести музыку"""
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            print('stop')
            self.mediaPlayer.pause()  # остановить
        else:
            self.mediaPlayer.play()  # продолжить

    def next_track(self):
        self.mediaPlayer.playlist().next()

    def previous_track(self):
        self.mediaPlayer.playlist().previous()

    def open_file(self):
        """Открыть окно для выбора файла"""
        filename, _ = QFileDialog.getOpenFileName(self, "Open music", 'G:/Sasha/work/PyMusic/tracks')
        print(f"Вручную добавлен трек: {filename}\n")
        if filename != '':
            url = QUrl.fromLocalFile(filename)
            self.mediaPlayer.playlist().addMedia(QMediaContent(url))
            self.ui.playButton.setText("Play")


def check_new_tracks():
    """Возвращает """
    new_txt = list(map(lambda x: x[7:], glob.glob("tracks/*.mp3")))
    return new_txt
