import sys
import csv
import datetime
import os
import multiprocessing as mlp
from widget import Ui_MainWindow
from PySide2 import QtCore, QtWidgets


class SyncObj(QtCore.QObject):
    progressBarUpdated = QtCore.Signal(int)
    tableUpdatedRow = QtCore.Signal((int, int, list))
    tableUpdatedHeader = QtCore.Signal(int)


class Winn(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Winn, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.check = False
        self.login_array = []
        self.data_array = []
        self.ui.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.ui.PathFile.setReadOnly(True)
        self.ui.OpenFile.clicked.connect(self.OpenFile)
        self.ui.AnalizFile.clicked.connect(self.make_pool)
        self.ui.serchLogin.clicked.connect(self.find_login)
        self.ui.serchData.clicked.connect(self.find_data)
        self.ui.saveData.clicked.connect(self.store_data)
        self.my_pool = mlp.Pool(1)
        self.callback_obj = SyncObj()
        self.callback_obj.progressBarUpdated.connect(self.ui.progressBar.setValue)
        self.callback_obj.tableUpdatedRow.connect(self.UpdateTableRow)
        self.callback_obj.tableUpdatedHeader.connect(self.UpdateTableHeadline)

    def OpenFile(self):
        file0 = QtWidgets.QFileDialog()
        open_file = file0.getExistingDirectory(self)
        self.ui.PathFile.setText('')
        self.ui.PathFile.setText(open_file)

    def UpdateTableRow(self, i, min, row):
        self.ui.tableWidget.insertRow(self.ui.tableWidget.rowCount())
        for j, v in enumerate(row):
            if j == 0:
                self.data_array.append(v)
            if j == 3:
                self.login_array.append(v)
            it = QtWidgets.QTableWidgetItem()
            it.setData(QtCore.Qt.DisplayRole, v)
            self.ui.tableWidget.setItem((i - min), j, it)

    def UpdateTableHeadline(self, row):
        self.ui.tableWidget.setHorizontalHeaderLabels(row)

    def block_button(self):
        self.ui.AnalizFile.setDisabled(True)
        self.ui.saveData.setDisabled(True)
        self.ui.serchData.setDisabled(True)
        self.ui.serchLogin.setDisabled(True)
        self.ui.OpenFile.setDisabled(True)

    def unblock_button(self):
        self.ui.AnalizFile.setDisabled(False)
        self.ui.saveData.setDisabled(False)
        self.ui.serchData.setDisabled(False)
        self.ui.serchLogin.setDisabled(False)
        self.ui.OpenFile.setDisabled(False)

    def make_pool(self):
        self.block_button()
        file_way = self.ui.PathFile.text()
        if os.path.exists(file_way) is False:
            QtWidgets.QMessageBox.about(self, 'Ошибка', 'Введите путь')
            self.ui.PathFile.setText('')
            self.unblock_button()
            return 2
        list_dir = os.listdir(file_way)
        csv_files = []
        for i in range(len(list_dir)):
            get_path = os.path.join(file_way, list_dir[i])
            check = os.path.isfile(get_path)
            if check:
                sp_file = list_dir[i].split('.')
                if sp_file[-1] == 'csv':
                    csv_files.append(get_path)
        if len(csv_files) == 0:
            QtWidgets.QMessageBox.about(self, 'Ошибка', 'Не найдены csv файлы')
            self.unblock_button()
        self.my_pool.apply_async(func=dir_reader, args=(csv_files,), callback=self.assign_data)

    
    def assign_data(self, solo_data):
        if len(self.data_array) != 0:
            self.data_array.clear()
        if len(self.login_array) != 0:
            self.login_array.clear()
        id = self.ui.comboBox.currentIndex()
        count_box = self.ui.comboBox.count()
        for i in range(count_box):
            if id == i:
                min = i * 100
                max = (i + 1) * 100 - 1
        ost = len(solo_data) % 100
        count_id = len(solo_data) - ost
        count_id = int(count_id / 100)
        self.UpdateTableHeadline(solo_data[0])
        value = 0
        self.ui.tableWidget.setRowCount(0)
        for i, row in enumerate(solo_data[1:]):
            value += 1
            self.callback_obj.progressBarUpdated.emit(value)
            if min <= i <= max:
                self.callback_obj.tableUpdatedRow.emit(i, min, row)
        if count_box > 1:
            self.ui.comboBox.clear()
            self.ui.comboBox.addItem("1 - ая сотня элементов")
            self.ui.comboBox.setCurrentIndex(0)
        for i in range(1, count_id):
            self.ui.comboBox.addItem("{0} - ая сотня элементов".format(i + 1))
        self.ui.comboBox.addItem("Последние элементы")
        self.callback_obj.progressBarUpdated.emit(value + 1)
        self.callback_obj.progressBarUpdated.emit(0)
        self.save_array = list.copy(solo_data)
        self.unblock_button()
        self.check = True
        

    def find_data(self):
        self.block_button()
        if self.login_array != []:
            self.login_array.clear()
        if self.check:
            enter = self.ui.dateTimeEdit.text()
            enter = enter.split(' ')
            data_N = enter[0]
            time_N = enter[1]
            data_N = data_N.split('.')
            time_N = time_N.split(':')
            unix_time = datetime.datetime(int(data_N[2]), int(data_N[1]), int(data_N[0]), int(time_N[0]), int(time_N[1]),
                                          int(time_N[2])).timestamp()
            unix_time = int(unix_time)
            unix_time += (36000)
            unix_time = str(unix_time)
            if unix_time in self.data_array:
                self.data_array.clear()
                self.ui.tableWidget.setRowCount(0)
                self.UpdateTableHeadline(self.save_array[0])
                p = 0
                value = 0
                for i, row in enumerate(self.save_array[1:]):
                    value += 1
                    self.callback_obj.progressBarUpdated.emit(value)
                    if unix_time == row[0]:
                        self.ui.tableWidget.insertRow(self.ui.tableWidget.rowCount())
                        for j, v in enumerate(row):
                            if j == 3:
                                self.login_array.append(v)
                            it = QtWidgets.QTableWidgetItem()
                            it.setData(QtCore.Qt.DisplayRole, v)
                            self.ui.tableWidget.setItem(p, j, it)
                        p += 1
                self.callback_obj.progressBarUpdated.emit(value + 1)
                self.callback_obj.progressBarUpdated.emit(0)
                self.unblock_button()
                pass
            else:
                QtWidgets.QMessageBox.about(self, 'Ошибка', 'Дата не найдена')
                self.unblock_button()
        else:
            QtWidgets.QMessageBox.about(self, 'Ошибка', 'Проанализируйте файл')
            self.unblock_button()

    def store_data(self):
        self.block_button()
        headline = ['begin', 'end', 'time interval', 'login', 'mac ab', 'ULSK1', 'BRAS ip', 'start count', 'alive count',
                  'stop count', 'incoming', 'outcoming', 'error_count', 'code 0', 'code 1011', 'code 1100', 'code -3',
                  'code -52', 'code -42', 'code -21', 'code -40', ' code -44', 'code -46', ' code -38']
        rowCount = self.ui.tableWidget.rowCount()
        columCount = 24
        d = QtWidgets.QFileDialog.getSaveFileName(self, "Choose a filename to save under", "/data_save",
                                                  "Файл Microsoft Excel (*.csv)")
        if d[0] == '':
            QtWidgets.QMessageBox.about(self, 'Ошибка', 'Вы отменили сохранение')
            self.unblock_button()
            return 1
        value = 0
        with open(d[0], 'w', newline='') as file_csv:
            writher = csv.writer(file_csv)
            writher.writerow(headline)
            for i in range(rowCount):
                save = []
                value += 1
                self.callback_obj.progressBarUpdated.emit(value)
                for j in range(columCount):
                    p = self.ui.tableWidget.item(i, j).text()
                    save.append(p)
                writher.writerow(save)
        self.callback_obj.progressBarUpdated.emit(value + 1)
        self.callback_obj.progressBarUpdated.emit(0)
        self.unblock_button()

    def find_login(self):
        self.block_button()
        if self.data_array != []:
            self.data_array.clear()
        if self.check:
            login, ok = QtWidgets.QInputDialog.getText(self, "Ввод логина",
                                                       "Введите логин для поиска:", QtWidgets.QLineEdit.Normal,
                                                       '')
            if ok and login:
                if login in self.login_array:
                    self.login_array.clear()
                    self.ui.tableWidget.setRowCount(0)
                    self.UpdateTableHeadline(self.save_array[0])
                    p = 0
                    value = 0
                    for i, row in enumerate(self.save_array[1:]):
                        value += 1
                        self.callback_obj.progressBarUpdated.emit(value)
                        if login in row:
                            self.ui.tableWidget.insertRow(self.ui.tableWidget.rowCount())
                            for j, v in enumerate(row):
                                if j == 0:
                                    self.data_array.append(v)
                                it = QtWidgets.QTableWidgetItem()
                                it.setData(QtCore.Qt.DisplayRole, v)
                                self.ui.tableWidget.setItem(p, j, it)
                            p += 1
                    self.callback_obj.progressBarUpdated.emit(value + 1)
                    self.callback_obj.progressBarUpdated.emit(0)
                    self.unblock_button()
                else:
                    QtWidgets.QMessageBox.about(self, 'Ошибка', 'Логина не найдено.')
                    self.unblock_button()
            else:
                QtWidgets.QMessageBox.about(self, 'Ошибка', 'Введите логин.')
                self.unblock_button()
        else:
            QtWidgets.QMessageBox.about(self, 'Ошибка', 'Проанализируйте файл.')
            self.unblock_button()    

def dir_reader(csv_files):
    all_data = []
    for i in range(len(csv_files)):
        with open(csv_files[i], 'r')as csv_file:
            reader = csv.reader(csv_file)  
            data = list(reader)
        all_data.append(data)
    solo_data = list.copy(all_data[0])
    for i in range(1, len(all_data)):
        all_data[i].remove(all_data[i][0])
        solo_data += all_data[i]
    return solo_data       


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = Winn()
    myapp.show()
    sys.exit(app.exec_())