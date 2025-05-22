import json
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QIntValidator
from PyQt5.QtWidgets import (
    QGroupBox,
    QFormLayout, 
    QLabel, 
    QLineEdit, 
    QHBoxLayout, 
    QPushButton, 
    QTextEdit, 
    QDialog
)

class CustomIntValidator(QIntValidator):
    def validate(self, input_str, pos):
        if input_str == "":
            return (QIntValidator.Intermediate, input_str, pos)
        if input_str.isdigit():
            # Check for leading zeros
            if input_str.startswith('0') and len(input_str) > 1:
                return (QIntValidator.Invalid, input_str, pos)
            value = int(input_str)
            if 0 <= value <= 100:
                return (QIntValidator.Acceptable, input_str, pos)
            else:
                return (QIntValidator.Invalid, input_str, pos)
        else:
            return (QIntValidator.Invalid, input_str, pos)
        

class LimitedTextEdit(QTextEdit):
    def __init__(self, max_length):
        super().__init__()
        self.max_length = max_length


    def keyPressEvent(self, event):
        current_text = self.toPlainText()
        if len(current_text) >= self.max_length and event.text() and event.key() != Qt.Key_Backspace:
            event.ignore()
            return
        super().keyPressEvent(event)


    def insertPlainText(self, text):
        current_text = self.toPlainText()
        if len(current_text) + len(text) > self.max_length:
            remaining_length = self.max_length - len(current_text)
            text = text[:remaining_length]
        super().insertPlainText(text)


    def insertFromMimeData(self, source):
        current_text = self.toPlainText()
        new_text = source.text()
        if len(current_text) + len(new_text) > self.max_length:
            remaining_length = self.max_length - len(current_text)
            new_text = new_text[:remaining_length]
        super().insertPlainText(new_text)


