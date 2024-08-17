import csv

from gui import *
from PyQt6.QtWidgets import *
from account import *

class Logic(QMainWindow, Ui_MainWindow):
    def __init__(self):
        """Connects every button to respective function call"""
        super().__init__()
        self.setupUi(self)
        self.sign_in_button.clicked.connect(lambda: self.log_on())
        self.forgot_password_link.clicked.connect(lambda: (self.stackedWidget.setCurrentIndex(2), self.clear_all()))
        self.new_user_link.clicked.connect(lambda: (self.stackedWidget.setCurrentIndex(1), self.clear_all()))
        self.Reset_password_button.clicked.connect(lambda: self.forgot_password())
        self.open_account_button.clicked.connect(lambda: self.open())
        self.deposit_button.clicked.connect(lambda: (self.stackedWidget.setCurrentIndex(4), self.clear_all()))
        self.withdraw_button.clicked.connect(lambda: (self.stackedWidget.setCurrentIndex(5), self.clear_all()))
        self.sign_out_button.clicked.connect(lambda: (self.stackedWidget.setCurrentIndex(0), self.clear_all()))
        self.confirm_deposit_button.clicked.connect(lambda: self.deposit())
        self.confirm_withdraw_button.clicked.connect(lambda: self.withdraw())
        self.new_acc_back_button.clicked.connect(lambda: (self.stackedWidget.setCurrentIndex(0), self.clear_all()))
        self.forgot_back_button.clicked.connect(lambda: (self.stackedWidget.setCurrentIndex(0), self.clear_all()))
        self.dep_back_button.clicked.connect(lambda: (self.stackedWidget.setCurrentIndex(3), self.clear_all()))
        self.with_back_button.clicked.connect(lambda: (self.stackedWidget.setCurrentIndex(3), self.clear_all()))
        self.signin_password_text.setEchoMode(QLineEdit.EchoMode.Password)
        self.new_user_pass_text.setEchoMode(QLineEdit.EchoMode.Password)
        self.new_user_confirm_pass_text.setEchoMode(QLineEdit.EchoMode.Password)
        self.forgot_new_password_text.setEchoMode(QLineEdit.EchoMode.Password)
        self.forgot_confirm_text.setEchoMode(QLineEdit.EchoMode.Password)

    def clear_all(self):
        """Clears every text box and error label"""
        self.forgot_confirm_text.setText('')
        self.signin_username_text.setText('')
        self.signin_password_text.setText('')
        self.forgot_new_password_text.setText('')
        self.dep_amount_text.setText('')
        self.with_amount_text.setText('')
        self.forgot_username_text.setText('')
        self.new_user_username_text.setText('')
        self.new_user_pass_text.setText('')
        self.new_user_confirm_pass_text.setText('')
        self.signin_error_label.setText('')
        self.new_user_error_label.setText('')
        self.forgot_error_label.setText('')
        self.withdraw_error_label.setText('')
        self.deposit_error_label.setText('')

    def log_on(self):
        """Sets current account to information entered in login page"""
        self.signin_error_label.setText('')
        if self.signin_username_text.text() != '' and self.signin_password_text.text() != '':
            with open('accounts.csv', newline='') as accounts_login:
                reader = csv.reader(accounts_login, delimiter=',')
                exists = False
                for row in reader:
                    if row[0] == self.signin_username_text.text() and row[1] == self.signin_password_text.text():
                        exists = True
                        self.current_user: Account = Account(row[0], float(row[2]))
                        self.account_name.setText(self.current_user.get_name())
                        self.balance_amount.setText(f"${float(self.current_user.get_balance()):.2f}")
                        self.stackedWidget.setCurrentIndex(3)
                if not exists:
                    self.signin_error_label.setText('Incorrect username or password.')
        else:
            self.signin_error_label.setText('Please fill out every field.')

    def open(self):
        """Creates a new account for new users"""
        self.new_user_error_label.setText('')
        if self.new_user_username_text.text() != '' and self.new_user_pass_text.text() != '' and self.new_user_confirm_pass_text.text() != '':
            if self.new_user_confirm_pass_text.text() == self.new_user_pass_text.text():
                with open('accounts.csv', newline='') as accounts:
                    reader = csv.reader(accounts, delimiter=",")
                    for row in reader:
                        if row[0] == self.new_user_username_text.text():
                            self.new_user_error_label.setText("This account already exists")
            else:
                self.new_user_error_label.setText("Passwords do not match")

            if self.new_user_error_label.text() == "":
                with open('accounts.csv', 'a', newline='') as accounts:
                    writer = csv.writer(accounts, delimiter=",")
                    writer.writerow([self.new_user_username_text.text(), self.new_user_pass_text.text(), 0])
                    self.stackedWidget.setCurrentIndex(0)
                    self.clear_all()

        else:
            self.new_user_error_label.setText("Please fill out every field")

    def forgot_password(self):
        """Resets password for existing user"""
        self.forgot_error_label.setText('')
        if self.forgot_username_text.text() != '' and self.forgot_new_password_text.text() != '' and self.forgot_confirm_text.text() != '':
            if self.forgot_new_password_text.text() == self.forgot_confirm_text.text():
                with open('accounts.csv', newline='') as accounts:
                    reader = csv.reader(accounts, delimiter=",")
                    acc_exists = False
                    for row in reader:
                        if row[0] == self.forgot_username_text.text():
                            acc_exists = True
                            if row[1] == self.forgot_new_password_text.text():
                                self.forgot_error_label.setText("You have used this password previously,\nplease choose another.")
                    if not acc_exists:
                        self.forgot_error_label.setText("Account doesn't exist")
            else:
                self.forgot_error_label.setText("Passwords do not match")

            if self.forgot_error_label.text() == "":
                data = []
                with open('accounts.csv', newline='') as accounts_read:
                    reader = csv.reader(accounts_read, delimiter=",")
                    for row in reader:
                        if row[0] == self.forgot_username_text.text():
                            row[1] = self.forgot_new_password_text.text()
                        data.append(row)
                with open('accounts.csv', 'w', newline='') as accounts_write:
                    writer = csv.writer(accounts_write, delimiter=",")
                    writer.writerows(data)
                self.stackedWidget.setCurrentIndex(0)
                self.clear_all()

        else:
            self.forgot_error_label.setText("Please fill out every field")

    def deposit(self):
        """Deposits money into current account"""
        self.deposit_error_label.setText('')
        if self.dep_amount_text.text() != '':
            try:
                value = float(self.dep_amount_text.text())
                if value >= 0:
                    data = []
                    with open('accounts.csv', newline='') as accounts_read:
                        reader = csv.reader(accounts_read, delimiter=",")
                        for row in reader:
                            if self.account_name.text() == row[0]:
                                row[2] = float(row[2]) + value
                                self.current_user.set_balance(row[2])
                                self.balance_amount.setText(f"${float(self.current_user.get_balance()):.2f}")
                            data.append(row)
                    with open('accounts.csv', 'w', newline='') as accounts_write:
                        writer = csv.writer(accounts_write, delimiter=",")
                        writer.writerows(data)
                    self.stackedWidget.setCurrentIndex(3)
                    self.clear_all()
                else:
                    self.deposit_error_label.setText("Please enter a positive number")
            except ValueError:
                self.deposit_error_label.setText('Please enter numerical value')
        else:
            self.deposit_error_label.setText('Please enter a value.')

    def withdraw(self):
        """Withdraws money from current account"""
        self.withdraw_error_label.setText('')
        if self.with_amount_text.text() != '':
            try:
                value = float(self.with_amount_text.text())
                if value >= 0:
                    data = []
                    with open('accounts.csv', newline='') as accounts_read:
                        reader = csv.reader(accounts_read, delimiter=",")
                        for row in reader:
                            if self.account_name.text() == row[0]:
                                if float(row[2]) >= value:
                                    row[2] = float(row[2]) - value
                                    self.current_user.set_balance(row[2])
                                    self.balance_amount.setText(f"${float(self.current_user.get_balance()):.2f}")
                                else:
                                    self.withdraw_error_label.setText(f"Value is greater \nthan current balance of: ${float(self.current_user.get_balance()):.2f}")
                            data.append(row)
                    if self.withdraw_error_label.text() == '':
                        with open('accounts.csv', 'w', newline='') as accounts_write:
                            writer = csv.writer(accounts_write, delimiter=",")
                            writer.writerows(data)
                        self.stackedWidget.setCurrentIndex(3)
                        self.clear_all()
                else:
                    self.withdraw_error_label.setText("Please enter a positive number")
            except ValueError:
                self.withdraw_error_label.setText('Please enter numerical value')
        else:
            self.withdraw_error_label.setText('Please enter a value.')
