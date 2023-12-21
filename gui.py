import os
import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox, QWidget
from PyQt5.QtGui import QFont
class FSB5ExtractorGUI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("FSB5解密工具")
        self.setFixedSize(300,350)
        self.init_ui()

    def init_ui(self):
        # 创建垂直布局
        main_layout = QVBoxLayout()

        # 创建标签、输入框和按钮
        self.input_label = QLabel("<b>选择要解密的文件夹:</b>:", self)
        self.input_entry = QLineEdit(self)
        self.input_button = QPushButton("选择文件夹", self)

        self.output_label = QLabel("<b>选择文件解密后的输出文件夹:</b>", self)
        self.output_entry = QLineEdit(self)
        self.output_button = QPushButton("选择文件夹", self)
        self.extract_button = QPushButton("开始解密", self)

        # 设置字体
        font = QFont("Microsoft YaHei")
        self.input_label.setFont(font)
        self.input_entry.setFont(font)
        self.input_button.setFont(font)
        self.output_label.setFont(font)
        self.output_entry.setFont(font)
        self.output_button.setFont(font)
        self.extract_button.setFont(font)

        self.input_entry.setFixedWidth(int(self.width() ))
        self.input_button.setFixedWidth(int(self.width() ))
        self.output_entry.setFixedWidth(int(self.width() ))
        self.output_button.setFixedWidth(int(self.width() ))
        self.extract_button.setFixedWidth(int(self.width() ))

        # 将控件加入垂直布局
        main_layout.addWidget(self.input_label)
        main_layout.addWidget(self.input_entry)
        main_layout.addWidget(self.input_button)
        main_layout.addWidget(self.output_label)
        main_layout.addWidget(self.output_entry)
        main_layout.addWidget(self.output_button)
        main_layout.addWidget(self.extract_button)

        # 创建中心容器，将垂直布局加入其中
        central_widget = QWidget(self)
        central_widget.setLayout(main_layout)

        # 设置中心容器
        self.setCentralWidget(central_widget)

        # 连接按钮点击事件
        self.extract_button.clicked.connect(self.start_extraction)
        self.input_button.clicked.connect(self.select_input_directory)
        self.output_button.clicked.connect(self.select_output_directory)

    def select_input_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "选择要解密的文件夹", os.getcwd())
        if directory:
            self.input_entry.setText(directory)

    def select_output_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "选择解密后的文件夹", os.path.join(os.getcwd(), "out"))
        if directory:
            self.output_entry.setText(directory)

    def start_extraction(self):
        input_directory = self.input_entry.text()
        output_directory = self.output_entry.text()

        # 如果未选择要解密的文件夹，默认为程序的当前文件夹
        if not input_directory:
            input_directory = os.getcwd()

        # 如果未选择解密后输出的文件夹，默认为当前文件夹的“out”文件夹，如果不存在则自动创建
        if not output_directory:
            output_directory = os.path.join(os.getcwd(), "out")
            os.makedirs(output_directory, exist_ok=True)

        # 检查是否存在有效的fsb文件
        fsb_files = [f for f in os.listdir(input_directory) if f.endswith(".fsb")]

        if not fsb_files:
            QMessageBox.warning(self, "未找到有效的fsb文件", "未找到有效的fsb文件，请重新选择要解密的文件夹。", QMessageBox.Ok)
            return

        command = f"python extract.py -o {output_directory} {input_directory}"

        try:
            subprocess.run(command, shell=True, check=True)
            self.show_extraction_finished_message()
        except subprocess.CalledProcessError as e:
            QMessageBox.warning(self, "解密失败", f"解密过程中出现错误：{e}", QMessageBox.Ok)

    def show_extraction_finished_message(self):
        QMessageBox.information(self, "解密完成", "解密完成！", QMessageBox.Ok)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FSB5ExtractorGUI()
    window.show()
    sys.exit(app.exec_())
