from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.uic import loadUi
import sys
import sqlite3
import time

class StartDB:
    def __init__(self):
        self.connect = sqlite3.connect('bank.db')
        self.connect.execute("""
            CREATE TABLE IF NOT EXISTS users(
            login VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            created VARCHAR(100),
            balance INT, 
            utilities_electricity INTEGER DEFAULT 34000,
            utilities_water INTEGER DEFAULT 34000, 
            utilities_sewer INTEGER DEFAULT 34000, 
            utilities_gas INTEGER DEFAULT 34000, 
            utilities_garbage INTEGER DEFAULT 34000
            );
        """)
        self.connect.commit()

class SignUp(QWidget):
    def __init__(self):
        super(SignUp, self).__init__()
        loadUi('signup.ui', self)
        self.hide_error()
        self.db = StartDB()
        self.signup.clicked.connect(self.register)

    def hide_error(self):
        self.error.hide()

    def show_error(self):
        self.error.show()

    def register(self):
        login = self.login.text()
        password = self.password.text()
        mail = self.mail.text()
        self.show_error()
        cursor = self.db.connect.cursor()
        try:
            cursor.execute(f"INSERT INTO users VALUES ('{login}', '{password}', '{mail}', '{time.ctime()}', 0, 34000, 34000, 34000, 34100, 34000);")
            self.error.setText("Успешно")
            self.close()
        except sqlite3.IntegrityError as s:
            print(s.args)
            if s.args == "('UNIQUE constraint failed: users.login',)":
                self.error.setText("Логин уже занят.")
            elif s.args == ('UNIQUE constraint failed: users.email',):
                self.error.setText("Почта уже занята.")
            else:
                self.error.setText("Логин занят.")
        self.db.connect.commit()

