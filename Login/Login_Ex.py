import sys
import json
import hashlib
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QLineEdit
from PyQt6.QtGui import QIcon, QAction

from Login import Ui_MainWindow   # file pyuic6 sinh ra từ Login.ui
from Home.Home_Ex import HomeWindow



class MainApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # ✅ Load danh sách user từ email.json
        self.users = self.load_users()

        # ✅ Mặc định vào trang Welcome
        self.stackedWidget.setCurrentIndex(0)

        # ===== CHUYỂN TRANG =====
        self.btn_Login.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.btn_Register.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.btn_Back.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.btn_Back_2.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.btn_Back_3.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.btn_ForgotPass.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(3))

        # ✅ Dùng nút bạn đã có sẵn
        self.btn_Register_2.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.btn_Login_3.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))

        # ===== LOGIN / REGISTER / RESET =====
        self.btn_Login_2.clicked.connect(self.login)
        self.btn_Register_4.clicked.connect(self.register)
        self.Finish_btn.clicked.connect(self.reset_password)

        # ===== ICON CHECK/✖ BÊN CẠNH EMAIL (1 action, đổi icon) =====
        self.email_status_action = QAction(self.Email_LineEdit)
        self.Email_LineEdit.addAction(self.email_status_action, QLineEdit.ActionPosition.TrailingPosition)
        self.email_status_action.setVisible(False)
        self.Email_LineEdit.textChanged.connect(self.check_email)

        # ===== NÚT ẨN/HIỆN PASSWORD TRONG LINEEDIT =====
        self.add_toggle_action(self.Password_LineEdit)
        self.add_toggle_action(self.Password_LineEdit_2)
        self.add_toggle_action(self.NewPassword_LineEdit)
        self.add_toggle_action(self.RePassword_LineEdit)

    # =================== JSON ===================

    def load_users(self):
        try:
            with open("Email.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save_users(self):
        with open("Email.json", "w", encoding="utf-8") as f:
            json.dump(self.users, f, indent=4, ensure_ascii=False)

    # =================== CHỨC NĂNG ===================

    def hash_password(self, pwd: str):
        return hashlib.sha256(pwd.encode()).hexdigest()

    # ====== CHECK EMAIL ======
    def check_email(self):
        email = self.Email_LineEdit.text().strip()

        if not email:
            self.email_status_action.setVisible(False)
            return

        exists = any(u["email"] == email for u in self.users)
        icon_path = "../images/check.png" if exists else "../images/x.png"

        self.email_status_action.setIcon(QIcon(icon_path))
        self.email_status_action.setVisible(True)

    # ====== TOGGLE PASSWORD ======
    def add_toggle_action(self, line_edit: QLineEdit):
        """Thêm icon con mắt vào QLineEdit"""
        icon_open = QIcon("../images/eye_open.png")
        icon_closed = QIcon("../images/eye_closed.png")

        action = QAction(icon_open, "", line_edit)  # ✅ fix constructor
        line_edit.addAction(action, QLineEdit.ActionPosition.TrailingPosition)
        line_edit.setEchoMode(QLineEdit.EchoMode.Password)

        def toggle():
            if line_edit.echoMode() == QLineEdit.EchoMode.Password:
                line_edit.setEchoMode(QLineEdit.EchoMode.Normal)
                action.setIcon(icon_closed)
            else:
                line_edit.setEchoMode(QLineEdit.EchoMode.Password)
                action.setIcon(icon_open)

        action.triggered.connect(toggle)

    # ====== LOGIN ======
    def login(self):
        email = self.Email_LineEdit.text().strip()
        pwd = self.Password_LineEdit.text()
        hashed_pwd = self.hash_password(pwd)

        user = next((u for u in self.users if u["email"] == email), None)
        if not user:
            QMessageBox.warning(self, "Login", "Tài khoản này chưa tồn tại!")
            return

        if user["password"] == hashed_pwd:
            QMessageBox.information(self, "Login", f"Xin chào {user['username']}!")
            # ✅ mở Home, đóng Login
            self.home = HomeWindow()
            self.home.show()
            self.close()
        else:
            QMessageBox.warning(self, "Login", "Sai mật khẩu!")

    # ====== REGISTER ======
    def register(self):
        user = self.UserName_LineEdit.text().strip()
        email = self.Email_LineEdit_2.text().strip()
        pwd = self.Password_LineEdit_2.text()

        if not user or not email or not pwd:
            QMessageBox.warning(self, "Register", "Vui lòng điền đầy đủ thông tin!")
            return

        if any(u["email"] == email for u in self.users):
            QMessageBox.warning(self, "Register", "Email này đã được đăng ký!")
            return

        new_user = {
            "username": user,
            "email": email,
            "password": self.hash_password(pwd),
            "password_plain": pwd
        }
        self.users.append(new_user)
        self.save_users()

        QMessageBox.information(self, "Register", f"Tạo tài khoản {user} thành công!")
        self.stackedWidget.setCurrentIndex(1)

    # ====== RESET PASSWORD ======
    def reset_password(self):
        email = self.Email_LineEdit.text().strip()
        new_pwd = self.NewPassword_LineEdit.text()
        re_pwd = self.RePassword_LineEdit.text()

        if not new_pwd or not re_pwd:
            QMessageBox.warning(self, "Reset Password", "Vui lòng nhập mật khẩu mới!")
            return

        if new_pwd != re_pwd:
            QMessageBox.warning(self, "Reset Password", "Mật khẩu nhập lại không khớp!")
            return

        for u in self.users:
            if u["email"] == email:
                u["password"] = self.hash_password(new_pwd)
                u["password_plain"] = new_pwd
                self.save_users()
                QMessageBox.information(self, "Reset Password", "Đổi mật khẩu thành công!")
                self.stackedWidget.setCurrentIndex(1)
                return

        QMessageBox.warning(self, "Reset Password", "Không tìm thấy email này!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())