class CpuMemoryConfig(QDialog):
    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window  # Store the main window reference
        self.set_window_properties()        
        self.initUI()
    
    def done(self, result):
        print("CPU and Memory Utilization configuration window closed successfully")
        super().done(result)

    
    def set_window_properties(self):
        self.setWindowTitle('CPU and Memory Utilization Configuration')
        self.setWindowIcon(QIcon('KPIT_logo.ico'))

        # Get the geometry of the MainWindow
        main_window_x = self.main_window.x()
        main_window_y = self.main_window.y()
        main_window_width = self.main_window.width()
        main_window_height = self.main_window.height()

        # Define window dimensions
        window_width = 750
        window_height = 400

        # Calculate the position to center the window
        x = main_window_x + (main_window_width - window_width) // 2
        y = main_window_y + (main_window_height - window_height) // 2

        # Set the geometry and fixed size of the window
        self.setGeometry(x, y, window_width, window_height)
        self.setFixedSize(window_width, window_height)


    def initUI(self):
        # Main layout
        main_layout = QHBoxLayout()

        # Threshold section
        threshold_group = QGroupBox("Threshold")
        threshold_group.setStyleSheet("QGroupBox { border: 1px solid #000000; }")
        threshold_layout = QFormLayout()
        threshold_layout.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)

        # CPU Usage
        cpu_usage_label = QLabel('CPU Usage')
        self.cpu_usage_input = QLineEdit()
        # self.cpu_usage_input.setValidator(QIntValidator(0, 100))
        self.cpu_usage_input.setValidator(CustomIntValidator(0, 100))
        cpu_usage_unit_label = QLabel('%')
        cpu_usage_layout = QHBoxLayout()
        cpu_usage_layout.addWidget(self.cpu_usage_input)
        cpu_usage_layout.addWidget(cpu_usage_unit_label)
        threshold_layout.addRow(cpu_usage_label, cpu_usage_layout)

        # Memory Usage
        memory_usage_label = QLabel('Memory Usage')
        self.memory_usage_input = QLineEdit()
        self.memory_usage_input.setValidator(CustomIntValidator(0, 100))
        memory_usage_unit_label = QLabel('%')
        memory_usage_layout = QHBoxLayout()
        memory_usage_layout.addWidget(self.memory_usage_input)
        memory_usage_layout.addWidget(memory_usage_unit_label)
        threshold_layout.addRow(memory_usage_label, memory_usage_layout)

        # CPU0 to CPU7
        self.cpu_inputs = []
        for i in range(8):
            label_text = f'CPU{i}'
            label = QLabel(label_text)
            input_field = QLineEdit()
            input_field.setValidator(CustomIntValidator(0, 100))
            unit_label = QLabel('%')
            cpu_layout = QHBoxLayout()
            cpu_layout.addWidget(input_field)
            cpu_layout.addWidget(unit_label)
            threshold_layout.addRow(label, cpu_layout)
            self.cpu_inputs.append(input_field)

        threshold_group.setLayout(threshold_layout)
        main_layout.addWidget(threshold_group)

        script_logging_report_button_layout = QFormLayout()
        script_logging_report_button_layout.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        script_exec_time_layout = QHBoxLayout()
        script_exec_time_label = QLabel('Script Execution Time')
        script_exec_time_label.setAlignment(Qt.AlignCenter)
        self.script_exec_time_input = QLineEdit()
        self.script_exec_time_input.setValidator(QIntValidator())
        self.script_exec_time_input.setFixedWidth(100)
        script_exec_time_unit_label = QLabel('sec')
        script_exec_time_layout.addWidget(script_exec_time_label)
        script_exec_time_layout.addWidget(self.script_exec_time_input)
        script_exec_time_layout.addWidget(script_exec_time_unit_label)
        script_logging_report_button_layout.addRow(script_exec_time_layout)

        # Initial Logging Delay
        initial_logging_delay_layout = QHBoxLayout()
        initial_logging_delay_label = QLabel('Initial Logging Delay')
        initial_logging_delay_label.setAlignment(Qt.AlignCenter)
        self.initial_logging_delay_input = QLineEdit()
        self.initial_logging_delay_input.setValidator(QIntValidator())
        self.initial_logging_delay_input.setFixedWidth(100)
        initial_logging_delay_unit_label = QLabel('sec')
        initial_logging_delay_layout.addWidget(initial_logging_delay_label)
        initial_logging_delay_layout.addWidget(self.initial_logging_delay_input)
        initial_logging_delay_layout.addWidget(initial_logging_delay_unit_label)
        script_logging_report_button_layout.addRow(initial_logging_delay_layout)
 
        # Test Report Name
        test_report_name_layout = QHBoxLayout()
        test_report_name_label = QLabel('Test Report Name')
        self.test_report_name_input = LimitedTextEdit(250)
        self.test_report_name_input.setFixedHeight(200)  # Adjust height to fit 250 characters
        self.test_report_name_input.setFixedWidth(250)  # Adjust width
        self.test_report_name_input.setPlaceholderText("Enter test report name here...")
        char_count_label = QLabel('0/250')
        self.test_report_name_input.textChanged.connect(lambda: char_count_label.setText(f"{len(self.test_report_name_input.toPlainText())}/250"))
        test_report_name_layout.addWidget(test_report_name_label)
        test_report_name_label.setAlignment(Qt.AlignCenter)
        test_report_name_layout.addWidget(self.test_report_name_input)
        test_report_name_layout.addWidget(char_count_label)
        script_logging_report_button_layout.addRow(test_report_name_layout)

        # Buttons
        buttons_layout = QHBoxLayout()
        self.ok_button = QPushButton('OK')
        self.ok_button.setEnabled(False)
        self.ok_button.clicked.connect(self.save_and_close)
        cancel_button = QPushButton('Cancel')
        cancel_button.clicked.connect(self.reject)
        buttons_layout.addWidget(self.ok_button)
        buttons_layout.addWidget(cancel_button)
        script_logging_report_button_layout.addRow(buttons_layout)

        main_layout.addLayout(script_logging_report_button_layout)

        self.setLayout(main_layout)        

        self.load_data()

        self.cpu_usage_input.textChanged.connect(self.check_fields)
        self.memory_usage_input.textChanged.connect(self.check_fields)
        for cpu_input in self.cpu_inputs:
            cpu_input.textChanged.connect(self.check_fields)
        self.script_exec_time_input.textChanged.connect(self.check_fields)
        self.initial_logging_delay_input.textChanged.connect(self.check_fields)
        self.test_report_name_input.textChanged.connect(self.check_fields)


    def limit_text(self, text_edit, max_length):
        current_text = text_edit.toPlainText()
        if len(current_text) > max_length:
            text_edit.setPlainText(current_text[:max_length])
        else:
            return len(current_text)
        

    def check_fields(self):
        if (self.cpu_usage_input.text() and 
            self.memory_usage_input.text() and 
            all(cpu_input.text() for cpu_input in self.cpu_inputs) and 
            self.script_exec_time_input.text() and 
            self.initial_logging_delay_input.text() and 
            self.test_report_name_input.toPlainText()):
            self.ok_button.setEnabled(True)
        else:
            self.ok_button.setEnabled(False)


    def load_data(self):
        try:
            with open('cpu_memory_utilization_config.json', 'r') as f:
                data = json.load(f)
                self.cpu_usage_input.setText(data['cpu_usage'])
                self.memory_usage_input.setText(data['memory_usage'])
                for i, cpu_input in enumerate(self.cpu_inputs):
                    cpu_input.setText(data['cpu_usage_list'][i])
                self.script_exec_time_input.setText(data['script_exec_time'])
                self.initial_logging_delay_input.setText(data['initial_logging_delay'])
                self.test_report_name_input.setPlainText(data['test_report_name'])
            self.check_fields()  # Call check_fields after loading data
        except FileNotFoundError:
            pass


    def save_and_close(self):
        data = {
            'cpu_usage': self.cpu_usage_input.text(),
            'memory_usage': self.memory_usage_input.text(),
            'cpu_usage_list': [cpu_input.text() for cpu_input in self.cpu_inputs],
            'script_exec_time': self.script_exec_time_input.text(),
            'initial_logging_delay': self.initial_logging_delay_input.text(),
            'test_report_name': self.test_report_name_input.toPlainText()
        }
        with open('cpu_memory_utilization_config.json', 'w') as f:
            json.dump(data, f, indent=4)  # Use indent=4 to write in vertical order
        self.accept()

