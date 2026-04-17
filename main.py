# zenith navigator (beta 1) pt-br
# by: juu.dev  17/04/2026

import os
import sys
import random
from urllib.parse import urlparse

try:
    from PyQt6.QtCore import QUrl, Qt, QTimer
    from PyQt6.QtWidgets import (
        QApplication,
        QMainWindow,
        QLineEdit,
        QToolBar,
        QAction,
        QStatusBar,
        QMessageBox,
        QLabel,
        QDialog,
        QFormLayout,
        QPushButton,
        QVBoxLayout,
        QPlainTextEdit,
        QWidget,
        QTabWidget,
        QHBoxLayout,
        QCheckBox,
    )
    from PyQt6.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
except ImportError as exc:
    print("PyQt6 and PyQt6-WebEngine are required.")
    print("Instale com: py -m pip install PyQt6 PyQt6-WebEngine")
    raise SystemExit(exc)

STRINGS = {
    "pt-BR": {
        "app_title": "Zenith Navigator",
        "new_tab": "Nova guia",
        "close_tab": "Fechar guia",
        "home": "Homepage",
        "refresh": "Recarregar",
        "devtools": "DevTools",
        "settings": "Configurações",
        "advanced_settings": "Configurações avançadas",
        "console": "Console",
        "apps": "Apps",
        "calculator": "Calculadora",
        "snake": "Jogo da Cobrinha",
        "dino": "Jogo do Dino",
        "offline": "Modo offline",
        "installer": "Instalador",
        "language": "Idioma",
        "engine": "Mecanismo",
        "html": "HTML",
        "css": "CSS",
        "js": "JS",
        "ts": "TS",
        "php": "Legacy PHP",
        "camera": "Câmera",
        "microphone": "Microfone",
        "geolocation": "Localização",
        "notifications": "Notificações",
        "enable_console": "Habilitar console",
        "console_disabled": "O console avançado está desabilitado. Ative em Configurações.",
        "url_invalid": "URL inválida",
        "cannot_load": "Não foi possível carregar o endereço informado.",
        "load_error": "Erro ao carregar a página",
        "ready": "Pronto",
        "install_instructions": "Execute 'py installer.py' para instalar dependências e criar atalho.",
        "permissions_saved": "Permissões atualizadas.",
        "close": "Fechar",
    },
    "en-US": {
        "app_title": "Zenith Navigator",
        "new_tab": "New Tab",
        "close_tab": "Close Tab",
        "home": "Homepage",
        "refresh": "Reload",
        "devtools": "DevTools",
        "settings": "Settings",
        "advanced_settings": "Advanced Settings",
        "console": "Console",
        "apps": "Apps",
        "calculator": "Calculator",
        "snake": "Snake Game",
        "dino": "Dino Game",
        "offline": "Offline Mode",
        "installer": "Installer",
        "language": "Language",
        "engine": "Engine",
        "html": "HTML",
        "css": "CSS",
        "js": "JS",
        "ts": "TS",
        "php": "Legacy PHP",
        "camera": "Camera",
        "microphone": "Microphone",
        "geolocation": "Geolocation",
        "notifications": "Notifications",
        "enable_console": "Enable console",
        "console_disabled": "Advanced console is disabled. Enable it in Settings.",
        "url_invalid": "Invalid URL",
        "cannot_load": "Unable to load the specified address.",
        "load_error": "Page failed to load",
        "ready": "Ready",
        "install_instructions": "Run 'py installer.py' to install dependencies and create a shortcut.",
        "permissions_saved": "Permissions updated.",
        "close": "Close",
    },
}

FEATURE_LABELS = {
    QWebEnginePage.Feature.MediaAudioCapture: "microphone",
    QWebEnginePage.Feature.MediaVideoCapture: "camera",
    QWebEnginePage.Feature.Geolocation: "geolocation",
    QWebEnginePage.Feature.Notifications: "notifications",
}

LOCAL_APPS = {
    "calculator": "calc.html",
    "snake": "snake.html",
    "dino": "dino.html",
    "offline": "offline.html",
}


class ConsoleDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Console Zenith")
        self.setMinimumSize(520, 320)

        layout = QVBoxLayout(self)
        self.output = QPlainTextEdit(self)
        self.output.setReadOnly(True)
        self.input = QLineEdit(self)
        self.input.setPlaceholderText("Digite um comando e pressione Enter")
        self.input.returnPressed.connect(self.execute_command)

        layout.addWidget(self.output)
        layout.addWidget(self.input)
        self.append_line("Console iniciado. Use comandos como: help, open <url>, openapp <snake|dino|calc>, language <pt-BR|en-US>, engine <HTML|CSS|JS|TS|PHP>, tabs, permissions, reload")

    def append_line(self, text: str):
        self.output.appendPlainText(text)

    def execute_command(self):
        command_text = self.input.text().strip()
        self.input.clear()
        if not command_text:
            return

        self.append_line(f"> {command_text}")
        args = command_text.split()
        command = args[0].lower()
        browser = self.parent()

        if command == "help":
            self.append_line("Comandos: help, open <url>, openapp <snake|dino|calc>, language <pt-BR|en-US>, engine <HTML|CSS|JS|TS|PHP>, tabs, permissions, reload")
        elif command == "open" and len(args) > 1:
            browser.open_url(" ".join(args[1:]))
        elif command == "openapp" and len(args) > 1:
            browser.open_app(args[1].lower())
        elif command == "language" and len(args) > 1:
            browser.set_language(args[1])
            self.append_line(f"Idioma alterado para {args[1]}")
        elif command == "engine" and len(args) > 1:
            browser.set_engine_mode(args[1].upper())
            self.append_line(f"Engine selecionado: {args[1].upper()}")
        elif command == "tabs":
            tabs = browser.tabs.count()
            self.append_line(f"Guias abertas: {tabs}")
        elif command == "permissions":
            self.append_line(str(browser.permissions))
        elif command == "reload":
            if browser.current_view:
                browser.current_view.reload()
                self.append_line("Recarregando guia atual...")
        else:
            self.append_line("Comando não reconhecido.")


class AdvancedSettingsDialog(QDialog):
    def __init__(self, browser):
        super().__init__(browser)
        self.browser = browser
        self.setWindowTitle(browser._t("advanced_settings"))
        self.setMinimumWidth(420)

        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.console_checkbox = QCheckBox(browser._t("enable_console"))
        self.console_checkbox.setChecked(browser.console_enabled)
        self.console_checkbox.stateChanged.connect(self._update_console_button)

        self.camera_checkbox = QCheckBox(browser._t("camera"))
        self.camera_checkbox.setChecked(browser.permissions["camera"])
        self.microphone_checkbox = QCheckBox(browser._t("microphone"))
        self.microphone_checkbox.setChecked(browser.permissions["microphone"])
        self.geolocation_checkbox = QCheckBox(browser._t("geolocation"))
        self.geolocation_checkbox.setChecked(browser.permissions["geolocation"])
        self.notifications_checkbox = QCheckBox(browser._t("notifications"))
        self.notifications_checkbox.setChecked(browser.permissions["notifications"])

        form.addRow(self.console_checkbox)
        form.addRow(self.camera_checkbox)
        form.addRow(self.microphone_checkbox)
        form.addRow(self.geolocation_checkbox)
        form.addRow(self.notifications_checkbox)

        layout.addLayout(form)

        button_layout = QHBoxLayout()
        self.open_console_button = QPushButton(browser._t("console"))
        self.open_console_button.clicked.connect(browser.open_console)
        self.open_console_button.setEnabled(browser.console_enabled)
        button_layout.addWidget(self.open_console_button)

        save_button = QPushButton(browser._t("close"))
        save_button.clicked.connect(self.save)
        button_layout.addWidget(save_button)
        layout.addLayout(button_layout)

    def _update_console_button(self):
        self.open_console_button.setEnabled(self.console_checkbox.isChecked())

    def save(self):
        self.browser.console_enabled = self.console_checkbox.isChecked()
        self.browser.permissions["camera"] = self.camera_checkbox.isChecked()
        self.browser.permissions["microphone"] = self.microphone_checkbox.isChecked()
        self.browser.permissions["geolocation"] = self.geolocation_checkbox.isChecked()
        self.browser.permissions["notifications"] = self.notifications_checkbox.isChecked()
        QMessageBox.information(self, self.browser._t("settings"), self.browser._t("permissions_saved"))
        self.close()


class ZenithBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_language = "pt-BR"
        self.engine_mode = "HTML"
        self.permissions = {
            "camera": False,
            "microphone": False,
            "geolocation": False,
            "notifications": False,
        }
        self.console_enabled = False
        self.tab_data = {}
        self.devtools_window = None

        self.setWindowTitle(self._t("app_title"))
        self.setMinimumSize(1024, 700)
        self.setWindowOpacity(0.98)

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self._switch_tab)
        self.setCentralWidget(self.tabs)

        self._create_navigation_bar()
        self._create_menu_bar()
        self._create_status_bar()
        self._set_translucent_style()

        self._load_default_tab()
        self._start_metric_updates()

    def _t(self, key: str) -> str:
        return STRINGS.get(self.current_language, STRINGS["pt-BR"]).get(key, key)

    def _create_navigation_bar(self):
        self.toolbar = QToolBar(self._t("apps"))
        self.toolbar.setMovable(False)
        self.toolbar.setStyleSheet("QToolBar { background: rgba(8, 15, 31, 0.85); border: none; padding: 6px; }")
        self.addToolBar(self.toolbar)

        self.new_tab_action = QAction("＋", self)
        self.new_tab_action.setStatusTip(self._t("new_tab"))
        self.new_tab_action.triggered.connect(self._load_new_tab)
        self.toolbar.addAction(self.new_tab_action)

        self.close_tab_action = QAction("✕", self)
        self.close_tab_action.setStatusTip(self._t("close_tab"))
        self.close_tab_action.triggered.connect(self._close_current_tab)
        self.toolbar.addAction(self.close_tab_action)

        self.back_action = QAction("◀", self)
        self.back_action.setStatusTip(self._t("home"))
        self.back_action.triggered.connect(self._navigate_back)
        self.toolbar.addAction(self.back_action)

        self.forward_action = QAction("▶", self)
        self.forward_action.setStatusTip(self._t("home"))
        self.forward_action.triggered.connect(self._navigate_forward)
        self.toolbar.addAction(self.forward_action)

        self.home_action = QAction("🏠", self)
        self.home_action.setStatusTip(self._t("home"))
        self.home_action.triggered.connect(self.open_home_page)
        self.toolbar.addAction(self.home_action)

        self.url_bar = QLineEdit(self)
        self.url_bar.returnPressed.connect(self._load_url_from_bar)
        self.url_bar.setPlaceholderText("Digite um endereço ou URL e pressione Enter")
        self.toolbar.addWidget(self.url_bar)

        self.devtools_action = QAction(self._t("devtools"), self)
        self.devtools_action.setStatusTip(self._t("devtools"))
        self.devtools_action.triggered.connect(self.toggle_devtools)
        self.toolbar.addAction(self.devtools_action)

    def _create_menu_bar(self):
        self.menuBar().clear()
        menu = self.menuBar()
        menu.setStyleSheet("QMenuBar { background: rgba(8, 15, 31, 0.88); color: #eef2ff; } QMenu { background: #111827; color: #f8fafc; }")

        file_menu = menu.addMenu(self._t("app_title"))
        file_menu.addAction(self._t("new_tab"), self._load_new_tab)
        file_menu.addAction(self._t("close_tab"), self._close_current_tab)
        file_menu.addSeparator()
        file_menu.addAction(self._t("home"), self.open_home_page)
        file_menu.addAction(self._t("installer"), self.open_installer)
        file_menu.addSeparator()
        file_menu.addAction(self._t("settings"), self.open_settings)
        file_menu.addAction(self._t("close"), self.close)

        view_menu = menu.addMenu(self._t("refresh"))
        view_menu.addAction(self._t("refresh"), self._reload_current_tab)
        view_menu.addAction(self._t("devtools"), self.toggle_devtools)

        engine_menu = view_menu.addMenu(self._t("engine"))
        engine_menu.addAction(self._t("html"), lambda: self.set_engine_mode("HTML"))
        engine_menu.addAction(self._t("css"), lambda: self.set_engine_mode("CSS"))
        engine_menu.addAction(self._t("js"), lambda: self.set_engine_mode("JS"))
        engine_menu.addAction(self._t("ts"), lambda: self.set_engine_mode("TS"))
        engine_menu.addAction(self._t("php"), lambda: self.set_engine_mode("PHP"))

        apps_menu = menu.addMenu(self._t("apps"))
        apps_menu.addAction(self._t("calculator"), lambda: self.open_app("calculator"))
        apps_menu.addAction(self._t("snake"), lambda: self.open_app("snake"))
        apps_menu.addAction(self._t("dino"), lambda: self.open_app("dino"))
        apps_menu.addAction(self._t("offline"), lambda: self.open_app("offline"))

        language_menu = menu.addMenu(self._t("language"))
        language_menu.addAction("English", lambda: self.set_language("en-US"))
        language_menu.addAction("Português", lambda: self.set_language("pt-BR"))

    def _create_status_bar(self):
        self.status = QStatusBar()
        self.status.setStyleSheet("QStatusBar { background: rgba(8, 15, 31, 0.85); color: #e2e8f0; }")
        self.setStatusBar(self.status)
        self.status.showMessage(self._t("ready"))

    def _set_translucent_style(self):
        self.setStyleSheet(
            "QMainWindow { background: rgba(12, 18, 33, 0.92); }"
            "QTabWidget::pane { border: 1px solid rgba(255,255,255,0.08); border-radius: 14px; }"
            "QTabBar::tab { background: rgba(255,255,255,0.08); border-radius: 12px; padding: 10px 16px; margin: 4px; }"
            "QTabBar::tab:selected { background: rgba(255,255,255,0.15); }"
        )

    def _load_default_tab(self):
        self.add_new_tab()
        self.open_home_page()

    def _start_metric_updates(self):
        self.metric_timer = QTimer(self)
        self.metric_timer.timeout.connect(self._update_tab_metrics)
        self.metric_timer.start(1200)

    @property
    def current_view(self):
        return self.tabs.currentWidget()

    def add_new_tab(self, url: QUrl = None, title: str = None):
        if url is None:
            url = QUrl.fromLocalFile(os.path.join(os.getcwd(), "home_page.html"))
        view = QWebEngineView()
        view.setUrl(url)
        view.urlChanged.connect(self._update_url_bar)
        view.loadProgress.connect(self._update_status)
        view.loadFinished.connect(self._handle_load_finished)
        view.page().featurePermissionRequested.connect(self._handle_permission_request)

        if title is None:
            title = self._t("new_tab")

        index = self.tabs.addTab(view, title)
        self.tabs.setCurrentIndex(index)
        self.tab_data[view] = {
            "url": url.toString(),
            "cpu": random.uniform(1.2, 8.6),
            "memory": random.randint(24, 96),
        }
        self._refresh_tab_title(view)
        return view

    def _refresh_tab_title(self, view: QWebEngineView):
        metrics = self.tab_data.get(view, {})
        title = view.title() or self._t("new_tab")
        if metrics:
            title = f"{title} [{metrics['cpu']:.1f}% CPU | {metrics['memory']}MB]"
        index = self.tabs.indexOf(view)
        if index != -1:
            self.tabs.setTabText(index, title)

    def _update_tab_metrics(self):
        for view, meta in list(self.tab_data.items()):
            meta["cpu"] = max(1.0, min(99.0, meta["cpu"] + random.uniform(-1.6, 1.8)))
            meta["memory"] = max(20, min(256, meta["memory"] + random.randint(-4, 5)))
            self._refresh_tab_title(view)

    def _switch_tab(self, index: int):
        view = self.current_view
        if view:
            self.url_bar.setText(view.url().toString())
            self._handle_load_finished(True)

    def _close_current_tab(self):
        current = self.tabs.currentIndex()
        if current != -1:
            self.close_tab(current)

    def close_tab(self, index: int):
        widget = self.tabs.widget(index)
        if widget in self.tab_data:
            del self.tab_data[widget]
        self.tabs.removeTab(index)
        if self.tabs.count() == 0:
            self._load_default_tab()

    def _navigate_back(self):
        if self.current_view:
            self.current_view.back()

    def _navigate_forward(self):
        if self.current_view:
            self.current_view.forward()

    def _reload_current_tab(self):
        if self.current_view:
            self.current_view.reload()

    def _update_url_bar(self, url: QUrl):
        self.url_bar.setText(url.toString())

    def _update_status(self, progress: int):
        self.status.showMessage(f"{self._t('refresh')}... {progress}%")

    def _handle_load_finished(self, success: bool):
        if success:
            self.status.showMessage(self._t("ready"))
        else:
            self.status.showMessage(self._t("load_error"))

    def _load_url_from_bar(self):
        address = self.url_bar.text().strip()
        if address:
            self.open_url(address)

    def _normalize_address(self, address: str) -> QUrl:
        address = address.strip()
        parsed = urlparse(address)

        if parsed.scheme:
            return QUrl(address)

        local_path = os.path.abspath(address)
        if os.path.exists(local_path):
            if self.engine_mode == "PHP" and local_path.endswith(".php"):
                return QUrl.fromLocalFile(local_path)
            return QUrl.fromLocalFile(local_path)

        if self.engine_mode == "PHP" and address.endswith(".php"):
            return QUrl(f"{address}")

        if address.startswith("www."):
            address = f"http://{address}"
        elif not address.startswith("http://") and not address.startswith("https://"):
            address = f"http://{address}"

        return QUrl(address)

    def open_url(self, address: str):
        url = self._normalize_address(address)
        if not url.isValid():
            QMessageBox.warning(self, self._t("url_invalid"), self._t("cannot_load"))
            return
        if not self.current_view:
            self.add_new_tab(url)
            return
        self.current_view.setUrl(url)
        if self.current_view in self.tab_data:
            self.tab_data[self.current_view]["url"] = url.toString()
        self._refresh_tab_title(self.current_view)

    def open_home_page(self):
        home_page_path = os.path.join(os.getcwd(), "home_page.html")
        if os.path.exists(home_page_path):
            self.open_url(home_page_path)
        else:
            if self.current_view:
                self.current_view.setHtml("<h1>Zenith Navigator</h1><p>Homepage local não encontrada.</p>")

    def toggle_devtools(self):
        if not self.current_view:
            return
        if self.devtools_window and self.devtools_window.isVisible():
            self.devtools_window.close()
            self.devtools_window = None
            return

        self.devtools_window = QWebEngineView()
        devtools_page = QWebEnginePage(self.current_view.page().profile())
        self.devtools_window.setPage(devtools_page)
        self.current_view.page().setDevToolsPage(devtools_page)
        self.devtools_window.setWindowTitle("Zenith Navigator DevTools")
        self.devtools_window.resize(1000, 700)
        self.devtools_window.show()

    def open_settings(self):
        settings_dialog = AdvancedSettingsDialog(self)
        settings_dialog.exec()

    def open_console(self):
        if not self.console_enabled:
            QMessageBox.information(self, self._t("console"), self._t("console_disabled"))
            return
        console_dialog = ConsoleDialog(self)
        console_dialog.exec()

    def open_app(self, app_name: str):
        filename = LOCAL_APPS.get(app_name)
        if not filename:
            return
        file_path = os.path.join(os.getcwd(), filename)
        if os.path.exists(file_path):
            self.add_new_tab(QUrl.fromLocalFile(file_path), self._t(app_name))
        else:
            QMessageBox.warning(self, self._t("apps"), f"Arquivo não encontrado: {filename}")

    def open_installer(self):
        installer_path = os.path.join(os.getcwd(), "installer.py")
        if os.path.exists(installer_path):
            QMessageBox.information(self, self._t("installer"), f"{self._t('install_instructions')}\n{installer_path}")
        else:
            QMessageBox.warning(self, self._t("installer"), "Instalador não encontrado.")

    def set_language(self, language_code: str):
        if language_code not in STRINGS:
            return
        self.current_language = language_code
        self.setWindowTitle(self._t("app_title"))
        self._create_navigation_bar()
        self._create_menu_bar()
        self._create_status_bar()

    def set_engine_mode(self, mode: str):
        self.engine_mode = mode
        self.status.showMessage(f"Engine: {mode}")

    def _handle_permission_request(self, security_origin: QUrl, feature):
        permission_key = FEATURE_LABELS.get(feature, None)
        if permission_key and self.permissions.get(permission_key, False):
            self.current_view.page().setFeaturePermission(
                security_origin,
                feature,
                QWebEnginePage.PermissionPolicy.PermissionGrantedByUser,
            )
        else:
            self.current_view.page().setFeaturePermission(
                security_origin,
                feature,
                QWebEnginePage.PermissionPolicy.PermissionDeniedByUser,
            )

    def _load_new_tab(self):
        self.add_new_tab()


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Zenith Navigator")
    browser = ZenithBrowser()
    browser.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

    