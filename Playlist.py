import glob
import sqlite3
from myplaylist import Ui_PlayList
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QTableWidgetItem, QHeaderView, QMessageBox, QTableWidget
from PyQt5.QtMultimedia import QMediaContent
from PyQt5.QtGui import QPalette, QLinearGradient, QBrush, QColor
from PyQt5.QtCore import QUrl


class PlayList(QMainWindow):
    """Окно плейлиста (скорей библиотека со всеми треками)"""

    def __init__(self, mediaplayer):
        super(PlayList, self).__init__()
        self.mediaPlayer = mediaplayer
        self.uiP = Ui_PlayList()
        self.uiP.setupUi(self)  # подключаем интерфейс
        self.init_ui()  # Нужно объяснять?)

    def init_ui(self):
        """Основная инициализация"""
        self.setWindowTitle('PlayList')
        # Флажки
        self.forms = {'mp3': '1',
                      'wav': '2'}

        self.click_cell = False

        self.update_base()
        self.get_base()
        self.get_queue()
        self.open_settings_txt()
        self.set_color()

        self.uiP.tableWidget.cellClicked.connect(self.clicked_cell)

        self.uiP.custom_button.clicked.connect(self.add_custom_file)
        self.uiP.custom_button.setDisabled(1)

        self.uiP.add_button.clicked.connect(self.add_track)
        self.uiP.delete_button.clicked.connect(self.delete_track)
        self.uiP.up_button.clicked.connect(self.up_track)
        self.uiP.down_button.clicked.connect(self.down_track)
        self.uiP.edit_button.clicked.connect(self.edit_cell)
        self.uiP.edit_button.setDisabled(1)

    def edit_cell(self):
        """Обновляет данные о треке в базу данных (альбом, исполнителя)"""
        if self.click_cell:  # если ячейку нажали
            cell = self.uiP.tableWidget.currentItem().text()
        else:  # если ячейку не нажали
            dlg = QMessageBox(self)
            dlg.setWindowTitle("ERROR")
            dlg.setText("Выберите ячейку, которую хотите изменить.")
            dlg.exec()
            return

        if cell == self.uiP.tableWidget.item(self.uiP.tableWidget.currentRow(), 0).text():
            dlg = QMessageBox(self)
            dlg.setWindowTitle("ERROR")
            dlg.setText("Название нельзя редактировать.")
            dlg.exec()
            return

        con = sqlite3.connect('base.sqlite')
        cur = con.cursor()
        text = self.uiP.lineEdit.text()
        name = self.uiP.tableWidget.item(self.uiP.tableWidget.currentRow(), 0)
        if self.uiP.tableWidget.currentColumn() == 1:
            cur.execute("""UPDATE songs SET team = ? WHERE name = ?""", (text, name))
        if self.uiP.tableWidget.currentColumn() == 2:
            cur.execute("""UPDATE songs SET album = ? WHERE name = ?""", (text, name))
        con.commit()
        con.close()
        self.get_base()

    def clicked_cell(self):
        self.click_cell = True

    def add_track(self):
        row = self.uiP.tableWidget.currentRow()
        cell = self.uiP.tableWidget.item(row, 0).text()
        form = self.uiP.tableWidget.item(row, 3).text()
        url = QUrl.fromLocalFile(f"tracks/{cell}.{form}")
        self.mediaPlayer.playlist().addMedia(QMediaContent(url))
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

    def delete_track(self):
        row = self.uiP.queue.currentRow()
        tracks = open('queue.txt', 'r').read().split('\n')
        tracks.pop(row)
        queue = open('queue.txt', 'w')
        queue.write('\n'.join(tracks))
        queue.close()
        self.get_queue()

    def up_track(self):
        """Поднимает трек в очереди"""
        row = self.uiP.queue.currentRow()
        tracks = open('queue.txt', 'r').read().split('\n')
        try:
            track = tracks[row]
            tracks[row] = tracks[row - 1]
            tracks[row - 1] = track
            queue = open('queue.txt', 'w')
            queue.write('\n'.join(tracks))
            queue.close()
            self.get_queue()
        except:
            return

    def down_track(self):
        """Опускает трек в очереди"""
        row = self.uiP.queue.currentRow()
        tracks = open('queue.txt', 'r').read().split('\n')
        try:
            track = tracks[row]
            tracks[row] = tracks[row + 1]
            tracks[row + 1] = track
            queue = open('queue.txt', 'w')
            queue.write('\n'.join(tracks))
            queue.close()
            self.get_queue()
        except:
            return

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
        tracks = check_new_tracks()
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
        while self.uiP.tableWidget.rowCount() > 0:  # Удаляем старые строки
            self.uiP.tableWidget.removeRow(0)
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
        self.uiP.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)

    def get_queue(self):
        txt = open("queue.txt").read().split('\n')
        while self.uiP.queue.rowCount() > 0:
            self.uiP.queue.removeRow(0)
        for i, row in enumerate(txt):
            self.uiP.queue.setRowCount(
                self.uiP.queue.rowCount() + 1)
            self.uiP.queue.setItem(
                i, 0, QTableWidgetItem(str(row)))

        self.uiP.queue.setEditTriggers(QTableWidget.NoEditTriggers)
        self.uiP.queue.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    def add_custom_file(self):
        """Открыть окно для выбора файла и добавить сторонний трек"""
        # проблема - QMediaPlayer не умеет работать с не локальными файлами (я не нашёл)
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


def check_new_tracks():
    """Возвращает """
    new_txt = list(map(lambda x: x[7:], glob.glob("tracks/*.mp3")))
    return new_txt
