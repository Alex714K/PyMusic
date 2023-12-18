import glob
import os
import sqlite3
from PyQt5 import QtWidgets
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from myplayer import Ui_MainWindow
from myplaylist import Ui_MainPlaylist
from mysetting import Ui_MainSetting
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QTableWidgetItem, QHeaderView, QStyle, QMessageBox
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from PyQt5.QtGui import QIcon, QPalette, QLinearGradient, QBrush, QColor
from PyQt5.QtCore import Qt, QUrl

mediaPlayer = QMediaPlayer()
playlist = QMediaPlaylist()
url = QUrl.fromLocalFile("tracks/Eye of the storm.mp3")
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
        self.uiP.setupUi(self)
        self.init_ui()

    def init_ui(self):
        """Основная инициализация"""
        self.forms = {'mp3': '1',
              'wav': '2'}

        self.update_base()
        self.get_base()
        self.get_queue()

        self.uiP.tableWidget.cellDoubleClicked.connect(self.choose_track)
        self.uiP.tableWidget.cellClicked.connect(self.clicked_cell)

        self.uiP.custom_button.clicked.connect(self.add_custom_file)

        self.uiP.add_button.clicked.connect(self.add_track)
        self.uiP.delete_button.clicked.connect(self.delete_track)
        self.uiP.up_button.clicked.connect(self.up_track)
        self.uiP.down_button.clicked.connect(self.down_track)


    def choose_track(self):
        # информация о названии клетки, строке, формате
        cell = self.uiP.tableWidget.currentItem().text()
        row = self.uiP.tableWidget.currentRow()
        form = self.uiP.tableWidget.item(row, 3).text()
        if self.uiP.tableWidget.item(row, 0).text() == cell:
            url = QUrl.fromLocalFile(f"tracks/{cell}.{form}")
            mediaPlayer.playlist().addMedia(QMediaContent(url))
            self.uiP.name.setText(f"Вставлен трек: {cell}")

    def clicked_cell(self):
        row = self.uiP.tableWidget.currentRow()
        # print(row)
        # self.cell = self.uiP.tableWidget.

    def add_track(self):
        # txt = open("queue.txt").read().split('\n')
        pass

    def delete_track(self):
        pass

    def up_track(self):
        pass

    def down_track(self):
        pass

    def update_base(self):
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
            path = paths[a]
            a += 1
            if name not in result:
                print(f"Трек добавился в базу: {name}\n")
                cur.execute("""INSERT INTO songs(name, format, way) VALUES(?, ?, ?)""", (name, form, path))
        con.commit()
        con.close()

    def get_base(self):
        """Загружает базу данных о плейлистах в правую таблицу"""
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


class Settings(QMainWindow):
    """Окно настроек"""

    def __init__(self):
        super(Settings, self).__init__()
        self.uiS = Ui_MainSetting()
        self.uiS.setupUi(self)
        self.init_ui()

    def init_ui(self):
        """Основная инициализация"""
        self.uiS.confirm_button.setDisabled(1)
        self.uiS.activate_button.setDisabled(1)

        self.open_settings_txt()

        self.set_settings_in_lines()
        # кнопки изменения цветов
        self.uiS.left_red.clicked.connect(self.red_left)
        self.uiS.left_green.clicked.connect(self.green_left)
        self.uiS.left_blue.clicked.connect(self.blue_left)
        self.uiS.right_red.clicked.connect(self.red_right)
        self.uiS.right_green.clicked.connect(self.green_right)
        self.uiS.right_blue.clicked.connect(self.blue_right)
        # кнопки подтверждения/отмены
        self.uiS.cancel_button.clicked.connect(self.cancel)
        self.uiS.activate_button.clicked.connect(self.activate)
        self.uiS.confirm_button.clicked.connect(self.confirm)
        # изменение данных в строках
        self.uiS.lineRed.textChanged.connect(self.activate_buttons)
        self.uiS.lineGreen.textChanged.connect(self.activate_buttons)
        self.uiS.lineBlue.textChanged.connect(self.activate_buttons)
        # выбор кол-во цветов
        self.uiS.comboBox.currentIndexChanged.connect(b)
        self.uiS.comboBox.setCurrentIndex(self.index)

    def open_settings_txt(self):
        """Открытие файла с сохранёнными настройками"""
        setting_txt = open("settings.txt").read().split('\n')
        self.red = int(setting_txt[0][4:])
        self.green = int(setting_txt[1][6:])
        self.blue = int(setting_txt[2][5:])
        self.folder = setting_txt[3][7:]

    def set_color(self):
        p = QPalette()
        gradient = QLinearGradient(0, 0, 0, 400)
        gradient.setColorAt(0.0, QColor(self.red, self.green, self.blue))
        p.setBrush(QPalette.Window, QBrush(gradient))
        self.setAutoFillBackground(True)
        self.setPalette(p)

    def set_variant_of_color(self):
        self.index = self.uiS.comboBox.currentIndex()

    def cancel(self):
        self.close()

    def activate(self):
        settins_txt = open("settings.txt", 'w')
        settins_txt.write(f"red={self.red}\n"
                          f"green={self.blue}\n"
                          f"blue={self.green}\n"
                          f"folder={self.folder}")
        settins_txt.close()
        self.uiS.activate_button.setDisabled(1)
        self.uiS.confirm_button.setDisabled(1)

    def confirm(self):
        settins_txt = open("settings.txt", 'w')
        settins_txt.write(f"red={self.red}\n"
                          f"green={self.blue}\n"
                          f"blue={self.green}\n"
                          f"folder={self.folder}")
        settins_txt.close()
        self.uiS.activate_button.setDisabled(1)
        self.uiS.confirm_button.setDisabled(1)
        self.close()

    def activate_buttons(self):
        self.uiS.activate_button.setEnabled(1)
        self.uiS.confirm_button.setEnabled(1)
        self.color_changed()

    def set_settings_in_lines(self):
        """Вставить параметры в строки"""
        self.uiS.lineRed.setText(str(self.red))
        self.uiS.lineBlue.setText(str(self.blue))
        self.uiS.lineGreen.setText(str(self.green))
        self.uiS.line_folder.setText(self.folder)

    def color_changed(self):
        self.red = int(self.uiS.lineRed.text())
        self.green = int(self.uiS.lineGreen.text())
        self.blue = int(self.uiS.lineBlue.text())

    def red_left(self):
        self.red -= 1
        self.uiS.lineRed.setText(str(self.red))

    def red_right(self):
        self.red += 1
        self.uiS.lineRed.setText(str(self.red))

    def green_left(self):
        self.green -= 1
        self.uiS.lineGreen.setText(str(self.green))

    def green_right(self):
        self.green += 1
        self.uiS.lineGreen.setText(str(self.green))

    def blue_left(self):
        self.blue -= 1
        self.uiS.lineBlue.setText(str(self.blue))

    def blue_right(self):
        self.blue += 1
        self.uiS.lineBlue.setText(str(self.blue))


