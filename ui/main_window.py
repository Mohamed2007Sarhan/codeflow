"""
Main Window for the Code Analysis and Debugging Visualizer
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt5.QtWidgets import (
    QMainWindow, QAction, QFileDialog, QApplication, QVBoxLayout, QWidget,
    QHBoxLayout, QSplitter, QLabel, QProgressBar, QTextEdit, QPushButton,
    QDialog, QListWidget, QListWidgetItem, QCheckBox, QMessageBox, QTreeWidgetItem,
    QTreeWidget, QTabWidget, QComboBox, QGroupBox, QFormLayout, QLineEdit, QSpinBox,
    QInputDialog, QButtonGroup, QRadioButton
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QIcon, QTextCharFormat, QColor, QFont
from analyzer.ast_analyzer import ASTAnalyzer
from analyzer.debug_engine import DebuggingEngine
from db.history_db import HistoryDatabase
from utils.export_utils import export_to_json, export_to_html
from visualization.flow_graph import FlowGraphVisualizer

class LanguageSelectionDialog(QDialog):
    """Dialog for selecting programming language"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.language = "python"
        self.compiler_path = ""
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Select Programming Language")
        self.setGeometry(200, 200, 400, 200)
        
        layout = QVBoxLayout()
        
        title = QLabel("Select Programming Language:")
        title.setStyleSheet("font-size: 14px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # Language selection
        self.python_radio = QRadioButton("Python (No compiler needed)")
        self.cpp_radio = QRadioButton("C++ (Requires g++ compiler)")
        self.java_radio = QRadioButton("Java (Requires javac compiler)")
        self.custom_radio = QRadioButton("Other Language")
        
        # Group buttons
        self.lang_group = QButtonGroup()
        self.lang_group.addButton(self.python_radio, 1)
        self.lang_group.addButton(self.cpp_radio, 2)
        self.lang_group.addButton(self.java_radio, 3)
        self.lang_group.addButton(self.custom_radio, 4)
        
        self.python_radio.setChecked(True)
        
        layout.addWidget(self.python_radio)
        layout.addWidget(self.cpp_radio)
        layout.addWidget(self.java_radio)
        layout.addWidget(self.custom_radio)
        
        # Compiler path input (hidden by default)
        self.compiler_group = QGroupBox("Compiler Path (if needed):")
        self.compiler_group.setVisible(False)
        compiler_layout = QVBoxLayout()
        self.compiler_input = QLineEdit()
        self.compiler_input.setPlaceholderText("Enter full path to compiler (e.g., C:\\MinGW\\bin\\g++.exe)")
        compiler_layout.addWidget(self.compiler_input)
        self.compiler_group.setLayout(compiler_layout)
        layout.addWidget(self.compiler_group)
        
        # Connect radio buttons to show/hide compiler input
        self.cpp_radio.toggled.connect(self.toggle_compiler_input)
        self.java_radio.toggled.connect(self.toggle_compiler_input)
        self.custom_radio.toggled.connect(self.toggle_compiler_input)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.ok_btn = QPushButton("OK")
        self.ok_btn.clicked.connect(self.accept)
        button_layout.addWidget(self.ok_btn)
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
    def toggle_compiler_input(self):
        """Show or hide compiler input based on selection"""
        show_compiler = (self.cpp_radio.isChecked() or 
                        self.java_radio.isChecked() or 
                        self.custom_radio.isChecked())
        self.compiler_group.setVisible(show_compiler)
        
    def accept(self):
        """Handle OK button click"""
        if self.python_radio.isChecked():
            self.language = "python"
        elif self.cpp_radio.isChecked():
            self.language = "cpp"
        elif self.java_radio.isChecked():
            self.language = "java"
        else:
            self.language = "other"
            
        self.compiler_path = self.compiler_input.text()
        super().accept()

class OperationSelectionDialog(QDialog):
    """Dialog for selecting operations to debug"""
    
    def __init__(self, operations, parent=None):
        super().__init__(parent)
        self.operations = operations
        self.selected_operations = []
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Select Operations for Debugging")
        self.setGeometry(200, 200, 500, 400)
        
        layout = QVBoxLayout()
        
        # Instructions
        instruction_label = QLabel("Select the operations you want to debug:")
        layout.addWidget(instruction_label)
        
        # List of operations with checkboxes
        self.list_widget = QListWidget()
        for op in self.operations:
            item = QListWidgetItem()
            checkbox = QCheckBox(f"Line {op.get('line', 'N/A')} – {op.get('type', 'Unknown')} operation")
            checkbox.setChecked(True)
            item.setSizeHint(checkbox.sizeHint())
            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, checkbox)
            
        layout.addWidget(self.list_widget)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.select_all_btn = QPushButton("Select All")
        self.select_all_btn.clicked.connect(self.select_all)
        button_layout.addWidget(self.select_all_btn)
        
        self.deselect_all_btn = QPushButton("Deselect All")
        self.deselect_all_btn.clicked.connect(self.deselect_all)
        button_layout.addWidget(self.deselect_all_btn)
        
        self.run_btn = QPushButton("Run Debug on Selected Only")
        self.run_btn.clicked.connect(self.accept)
        button_layout.addWidget(self.run_btn)
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
    def select_all(self):
        """Select all operations"""
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            checkbox = self.list_widget.itemWidget(item)
            checkbox.setChecked(True)
            
    def deselect_all(self):
        """Deselect all operations"""
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            checkbox = self.list_widget.itemWidget(item)
            checkbox.setChecked(False)
            
    def accept(self):
        """Handle OK button click"""
        self.selected_operations = []
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            checkbox = self.list_widget.itemWidget(item)
            if checkbox.isChecked():
                self.selected_operations.append(self.operations[i])
        super().accept()

