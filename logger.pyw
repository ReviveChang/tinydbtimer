import sys
import datetime
import psycopg2
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer

import dblogger


class LoggerWindow(QMainWindow, dblogger.Ui_Dialog):
    def __init__(self, parent=None):
        super(LoggerWindow, self).__init__(parent)
        self.conn = psycopg2.connect("dbname=Record user=Virtue password=0030")
        self.cur = self.conn.cursor()
        self.begin = datetime.datetime.now()
        self.end = datetime.datetime.now()
        self.timer = QTimer()
        self.timer_b = QTimer()
        self.setupUi(self)
        self.tag = 'Anki'
        self.flag = True
        self.is_blank = False
        self.interact()

    def interact(self):
        self.pushButton_3.setHidden(True)
        self.pushButton_4.setHidden(True)
        self.timer.timeout.connect(self.show_time)
        self.timer_b.timeout.connect(self.show_cur)
        self.pushButton_1.clicked.connect(self.press_button)
        self.pushButton_2.clicked.connect(QApplication.quit)
        self.pushButton_3.clicked.connect(self.press_add)
        self.pushButton_4.clicked.connect(self.press_dim)
        self.radioButton_1.setChecked(True)
        self.radioButton_1.toggled.connect(self.set_tag)
        self.radioButton_2.toggled.connect(self.set_tag)
        self.radioButton_3.toggled.connect(self.set_tag)
        self.radioButton_4.toggled.connect(self.set_tag)
        self.radioButton_5.toggled.connect(self.set_tag)
        self.radioButton_6.toggled.connect(self.set_blank)
        self.timer_b.start(100)

    def set_tag(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            self.tag = radioButton.text()
            # print(self.tag)

    def set_blank(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            self.is_blank= True
            # print(self.tag)

    def show_time(self):
        time = datetime.datetime(1990, 1, 1, 0, 0, 0)+(datetime.datetime.now() - self.begin)
        self.lcdNumber.display(time.strftime('%H:%M:%S'))

    def show_cur(self):
        self.lcdNumber.display(datetime.datetime.now().strftime('%H:%M:%S'))

    def press_button(self):
        if self.flag:
            self.log_begin()
            # print('Logging begin!')
        else:
            self.log_end()
            # print('Logging Finished')

    def press_add(self):
        self.begin = self.begin - datetime.timedelta(minutes=5)

    def press_dim(self):
        if self.begin+datetime.timedelta(minutes=5) < datetime.datetime.now():
            self.begin = self.begin + datetime.timedelta(minutes=5)

    def upload(self):
        #print('Uploading...')
        sql = "INSERT INTO work (begintime, endtime, tag, time, amount) VALUES (%s, %s, %s, %s, %s);"
        value = [self.begin.strftime('%Y-%m-%d %H:%M:%S'), self.end.strftime('%Y-%m-%d %H:%M:%S'), self.tag,
                 str(self.end-self.begin), self.lineEdit_2.text()]
        try:
            self.cur.execute(sql, value)
            self.conn.commit()
            # print('Uploaded')
        except Exception:
            self.conn.rollback()
            # print('Error!')

    def log_begin(self):
        self.begin = datetime.datetime.now()
        self.flag = False
        self.pushButton_1.setText("Log it!")
        self.pushButton_3.setHidden(False)
        self.pushButton_4.setHidden(False)
        self.timer_b.stop()
        self.timer.start(100)

    def log_end(self):
        if self.is_blank:
            self.tag = self.lineEdit.text()
        self.end = datetime.datetime.now()
        self.pushButton_1.setText('Begin!')
        self.pushButton_3.setHidden(True)
        self.pushButton_4.setHidden(True)
        self.flag = True
        self.upload()
        self.timer.stop()
        self.timer_b.start(100)
        self.lcdNumber.display(datetime.datetime.now().strftime("%H:%M:%S"))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = LoggerWindow()
    MainWindow.show()
    sys.exit(app.exec_())
