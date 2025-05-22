import sys, os, json, re
from PyQt5.QtCore import QSize, Qt, QRegularExpression
from PyQt5.QtGui import QIcon, QIntValidator, QRegularExpressionValidator
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

from cpu_memory_utilization_config_final import CpuMemoryConfig

common_groupbox_style = """
QGroupBox {
    background-color: #F5F5F5;
    border: 1px solid #000000;
    margin-top: 10px;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top center;
    padding-left: 0px;  /* Move title to the right */
    padding-top: 0px;
}
"""

# common_groupbox_style = "QGroupBox { background-color: #F5F5F5; border: 1px solid #000000; }"
common_enabled_style = "QPushButton:enabled {background-color: #D6D6D6; border: 1.5px solid #0078D7; }"
common_enabled_style_green = "QPushButton:enabled {background-color: #60A917; border: 1.5px solid #0078D7;}"
common_enabled_style_red = "QPushButton:enabled {background-color: red; border: 1.5px solid #0078D7;}"
common_hover_style = "QPushButton:enabled:hover {background-color: #DAE8FC; border: 0.5px solid #0078D7;}"

# Create a regular expression pattern for IP address validation
ip_address_pattern = r"^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"

# Create a QRegularExpressionValidator object
ip_address_validator = QRegularExpressionValidator(QRegularExpression(ip_address_pattern))


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


    def set_window_properties(self):
        self.setWindowTitle("Gen2 Platform Validation Test Automation Framework")
        self.setWindowIcon(QIcon('KPIT_logo.ico'))

        # Get the screen geometry
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        # Define window dimensions
        window_width = 1150
        window_height = 950

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
    

    def create_tester_tab(self):
        layout = QVBoxLayout()

        layout.addWidget(self.create_kpis_group())
        
        background_colors = ["#D0CEE2", "#FFFF88", "#60A917", "red"]
        label_names = ["Not Tested", "In Progress", "PASS / Configuration Done", "FAIL / Configuration Not Done"]

        layout.addWidget(self.create_test_status_group(background_colors, label_names))

        layout.addWidget(self.create_configuration_group())

        layout.addLayout(self.create_run_button_layout())
        
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
        kpis_group.setStyleSheet(common_groupbox_style)
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
        kpi_widget.setFixedHeight(380)  

        kpi_layout = QVBoxLayout()
        kpi_layout.addWidget(self.create_kpi_row("CPU and Memory Utilization"))
        kpi_layout.addWidget(self.create_kpi_row("Heap Memory"))
        kpi_layout.addWidget(self.create_kpi_row("Startup Time"))
        kpi_layout.addWidget(self.create_kpi_row("Cyclic and Turnaround Time"))
        kpi_layout.addWidget(self.create_kpi_row("Throughput and Fault Injection"))
        kpi_layout.addWidget(self.create_kpi_row("Execution Time"))
        kpi_layout.addWidget(self.create_kpi_row("Shutdown Time"))
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

        self.kev_checkboxes = [] 

        kev_layout = QVBoxLayout()        
        kev_layout.addWidget(self.create_kpi_row("Continuous KEV", checkbox_list=self.kev_checkboxes))
        kev_layout.addWidget(self.create_kpi_row("Event Trigger KEV", checkbox_list=self.kev_checkboxes))

        kev_group.setLayout(kev_layout)
        return kev_group


    def create_xcp_group(self):
        xcp_group = QGroupBox("XCP")
        xcp_group.setStyleSheet("QGroupBox { border: 1px solid #000000; }")
        xcp_group.setFixedHeight(200)  

        self.xcp_checkboxes = []

        xcp_layout = QVBoxLayout()       
        xcp_layout.addWidget(self.create_kpi_row("RAM Monitor", checkbox_list=self.xcp_checkboxes))
        xcp_layout.addWidget(self.create_kpi_row("Event Trigger RAM Monitor", checkbox_list=self.xcp_checkboxes))
        xcp_layout.addWidget(self.create_kpi_row("APL Communication Layout", checkbox_list=self.xcp_checkboxes))
        xcp_layout.setSpacing(0) 

        xcp_group.setLayout(xcp_layout)
        return xcp_group
        
 
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
        folder_button.setStyleSheet(common_enabled_style + common_hover_style)
        folder_button.setEnabled(False)
        folder_button.clicked.connect(lambda: self.open_file_manager(r'D:\Gen 3\GUI Files'))

        row_layout.addWidget(edit_button)
        row_layout.addWidget(folder_button)

        row_widget.setLayout(row_layout)

        checkbox.stateChanged.connect(lambda state: self.toggle_buttons(state, status_label, label, checkbox, checkbox_list, edit_button, folder_button))

        if checkbox_list is not None:
            checkbox_list.append(checkbox)

        return row_widget   
    

    def create_configuration_group(self):
        configuration_group = QGroupBox('Configuration')
        configuration_group.setStyleSheet(common_groupbox_style)

        configuration_layout = self.create_configuration_layout()

        configuration_group.setLayout(configuration_layout)
        return configuration_group
    

    def create_configuration_layout(self):
        configuration_layout = QVBoxLayout()

        configuration_status_layout = self.create_configuration_status_layout()

        ecu_selection_login_credential_layout = self.create_ecu_selection_login_credential_layout()

        configuration_layout.addLayout(configuration_status_layout)
        configuration_layout.addLayout(ecu_selection_login_credential_layout)
        return configuration_layout
    

    def create_configuration_status_layout(self):
        configuration_status_layout = QHBoxLayout()

        self.configuration_status_label = QLabel()
        self.configuration_status_label.setFixedSize(30, 30)
        self.configuration_status_label.setStyleSheet("background-color: red;")

        configuration_status_layout.addStretch()
        configuration_status_layout.addWidget(self.configuration_status_label)
        return configuration_status_layout
    

    def create_ecu_selection_login_credential_layout(self):
        ecu_select_login_credential_layout = QHBoxLayout()
        
        ecu_selection_group = self.create_ecu_selection_group()
        login_credential_group = self.create_login_credential_group()
        
        ecu_select_login_credential_layout.addWidget(ecu_selection_group)
        ecu_select_login_credential_layout.addWidget(login_credential_group)
        return ecu_select_login_credential_layout
    

    def create_ecu_selection_group(self):
        ecu_selection_group = QGroupBox('ECU Selection')
        ecu_selection_group.setStyleSheet(common_groupbox_style)

        ecu_selection_layout = self.create_ecu_selection_layout()

        ecu_selection_group.setLayout(ecu_selection_layout)
        return ecu_selection_group
    

    def create_ecu_selection_layout(self):
        ecu_selection_layout = QVBoxLayout()

        padas_group = self.create_padas_group()

        elite_group = self.create_elite_group()

        ignition_status_group = self.create_ignition_status_group()

        ecu_selection_layout.addWidget(padas_group)
        ecu_selection_layout.addWidget(elite_group)
        ecu_selection_layout.addWidget(ignition_status_group)
        return ecu_selection_layout
    

    def create_padas_group(self):
        padas_group = QGroupBox('PADAS')
        padas_group.setStyleSheet(common_groupbox_style)
        padas_group.setFixedHeight(80)

        padas_layout = QVBoxLayout()

        self.padas_checkbox = QCheckBox('R-Car S4 (PADAS)')
        self.padas_checkbox.stateChanged.connect(self.update_checkbox_states)

        padas_layout.addWidget(self.padas_checkbox)

        padas_group.setLayout(padas_layout)
        return padas_group
        

    def create_elite_group(self):
        elite_group = QGroupBox('Elite')
        elite_group.setStyleSheet(common_groupbox_style)

        elite_layout = QVBoxLayout()

        self.RCar_checkbox = QCheckBox('R-Car S4')
        self.RCar_checkbox.stateChanged.connect(self.update_checkbox_states)
        self.SoC0_checkbox = QCheckBox('Qualcomm SoC0')
        self.SoC0_checkbox.stateChanged.connect(self.update_checkbox_states)
        self.SoC1_checkbox = QCheckBox('Qualcomm SoC1')
        self.SoC1_checkbox.stateChanged.connect(self.update_checkbox_states)

        elite_layout.addWidget(self.RCar_checkbox)
        elite_layout.addWidget(self.SoC0_checkbox)
        elite_layout.addWidget(self.SoC1_checkbox)

        elite_group.setLayout(elite_layout)
        return elite_group
        

    def create_ignition_status_group(self):
        ignition_status_group = QGroupBox('Ignition Status')
        ignition_status_group.setStyleSheet(common_groupbox_style)

        ignition_status_layout = QVBoxLayout()

        relay_layout = self.create_relay_layout()

        IG_button_layout = self.create_IG_button_layout()

        ignition_status_layout.addLayout(relay_layout)
        ignition_status_layout.addLayout(IG_button_layout)

        ignition_status_group.setLayout(ignition_status_layout)
        return ignition_status_group
    

    def create_relay_layout(self):
        relay_layout = QFormLayout()
        relay_layout.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)

        relay_port_label = QLabel('Relay Serial Port')

        relay_port_layout = QHBoxLayout()

        self.relay_port_input = QLineEdit()
        self.relay_port_input.setFixedWidth(80)
        self.relay_port_input.textChanged.connect(self.update_button_states)


        relay_port_unit_label = QLabel('(e.g. COM1, COM4)')
        relay_port_unit_label.setStyleSheet("font-size: 12px;")

        relay_port_layout.addWidget(self.relay_port_input)
        relay_port_layout.addWidget(relay_port_unit_label)

        relay_layout.addRow(relay_port_label, relay_port_layout)

        relay_baudrate_layout = QHBoxLayout()

        relay_baudrate_label = QLabel('Relay Baudrate')

        self.relay_baudrate_input = QLineEdit()
        self.relay_baudrate_input.setValidator(QIntValidator())
        self.relay_baudrate_input.setFixedWidth(80)
        self.relay_baudrate_input.textChanged.connect(self.update_button_states)

        relay_baudrate_unit_label = QLabel('(e.g. 9600, 115200)')
        relay_baudrate_unit_label.setStyleSheet("font-size: 12px;")
        
        relay_baudrate_layout.addWidget(self.relay_baudrate_input)
        relay_baudrate_layout.addWidget(relay_baudrate_unit_label)

        relay_layout.addRow(relay_baudrate_label, relay_baudrate_layout)
        return relay_layout
    

    def create_IG_button_layout(self):
        IG_button_layout = QHBoxLayout()

        self.IG_OFF_button = QPushButton('IG OFF')   
        self.IG_OFF_button.setFixedSize(150,35)     
        self.IG_OFF_button.setStyleSheet(common_enabled_style + common_hover_style)
        self.IG_OFF_button.clicked.connect(self.IG_ON_Off)
        self.IG_OFF_button.setEnabled(False)

        self.IG_ON_button = QPushButton('IG ON')
        self.IG_ON_button.setFixedSize(150, 35)
        self.IG_ON_button.setStyleSheet(common_enabled_style + common_hover_style)
        self.IG_ON_button.clicked.connect(self.IG_ON_Off)
        self.IG_ON_button.setEnabled(False)

        IG_button_layout.addWidget(self.IG_OFF_button)
        IG_button_layout.addWidget(self.IG_ON_button)
        return IG_button_layout
    

    def create_login_credential_group(self):
        login_credential_group = QGroupBox('Login Credentials')
        login_credential_group.setStyleSheet(common_groupbox_style)

        login_credential_layout = self.create_login_credential_layout()

        login_credential_group.setLayout(login_credential_layout)
        return login_credential_group
    

    def create_login_credential_layout(self):
        login_credential_layout = QVBoxLayout()

        Rcar_group = self.create_Rcar_group()
        SoC0_group = self.create_SoC0_group()
        SoC1_group = self.create_SoC1_group()

        login_credential_layout.addWidget(Rcar_group)
        login_credential_layout.addWidget(SoC0_group)
        login_credential_layout.addWidget(SoC1_group)
        return login_credential_layout
    

    def create_Rcar_group(self):
        Rcar_group = QGroupBox('R-Car S4')
        Rcar_group.setStyleSheet(common_groupbox_style)

        Rcar_layout = self.create_Rcar_layout()

        Rcar_group.setLayout(Rcar_layout)
        return Rcar_group
    

    def create_Rcar_layout(self):
        Rcar_layout = QHBoxLayout()

        Rcar_telent_layout = self.create_Rcar_telent_layout()

        Rcar_FTP_layout = self.create_Rcar_FTP_layout()

        Rcar_layout.addLayout(Rcar_telent_layout)
        Rcar_layout.addLayout(Rcar_FTP_layout)
        return Rcar_layout
    

    def create_Rcar_telent_layout(self):
        Rcar_telent_layout = QFormLayout()
        Rcar_telent_layout.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        self.Rcar_IP_label = QLabel('R-Car IP Address')
        self.Rcar_IP_label.setEnabled(False)
        
        self.Rcar_IP_input = QLineEdit()
        self.Rcar_IP_input.setFixedWidth(150)
        self.Rcar_IP_input.setPlaceholderText('Enter IP Address')
        self.Rcar_IP_input.setValidator(ip_address_validator)
        self.Rcar_IP_input.textChanged.connect(self.update_button_states)
        self.Rcar_IP_input.setEnabled(False)
        
        Rcar_telent_layout.addRow(self.Rcar_IP_label, self.Rcar_IP_input)
        
        self.Rcar_telnet_username_label = QLabel('Telnet Username')
        self.Rcar_telnet_username_label.setEnabled(False)
        
        self.Rcar_telnet_username_input = QLineEdit()
        self.Rcar_telnet_username_input.setFixedWidth(150)
        self.Rcar_telnet_username_input.setPlaceholderText('Enter Username')
        self.Rcar_telnet_username_input.textChanged.connect(self.update_button_states)
        self.Rcar_telnet_username_input.setEnabled(False)
        
        Rcar_telent_layout.addRow(self.Rcar_telnet_username_label, self.Rcar_telnet_username_input)
        
        self.Rcar_telnet_password_label = QLabel('Telnet Password')
        self.Rcar_telnet_password_label.setEnabled(False)
        
        self.Rcar_telnet_password_input = QLineEdit()
        self.Rcar_telnet_password_input.setFixedWidth(150)  
        self.Rcar_telnet_password_input.setPlaceholderText('Enter Password')
        self.Rcar_telnet_password_input.textChanged.connect(self.update_button_states)
        self.Rcar_telnet_password_input.setEnabled(False)
        
        Rcar_telent_layout.addRow(self.Rcar_telnet_password_label, self.Rcar_telnet_password_input)
        return Rcar_telent_layout
    

    def create_Rcar_FTP_layout(self):
        Rcar_FTP_layout = QFormLayout()
        Rcar_FTP_layout.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        self.Rcar_FTP_username_label = QLabel('FTP Username')
        self.Rcar_FTP_username_label.setEnabled(False)

        self.Rcar_FTP_username_input = QLineEdit()
        self.Rcar_FTP_username_input.setFixedWidth(150)
        self.Rcar_FTP_username_input.setPlaceholderText('Enter Username')
        self.Rcar_FTP_username_input.textChanged.connect(self.update_button_states)
        self.Rcar_FTP_username_input.setEnabled(False)

        Rcar_FTP_layout.addRow(self.Rcar_FTP_username_label, self.Rcar_FTP_username_input)

        self.Rcar_FTP_password_label = QLabel('FTP Password')
        self.Rcar_FTP_password_label.setEnabled(False)

        self.Rcar_FTP_password_input = QLineEdit()
        self.Rcar_FTP_password_input.setFixedWidth(150)
        self.Rcar_FTP_password_input.setPlaceholderText('Enter Password')
        self.Rcar_FTP_password_input.textChanged.connect(self.update_button_states)
        self.Rcar_FTP_password_input.setEnabled(False)

        Rcar_FTP_layout.addRow(self.Rcar_FTP_password_label, self.Rcar_FTP_password_input)
        return Rcar_FTP_layout
    

    def create_SoC0_group(self):
        SoC0_group = QGroupBox('SoC0')
        SoC0_group.setStyleSheet(common_groupbox_style)

        SoC0_layout = self.create_SoC0_layout()

        SoC0_group.setLayout(SoC0_layout)
        return SoC0_group
    

    def create_SoC0_layout(self):
        SoC0_layout = QHBoxLayout()

        SoC0_telent_layout = self.create_SoC0_telent_layout()

        SoC0_FTP_layout = self.create_SoC0_FTP_layout()

        SoC0_layout.addLayout(SoC0_telent_layout)
        SoC0_layout.addLayout(SoC0_FTP_layout)
        return SoC0_layout
    

    def create_SoC0_telent_layout(self):
        SoC0_telent_layout = QFormLayout()
        SoC0_telent_layout.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.SoC0_IP_label = QLabel('SoC0 IP Address')
        self.SoC0_IP_label.setEnabled(False)

        self.SoC0_IP_input = QLineEdit()
        self.SoC0_IP_input.setFixedWidth(150)
        self.SoC0_IP_input.setPlaceholderText('Enter IP Address')
        self.SoC0_IP_input.textChanged.connect(self.update_button_states)
        self.SoC0_IP_input.setEnabled(False)

        SoC0_telent_layout.addRow(self.SoC0_IP_label, self.SoC0_IP_input)

        self.SoC0_telnet_username_label = QLabel('Telnet Username')
        self.SoC0_telnet_username_label.setEnabled(False)


        self.SoC0_telnet_username_input = QLineEdit()
        self.SoC0_telnet_username_input.setFixedWidth(150)
        self.SoC0_telnet_username_input.setPlaceholderText('Enter Username')
        self.SoC0_telnet_username_input.textChanged.connect(self.update_button_states)
        self.SoC0_telnet_username_input.setEnabled(False)

        SoC0_telent_layout.addRow(self.SoC0_telnet_username_label, self.SoC0_telnet_username_input)

        self.SoC0_telnet_password_label = QLabel('Telnet Password')
        self.SoC0_telnet_password_label.setEnabled(False)

        self.SoC0_telnet_password_input = QLineEdit()
        self.SoC0_telnet_password_input.setFixedWidth(150)
        self.SoC0_telnet_password_input.setPlaceholderText('Enter Password')
        self.SoC0_telnet_password_input.textChanged.connect(self.update_button_states)
        self.SoC0_telnet_password_input.setEnabled(False)

        SoC0_telent_layout.addRow(self.SoC0_telnet_password_label, self.SoC0_telnet_password_input)
        return SoC0_telent_layout
    

    def create_SoC0_FTP_layout(self):
        SoC0_FTP_layout = QFormLayout()
        SoC0_FTP_layout.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.SoC0_FTP_username_label = QLabel('FTP Username')
        self.SoC0_FTP_username_label.setEnabled(False)

        self.SoC0_FTP_username_input = QLineEdit()
        self.SoC0_FTP_username_input.setFixedWidth(150)
        self.SoC0_FTP_username_input.setPlaceholderText('Enter Username')
        self.SoC0_FTP_username_input.textChanged.connect(self.update_button_states)
        self.SoC0_FTP_username_input.setEnabled(False)

        SoC0_FTP_layout.addRow(self.SoC0_FTP_username_label, self.SoC0_FTP_username_input)

        self.SoC0_FTP_password_label = QLabel('FTP Password')
        self.SoC0_FTP_password_label.setEnabled(False)

        self.SoC0_FTP_password_input = QLineEdit()
        self.SoC0_FTP_password_input.setFixedWidth(150) 
        self.SoC0_FTP_password_input.setPlaceholderText('Enter Password')
        self.SoC0_FTP_password_input.textChanged.connect(self.update_button_states)
        self.SoC0_FTP_password_input.setEnabled(False)

        SoC0_FTP_layout.addRow(self.SoC0_FTP_password_label, self.SoC0_FTP_password_input)
        return SoC0_FTP_layout
    

    def create_SoC1_group(self):
        SoC1_group = QGroupBox('SoC1')
        SoC1_group.setStyleSheet(common_groupbox_style)

        SoC1_layout = self.create_SoC1_layout()

        SoC1_group.setLayout(SoC1_layout)
        return SoC1_group
    

    def create_SoC1_layout(self):
        SoC1_layout = QHBoxLayout()

        SoC1_telent_layout = self.create_SoC1_telent_layout()

        SoC1_FTP_layout = self.create_SoC1_FTP_layout()

        SoC1_layout.addLayout(SoC1_telent_layout)
        SoC1_layout.addLayout(SoC1_FTP_layout)
        return SoC1_layout
    

    def create_SoC1_telent_layout(self):
        SoC1_telent_layout = QFormLayout()
        SoC1_telent_layout.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.SoC1_IP_label = QLabel('SoC1 IP Address')
        self.SoC1_IP_label.setEnabled(False)

        self.SoC1_IP_input = QLineEdit()
        self.SoC1_IP_input.setFixedWidth(150)
        self.SoC1_IP_input.setPlaceholderText('Enter IP Address')
        self.SoC1_IP_input.textChanged.connect(self.update_button_states)
        self.SoC1_IP_input.setEnabled(False)

        SoC1_telent_layout.addRow(self.SoC1_IP_label, self.SoC1_IP_input)

        self.SoC1_telnet_username_label = QLabel('Telnet Username')
        self.SoC1_telnet_username_label.setEnabled(False)

        self.SoC1_telnet_username_input = QLineEdit()
        self.SoC1_telnet_username_input.setFixedWidth(150)
        self.SoC1_telnet_username_input.setPlaceholderText('Enter Username')
        self.SoC1_telnet_username_input.textChanged.connect(self.update_button_states)
        self.SoC1_telnet_username_input.setEnabled(False)

        SoC1_telent_layout.addRow(self.SoC1_telnet_username_label, self.SoC1_telnet_username_input)

        self.SoC1_telnet_password_label = QLabel('Telnet Password')
        self.SoC1_telnet_password_label.setEnabled(False)

        self.SoC1_telnet_password_input = QLineEdit()
        self.SoC1_telnet_password_input.setFixedWidth(150)
        self.SoC1_telnet_password_input.setPlaceholderText('Enter Password')
        self.SoC1_telnet_password_input.textChanged.connect(self.update_button_states)
        self.SoC1_telnet_password_input.setEnabled(False)


        SoC1_telent_layout.addRow(self.SoC1_telnet_password_label, self.SoC1_telnet_password_input)
        return SoC1_telent_layout
    

    def create_SoC1_FTP_layout(self):
        SoC1_FTP_layout = QFormLayout()
        SoC1_FTP_layout.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.SoC1_FTP_username_label = QLabel('FTP Username')
        self.SoC1_FTP_username_label.setEnabled(False)

        self.SoC1_FTP_username_input = QLineEdit()
        self.SoC1_FTP_username_input.setFixedWidth(150)
        self.SoC1_FTP_username_input.setPlaceholderText('Enter Username')
        self.SoC1_FTP_username_input.textChanged.connect(self.update_button_states)
        self.SoC1_FTP_username_input.setEnabled(False)

        SoC1_FTP_layout.addRow(self.SoC1_FTP_username_label, self.SoC1_FTP_username_input)

        self.SoC1_FTP_password_label = QLabel('FTP Password')
        self.SoC1_FTP_password_label.setEnabled(False)

        self.SoC1_FTP_password_input = QLineEdit()
        self.SoC1_FTP_password_input.setFixedWidth(150) 
        self.SoC1_FTP_password_input.setPlaceholderText('Enter Password')
        self.SoC1_FTP_password_input.textChanged.connect(self.update_button_states)
        self.SoC1_FTP_password_input.setEnabled(False)

        SoC1_FTP_layout.addRow(self.SoC1_FTP_password_label, self.SoC1_FTP_password_input)
        return SoC1_FTP_layout


    def create_run_button_layout(self):
        run_button_layout = QHBoxLayout()

        self.run_button = QPushButton('RUN')
        self.run_button.setFixedSize(250, 50)
        self.run_button.setStyleSheet("QPushButton:enabled {font-size: 25px;} " + common_enabled_style + common_hover_style)
        self.run_button.setEnabled(True)

        run_button_layout.addStretch()
        run_button_layout.addWidget(self.run_button)
        run_button_layout.addStretch()
        return run_button_layout


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

            self.check_KPIs_config(label, edit_button)
        else:
            status_label.setStyleSheet("background-color: #D0CEE2;")

            edit_button.setStyleSheet("")

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


    def create_test_status_group(self, background_colors, label_names):
        test_status_group = QGroupBox("Test Status")
        test_status_group.setStyleSheet(common_groupbox_style)
        test_status_group.setFixedHeight(80)

        test_status_layout = QHBoxLayout()

        for i in range(len(background_colors)):
            row_widget = QWidget()

            row_layout = QHBoxLayout()

            status = QLabel()
            status.setFixedSize(40, 30)
            status.setStyleSheet(f"background-color: {background_colors[i]};")

            status_label = QLabel(label_names[i])
            status_label.setFixedHeight(30)

            row_layout.addWidget(status)
            row_layout.addWidget(status_label)

            row_widget.setLayout(row_layout)

            test_status_layout.addWidget(row_widget)

        test_status_group.setLayout(test_status_layout)
        return test_status_group    


    def update_checkbox_states(self):
        # Helper function to enable/disable a list of widgets
        def set_widgets_enabled(widgets, enabled):
            for widget in widgets:
                widget.setEnabled(enabled)

        # Define widget groups for each checkbox
        checkbox_widget_map = {
            self.RCar_checkbox: [
                self.Rcar_IP_label, self.Rcar_IP_input,
                self.Rcar_telnet_username_label, self.Rcar_telnet_username_input,
                self.Rcar_telnet_password_label, self.Rcar_telnet_password_input,
                self.Rcar_FTP_username_label, self.Rcar_FTP_username_input,
                self.Rcar_FTP_password_label, self.Rcar_FTP_password_input
            ],
            self.SoC0_checkbox: [
                self.SoC0_IP_label, self.SoC0_IP_input,
                self.SoC0_telnet_username_label, self.SoC0_telnet_username_input,
                self.SoC0_telnet_password_label, self.SoC0_telnet_password_input,
                self.SoC0_FTP_username_label, self.SoC0_FTP_username_input,
                self.SoC0_FTP_password_label, self.SoC0_FTP_password_input
            ],
            self.SoC1_checkbox: [
                self.SoC1_IP_label, self.SoC1_IP_input,
                self.SoC1_telnet_username_label, self.SoC1_telnet_username_input,
                self.SoC1_telnet_password_label, self.SoC1_telnet_password_input,
                self.SoC1_FTP_username_label, self.SoC1_FTP_username_input,
                self.SoC1_FTP_password_label, self.SoC1_FTP_password_input
            ]
        }

        # Enable/disable R-Car widgets if either PADAS or R-Car is checked
        rcar_enabled = self.padas_checkbox.isChecked() or self.RCar_checkbox.isChecked()
        set_widgets_enabled(checkbox_widget_map[self.RCar_checkbox], rcar_enabled)

        # Enable/disable SoC0 and SoC1 widgets based on their checkboxes
        for checkbox in [self.SoC0_checkbox, self.SoC1_checkbox]:
            set_widgets_enabled(checkbox_widget_map[checkbox], checkbox.isChecked())

        # Manage mutual exclusivity between PADAS and other checkboxes
        other_checkboxes = [self.RCar_checkbox, self.SoC0_checkbox, self.SoC1_checkbox]

        if self.padas_checkbox.isChecked():
            for cb in other_checkboxes:
                cb.setEnabled(False)
        elif any(cb.isChecked() for cb in other_checkboxes):
            self.padas_checkbox.setEnabled(False)
        else:
            self.padas_checkbox.setEnabled(True)
            for cb in other_checkboxes:
                cb.setEnabled(True)

        # Update related buttons
        self.update_button_states()


    def update_button_states(self):    
        if self.configuration_section_input_fields():
            print("all fields configured")
            self.IG_OFF_button.setEnabled(True)        
            self.IG_ON_button.setEnabled(True) 
            # self.run_button.setEnabled(False)
            self.configuration_status_label.setStyleSheet("background-color: #60A917;")
        else:
            self.IG_OFF_button.setEnabled(False)
            self.IG_ON_button.setEnabled(False)
            self.run_button.setEnabled(True)
            self.configuration_status_label.setStyleSheet("background-color: red;")       


    def configuration_section_input_fields(self):
        input_fields = []
        
        if self.padas_checkbox.isChecked() or self.RCar_checkbox.isChecked():
            input_fields.extend([
                self.Rcar_IP_input.text(),
                self.Rcar_telnet_username_input.text(),
                self.Rcar_telnet_password_input.text(),
                self.Rcar_FTP_username_input.text(),
                self.Rcar_FTP_password_input.text()
            ])
        
        if self.SoC0_checkbox.isChecked():
            input_fields.extend([
                self.SoC0_IP_input.text(),
                self.SoC0_telnet_username_input.text(),
                self.SoC0_telnet_password_input.text(),
                self.SoC0_FTP_username_input.text(),
                self.SoC0_FTP_password_input.text()
            ])
            
        if self.SoC1_checkbox.isChecked():
            input_fields.extend([
                self.SoC1_IP_input.text(),
                self.SoC1_telnet_username_input.text(),
                self.SoC1_telnet_password_input.text(),
                self.SoC1_FTP_username_input.text(),
                self.SoC1_FTP_password_input.text()
            ])                    
            
        if input_fields:  # Check if any of the checkboxes are checked
            input_fields.extend([
                self.relay_port_input.text(),
                self.relay_baudrate_input.text()
            ])
        
        # print("Input Fields:", input_fields)
        
        if not input_fields:  # If input_fields is empty, return False
            return False
        else:
            return all(input_fields)


    def IG_ON_Off(self):
        sender = self.sender()
        if sender == self.IG_ON_button:
            # Code to be executed when IG ON button is clicked
            print("IG ON button clicked")
        elif sender == self.IG_OFF_button:
            # Code to be executed when IG OFF button is clicked
            print("IG OFF button clicked")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