class Player(QMainWindow):
    """Основное окно"""

    def __init__(self):
        super(Player, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)  # подключаем интерфейс
        self.init_ui()

    def init_ui(self):
        """Основная инициализация"""
        self.ui.playButton.setIcon(
            self.style().standardIcon(QStyle.SP_MediaPlay))

        self.forms = {'mp3': '1',
                      'wav': '2'}
        # флажки
        self.playing = False
        self.player_changing = False

        self.update_base()
        self.open_settings_txt()
        self.set_color()

        mediaPlayer.stateChanged.connect(self.mediastate_changed)
        mediaPlayer.positionChanged.connect(self.position_changed)
        mediaPlayer.durationChanged.connect(self.duration_changed)

        self.ui.horizontalSlider.valueChanged.connect(self.set_position)

        self.ui.openAudio.clicked.connect(self.open_file)
        self.ui.playlist.triggered.connect(self.open_playlists)
        self.ui.playButton.clicked.connect(self.pause_music)
        self.ui.win_options.triggered.connect(self.open_parametr)

        self.ui.next_button.clicked.connect(mediaPlayer.playlist().next)
        self.ui.previous_button.clicked.connect(mediaPlayer.playlist().previous)

    def set_position(self, position):
        if not self.player_changing:
            mediaPlayer.setPosition(position)

    def mediastate_changed(self):
        if mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.ui.playButton.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause)

            )

        else:
            self.ui.playButton.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay)

            )

    def position_changed(self, position):
        self.player_changing = True
        self.ui.horizontalSlider.setValue(position)
        self.player_changing = False

    def duration_changed(self, duration):
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
        con = sqlite3.connect('base.sqlite')
        cur = con.cursor()
        result1 = cur.execute("""SELECT
                    songs.name FROM songs""").fetchall()
        result = list(map(lambda x: x[0], result1))
        # for i in result1:
        #     result.append(i[0])
        tracks, paths = check_new_tracks()
        a = 0
        for track in tracks:
            name = track[:-4]
            form = self.forms[track[-3:]]
            path = paths[a]
            a += 1
            if name not in result:
                print(f"Трек добавился в базу: {name}\n")
                cur.execute("""INSERT INTO songs(name, format, way) VALUES(?, ?, ?)""", (name, form, path))
        con.commit()
        con.close()

    def open_settings_txt(self):
        """Открытие файла с сохранёнными настройками"""
        setting_txt = open("settings.txt").read().split('\n')
        self.red = int(setting_txt[0][4:])
        self.green = int(setting_txt[1][6:])
        self.blue = int(setting_txt[2][5:])
        self.folder = setting_txt[3][7:]

    def set_color(self):
        p = QPalette()
        gradient = QLinearGradient(0, 0, 0, 400)
        gradient.setColorAt(0.0, QColor(self.red, self.green, self.blue))
        p.setBrush(QPalette.Window, QBrush(gradient))
        self.setAutoFillBackground(True)
        self.setPalette(p)

    def pause_music(self):
        """Остановить или воспроизвести музыку"""
        if mediaPlayer.state() == QMediaPlayer.PlayingState:
            mediaPlayer.pause()  # остановить
            self.ui.playButton.setText('Play')
        else:
            mediaPlayer.play()  # продолжить
            self.ui.playButton.setText('Stop')

    def open_file(self):
        """Открыть окно для выбора файла"""
        filename, _ = QFileDialog.getOpenFileName(self, "Open music", 'G:/Sasha/work/PyMusic/tracks')
        print(f"Вручную добавлен трек: {filename}\n")
        if filename != '':
            url = QUrl.fromLocalFile(filename)
            mediaPlayer.playlist().addMedia(QMediaContent(url))
            self.ui.playButton.setText("Play")


def check_new_tracks():
    new_txt = list(map(lambda x: x[7:], glob.glob("tracks/*.mp3")))
    path = list(map(lambda x: os.path.abspath(f"tracks/{x}"), new_txt))
    print(f"check_new_tracks: \n{new_txt}\n")
    return new_txt, path
