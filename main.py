import glob
import os
import sqlite3
from PyQt5 import QtWidgets
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from myplayer import Ui_MainWindow
from myplaylist import Ui_MainPlaylist
from mysetting import Ui_MainSetting
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QTableWidgetItem, QHeaderView, QStyle
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtGui import QIcon, QPalette
from PyQt5.QtCore import Qt, QUrl
# почти все импорты временны и большая часть убирётся


def b():
    """Затычка"""
    print(1)
    pass


def check_new_tracks():
    txt = open('old_tracks.txt').read().split('\n')
    new_txt = list(map(lambda x: x[7:], glob.glob("tracks/*.mp3")))
    for track in new_txt:
        if track not in txt:
            txt.append(track)
    for track in txt:
        if track not in new_txt:
            txt.remove(track)
    new_txt = open('old_tracks.txt', 'w').write('\n'.join(txt))
    return txt


class PlayList(QMainWindow):
    """Окно плейлиста (скорей библиотека со всеми треками)"""
    def __init__(self):
        super(PlayList, self).__init__()
        self.uiP = Ui_MainPlaylist()
        self.uiP.setupUi(self)
        self.init_ui()

    def init_ui(self):
        """Основная инициализация"""
        self.update_base()
        self.get_base()
        self.get_queue()

        self.uiP.tableWidget.cellClicked.connect(self.clicked_cell)

        self.uiP.custom_button.clicked.connect(self.add_custom_file)

        self.uiP.add_button.clicked.connect(self.add_track)
        self.uiP.delete_button.clicked.connect(self.delete_track)
        self.uiP.up_button.clicked.connect(self.up_track)
        self.uiP.down_button.clicked.connect(self.down_track)

        # self.uiP.q

    def clicked_cell(self):
        row = self.uiP.tableWidget.currentRow()
        print(row)
        # self.cell = self.uiP.tableWidget.


    def add_track(self):
        txt = open("queue.txt").read().split('\n')

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
        result = list()
        for i in result1:
            result.append(i[0])
        tracks = check_new_tracks()
        for track in tracks:
            if track[:-4] not in result:
                print(track[:-4])
                cur.execute("""INSERT INTO songs(name) VALUES(?)""", (track[:-4],))
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
        name = path[path.rfind('/') + 1:-4]
        print(path[path.rfind('/') + 1:-4])
        con = sqlite3.connect('base.sqlite')
        cur = con.cursor()
        result1 = cur.execute("""SELECT
                            songs.name FROM songs WHERE custom = ?""", (path,)).fetchall()
        result = list()
        for i in result1:
            result.append(i[0])
        if name not in result:
            cur.execute("""INSERT INTO songs(name, custom) VALUES(?, ?)""", (name, path))
            con.commit()
        con.close()


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

    def open_settings_txt(self):
        """Открытие файла с сохранёнными настройками"""
        setting_txt = open("settings.txt").read().split('\n')
        self.red = int(setting_txt[0][4:])
        self.green = int(setting_txt[1][6:])
        self.blue = int(setting_txt[2][5:])
        self.folder = setting_txt[3][7:]

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


class MyWindow(QMainWindow):
    """Основное окно"""
    def __init__(self):
        super(MyWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)  # подключаем интерфейс
        self.init_ui()

    def init_ui(self):
        """Основная инициализация"""
        check_new_tracks()
        # создаём проигрыватель
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        # флажки
        self.playing = False

        self.mediaPlayer.stateChanged.connect(self.mediastate_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)

        self.ui.horizontalSlider.valueChanged.connect(self.set_position)

        self.ui.openAudio.clicked.connect(self.open_file)
        self.ui.playlist.triggered.connect(self.open_playlists)
        self.ui.playButton.clicked.connect(self.pause_music)
        self.ui.win_options.triggered.connect(self.open_parametr)

        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile('tracks/Eye Of The_Storm.mp3')))  # временно

    def set_position(self, position):
        self.mediaPlayer.setPosition(position)

    def mediastate_changed(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.ui.playButton.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause)

            )

        else:
            self.ui.playButton.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay)

            )

    def position_changed(self, position):
        self.ui.horizontalSlider.setValue(position)

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

    def pause_music(self):
        """Остановить или воспроизвести музыку"""
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()  # остановить
            self.ui.playButton.setText('Play')
        else:
            self.mediaPlayer.play()  # продолжить
            self.ui.playButton.setText('Stop')

    def open_file(self):
        """Открыть окно для выбора файла"""
        filename, _ = QFileDialog.getOpenFileName(self, "Open music", 'G:/Sasha/work/PyMusic/tracks')
        print(filename)
        if filename != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.ui.playButton.setText("Play")


if __name__ == "__main__":
    import sys

app = QApplication(sys.argv)
application = MyWindow()
application.show()
sys.exit(app.exec())
