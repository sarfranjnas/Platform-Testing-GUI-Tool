import sys, os, json
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication, 
    QMainWindow, 
    QTabWidget, 
    QWidget, 
    QLabel,
    QLineEdit,
    QVBoxLayout, 
    QHBoxLayout,
    QFormLayout,
    QCheckBox, 
    QGroupBox, 
    QPushButton,
    QStyle,
    QMessageBox,
    QScrollArea
)

from cpu_memory_utilization_config_2 import CpuMemoryConfig

common_enabled_style_green = "QPushButton:enabled {background-color: #60A917; border: 1px solid #0078D7;}"
common_enabled_style_red = "QPushButton:enabled {background-color: red; border: 1px solid #0078D7;}"
common_hover_style = "QPushButton:enabled:hover {background-color: #DAE8FC; border: 0.5px solid #0078D7;}"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.set_window_properties()

        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()

        self.tab_widget.addTab(self.tab1, "Tester")
        self.tab_widget.addTab(self.tab2, "Console")
        self.tab_widget.addTab(self.tab3, "About")

        self.create_tester_tab()

        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Window size: 600x600")    


    def set_window_properties(self):
        self.setWindowTitle("Gen2 Platform Validation Test Automation Framework")
        self.setWindowIcon(QIcon('KPIT_logo.ico'))

        # Get the screen geometry
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        # Define window dimensions
        window_width = 1200
        window_height = 1000

        # Ensure the window dimensions do not exceed the screen dimensions
        window_width = min(window_width, screen_width)
        window_height = min(window_height, screen_height)

        # Calculate the position to center the window horizontally and position at top
        x = (screen_width - window_width) // 2
        y = 10  # Position at top

        # Set the geometry and fixed size of the window
        self.setGeometry(x, y, window_width, window_height)
        self.setFixedSize(window_width, window_height)

        # Remove the maximize button
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)


    def resizeEvent(self, event):
        self.status_bar.showMessage(f"Window size: {self.width()}x{self.height()}")
        super().resizeEvent(event)


    def create_tester_tab(self):
        layout = QVBoxLayout()

        layout.addWidget(self.create_kpis_group())
        
        background_colors = ["#D0CEE2", "#FFFF88", "#60A917", "red"]
        label_names = ["Not Tested", "In Progress", "PASS / Configuration Done", "FAIL / Configuration Not Done"]

        layout.addWidget(self.create_test_status_group(background_colors, label_names))

        configuration_group = QGroupBox('Configuration')
        configuration_group.setStyleSheet("QGroupBox { background-color: #F5F5F5; border: 1px solid #000000; }")

        # configuration_status_layout = QHBoxLayout()
        # configuration_status_label = QLabel()
        # configuration_status_label.setFixedSize(25, 25)
        # configuration_status_label.setStyleSheet("background-color: red;")

        # configuration_status_layout.addStretch()
        # configuration_status_layout.addWidget(configuration_status_label)
        # configuration_group.setLayout(configuration_status_layout)

        configuration_layout = QHBoxLayout()        

        ecu_selection_group = QGroupBox('ECU Selection')
        ecu_selection_group.setStyleSheet("QGroupBox { background-color: #F5F5F5; border: 1px solid #000000; }")

        ecu_selection_layout = QVBoxLayout()
        ecu_selection_group.setLayout(ecu_selection_layout)        

        padas_group = QGroupBox('PADAS')
        padas_group.setStyleSheet("QGroupBox { background-color: #F5F5F5; border: 1px solid #000000; }")
        padas_group.setFixedHeight(80)

        padas_checkbox = QCheckBox('R-Car S4 (PADAS)')
        padas_layout = QVBoxLayout()
        padas_layout.setSpacing(0)
        padas_layout.addWidget(padas_checkbox)
        padas_group.setLayout(padas_layout)
        
        ecu_selection_layout.addWidget(padas_group)

        elite_group = QGroupBox('Elite')
        elite_group.setStyleSheet("QGroupBox { background-color: #F5F5F5; border: 1px solid #000000; }")
        elite_group.setFixedHeight(150)

        elite_layout = QVBoxLayout()
        elite_layout.setSpacing(0)

        RCar_checkbox = QCheckBox('R-Car S4')
        SoC0_checkbox = QCheckBox('Qualcomm SoC 0')
        SoC1_checkbox = QCheckBox('Qualcomm SoC 1')
                
        elite_layout.addWidget(RCar_checkbox)
        elite_layout.addWidget(SoC0_checkbox)
        elite_layout.addWidget(SoC1_checkbox)
        elite_group.setLayout(elite_layout)

        ecu_selection_layout.addWidget(elite_group)

        ignition_status_group = QGroupBox('Ignition Status')
        ignition_status_group.setStyleSheet("QGroupBox { background-color: #F5F5F5; border: 1px solid #000000; }")

        ignition_status_layout = QVBoxLayout()

        relay_port_layout = QFormLayout()
        relay_port_label = QLabel('Relay Serial Port')
        relay_port_input = QLineEdit()
        relay_port_unit_label = QLabel('e.g. COM1, COM4')

        input_layout = QHBoxLayout()
        input_layout.addWidget(relay_port_input)
        input_layout.addWidget(relay_port_unit_label)

        relay_port_layout.addRow(relay_port_label, input_layout)

        relay_baudrate_layout = QHBoxLayout()
        relay_baudrate_label = QLabel('Relay Baudrate')
        relay_baudrate_input = QLineEdit()
        relay_baudrate_layout.addWidget(relay_baudrate_label)
        relay_baudrate_layout.addWidget(relay_baudrate_input)

        # For IG buttons, QHBoxLayout is more suitable
        IG_button_layout = QHBoxLayout()
        IG_OFF_button = QPushButton('IG OFF')
        IG_ON_button = QPushButton('IG ON')
        IG_button_layout.addWidget(IG_OFF_button)
        IG_button_layout.addWidget(IG_ON_button)

        ignition_status_layout.addLayout(relay_port_layout)
        ignition_status_layout.addLayout(relay_baudrate_layout)
        ignition_status_layout.addLayout(IG_button_layout)
                
        ignition_status_group.setLayout(ignition_status_layout)

        ecu_selection_layout.addWidget(ignition_status_group)
        # ecu_selection_group.setLayout(ecu_selection_layout)

        configuration_layout.addWidget(ecu_selection_group)

        # Create a group box for login credentials
        login_credential_group = QGroupBox('Login Credentials')
        login_credential_group.setStyleSheet("QGroupBox { background-color: #F5F5F5; border: 1px solid #000000; }")

         # Create a vertical layout for the login credential group
        login_credential_layout = QVBoxLayout()
        login_credential_group.setLayout(login_credential_layout)

        # Create a group box for R-Car S4
        Rcar_group = QGroupBox('R-Car S4')
        Rcar_group.setStyleSheet("QGroupBox { background-color: #F5F5F5; border: 1px solid #000000; }")

        # Create a horizontal layout for the R-Car group
        Rcar_layout = QHBoxLayout()

        # Create a form layout for R-Car telnet credentials
        Rcar_telent_layout = QFormLayout()
        Rcar_IP_label = QLabel('R-Car IP Address')
        Rcar_IP_input = QLineEdit()
        Rcar_telent_layout.addRow(Rcar_IP_label, Rcar_IP_input)
        Rcar_telnet_username_label = QLabel('Telnet Username')
        Rcar_telnet_username_input = QLineEdit()
        Rcar_telent_layout.addRow(Rcar_telnet_username_label, Rcar_telnet_username_input)
        Rcar_telnet_password_label = QLabel('Telnet Password')
        Rcar_telnet_password_input = QLineEdit()
        Rcar_telnet_password_input.setEchoMode(QLineEdit.Password)  # Hide password input
        Rcar_telent_layout.addRow(Rcar_telnet_password_label, Rcar_telnet_password_input)

        # Add the telnet layout to the R-Car layout
        Rcar_layout.addLayout(Rcar_telent_layout)

        # Create a form layout for R-Car FTP credentials
        Rcar_FTP_layout = QFormLayout()
        Rcar_FTP_username_label = QLabel('FTP Username')
        Rcar_FTP_username_input = QLineEdit()
        Rcar_FTP_layout.addRow(Rcar_FTP_username_label, Rcar_FTP_username_input)
        Rcar_FTP_password_label = QLabel('FTP Password')
        Rcar_FTP_password_input = QLineEdit()
        Rcar_FTP_password_input.setEchoMode(QLineEdit.Password)  # Hide password input
        Rcar_FTP_layout.addRow(Rcar_FTP_password_label, Rcar_FTP_password_input)

        # Add the FTP layout to the R-Car layout
        Rcar_layout.addLayout(Rcar_FTP_layout)

        # Set the layout for the R-Car group
        Rcar_group.setLayout(Rcar_layout)

        # Add the R-Car group to the login credential layout
        login_credential_layout.addWidget(Rcar_group)

        # Create a group box for SoC 0
        SoC0_group = QGroupBox('SoC 0')
        SoC0_group.setStyleSheet("QGroupBox { background-color: #F5F5F5; border: 1px solid #000000; }")

        # Create a horizontal layout for the SoC 0 group
        SoC0_layout = QHBoxLayout()

        # Create a form layout for SoC 0 telnet credentials
        SoC0_telent_layout = QFormLayout()
        SoC0_IP_label = QLabel('SoC 0 IP Address')
        SoC0_IP_input = QLineEdit()
        SoC0_telent_layout.addRow(SoC0_IP_label, SoC0_IP_input)
        SoC0_telnet_username_label = QLabel('Telnet Username')
        SoC0_telnet_username_input = QLineEdit()
        SoC0_telent_layout.addRow(SoC0_telnet_username_label, SoC0_telnet_username_input)
        SoC0_telnet_password_label = QLabel('Telnet Password')
        SoC0_telnet_password_input = QLineEdit()
        SoC0_telnet_password_input.setEchoMode(QLineEdit.Password)  # Hide password input
        SoC0_telent_layout.addRow(SoC0_telnet_password_label, SoC0_telnet_password_input)

        # Add the telnet layout to the SoC 0 layout
        SoC0_layout.addLayout(SoC0_telent_layout)

        # Create a form layout for SoC 0 FTP credentials
        SoC0_FTP_layout = QFormLayout()
        SoC0_FTP_username_label = QLabel('FTP Username')
        SoC0_FTP_username_input = QLineEdit()
        SoC0_FTP_layout.addRow(SoC0_FTP_username_label, SoC0_FTP_username_input)
        SoC0_FTP_password_label = QLabel('FTP Password')
        SoC0_FTP_password_input = QLineEdit()
        SoC0_FTP_password_input.setEchoMode(QLineEdit.Password)  # Hide password input
        SoC0_FTP_layout.addRow(SoC0_FTP_password_label, SoC0_FTP_password_input)

        # Add the FTP layout to the SoC 0 layout
        SoC0_layout.addLayout(SoC0_FTP_layout)

        # Set the layout for the SoC 0 group
        SoC0_group.setLayout(SoC0_layout)

        # Add the SoC 0 group to the login credential layout
        login_credential_layout.addWidget(SoC0_group)

        # Create a group box for SoC 1
        SoC1_group = QGroupBox('SoC 1')
        SoC1_group.setStyleSheet("QGroupBox { background-color: #F5F5F5; border: 1px solid #000000; }")

        # Create a horizontal layout for the SoC 1 group
        SoC1_layout = QHBoxLayout()

        # Create a form layout for SoC 1 telnet credentials
        SoC1_telent_layout = QFormLayout()
        SoC1_IP_label = QLabel('SoC 1 IP Address')
        SoC1_IP_input = QLineEdit()
        SoC1_telent_layout.addRow(SoC1_IP_label, SoC1_IP_input)
        SoC1_telnet_username_label = QLabel('Telnet Username')
        SoC1_telnet_username_input = QLineEdit()
        SoC1_telent_layout.addRow(SoC1_telnet_username_label, SoC1_telnet_username_input)
        SoC1_telnet_password_label = QLabel('Telnet Password')
        SoC1_telnet_password_input = QLineEdit()
        SoC1_telnet_password_input.setEchoMode(QLineEdit.Password)  # Hide password input
        SoC1_telent_layout.addRow(SoC1_telnet_password_label, SoC1_telnet_password_input)

        # Add the telnet layout to the SoC 1 layout
        SoC1_layout.addLayout(SoC1_telent_layout)

        # Create a form layout for SoC 1 FTP credentials
        SoC1_FTP_layout = QFormLayout()
        SoC1_FTP_username_label = QLabel('FTP Username')
        SoC1_FTP_username_input = QLineEdit()
        SoC1_FTP_layout.addRow(SoC1_FTP_username_label, SoC1_FTP_username_input)
        SoC1_FTP_password_label = QLabel('FTP Password')
        SoC1_FTP_password_input = QLineEdit()
        SoC1_FTP_password_input.setEchoMode(QLineEdit.Password)  # Hide password input
        SoC1_FTP_layout.addRow(SoC1_FTP_password_label, SoC1_FTP_password_input)

        # Add the FTP layout to the SoC 1 layout
        SoC1_layout.addLayout(SoC1_FTP_layout)

        # Set the layout for the SoC 1 group
        SoC1_group.setLayout(SoC1_layout)

        # Add the SoC 1 group to the login credential layout
        login_credential_layout.addWidget(SoC1_group)

        # Set the layout for the login credential group
        # login_credential_group.setLayout(login_credential_layout)

        # Add the login credential group to the main layout
        configuration_layout.addWidget(login_credential_group)
        configuration_layout.addStretch()

        configuration_group.setLayout(configuration_layout)

        layout.addWidget(configuration_group)

        # Create a QWidget and set the layout
        container = QWidget()
        container.setLayout(layout)

        # Create a QScrollArea and set the container as its widget
        scroll_area = QScrollArea()
        scroll_area.setWidget(container)
        scroll_area.setWidgetResizable(True)

        # Set the scroll area as the layout for tab1
        tab1_layout = QVBoxLayout()
        tab1_layout.addWidget(scroll_area)
        self.tab1.setLayout(tab1_layout)


    def create_kpis_group(self):
        kpis_group = QGroupBox("KPIs")
        kpis_group.setStyleSheet("QGroupBox { background-color: #F5F5F5; border: 1px solid #000000; }")
        kpis_layout = QVBoxLayout()

        kpi_diag_layout = QHBoxLayout()
        kpi_widget = self.create_kpi_widget()
        diag_group = self.create_diag_group()
        kpi_diag_layout.addWidget(kpi_widget)
        kpi_diag_layout.addWidget(diag_group)

        kev_xcp_layout = QHBoxLayout()
        kev_group = self.create_kev_group()
        xcp_group = self.create_xcp_group()
        kev_xcp_layout.addWidget(kev_group)
        kev_xcp_layout.addWidget(xcp_group)

        kpis_layout.addLayout(kpi_diag_layout)
        kpis_layout.addLayout(kev_xcp_layout)

        kpis_group.setLayout(kpis_layout)
        return kpis_group

    def create_kpi_widget(self):
        kpi_widget = QWidget()
        kpi_widget.setFixedHeight(350)  
        kpi_layout = QVBoxLayout()
        kpi_layout.addWidget(self.create_kpi_row("CPU and Memory Utilization"))
        kpi_layout.addWidget(self.create_kpi_row("Heap Memory"))
        kpi_layout.addWidget(self.create_kpi_row("Startup Time"))
        kpi_layout.addWidget(self.create_kpi_row("Cyclic and Turnaround Time"))
        kpi_layout.addWidget(self.create_kpi_row("Throughput and Fault Injection"))
        kpi_layout.addWidget(self.create_kpi_row("Execution Time"))
        kpi_layout.addWidget(self.create_kpi_row("Shutdown Time"))
        # kpi_layout.setContentsMargins(0, 0, 0, 0)  
        kpi_layout.setSpacing(0)  
        kpi_widget.setLayout(kpi_layout)
        return kpi_widget

    def create_diag_group(self):
        diag_group = QGroupBox("Diag")
        diag_group.setStyleSheet("QGroupBox { border: 1px solid #000000; }")
        diag_layout = QVBoxLayout()
        diag_layout.addWidget(self.create_kpi_row("Fault Injection"))
        diag_layout.addWidget(self.create_kpi_row("Diagostic Trouble Code (DTC)"))
        diag_layout.addWidget(self.create_kpi_row("Reprogramming"))
        diag_layout.addWidget(self.create_kpi_row("Data Integrity"))
        diag_group.setLayout(diag_layout)
        return diag_group

    def create_kev_group(self):
        kev_group = QGroupBox("KEV Generation and Movement")
        kev_group.setStyleSheet("QGroupBox { border: 1px solid #000000; }")        
        kev_layout = QVBoxLayout()
        self.kev_checkboxes = []
        kev_layout.addWidget(self.create_kpi_row("Continuous KEV", checkbox_list=self.kev_checkboxes))
        kev_layout.addWidget(self.create_kpi_row("Event Trigger KEV", checkbox_list=self.kev_checkboxes))
        kev_group.setLayout(kev_layout)
        return kev_group

    def create_xcp_group(self):
        xcp_group = QGroupBox("XCP")
        xcp_group.setStyleSheet("QGroupBox { border: 1px solid #000000; }")
        xcp_group.setFixedHeight(170)  
        xcp_layout = QVBoxLayout()
        self.xcp_checkboxes = []
        xcp_layout.addWidget(self.create_kpi_row("RAM Monitor", checkbox_list=self.xcp_checkboxes))
        xcp_layout.addWidget(self.create_kpi_row("Event Trigger RAM Monitor", checkbox_list=self.xcp_checkboxes))
        xcp_layout.addWidget(self.create_kpi_row("APL Communication Layout", checkbox_list=self.xcp_checkboxes))
        xcp_layout.setSpacing(0) 
        xcp_group.setLayout(xcp_layout)
        return xcp_group
    

    def create_test_status_group(self, background_colors, label_names):
        test_status_group = QGroupBox("Test Status")
        test_status_group.setStyleSheet("QGroupBox { background-color: #F5F5F5; border: 1px solid #000000; }")
        test_status_group.setFixedHeight(80)
        test_status_layout = QHBoxLayout()

        for i in range(len(background_colors)):
            row_widget = QWidget()
            row_layout = QHBoxLayout()

            status = QLabel()
            status.setFixedSize(30, 30)
            status.setStyleSheet(f"background-color: {background_colors[i]};")

            status_label = QLabel(label_names[i])

            row_layout.addWidget(status)
            row_layout.addWidget(status_label)
            row_widget.setLayout(row_layout)

            test_status_layout.addWidget(row_widget)

        test_status_group.setLayout(test_status_layout)
        return test_status_group

 
    def create_kpi_row(self, label, checkbox_list=None):
        row_widget = QWidget()
        row_layout = QHBoxLayout()

        status_label = QLabel()
        status_label.setFixedSize(25, 25)
        status_label.setStyleSheet("background-color: #D0CEE2;")

        row_layout.addWidget(status_label)

        checkbox = QCheckBox(label)
        row_layout.addWidget(checkbox)

        edit_button = QPushButton()
        edit_button.setFixedSize(30, 30)
        edit_button.setIcon(QIcon('pencil_write_icon.png')) 
        edit_button.setIconSize(QSize(25, 25))
        edit_button.setEnabled(False)
        edit_button.clicked.connect(lambda: self.on_button_click(label, edit_button))

        folder_button = QPushButton()
        folder_button.setFixedSize(30, 30)
        folder_button.setIcon(self.style().standardIcon(QStyle.SP_DirOpenIcon))
        folder_button.setEnabled(False)
        # folder_button.clicked.connect(lambda: self.on_button_click(label))
        folder_button.clicked.connect(lambda: self.open_file_manager(r'D:\Gen 3\GUI Fil'))

        row_layout.addWidget(edit_button)
        row_layout.addWidget(folder_button)
        row_widget.setLayout(row_layout)

        checkbox.stateChanged.connect(lambda state: self.toggle_buttons(state, status_label, label, checkbox, checkbox_list, edit_button, folder_button))

        if checkbox_list is not None:
            checkbox_list.append(checkbox)

        return row_widget
    

    def toggle_buttons(self, state, status_label, label, current_checkbox, checkbox_list, edit_button, folder_button):
        enabled = state == Qt.Checked

        print(f"{label} is {enabled}")

        edit_button.setEnabled(enabled)
        folder_button.setEnabled(enabled)

        if enabled:            
            if checkbox_list is not None:
                for checkbox in checkbox_list:
                    if checkbox != current_checkbox:
                        checkbox.setEnabled(False) 

            status_label.setStyleSheet("background-color: #60A917;")

            folder_button.setStyleSheet("QPushButton:enabled {border: 1px solid #0078D7;}" + common_hover_style)          

            self.check_KPIs_config(label, edit_button)
        else:
            status_label.setStyleSheet("background-color: #D0CEE2;")
            edit_button.setStyleSheet("")
            folder_button.setStyleSheet("")
            if checkbox_list is not None:
                for checkbox in checkbox_list:
                    checkbox.setEnabled(True)


    def check_KPIs_config(self, label, edit_button):
        if label == "CPU and Memory Utilization":
            try:
                with open('cpu_memory_utilization_config.json', 'r') as f:
                    data = json.load(f)

                if (data['cpu_usage'] and 
                    data['memory_usage'] and 
                    all(data['cpu_usage_list']) and 
                    data['script_exec_time'] and 
                    data['initial_logging_delay'] and 
                    data['test_report_name']):
                    edit_button.setStyleSheet(common_enabled_style_green + common_hover_style)
                else:
                    edit_button.setStyleSheet(common_enabled_style_red + common_hover_style)
            except FileNotFoundError:
                edit_button.setStyleSheet(common_enabled_style_red + common_hover_style)
        else:     
            edit_button.setStyleSheet(common_enabled_style_red + common_hover_style)


    def on_button_click(self, label, edit_button):
        print(f"{label} edit button is clicked")
        
        try:
            if label == "CPU and Memory Utilization":
                self.setEnabled(False)
                cpu_mem = CpuMemoryConfig(self)
                cpu_mem.setModal(True)  # Set the window as modal
                cpu_mem.exec_()  # Show the modal dialog and wait for it to close
                # cpu_mem.show()  # Show the modal dialog
                self.setEnabled(True)  # Enable the main window after the modal dialog closes
                self.check_KPIs_config(label, edit_button)
        except Exception as e:
            print(f"Error: {e}")

    
    def open_file_manager(self, path):
        if os.path.exists(path):
            if os.name == 'nt': # Windows
                os.startfile(path)
            elif os.name == 'posix': # macOS or Linux
                os.system(f'open "{path}"' if sys.platform == 'darwin' else f'xdg-open "{path}"')
        else:
            QMessageBox.warning(self, "Path Not Found", f"The path '{path}' does not exist.")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
