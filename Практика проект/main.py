import sys
import sqlite3
import math

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QMessageBox, QButtonGroup

Time = ['Present Simple', 'Future Simple', 'Past Simple', 'Future Continuous', 'Present Continuous', 'Past Continuous','Future Perfect', 'Present Perfect', 'Past Perfect', 'Future Perfect Continuous', 'Present Perfect Continuous', 'Past Perfect Continuous']
Banned = ['1','2','3','4','5','6','7','8','9','0','~','`','!','@','"','$',';','%','^',':','&','?','*','(',')','-','_','=','+',' ','[','{',']','}',"'",'<',',','>','.','/','|']
Banned1 = ['~','`','!','@','"','$',';','%','^',':','&','?','*','(',')','-','_','=','+',' ','[','{',']','}',"'",'<',',','>','.','/','|']
Saved = ['q','w','e','r','t','y','u','i','o','p','a','s','d','f','g','h','j','k','l','z','x','c','v','b','n','m','Q','W','E','R','T','Y','U','I','O','P','A','S','D','F','G','H','J','K','L','Z','X','C','V','B','N','M']

class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui',self)

        self.user_login = ''
        self.current_rasdel = ''
        self.number_que = 0
        self.progress = 0
        self.current_answer = ''
        self.choise_answer = ''
        self.razdel = ''
        self.time = ''
        self.lvl_test = False
        
        self.pushButton.clicked.connect(self.log_in)
        self.pushButton_2.clicked.connect(lambda: self.swap_window(1))
        self.pushButton_6.clicked.connect(lambda: self.swap_window(0))
        self.pushButton_3.clicked.connect(self.register)
        self.pushButton_5.clicked.connect(self.profil)
        self.pushButton_30.clicked.connect(lambda: self.swap_window(2))
        self.pushButton_92.clicked.connect(self.back)
        self.pushButton_91.clicked.connect(self.test)
        self.pushButton_56.clicked.connect(self.test_lvl)
        self.pushButton_13.clicked.connect(self.check_answer)
        self.pushButton_32.clicked.connect(self.new_que)
        self.pushButton_33.clicked.connect(self.new_que)
        self.pushButton_29.clicked.connect(self.check_answer_2)
        self.pushButton_34.clicked.connect(self.new_que_2)
        self.pushButton_35.clicked.connect(self.new_que_2)
        self.pushButton_94.clicked.connect(self.glavnay)
        self.pushButton_90.clicked.connect(self.teor)
        self.pushButton_88.clicked.connect(self.glavnay)
        self.pushButton_87.clicked.connect(self.teor_back)

        self.btn_rasdel = QButtonGroup()
        self.btn_rasdel.addButton(self.pushButton_8)
        self.btn_rasdel.addButton(self.pushButton_7)
        self.btn_rasdel.addButton(self.pushButton_9)
        self.btn_rasdel.addButton(self.pushButton_41)
        self.btn_rasdel.addButton(self.pushButton_42)
        self.btn_rasdel.buttonClicked.connect(self.rasdel)

        self.btn_ans = QButtonGroup()
        self.btn_ans.addButton(self.pushButton_12)
        self.btn_ans.addButton(self.pushButton_11)
        self.btn_ans.addButton(self.pushButton_10)
        self.btn_ans.addButton(self.pushButton_14)
        self.btn_ans.buttonClicked.connect(self.choise)

        self.btn_teor = QButtonGroup()
        self.btn_teor.addButton(self.pushButton_27)
        self.btn_teor.addButton(self.pushButton_28)
        self.btn_teor.addButton(self.pushButton_31)
        self.btn_teor.buttonClicked.connect(self.teor_choise)

        self.btn_teor_1 = QButtonGroup()
        self.btn_teor_1.addButton(self.pushButton_36)
        self.btn_teor_1.addButton(self.pushButton_37)
        self.btn_teor_1.addButton(self.pushButton_38)
        self.btn_teor_1.addButton(self.pushButton_39)
        self.btn_teor_1.buttonClicked.connect(self.teor_choise_2)

    def teor_back(self):
        self.swap_window(2)
        self.stackedWidget_6.setCurrentIndex(0)
        self.stackedWidget_5.setCurrentIndex(0)

    def teor_choise(self, btn):
        self.time = btn.text() + ' '
        self.stackedWidget_5.setCurrentIndex(1)
        

    def teor_choise_2(self, btn):
        self.time += btn.text()
        self.stackedWidget_5.setCurrentIndex(0)
        for i in range(12):
            if Time[i] == self.time:
                self.stackedWidget_6.setCurrentIndex(i + 1)

    def teor(self):
        self.swap_window(7)
        self.label_31.setText(self.razdel)

    def new_que(self):
        self.stackedWidget_2.setCurrentIndex(2)
        self.btn_drop()
        if self.number_que == 5:
            self.swap_window(5)
        self.que()

    def glavnay(self):
        self.back()
        self.swap_window(2)
        self.stackedWidget_6.setCurrentIndex(0)
        self.stackedWidget_5.setCurrentIndex(0)

    def new_que_2(self):
        self.stackedWidget_3.setCurrentIndex(2)
        self.lineEdit_6.clear()
        self.que()
        if self.number_que == 11:
            
            self.swap_window(6)
            self.label_79.setText(self.razdel)
            if self.lvl_test:
                self.label_79.setText('Тест')
                self.label_23.setText(self.lvl(math.ceil(self.progress)))
                self.label_9.setText('Уровень знания языка: ' + self.lvl(math.ceil(self.progress)))
            else:
                self.label_23.setText(str(self.progress * 10) + '%')
            self.label_32.setText(str(self.progress) + '/10')
            if self.razdel == 'Основы':
                self.progressBar.setValue(self.progress)
            elif self.razdel == 'Я - из...':
                self.progressBar_2.setValue(self.progress)
            elif self.razdel == 'Времена':
                self.progressBar_6.setValue(self.progress)
            elif self.razdel == 'Знакомство':
                self.progressBar_7.setValue(self.progress)
            elif self.razdel == 'Моя семья':
                self.progressBar_8.setValue(self.progress)

    def check_answer_2(self):
        if self.lineEdit_6.text() == self.current_answer:
            self.stackedWidget_3.setCurrentIndex(0)
            self.progress += 1
            print(self.progress)
            self.progressBar_9.setValue(self.progress)
        else:
            self.stackedWidget_3.setCurrentIndex(1)        
            

    def check_answer(self):
        if self.choise_answer == self.current_answer:
            self.stackedWidget_2.setCurrentIndex(0)
            self.progress += 1
            print(self.progress)
            self.progressBar_3.setValue(self.progress)
        else:
            self.stackedWidget_2.setCurrentIndex(1)

    def btn_drop(self):
        self.pushButton_12.setStyleSheet('border-radius: 25px; background-color: rgb(134, 115, 161); border: 2px solid red; border-color: rgb(255, 255, 255); color: rgb(255, 255, 255);')
        self.pushButton_11.setStyleSheet('border-radius: 25px; background-color: rgb(134, 115, 161); border: 2px solid red; border-color: rgb(255, 255, 255); color: rgb(255, 255, 255);')
        self.pushButton_10.setStyleSheet('border-radius: 25px; background-color: rgb(134, 115, 161); border: 2px solid red; border-color: rgb(255, 255, 255); color: rgb(255, 255, 255);')
        self.pushButton_14.setStyleSheet('border-radius: 25px; background-color: rgb(134, 115, 161); border: 2px solid red; border-color: rgb(255, 255, 255); color: rgb(255, 255, 255);')
            

    def choise(self, btn):
        self.pushButton_12.setStyleSheet('border-radius: 25px; background-color: rgb(134, 115, 161); border: 2px solid red; border-color: rgb(255, 255, 255); color: rgb(255, 255, 255);')
        self.pushButton_11.setStyleSheet('border-radius: 25px; background-color: rgb(134, 115, 161); border: 2px solid red; border-color: rgb(255, 255, 255); color: rgb(255, 255, 255);')
        self.pushButton_10.setStyleSheet('border-radius: 25px; background-color: rgb(134, 115, 161); border: 2px solid red; border-color: rgb(255, 255, 255); color: rgb(255, 255, 255);')
        self.pushButton_14.setStyleSheet('border-radius: 25px; background-color: rgb(134, 115, 161); border: 2px solid red; border-color: rgb(255, 255, 255); color: rgb(255, 255, 255);')
        btn.setStyleSheet('border-radius: 25px; background-color: rgb(178, 153, 214); border: 2px solid red; border-color: rgb(255, 255, 255); color: rgb(255, 255, 255);')
        self.choise_answer = btn.text()

    def que(self):
        self.number_que += 1
        if self.number_que <= 5:
            self.stackedWidget_2.setCurrentIndex(2)
            con = sqlite3.connect("reg.db")
            cur = con.cursor()
            res = cur.execute("""SELECT * FROM test where id = ?""", (self.number_que, )).fetchall()
            print(res)
            self.label_19.setText(str(res[0][0]) + '.' + str(res[0][1]))
            self.pushButton_12.setText(str(res[0][2]))
            self.pushButton_11.setText(str(res[0][3]))
            self.pushButton_10.setText(str(res[0][4]))
            self.pushButton_14.setText(str(res[0][5]))
            self.progressBar_3.setValue(self.progress)
            self.current_answer = str(res[0][6])
        elif self.number_que <= 10:
            self.stackedWidget_2.setCurrentIndex(2)
            con = sqlite3.connect("reg.db")
            cur = con.cursor()
            res = cur.execute("""SELECT * FROM test where id = ?""", (self.number_que, )).fetchall()
            print(res)
            self.label_42.setText(str(res[0][0]) + '.' + str(res[0][1]))
            self.progressBar_9.setValue(self.progress)
            self.current_answer = str(res[0][6])

    def lvl(self, i):
        if i == 0:
            return 'A1'
        elif i == 1:
            return 'A2'
        elif i == 2:
            return 'B1'
        elif i == 3:
            return 'B2'
        elif i == 4:
            return 'C1'
        elif i == 5:
            return 'C2'

    def test_lvl(self):
        self.que()
        self.lvl_test = True
        self.swap_window(4)


    def test(self):
        self.que()
        self.swap_window(4)

    def back(self):
        self.stackedWidget_4.setCurrentIndex(0)


    def profil(self):
        self.swap_window(3)
        self.label_12.setText('Имя: ' + self.user_login)
        con = sqlite3.connect("reg.db")
        cur = con.cursor()
        res = cur.execute("""SELECT * FROM regis where Name = ?""", (self.user_login, )).fetchall()
        print(res)
        self.label_9.setText('Уровень знания языка: ' + self.lvl(res[0][2]))
        self.progressBar.setValue(int(res[0][3]))
        self.progressBar_2.setValue(int(res[0][4]))
        self.progressBar_6.setValue(int(res[0][5]))
        self.progressBar_7.setValue(int(res[0][6]))
        self.progressBar_8.setValue(int(res[0][7]))  

    def rasdel(self, btn):
        self.stackedWidget_4.setCurrentIndex(1)
        self.label_75.setText(btn.text())
        self.razdel = btn.text()
        

    def log_in(self):
        con = sqlite3.connect("reg.db")
        cur = con.cursor()
        res_name = cur.execute("""SELECT Name FROM regis""").fetchall()
        res_password = cur.execute("""SELECT password FROM regis""").fetchall()
        self.a = False
        for i in range(len(res_name)):
            name = str(res_name[i])[2:-3]
            if name == self.lineEdit.text():
                self.a = True
                pas = str(res_password[i])[2:-3]
                if self.lineEdit_2.text() == pas:
                    self.swap_window(2)
                    self.user_login = name
                    self.lineEdit.clear()
                    self.lineEdit_2.clear()
                else:
                    self.message = QMessageBox(self)
                    self.message.setText("Неверный пароль!")
                    self.message.setWindowTitle("Error")
                    self.message.exec()
                    self.lineEdit_2.clear()
        if not self.a:
            self.message = QMessageBox(self)
            self.message.setText("Неверный логин!")
            self.message.setWindowTitle("Error")
            self.message.exec()
            self.lineEdit.clear()
            self.lineEdit_2.clear()  

    def swap_window(self, index):
        self.stackedWidget.setCurrentIndex(index)

    def check_ban(self, text):
        for i in range(len(text)):
            if text[i] in Banned:
                return False
        return True

    def check_ban1(self, text):
        for i in range(len(text)):
            if text[i] in Banned1:
                return False
        return True

    def check_ban2(self, text):
        for i in range(len(text)):
            if text[i] in Saved:
                return False
        return True
        
    def register(self):
        if self.check():
            con = sqlite3.connect("reg.db")
            cur = con.cursor()
            cur.execute("""INSERT INTO regis VALUES(?,?)""",(self.lineEdit_3.text(),self.lineEdit_4.text()))
            con.commit()
            con.close()
            self.message = QMessageBox(self)
            self.message.setText("Вы успешно зарегестрировались!")
            self.message.setWindowTitle("Регистрация")
            self.message.exec()
            self.lineEdit_3.clear()
            self.lineEdit_4.clear()
            self.lineEdit_5.clear()
            self.swap_window(0)

    def check(self):
        con = sqlite3.connect("reg.db")
        cur = con.cursor()
        res_name = cur.execute("""SELECT Name FROM regis""").fetchall()
        name = self.lineEdit_3.text()
        password = self.lineEdit_4.text()
        rep_password = self.lineEdit_5.text()
        x = []
        for i in range(len(res_name)):
            x.append(res_name[i][0])
        print(x)
        if not self.check_ban(name):
            self.message = QMessageBox(self)
            self.message.setText("ФИО может содержать только буквы.\n Провертье корректно ли введены данные!")
            self.message.setWindowTitle("Error")
            self.message.exec()
        elif x.count(name) >= 1:
            self.message = QMessageBox(self)
            self.message.setText("Такой ник уже есть")
            self.message.setWindowTitle("Error")
            self.message.exec()
        elif not self.check_ban1(password) or not self.check_ban1(rep_password):
            self.message = QMessageBox(self)
            self.message.setText("Пароль содержит запрещенные символы. Такие как ( ; } { > < ? /...) \n Провертье корректно ли введены данные!")
            self.message.setWindowTitle("Error")
            self.message.exec()
        elif self.check_ban2(password) or self.check_ban2(rep_password):
            self.message = QMessageBox(self)
            self.message.setText("Пароль должен содержать буквы латинского алфавита!")
            self.message.setWindowTitle("Error")
            self.message.exec()
        elif name == '' or password == '':
            self.message = QMessageBox(self)
            self.message.setText("Заполните все окна!")
            self.message.setWindowTitle("Error")
            self.message.exec()
            return False
        elif password != rep_password:
            self.message = QMessageBox(self)
            self.message.setText("Пароли не совпадают \n будте внимательнее!\n XP")
            self.message.setWindowTitle("Error")
            self.message.exec()
            return False
        else:
            return True
            

        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
