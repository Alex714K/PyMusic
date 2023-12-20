import glob
import os
import sqlite3
from PyQt5 import QtWidgets
from myplayer import Ui_MainWindow
from myplaylist import Ui_MainPlaylist
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QTableWidgetItem, QHeaderView, QStyle, QMessageBox
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from PyQt5.QtGui import QIcon, QPalette, QLinearGradient, QBrush, QColor
from PyQt5.QtCore import Qt, QUrl
from Setting import Settings

mediaPlayer = QMediaPlayer()
playlist = QMediaPlaylist()
txt_queue = open('queue.txt', 'r').read().split('\n')
for i in txt_queue:
    print(i)
    url = QUrl.fromLocalFile(f"tracks/{i}")
    playlist.addMedia(QMediaContent(url))
# url = QUrl.fromLocalFile("tracks/Eye of the storm.mp3")
# url = QUrl.fromLocalFile("tracks/This Is It.mp3")

mediaPlayer.setPlaylist(playlist)
mediaPlayer.playlist().setCurrentIndex(0)
# mediaPlayer.playlist().addMedia(QMediaContent(url))


def b():
    """Затычка"""
    print("Затычка")
    pass


class PlayList(QMainWindow):
    """Окно плейлиста (скорей библиотека со всеми треками)"""

    def __init__(self):
        super(PlayList, self).__init__()
        self.uiP = Ui_MainPlaylist()
        self.uiP.setupUi(self) # подключаем интерфейс
        self.init_ui() # Нужно объяснять?)

    def init_ui(self):
        """Основная инициализация"""
        self.forms = {'mp3': '1',
              'wav': '2'}

        self.update_base()
        self.get_base()
        self.get_queue()
        self.open_settings_txt()
        self.set_color()

        self.uiP.tableWidget.cellDoubleClicked.connect(self.choose_track)

        self.uiP.custom_button.clicked.connect(self.add_custom_file)

        self.uiP.add_button.clicked.connect(self.add_track)
        self.uiP.delete_button.clicked.connect(self.delete_track)
        self.uiP.up_button.clicked.connect(self.up_track)
        self.uiP.down_button.clicked.connect(self.down_track)

    def choose_track(self):
        """Добавляет трек в очередь (нужно нажать на название!!!)"""
        # информация о названии клетки, строке, формате
        cell = self.uiP.tableWidget.currentItem().text()
        row = self.uiP.tableWidget.currentRow()
        form = self.uiP.tableWidget.item(row, 3).text()
        if self.uiP.tableWidget.item(row, 0).text() == cell:
            url = QUrl.fromLocalFile(f"tracks/{cell}.{form}")
            mediaPlayer.playlist().addMedia(QMediaContent(url))
            self.uiP.name.setText(f"Вставлен трек: {cell}")
            names = open('queue.txt', 'r').read().split('\n')
            queue = open('queue.txt', 'w')
            if names == ['']:
                queue.write(f'{cell}.{form}')
            else:
                names.append(f'{cell}.{form}')
                queue.write('\n'.join(names))
            queue.close()
            self.get_queue()

    def add_track(self):
        pass

    def delete_track(self):
        pass

    def up_track(self):
        pass

    def down_track(self):
        pass

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

    def update_base(self):
        """Добавляет/Удаляет треки из базы данных"""
        con = sqlite3.connect('base.sqlite')
        cur = con.cursor()
        result1 = cur.execute("""SELECT
                            songs.name FROM songs""").fetchall()
        result = list(map(lambda x: x[0], result1))
        tracks, paths = check_new_tracks()
        a = 0
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

    def get_base(self):
        """Загружает базу данных о плейлистах в левую таблицу"""
        con = sqlite3.connect('base.sqlite')
        cur = con.cursor()
        result = cur.execute("""SELECT
                                songs.name,
                                teams.team,
                                albums.album,
                                format.format
                    
                            FROM
                                songs
                            LEFT JOIN teams
                                ON songs.team = teams.id
                            LEFT JOIN albums
                                on songs.album = albums.id
                            LEFT JOIN format
                                ON songs.format = format.id""").fetchall()
        con.close()
        # суём список треков в таблицу
        for i, row in enumerate(result):
            self.uiP.tableWidget.setRowCount(
                self.uiP.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.uiP.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        # ставим размер столбцов в соответствии с шириной названий
        self.uiP.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.uiP.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.uiP.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

    def get_queue(self):
        txt = open("queue.txt").read().split('\n')
        while self.uiP.queue.rowCount() > 0:
            self.uiP.queue.removeRow(0)
        for i, row in enumerate(txt):
            self.uiP.queue.setRowCount(
                self.uiP.queue.rowCount() + 1)
            self.uiP.queue.setItem(
                i, 0, QTableWidgetItem(str(row)))

        self.uiP.queue.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.uiP.queue.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    def add_custom_file(self):
        """Открыть окно для выбора файла и добавить сторонний трек"""
        path, _ = QFileDialog.getOpenFileName(self, "Open music")
        if path == '':
            return
        name = path[path.rfind('/') + 1:-4]
        try:
            form = self.forms[path[-3:]]
        except:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("ERROR")
            dlg.setText("Не верный формат. Только mp3 или wav!")
            dlg.exec()
            return
        con = sqlite3.connect('base.sqlite')
        cur = con.cursor()
        result1 = cur.execute("""SELECT
                            songs.name FROM songs WHERE custom = ?""", (path,)).fetchall()
        result = list()
        for i in result1:
            result.append(i[0])
        if name not in result:
            cur.execute("""INSERT INTO songs(name, format, custom, way) VALUES(?, ?, ?)""", (name, form, path, path))
            con.commit()
        con.close()
        self.get_base()


class Player(QMainWindow):
    """Основное окно"""

    def __init__(self):
        super(Player, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)  # подключаем интерфейс
        self.init_ui()  # Нужно объяснять?)

    def init_ui(self):
        """Основная инициализация"""
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

        # если изменилось состояние (play/stop)
        mediaPlayer.stateChanged.connect(self.mediastate_changed)
        # если музыка проигралась одну секунду (двигает ползунок)
        mediaPlayer.positionChanged.connect(self.position_changed)
        # если изменился трек, подгоняется длинна ползунка
        mediaPlayer.durationChanged.connect(self.duration_changed)

        self.ui.horizontalSlider.valueChanged.connect(self.set_position)  # если ползунок подвигали

        self.ui.openAudio.clicked.connect(self.open_file)
        self.ui.playlist.triggered.connect(self.open_playlists)
        self.ui.win_options.triggered.connect(self.open_parametr)
        self.ui.playButton.clicked.connect(self.pause_music)

        self.ui.next_button.clicked.connect(mediaPlayer.playlist().next)  # трек вперёд
        self.ui.previous_button.clicked.connect(mediaPlayer.playlist().previous)  # трек назад

    def set_position(self, position):
        """Двигаем плеер в зависимости от позиции ползунка"""
        if not self.player_changing:  # если это делает пользователь
            mediaPlayer.setPosition(position)

    def mediastate_changed(self):
        """Меняет иконку кнопки play"""
        if mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.ui.playButton.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause)

            )

        else:
            self.ui.playButton.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay)

            )

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
        """Открывает окно с библиотекой"""
        self.wplay = PlayList()
        self.wplay.show()

    def update_base(self):
        """Добавляет/Удаляет треки из базы данных"""
        con = sqlite3.connect('base.sqlite')
        cur = con.cursor()
        result1 = cur.execute("""SELECT
                            songs.name FROM songs""").fetchall()
        result = list(map(lambda x: x[0], result1))
        tracks, paths = check_new_tracks()
        a = 0
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
        if mediaPlayer.state() == QMediaPlayer.PlayingState:
            mediaPlayer.pause()  # остановить
        else:
            mediaPlayer.play()  # продолжить

    def open_file(self):
        """Открыть окно для выбора файла"""
        filename, _ = QFileDialog.getOpenFileName(self, "Open music", 'G:/Sasha/work/PyMusic/tracks')
        print(f"Вручную добавлен трек: {filename}\n")
        if filename != '':
            url = QUrl.fromLocalFile(filename)
            mediaPlayer.playlist().addMedia(QMediaContent(url))
            self.ui.playButton.setText("Play")


def check_new_tracks():
    """Возвращает """
    new_txt = list(map(lambda x: x[7:], glob.glob("tracks/*.mp3")))
    path = list(map(lambda x: os.path.abspath(f"tracks/{x}"), new_txt))
    # print(f"check_new_tracks: {new_txt}\n")
    return new_txt, path
