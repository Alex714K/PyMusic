from mysetting import Ui_Settings
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QPalette, QLinearGradient, QBrush, QColor


class Settings(QMainWindow):
    """Окно настроек"""
    def __init__(self):
        super(Settings, self).__init__()
        self.uiS = Ui_Settings()
        self.uiS.setupUi(self)
        self.init_ui()

    def init_ui(self):
        """Основная инициализация"""
        self.setWindowTitle('Settings')

        self.uiS.confirm_button.setDisabled(1)
        self.uiS.activate_button.setDisabled(1)

        self.set_color()

        self.open_settings_txt()

        self.set_settings_in_lines()
        # кнопки изменения цветов
        self.uiS.left_red.clicked.connect(self.red_left)
        self.uiS.left_green.clicked.connect(self.green_left)
        self.uiS.left_blue.clicked.connect(self.blue_left)
        self.uiS.right_red.clicked.connect(self.red_right)
        self.uiS.right_green.clicked.connect(self.green_right)
        self.uiS.right_blue.clicked.connect(self.blue_right)

        self.uiS.left_red_2.clicked.connect(self.red_left2)
        self.uiS.left_green_2.clicked.connect(self.green_left2)
        self.uiS.left_blue_2.clicked.connect(self.blue_left2)
        self.uiS.right_red_2.clicked.connect(self.red_right2)
        self.uiS.right_green_2.clicked.connect(self.green_right2)
        self.uiS.right_blue_2.clicked.connect(self.blue_right2)

        self.uiS.left_red_3.clicked.connect(self.red_left3)
        self.uiS.left_green_3.clicked.connect(self.green_left3)
        self.uiS.left_blue_3.clicked.connect(self.blue_left3)
        self.uiS.right_red_3.clicked.connect(self.red_right3)
        self.uiS.right_green_3.clicked.connect(self.green_right3)
        self.uiS.right_blue_3.clicked.connect(self.blue_right3)
        # кнопки подтверждения/отмены
        self.uiS.cancel_button.clicked.connect(self.cancel)
        self.uiS.activate_button.clicked.connect(self.activate)
        self.uiS.confirm_button.clicked.connect(self.confirm)
        # изменение данных в строках
        self.uiS.lineRed.textChanged.connect(self.color_changed)
        self.uiS.lineGreen.textChanged.connect(self.color_changed)
        self.uiS.lineBlue.textChanged.connect(self.color_changed)
        self.uiS.lineRed_2.textChanged.connect(self.color_changed)
        self.uiS.lineGreen_2.textChanged.connect(self.color_changed)
        self.uiS.lineBlue_2.textChanged.connect(self.color_changed)
        self.uiS.lineRed_3.textChanged.connect(self.color_changed)
        self.uiS.lineGreen_3.textChanged.connect(self.color_changed)
        self.uiS.lineBlue_3.textChanged.connect(self.color_changed)
        # выбор кол-во цветов
        self.uiS.comboBox.currentIndexChanged.connect(self.set_variant_of_color)
        self.uiS.comboBox.setCurrentIndex(self.variant)

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
        self.volume = setting_txt[11][7:]

    def set_color(self):
        """Выставляет цвет фона у окна"""
        p = QPalette()
        gradient = QLinearGradient(0, 0, 0, 400)

        gradient.setColorAt(0.0, QColor(215, 215, 215))

        p.setBrush(QPalette.Window, QBrush(gradient))
        self.setAutoFillBackground(True)
        self.setPalette(p)

    def set_variant_of_color(self):
        """Одноцветный/Двухцветный/Трёхцветный"""
        self.variant = self.uiS.comboBox.currentIndex()
        self.activate_buttons()

    def cancel(self):
        """Закрывает окно"""
        self.close()

    def activate(self):
        """Только сохраняет настройки"""
        settins_txt = open("settings.txt", 'w')
        settins_txt.write(f"red={self.red}\n"
                          f"green={self.green}\n"
                          f"blue={self.blue}\n"
                          f"red2={self.red2}\n"
                          f"green2={self.green2}\n"
                          f"blue2={self.blue2}\n"
                          f"red3={self.red3}\n"
                          f"green3={self.green3}\n"
                          f"blue3={self.blue3}\n"
                          f"folder={self.folder}\n"
                          f"variant={self.variant}"
                          f"volume={self.volume}")
        settins_txt.close()
        self.uiS.activate_button.setDisabled(1)
        self.uiS.confirm_button.setDisabled(1)

    def confirm(self):
        """Сохраняет настройки и закрывает окно"""
        settins_txt = open("settings.txt", 'w')
        settins_txt.write(f"red={self.red}\n"
                          f"green={self.green}\n"
                          f"blue={self.blue}\n"
                          f"red2={self.red2}\n"
                          f"green2={self.green2}\n"
                          f"blue2={self.blue2}\n"
                          f"red3={self.red3}\n"
                          f"green3={self.green3}\n"
                          f"blue3={self.blue3}\n"
                          f"folder={self.folder}\n"
                          f"variant={self.variant}"
                          f"volume={self.volume}")
        settins_txt.close()
        self.uiS.activate_button.setDisabled(1)
        self.uiS.confirm_button.setDisabled(1)
        self.close()

    def activate_buttons(self):
        """Активирует кнопки"""
        self.uiS.activate_button.setEnabled(1)
        self.uiS.confirm_button.setEnabled(1)

    def set_settings_in_lines(self):
        """Вставить параметры в строки"""
        self.uiS.lineRed.setText(str(self.red))
        self.uiS.lineBlue.setText(str(self.blue))
        self.uiS.lineGreen.setText(str(self.green))
        self.uiS.lineRed_2.setText(str(self.red2))
        self.uiS.lineBlue_2 .setText(str(self.blue2))
        self.uiS.lineGreen_2.setText(str(self.green2))
        self.uiS.lineRed_3.setText(str(self.red3))
        self.uiS.lineBlue_3.setText(str(self.blue3))
        self.uiS.lineGreen_3.setText(str(self.green3))
        self.uiS.line_folder.setText(self.folder)

    def color_changed(self):
        """Вытаскивает из строк в программу показатели цветов"""
        self.red = int(self.uiS.lineRed.text())
        self.green = int(self.uiS.lineGreen.text())
        self.blue = int(self.uiS.lineBlue.text())
        self.red2 = int(self.uiS.lineRed_2.text())
        self.green2 = int(self.uiS.lineGreen_2.text())
        self.blue2 = int(self.uiS.lineBlue_2.text())
        self.red3 = int(self.uiS.lineRed_3.text())
        self.green3 = int(self.uiS.lineGreen_3.text())
        self.blue3 = int(self.uiS.lineBlue_3.text())
        self.activate_buttons()

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

    def red_left2(self):
        self.red2 -= 1
        self.uiS.lineRed_2.setText(str(self.red2))

    def red_right2(self):
        self.red2 += 1
        self.uiS.lineRed_2.setText(str(self.red2))

    def green_left2(self):
        self.green2 -= 1
        self.uiS.lineGreen_2.setText(str(self.green2))

    def green_right2(self):
        self.green2 += 1
        self.uiS.lineGreen_2.setText(str(self.green2))

    def blue_left2(self):
        self.blue2 -= 1
        self.uiS.lineBlue_2.setText(str(self.blue2))

    def blue_right2(self):
        self.blue2 += 1
        self.uiS.lineBlue_2.setText(str(self.blue2))

    def red_left3(self):
        self.red3 -= 1
        self.uiS.lineRed_3.setText(str(self.red3))

    def red_right3(self):
        self.red3 += 1
        self.uiS.lineRed_3.setText(str(self.red3))

    def green_left3(self):
        self.green3 -= 1
        self.uiS.lineGreen_3.setText(str(self.green3))

    def green_right3(self):
        self.green3 += 1
        self.uiS.lineGreen_3.setText(str(self.green3))

    def blue_left3(self):
        self.blue3 -= 1
        self.uiS.lineBlue_3.setText(str(self.blue3))

    def blue_right3(self):
        self.blue3 += 1
        self.uiS.lineBlue_3.setText(str(self.blue3))