class Personal(QWidget):
    def __init__(self, login):
        super(Personal, self).__init__()
        self.login = login 
        loadUi('personal.ui', self)     
        self.username.setText(login)
        self.db = StartDB()
        cursor = self.db.connect.cursor()
        result = cursor.execute(f"SELECT balance FROM users WHERE login = '{login}';")
        self.balance.setText(f"{result.fetchall()[0][0]} KGS")
        self.make.clicked.connect(self.make_money)
        self.hide_transfer()
        self.hide_payment_buttons()
        self.hide_payment()
        self.transfer.clicked.connect(self.user_transfer)
        self.send.clicked.connect(self.user_transfer)
        self.payment.clicked.connect(self.payment_1)
        cursor.connection.commit()

    def hide_buttons(self):
        self.make.hide()
        self.transfer.hide()
        self.payment.hide()
        self.history.hide()

    def hide_transfer(self):
        self.result.hide()
        self.input_login.hide()
        self.amount.hide()
        self.send.hide()

    def show_transfer(self):
        self.input_login.show()
        self.amount.show()
        self.send.show()

    def hide_payment(self):
        self.result_2.hide()
        self.amount_2.hide()
        self.send_2.hide()

    def hide_payment_buttons(self):
        self.electricity.hide()
        self.water.hide()
        self.sewer.hide()
        self.gas.hide()
        self.garbage.hide()

    def show_payment_buttons(self):
        self.electricity.show()
        self.water.show()
        self.sewer.show()
        self.gas.show()
        self.garbage.show()    

    def show_payment(self):
        self.result_2.show()
        self.amount_2.show()
        self.send_2.show()

    def update_balance(self):
        cursor = self.db.connect.cursor()
        result = cursor.execute(f"SELECT balance FROM users WHERE login = '{self.login}';")
        self.balance.setText(f"{result.fetchall()[0][0]} KGS")
    
    def make_money(self):
        cursor = self.db.connect.cursor()
        cursor.execute(f"UPDATE users SET balance = balance + {10} WHERE login = '{self.login}';")
        self.db.connect.commit()
        self.update_balance()

    def user_transfer(self):
        self.show_transfer()
        self.result.hide()
        input_login = self.input_login.text()
        amount = self.amount.text()
        cursor = self.db.connect.cursor()
        cursor.execute(f"SELECT login FROM users WHERE login = '{input_login}';")
        result = cursor.fetchall()
        if result != []:
            cursor.execute(f"SELECT balance FROM users WHERE login = '{self.login}';")
            users_balance = cursor.fetchall()[0][0]
            print(users_balance)
            if users_balance >= int(amount):
                cursor.execute(f"UPDATE users SET balance = balance - {amount} WHERE login = '{self.login}';")
                cursor.execute(f"UPDATE users SET balance = balance + {amount} WHERE login = '{input_login}';")
                self.db.connect.commit()
                self.update_balance()
                self.result.show()
                self.result.setText("Успешно")
            else:
                self.result.show()  
                self.result.setText("Недостаточно средств.")        
        elif result  == [] and input_login and amount:
            self.result.show()
            self.result.setText("Не найден.")

    def payment_1(self):
        self.hide_transfer()
        self.show_payment_buttons()
        self.hide_buttons()
        self.electricity.clicked.connect(self.energy)
        self.water.clicked.connect(self.waters)
        self.sewer.clicked.connect(self.sewers)
        self.gas.clicked.connect(self.gass)
        self.garbage.clicked.connect(self.garbages)
        

    def energy(self):
        self.show_payment()
        self.hide_payment_buttons()
        login = self.username.text()
        self.result_2.hide()
        amount = self.amount_2.text()
        print(amount)
        
        cursor = self.db.connect.cursor()
        cursor.execute(f"SELECT balance FROM users WHERE login = '{login}';")
        balance = cursor.fetchall()[0][0]
        if balance >= amount:
            cursor.execute(f"UPDATE users SET utilities_electricity = utilities_electricity - '{amount}' WHERE login = '{login}';")
            self.db.connect.commit()
            self.result_2.setText("Успешно оплачено")
        else:
            self.result_2.setText("Недостаточно средств.")

    def waters(self):
        self.show_payment()
        self.hide_payment_buttons()
        login = self.username.text()
        self.result_2.hide()
        amount = self.amount_2.text()
        print(amount)
        
        cursor = self.db.connect.cursor()
        cursor.execute(f"SELECT balance FROM users WHERE login = '{login}';")
        balance = cursor.fetchall()[0][0]
        if balance >= amount:
            cursor.execute(f"UPDATE users SET utilities_water = utilities_water - '{amount}' WHERE login = '{login}';")
            self.db.connect.commit()
            self.result_2.setText("Успешно оплачено")
        else:
            self.result_2.setText("Недостаточно средств.")

    def sewers(self):
        self.show_payment()
        self.hide_payment_buttons()
        login = self.username.text()
        self.result_2.hide()
        amount = self.amount_2.text()
        print(amount)
        
        cursor = self.db.connect.cursor()
        cursor.execute(f"SELECT balance FROM users WHERE login = '{login}';")
        balance = cursor.fetchall()[0][0]
        if balance >= amount:
            cursor.execute(f"UPDATE users SET utilities_sewer = utilities_sewer - '{amount}' WHERE login = '{login}';")
            self.db.connect.commit()
            self.result_2.setText("Успешно оплачено")
        else:
            self.result_2.setText("Недостаточно средств.")

    def gass(self):
        self.show_payment()
        self.hide_payment_buttons()
        login = self.username.text()
        self.result_2.hide()
        amount = self.amount_2.text()
        print(amount)
        
        cursor = self.db.connect.cursor()
        cursor.execute(f"SELECT balance FROM users WHERE login = '{login}';")
        balance = cursor.fetchall()[0][0]
        if balance >= amount:
            cursor.execute(f"UPDATE users SET utilities_gas = utilities_gas - '{amount}' WHERE login = '{login}';")
            self.db.connect.commit()
            self.result_2.setText("Успешно оплачено")
        else:
            self.result_2.setText("Недостаточно средств.")

    def garbages(self):
        self.show_payment()
        self.hide_payment_buttons()
        login = self.username.text()
        self.result_2.hide()
        amount = self.amount_2.text()
        print(amount)
        
        cursor = self.db.connect.cursor()
        cursor.execute(f"SELECT balance FROM users WHERE login = '{login}';")
        balance = cursor.fetchall()[0][0]
        if balance >= amount:
            cursor.execute(f"UPDATE users SET utilities_garbage = utilities_garbage - '{amount}' WHERE login = '{login}';")
            self.db.connect.commit()
            self.result_2.setText("Успешно оплачено")
        else:
            self.result_2.setText("Недостаточно средств.")


class Bank(QMainWindow, ):
    def __init__(self):
        super(Bank, self).__init__()
        loadUi('main.ui', self)
        self.hide_error()
        self.signin.clicked.connect(self.check_login)
        self.class_signup = SignUp()
        self.signup.clicked.connect(self.show_signup)
        self.db = StartDB()

    def show_signup(self):
        self.class_signup.show()

    def hide_error(self):
        self.error.hide()

    def show_error(self):
        self.error.show()

    def check_login(self):
        login = self.login.text()
        password = self.password.text()
        cursor = self.db.connect.cursor()
        cursor.execute(f"SELECT * FROM users WHERE login = '{login}' AND password = '{password}';")
        result = cursor.fetchall()
        if result != []:
            self.show_error()
            self.error.setText("Ok")
            self.personal = Personal(login)
            self.personal.show()
            self.close()
        else:
            self.show_error()
            self.error.setText("Неправильные данные")

app = QApplication(sys.argv)
bank = Bank()
bank.show()
app.exec_()
