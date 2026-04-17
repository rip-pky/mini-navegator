import os
import sys
import subprocess

PROJECT_NAME = "Zenith Navigator"
BAT_NAME = "run_zenith.bat"


def create_shortcut():
    bat_path = os.path.join(os.getcwd(), BAT_NAME)
    with open(bat_path, "w", encoding="utf-8") as bat_file:
        bat_file.write("@echo off\n")
        bat_file.write("cd /d %~dp0\n")
        bat_file.write("py main.py\n")
    print(f"Criado: {bat_path}")


def install_dependencies():
    print("Instalando dependências...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyQt6", "PyQt6-WebEngine"])
    print("Dependências instaladas com sucesso.")


def main():
    print(f"{PROJECT_NAME} Installer")
    create_shortcut()
    try:
        install_dependencies()
    except subprocess.CalledProcessError:
        print("Erro ao instalar dependências. Verifique sua conexão e tente novamente.")


if __name__ == "__main__":
    main()