class LoadingModal(QDialog):
    """Modal dialog for showing loading progress"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Analyzing Code")
        self.setModal(True)
        self.setFixedSize(400, 200)
        
        layout = QVBoxLayout()
        
        self.status_label = QLabel("Analyzing your code...")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        layout.addWidget(self.progress_bar)
        
        self.step_label = QLabel("")
        self.step_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.step_label)
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        layout.addWidget(self.cancel_btn)
        
        self.setLayout(layout)
        
    def update_progress(self, message, percent):
        """Update the progress display"""
        self.step_label.setText(message)
        self.progress_bar.setValue(percent)

class ProjectFileSelector(QDialog):
    """Dialog for selecting files in a project"""
    
    def __init__(self, project_files, parent=None):
        super().__init__(parent)
        self.project_files = project_files
        self.selected_file = None
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Select Project File")
        self.setGeometry(200, 200, 400, 300)
        
        layout = QVBoxLayout()
        
        title = QLabel("Select a file to debug:")
        layout.addWidget(title)
        
        self.file_list = QListWidget()
        for file_path in self.project_files:
            file_name = os.path.basename(file_path)
            item = QListWidgetItem(file_name)
            item.setData(Qt.UserRole, file_path)
            self.file_list.addItem(item)
            
        self.file_list.itemDoubleClicked.connect(self.accept)
        layout.addWidget(self.file_list)
        
        button_layout = QHBoxLayout()
        self.ok_btn = QPushButton("OK")
        self.ok_btn.clicked.connect(self.accept)
        button_layout.addWidget(self.ok_btn)
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
    def accept(self):
        """Handle OK button click"""
        current_item = self.file_list.currentItem()
        if current_item:
            self.selected_file = current_item.data(Qt.UserRole)
        super().accept()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_file = None
        self.current_code = ""
        self.analysis_results = {}
        self.execution_steps = []
        self.variables_state = {}
        self.flow_graph = {}
        self.history_db = HistoryDatabase()
        self.debug_engine = None
        self.project_files = []  # For multi-file project support
        self.project_debug_engines = {}  # Debug engines for each file in project
        self.current_project_file = None  # Currently selected file in project
        self.current_language = "python"  # Default language
        self.compiler_path = ""  # Compiler path for non-Python languages
        
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle('CodeFlow Debugger')
        self.setGeometry(100, 100, 1200, 800)
        
        # Set window icon if images.png exists
        icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "images.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        self.set_dark_theme()
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout with splitters
        main_layout = QHBoxLayout(central_widget)
        
        # Left sidebar (History Panel)
        self.history_panel = self.create_history_panel()
        main_layout.addWidget(self.history_panel)
        
        # Center area with code viewer and bottom timeline
        center_splitter = QSplitter(Qt.Vertical)
        
        # Code viewer
        self.code_viewer = QTextEdit()
        self.code_viewer.setReadOnly(True)
        self.code_viewer.setStyleSheet("background-color: #1e1e1e; color: #ffffff; font-family: Consolas, monospace;")
        center_splitter.addWidget(self.code_viewer)
        
        # Bottom area (Execution Timeline / Debug Output)
        self.timeline_panel = self.create_timeline_panel()
        center_splitter.addWidget(self.timeline_panel)
        
        center_splitter.setSizes([500, 200])  # Set initial sizes
        main_layout.addWidget(center_splitter)
        
        # Right sidebar (Structured Panels)
        self.right_panel = self.create_right_panel()
        main_layout.addWidget(self.right_panel)
        
        # Create status bar
        self.status_bar = self.statusBar()
        self.status_bar.showMessage('Ready')
        
        # Create toolbar
        self.create_toolbar()
        
        # Initialize button states
        self.update_button_states()
        
        # Show language selection on startup
        self.select_language()
        
    def select_language(self):
        """Show language selection dialog on startup"""
        dialog = LanguageSelectionDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.current_language = dialog.language
            self.compiler_path = dialog.compiler_path
            self.status_bar.showMessage(f'Language set to: {self.current_language}')
            if self.compiler_path:
                self.status_bar.showMessage(f'Language: {self.current_language}, Compiler: {self.compiler_path}')
        else:
            self.current_language = "python"  # Default to Python
            self.status_bar.showMessage('Language set to default: Python')
        
    def set_dark_theme(self):
        """Apply a dark theme to the application"""
        dark_stylesheet = """
        QMainWindow {
            background-color: #2b2b2b;
        }
        QMenuBar {
            background-color: #3c3f41;
            color: #ffffff;
        }
        QMenuBar::item {
            background: transparent;
        }
        QMenuBar::item:selected {
            background: #4b6eaf;
        }
        QMenuBar::item:pressed {
            background: #4b6eaf;
        }
        QMenu {
            background-color: #3c3f41;
            color: #ffffff;
        }
        QMenu::item:selected {
            background-color: #4b6eaf;
        }
        QToolBar {
            background-color: #3c3f41;
            border: none;
        }
        QPushButton {
            background-color: #4b6eaf;
            color: white;
            border: none;
            padding: 5px;
            border-radius: 3px;
        }
        QPushButton:hover {
            background-color: #5a7dc0;
        }
        QPushButton:disabled {
            background-color: #555555;
        }
        QProgressBar {
            border: 1px solid grey;
            border-radius: 3px;
            text-align: center;
        }
        QProgressBar::chunk {
            background-color: #4b6eaf;
        }
        QTextEdit {
            background-color: #1e1e1e;
            color: #ffffff;
            selection-background-color: #4b6eaf;
        }
        QListView, QTreeView {
            background-color: #2b2b2b;
            color: #ffffff;
            alternate-background-color: #323232;
        }
        QListView::item:selected, QTreeView::item:selected {
            background-color: #4b6eaf;
        }
        QLabel {
            color: #ffffff;
        }
        QDialog {
            background-color: #2b2b2b;
        }
        QCheckBox {
            color: #ffffff;
        }
        QGroupBox {
            border: 1px solid #555555;
            margin-top: 1ex;
            color: #ffffff;
        }
        QGroupBox::title {
            subline: 0px 0px 0px 0px;
        }
        QRadioButton {
            color: #ffffff;
        }
        QLineEdit {
            background-color: #1e1e1e;
            color: #ffffff;
            border: 1px solid #555555;
            padding: 3px;
        }
        """
        self.setStyleSheet(dark_stylesheet)
        
    def create_menu_bar(self):
        """Create the menu bar with File, Open, Run, etc."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('File')
        
        open_action = QAction('Open File', self)
        open_action.setShortcut('Ctrl+O')
        open_action.setStatusTip('Open a file')
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
        open_project_action = QAction('Open Project', self)
        open_project_action.setStatusTip('Open a project folder')
        open_project_action.triggered.connect(self.open_project)
        file_menu.addAction(open_project_action)
        
        language_action = QAction('Select Language', self)
        language_action.setStatusTip('Select programming language')
        language_action.triggered.connect(self.select_language)
        file_menu.addAction(language_action)
        
        save_action = QAction('Save', self)
        save_action.setShortcut('Ctrl+S')
        save_action.setStatusTip('Save current session')
        save_action.triggered.connect(self.save_session)
        file_menu.addAction(save_action)
        
        export_menu = file_menu.addMenu('Export')
        
        export_json_action = QAction('Export to JSON', self)
        export_json_action.setStatusTip('Export session to JSON')
        export_json_action.triggered.connect(self.export_to_json)
        export_menu.addAction(export_json_action)
        
        export_html_action = QAction('Export to HTML', self)
        export_html_action.setStatusTip('Export session to HTML')
        export_html_action.triggered.connect(self.export_to_html)
        export_menu.addAction(export_html_action)
        
        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
    def create_toolbar(self):
        """Create the toolbar with main actions"""
        toolbar = self.addToolBar('Main')
        
        open_action = QAction(QIcon(), 'Open File', self)
        open_action.setStatusTip('Open a file')
        open_action.triggered.connect(self.open_file)
        toolbar.addAction(open_action)
        
        open_project_action = QAction(QIcon(), 'Open Project', self)
        open_project_action.setStatusTip('Open a project folder')
        open_project_action.triggered.connect(self.open_project)
        toolbar.addAction(open_project_action)
        
        language_action = QAction(QIcon(), 'Select Language', self)
        language_action.setStatusTip('Select programming language')
        language_action.triggered.connect(self.select_language)
        toolbar.addAction(language_action)
        
        run_action = QAction(QIcon(), 'Run', self)
        run_action.setStatusTip('Run analysis')
        run_action.triggered.connect(self.run_analysis)
        toolbar.addAction(run_action)
        
        save_action = QAction(QIcon(), 'Save', self)
        save_action.setStatusTip('Save current session')
        save_action.triggered.connect(self.save_session)
        toolbar.addAction(save_action)
        
    def create_history_panel(self):
        """Create the left sidebar (History Panel)"""
        history_widget = QWidget()
        layout = QVBoxLayout(history_widget)
        
        title = QLabel('History')
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # Placeholder for history items
        self.history_list = QListWidget()
        self.history_list.setStyleSheet("background-color: #1e1e1e; color: #ffffff;")
        self.refresh_history()
        layout.addWidget(self.history_list)
        
        return history_widget
        
    def refresh_history(self):
        """Refresh the history panel with recent sessions"""
        self.history_list.clear()
        recent_sessions = self.history_db.get_recent_sessions()
        for session in recent_sessions:
            item_text = f"Session #{session['id']} - {session['filename']} - {session['timestamp']}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, session['id'])  # Store session ID
            self.history_list.addItem(item)
        
    def create_right_panel(self):
        """Create the right sidebar with structured panels"""
        right_widget = QWidget()
        layout = QVBoxLayout(right_widget)
        
        title = QLabel('Analysis Panels')
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # Create tab widget for different panels
        self.tab_widget = QTabWidget()
        
        # Variables Panel
        self.variables_panel = QTextEdit()
        self.variables_panel.setReadOnly(True)
        self.variables_panel.setStyleSheet("background-color: #1e1e1e; color: #ffffff;")
        self.tab_widget.addTab(self.variables_panel, "Variables")
        
        # Functions Panel
        self.functions_panel = QTextEdit()
        self.functions_panel.setReadOnly(True)
        self.functions_panel.setStyleSheet("background-color: #1e1e1e; color: #ffffff;")
        self.tab_widget.addTab(self.functions_panel, "Functions")
        
        # Classes Panel
        self.classes_panel = QTextEdit()
        self.classes_panel.setReadOnly(True)
        self.classes_panel.setStyleSheet("background-color: #1e1e1e; color: #ffffff;")
        self.tab_widget.addTab(self.classes_panel, "Classes")
        
        # Conditionals & Loops Panel
        self.conditionals_panel = QTextEdit()
        self.conditionals_panel.setReadOnly(True)
        self.conditionals_panel.setStyleSheet("background-color: #1e1e1e; color: #ffffff;")
        self.tab_widget.addTab(self.conditionals_panel, "Control Flow")
        
        # Debug Info Panel
        self.debug_info_panel = QTextEdit()
        self.debug_info_panel.setReadOnly(True)
        self.debug_info_panel.setStyleSheet("background-color: #1e1e1e; color: #ffffff;")
        self.tab_widget.addTab(self.debug_info_panel, "Debug Info")
        
        # Flow Graph Panel
        self.flow_graph_panel = QTextEdit()
        self.flow_graph_panel.setReadOnly(True)
        self.flow_graph_panel.setStyleSheet("background-color: #1e1e1e; color: #ffffff;")
        self.tab_widget.addTab(self.flow_graph_panel, "Flow Graph")
        
        layout.addWidget(self.tab_widget)
        return right_widget
        
    def create_timeline_panel(self):
        """Create the bottom area (Execution Timeline / Debug Output)"""
        timeline_widget = QWidget()
        layout = QVBoxLayout(timeline_widget)
        
        title = QLabel('Execution Timeline')
        title.setStyleSheet("font-size: 14px; font-weight: bold; margin: 5px;")
        layout.addWidget(title)
        
        self.timeline_display = QTextEdit()
        self.timeline_display.setReadOnly(True)
        self.timeline_display.setStyleSheet("background-color: #1e1e1e; color: #ffffff; font-family: Consolas, monospace;")
        layout.addWidget(self.timeline_display)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        self.step_forward_btn = QPushButton('Step Forward')
        self.step_forward_btn.clicked.connect(self.step_forward)
        button_layout.addWidget(self.step_forward_btn)
        
        self.step_back_btn = QPushButton('Step Back')
        self.step_back_btn.clicked.connect(self.step_back)
        button_layout.addWidget(self.step_back_btn)
        
        self.run_selected_btn = QPushButton('Run Selected')
        self.run_selected_btn.clicked.connect(self.run_selected)
        button_layout.addWidget(self.run_selected_btn)
        
        self.run_all_btn = QPushButton('Run All')
        self.run_all_btn.clicked.connect(self.run_all)
        button_layout.addWidget(self.run_all_btn)
        
        self.pause_btn = QPushButton('Pause')
        self.pause_btn.clicked.connect(self.pause_execution)
        button_layout.addWidget(self.pause_btn)
        
        self.reset_btn = QPushButton('Reset')
        self.reset_btn.clicked.connect(self.reset_debugging)
        button_layout.addWidget(self.reset_btn)
        
        # Project file selector
        self.project_file_selector = QComboBox()
        self.project_file_selector.currentIndexChanged.connect(self.on_project_file_changed)
        button_layout.addWidget(QLabel("File:"))
        button_layout.addWidget(self.project_file_selector)
        
        layout.addLayout(button_layout)
        
        return timeline_widget
        
    def open_file(self):
        """Handle opening a file"""
        # Determine file filter based on selected language
        if self.current_language == "python":
            file_filter = "Python Files (*.py);;All Files (*)"
        elif self.current_language == "cpp":
            file_filter = "C++ Files (*.cpp *.h *.hpp);;All Files (*)"
        elif self.current_language == "java":
            file_filter = "Java Files (*.java);;All Files (*)"
        else:
            file_filter = "All Files (*)"
            
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            'Open File', 
            '', 
            file_filter
        )
        
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    content = file.read()
                    self.code_viewer.setText(content)
                    self.current_file = file_path
                    self.current_code = content
                    self.project_files = [file_path]  # Single file project
                    self.current_project_file = file_path
                    self.project_file_selector.clear()
                    self.project_file_selector.addItem(os.path.basename(file_path), file_path)
                    self.project_file_selector.setCurrentIndex(0)
                self.status_bar.showMessage(f'Loaded: {file_path} [{self.current_language}]')
                self.highlight_code_lines()
                self.update_button_states()
            except Exception as e:
                self.status_bar.showMessage(f'Error loading file: {str(e)}')
                
    def open_project(self):
        """Handle opening a project folder"""
        folder_path = QFileDialog.getExistingDirectory(self, 'Open Project Folder')
        
        if folder_path:
            try:
                # Find files based on selected language
                import glob
                import os
                
                if self.current_language == "python":
                    project_files = glob.glob(os.path.join(folder_path, "**", "*.py"), recursive=True)
                elif self.current_language == "cpp":
                    project_files = glob.glob(os.path.join(folder_path, "**", "*.cpp"), recursive=True) + \
                                   glob.glob(os.path.join(folder_path, "**", "*.h"), recursive=True) + \
                                   glob.glob(os.path.join(folder_path, "**", "*.hpp"), recursive=True)
                elif self.current_language == "java":
                    project_files = glob.glob(os.path.join(folder_path, "**", "*.java"), recursive=True)
                else:
                    # For other languages, find all files
                    project_files = glob.glob(os.path.join(folder_path, "**", "*"), recursive=True)
                    # Filter out directories
                    project_files = [f for f in project_files if os.path.isfile(f)]
                
                if not project_files:
                    self.status_bar.showMessage(f'No {self.current_language} files found in the selected folder')
                    return
                    
                # Show file selector dialog
                file_selector = ProjectFileSelector(project_files, self)
                if file_selector.exec_() == QDialog.Accepted and file_selector.selected_file:
                    selected_file = file_selector.selected_file
                    
                    # Load the selected file
                    with open(selected_file, 'r') as file:
                        content = file.read()
                        self.code_viewer.setText(content)
                        self.current_file = selected_file
                        self.current_code = content
                        self.project_files = project_files
                        self.current_project_file = selected_file
                        
                    # Update project file selector
                    self.project_file_selector.clear()
                    for file_path in project_files:
                        self.project_file_selector.addItem(os.path.basename(file_path), file_path)
                    self.project_file_selector.setCurrentText(os.path.basename(selected_file))
                        
                    self.status_bar.showMessage(f'Loaded project with {len(project_files)} {self.current_language} files. Selected: {os.path.basename(selected_file)}')
                    self.highlight_code_lines()
                    self.update_button_states()
                else:
                    self.status_bar.showMessage('Project loading cancelled')
            except Exception as e:
                self.status_bar.showMessage(f'Error loading project: {str(e)}')
                
    def on_project_file_changed(self, index):
        """Handle project file selection change"""
        if index >= 0:
            selected_file = self.project_file_selector.itemData(index)
            if selected_file and os.path.exists(selected_file):
                try:
                    with open(selected_file, 'r') as file:
                        content = file.read()
                        self.code_viewer.setText(content)
                        self.current_project_file = selected_file
                        self.current_code = content
                    self.status_bar.showMessage(f'Loaded: {os.path.basename(selected_file)} [{self.current_language}]')
                    self.highlight_code_lines()
                except Exception as e:
                    self.status_bar.showMessage(f'Error loading file: {str(e)}')
                
    def highlight_code_lines(self):
        """Highlight lines in the code viewer based on execution state"""
        if not self.debug_engine:
            return
            
        # Get the current text
        code_text = self.code_viewer.toPlainText()
        self.code_viewer.clear()
        self.code_viewer.setText(code_text)
        
        # Create text formats for different states
        success_format = QTextCharFormat()
        success_format.setBackground(QColor(46, 125, 50))  # Green
        success_format.setForeground(QColor(255, 255, 255))
        
        error_format = QTextCharFormat()
        error_format.setBackground(QColor(211, 47, 47))  # Red
        error_format.setForeground(QColor(255, 255, 255))
        
        current_format = QTextCharFormat()
        current_format.setBackground(QColor(30, 136, 229))  # Blue
        current_format.setForeground(QColor(255, 255, 255))
        
        # Highlight lines based on execution state
        lines = code_text.split('\n')
        if not lines:
            return
            
        # Get execution flow for visualization
        execution_flow = self.debug_engine.get_execution_flow()
        
        for i, line in enumerate(lines):
            line_num = i + 1
            line_state = self.debug_engine.get_line_state(line_num)
            
            # Move cursor to the line
            cursor = self.code_viewer.textCursor()
            cursor.movePosition(cursor.Start)
            cursor.movePosition(cursor.Down, cursor.MoveAnchor, i)
            cursor.movePosition(cursor.EndOfLine, cursor.KeepAnchor)
            
            # Apply formatting based on state
            if self.debug_engine.execution_steps and self.debug_engine.current_step < len(self.debug_engine.execution_steps):
                if line_num == self.debug_engine.execution_steps[self.debug_engine.current_step]['line']:
                    cursor.setCharFormat(current_format)
                elif line_state['status'] == 'success':
                    cursor.setCharFormat(success_format)
                elif line_state['status'] == 'error':
                    cursor.setCharFormat(error_format)
                
    def save_session(self):
        """Handle saving the current session"""
        if not self.current_file:
            self.status_bar.showMessage('No file loaded to save')
            return
            
        try:
            session_id = self.history_db.save_session(
                os.path.basename(self.current_file),
                self.current_code,
                self.analysis_results,
                self.execution_steps,
                self.variables_state,
                self.flow_graph
            )
            self.status_bar.showMessage(f'Session saved with ID: {session_id}')
            self.refresh_history()
        except Exception as e:
            self.status_bar.showMessage(f'Error saving session: {str(e)}')
            
    def export_to_json(self):
        """Export current session to JSON"""
        if not self.current_file:
            self.status_bar.showMessage('No session to export')
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self, 
            'Export to JSON', 
            '', 
            'JSON Files (*.json)'
        )
        
        if file_path:
            try:
                export_data = {
                    'filename': os.path.basename(self.current_file),
                    'code': self.current_code,
                    'analysis_results': self.analysis_results,
                    'execution_steps': self.execution_steps,
                    'variables_state': self.variables_state,
                    'flow_graph': self.flow_graph
                }
                
                if export_to_json(export_data, file_path):
                    self.status_bar.showMessage(f'Exported to JSON: {file_path}')
                else:
                    self.status_bar.showMessage('Error exporting to JSON')
            except Exception as e:
                self.status_bar.showMessage(f'Error exporting to JSON: {str(e)}')
                
    def export_to_html(self):
        """Export current session to HTML"""
        if not self.current_file:
            self.status_bar.showMessage('No session to export')
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self, 
            'Export to HTML', 
            '', 
            'HTML Files (*.html)'
        )
        
        if file_path:
            try:
                export_data = {
                    'filename': os.path.basename(self.current_file),
                    'code': self.current_code,
                    'variables': self.analysis_results.get('variables', []),
                    'functions': self.analysis_results.get('functions', []),
                    'classes': self.analysis_results.get('classes', []),
                    'execution_steps': self.execution_steps
                }
                
                if export_to_html(export_data, file_path):
                    self.status_bar.showMessage(f'Exported to HTML: {file_path}')
                else:
                    self.status_bar.showMessage('Error exporting to HTML')
            except Exception as e:
                self.status_bar.showMessage(f'Error exporting to HTML: {str(e)}')
        
    def run_analysis(self):
        """Run the code analysis process"""
        if not self.current_code:
            self.status_bar.showMessage('No code to analyze. Please open a file first.')
            return
            
        self.show_loading_modal()
        
    def show_loading_modal(self):
        """Show the loading modal with progress"""
        self.loading_modal = LoadingModal(self)
        self.loading_modal.show()
        
        # Simulate analysis steps
        steps = [
            ("Building AST", 12),
            ("Extracting Variables", 27),
            ("Detecting Functions", 41),
            ("Collecting Classes", 55),
            ("Scanning Conditionals and Loops", 72),
            ("Generating Execution Graph", 89),
            ("Finalizing", 99),
            ("Done", 100)
        ]
        
        # Perform actual analysis
        self.perform_analysis()
        
        # Update progress
        for i, (message, percent) in enumerate(steps):
            QTimer.singleShot(i * 300, lambda m=message, p=percent: self.update_loading_progress(m, p))
            
    def update_loading_progress(self, message, percent):
        """Update the loading modal progress"""
        if hasattr(self, 'loading_modal'):
            self.loading_modal.update_progress(message, percent)
            if percent == 100:
                QTimer.singleShot(500, self.loading_modal.close)
                QTimer.singleShot(600, self.on_analysis_complete)
                
    def perform_analysis(self):
        """Perform the actual code analysis"""
        try:
            if self.current_language.lower() == "python":
                # Analyze the code
                analyzer = ASTAnalyzer(self.current_code)
                if analyzer.analyze():
                    self.analysis_results = analyzer.get_results()
            else:
                # For non-Python languages, create basic analysis results
                self.analysis_results = {
                    'variables': [],
                    'functions': [],
                    'classes': [],
                    'conditionals': [],
                    'loops': []
                }
                # In a real implementation, this would use language-specific parsers
        except Exception as e:
            print(f"Analysis error: {e}")
            
    def on_analysis_complete(self):
        """Handle completion of the analysis"""
        self.status_bar.showMessage('Analysis complete')
        
        # Update the panels with analysis results
        self.update_analysis_panels()
        
        # Show operation selection dialog only for Python
        if self.current_language.lower() == "python":
            self.show_operation_selection()
        else:
            # For non-Python languages, directly initialize debugging
            self.initialize_debugging()
        
    def update_analysis_panels(self):
        """Update the right sidebar panels with analysis results"""
        # Variables panel
        var_text = ""
        for var in self.analysis_results.get('variables', []):
            var_text += f"{var['name']} = {var['value']} (line {var['line']})\n"
        self.variables_panel.setText(var_text or "No variables found")
        
        # Functions panel
        func_text = ""
        for func in self.analysis_results.get('functions', []):
            params = ", ".join(func['params'])
            func_text += f"{func['name']}({params}) (line {func['line']})\n"
        self.functions_panel.setText(func_text or "No functions found")
        
        # Classes panel
        class_text = ""
        for cls in self.analysis_results.get('classes', []):
            methods = ", ".join(cls['methods'])
            class_text += f"{cls['name']} (line {cls['line']}) - Methods: {methods}\n"
        self.classes_panel.setText(class_text or "No classes found")
        
        # Conditionals & Loops panel
        cond_text = ""
        for cond in self.analysis_results.get('conditionals', []):
            cond_text += f"{cond['type']} (line {cond['line']}) - {cond['test']}\n"
        for loop in self.analysis_results.get('loops', []):
            cond_text += f"{loop['type']} loop (line {loop['line']})\n"
        self.conditionals_panel.setText(cond_text or "No conditionals or loops found")
        
    def show_operation_selection(self):
        """Show the operation selection dialog"""
        # Combine all operations from analysis results
        operations = []
        
        # Add variables
        for var in self.analysis_results.get('variables', []):
            operations.append({'type': 'variable assignment', 'line': var['line']})
            
        # Add functions
        for func in self.analysis_results.get('functions', []):
            operations.append({'type': 'function definition', 'line': func['line']})
            
        # Add classes
        for cls in self.analysis_results.get('classes', []):
            operations.append({'type': 'class definition', 'line': cls['line']})
            
        # Add conditionals
        for cond in self.analysis_results.get('conditionals', []):
            operations.append({'type': 'conditional', 'line': cond['line']})
            
        # Add loops
        for loop in self.analysis_results.get('loops', []):
            operations.append({'type': 'loop', 'line': loop['line']})
            
        # Sort by line number
        operations.sort(key=lambda x: x['line'])
        
        if operations:
            dialog = OperationSelectionDialog(operations, self)
            if dialog.exec_() == QDialog.Accepted:
                self.selected_operations = dialog.selected_operations
                self.status_bar.showMessage(f"Selected {len(self.selected_operations)} operations for debugging")
                self.initialize_debugging()
            else:
                self.status_bar.showMessage("Operation selection cancelled")
        else:
            self.status_bar.showMessage("No operations found to debug")
            
    def initialize_debugging(self):
        """Initialize the debugging engine"""
        try:
            # Create debug engine for the current file
            filename = os.path.basename(self.current_project_file) if self.current_project_file else "main.py"
            self.debug_engine = DebuggingEngine(self.current_code, filename, self.current_language)
            
            # Set compiler path if provided
            if self.compiler_path:
                self.debug_engine.set_compiler_path(self.compiler_path)
            
            if self.debug_engine.parse():
                self.debug_engine.initialize_execution_steps()
                self.execution_steps = self.debug_engine.execution_steps
                self.update_timeline_display()
                self.highlight_code_lines()
                self.update_debug_info_panel()
                self.generate_flow_graph()
                self.status_bar.showMessage("Debugging initialized")
                self.update_button_states()
            else:
                self.status_bar.showMessage("Failed to initialize debugging engine")
                error_info = self.debug_engine.get_error_info()
                if error_info['has_error']:
                    self.show_error_message(f"Syntax Error at line {error_info['line']}: {error_info['message']}")
        except Exception as e:
            self.status_bar.showMessage(f"Error initializing debugging: {str(e)}")
            
    def update_timeline_display(self):
        """Update the timeline display with execution steps"""
        if not self.debug_engine:
            return
            
        timeline_text = ""
        steps = self.debug_engine.get_execution_timeline()
        
        for i, step in enumerate(steps):
            # Get line state
            line_state = self.debug_engine.get_line_state(step['line'])
            
            # Add status indicator
            if i == self.debug_engine.current_step:
                marker = "→"  # Current step
                status_char = "●"
            else:
                marker = " "
                if line_state['status'] == 'success':
                    status_char = "✓"
                elif line_state['status'] == 'error':
                    status_char = "✗"
                else:
                    status_char = "○"
                    
            # Color code based on status
            if line_state['status'] == 'success':
                status_text = f"<span style='color:#4CAF50;'>{status_char}</span>"
            elif line_state['status'] == 'error':
                status_text = f"<span style='color:#F44336;'>{status_char}</span>"
            else:
                status_text = f"<span style='color:#9E9E9E;'>{status_char}</span>"
                
            timeline_text += f"{marker} Step {i+1}: {status_text} {step['description']} [{step['filename']}]\n"
            
        self.timeline_display.setHtml(timeline_text)
        
    def update_debug_info_panel(self):
        """Update the debug info panel with current debugging information"""
        if not self.debug_engine:
            return
            
        debug_info = ""
        debug_info += f"Language: {self.current_language}\n"
        debug_info += f"Current Step: {self.debug_engine.current_step + 1}/{len(self.debug_engine.get_execution_timeline())}\n"
        debug_info += f"Total Steps: {len(self.debug_engine.get_execution_timeline())}\n"
        debug_info += f"Breakpoints: {len(self.debug_engine.breakpoints)}\n"
        debug_info += f"Current File: {self.debug_engine.filename}\n"
        
        # Execution flow
        execution_flow = self.debug_engine.get_execution_flow()
        debug_info += f"\nExecution Flow: {len(execution_flow)} steps executed\n"
        if execution_flow:
            debug_info += f"Flow: {' -> '.join(map(str, execution_flow[-10:]))}"  # Show last 10 steps
            if len(execution_flow) > 10:
                debug_info += " ..."
        
        # Error information
        error_info = self.debug_engine.get_error_info()
        if error_info['has_error']:
            debug_info += f"\n\nERROR DETECTED:\n"
            debug_info += f"File: {error_info['filename']}\n"
            debug_info += f"Line: {error_info['line']}\n"
            debug_info += f"Message: {error_info['message']}\n"
        else:
            debug_info += f"\n\nNo errors detected\n"
            
        self.debug_info_panel.setText(debug_info)
        
    def generate_flow_graph(self):
        """Generate and display the execution flow graph"""
        if not self.debug_engine:
            return
            
        try:
            # Create flow graph visualizer
            visualizer = FlowGraphVisualizer()
            
            # Generate flow graph from execution steps
            steps = self.debug_engine.get_execution_timeline()
            graph = visualizer.generate_flow_graph(steps)
            
            # Get graph data
            graph_data = visualizer.get_graph_data()
            
            # Display graph information
            flow_text = f"Execution Flow Graph [{self.current_language}]:\n"
            flow_text += f"Nodes: {len(graph_data['nodes'])}\n"
            flow_text += f"Edges: {len(graph_data['edges'])}\n\n"
            
            flow_text += "Nodes:\n"
            for node in graph_data['nodes'][:10]:  # Show first 10 nodes
                flow_text += f"  {node['id']}: {node['label']}\n"
            if len(graph_data['nodes']) > 10:
                flow_text += f"  ... and {len(graph_data['nodes']) - 10} more nodes\n\n"
                
            flow_text += "Edges:\n"
            for edge in graph_data['edges'][:10]:  # Show first 10 edges
                flow_text += f"  {edge['source']} -> {edge['target']}: {edge['label']}\n"
            if len(graph_data['edges']) > 10:
                flow_text += f"  ... and {len(graph_data['edges']) - 10} more edges\n"
                
            self.flow_graph_panel.setText(flow_text)
            self.status_bar.showMessage("Flow graph generated")
        except Exception as e:
            self.flow_graph_panel.setText(f"Error generating flow graph: {str(e)}")
            
    def show_error_message(self, message):
        """Show an error message dialog"""
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle("Error")
        msg_box.setText(message)
        msg_box.exec_()
        
    def update_button_states(self):
        """Update the enabled/disabled state of buttons based on current state"""
        has_debug_engine = self.debug_engine is not None
        
        self.step_forward_btn.setEnabled(has_debug_engine)
        self.step_back_btn.setEnabled(has_debug_engine)
        self.run_all_btn.setEnabled(has_debug_engine)
        self.reset_btn.setEnabled(has_debug_engine)
        self.pause_btn.setEnabled(has_debug_engine)
        
    def step_forward(self):
        """Move one step forward in execution"""
        if not self.debug_engine:
            return
            
        self.status_bar.showMessage('Stepping forward...')
        if self.debug_engine.step_forward():
            self.update_timeline_display()
            self.highlight_code_lines()
            self.update_debug_info_panel()
            self.status_bar.showMessage('Step forward completed')
            
            # Check for errors
            if self.debug_engine.has_error():
                error_info = self.debug_engine.get_error_info()
                self.show_error_message(f"Runtime Error in {error_info['filename']} at line {error_info['line']}: {error_info['message']}")
        else:
            self.status_bar.showMessage('No more steps to execute')
        
    def step_back(self):
        """Move one step backward in execution"""
        if not self.debug_engine:
            return
            
        self.status_bar.showMessage('Stepping back...')
        if self.debug_engine.step_back():
            self.update_timeline_display()
            self.highlight_code_lines()
            self.update_debug_info_panel()
            self.status_bar.showMessage('Step back completed')
        else:
            self.status_bar.showMessage('Already at the first step')
        
    def run_selected(self):
        """Run only the selected operations"""
        if hasattr(self, 'selected_operations') and self.selected_operations:
            self.status_bar.showMessage(f'Running {len(self.selected_operations)} selected operations...')
        else:
            self.status_bar.showMessage('No operations selected')
        
    def run_all(self):
        """Run all operations"""
        if not self.debug_engine:
            return
            
        self.status_bar.showMessage('Running all operations...')
        try:
            if self.debug_engine.run_to_end():
                self.update_timeline_display()
                self.highlight_code_lines()
                self.update_debug_info_panel()
                self.status_bar.showMessage('Execution completed')
                
                # Check for errors
                if self.debug_engine.has_error():
                    error_info = self.debug_engine.get_error_info()
                    self.show_error_message(f"Runtime Error in {error_info['filename']} at line {error_info['line']}: {error_info['message']}")
            else:
                self.status_bar.showMessage('Execution failed')
        except Exception as e:
            self.status_bar.showMessage(f'Error during execution: {str(e)}')
        
    def pause_execution(self):
        """Pause the current execution"""
        self.status_bar.showMessage('Execution paused')
        # Implementation will be added later
        
    def reset_debugging(self):
        """Reset the debugging session"""
        if self.debug_engine:
            self.debug_engine.reset_execution()
            self.debug_engine.initialize_execution_steps()
            self.update_timeline_display()
            self.highlight_code_lines()
            self.update_debug_info_panel()
            self.generate_flow_graph()
            self.status_bar.showMessage('Debugging session reset')