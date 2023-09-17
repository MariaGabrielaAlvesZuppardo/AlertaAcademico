import subprocess

def install_requirements():
    # Lista de dependências
    requirements = [
        "Flask==2.0.1",
        "Flask-SQLAlchemy==2.5.1",
        "Flask-Login==0.5.0",
        "Flask-WTF==0.15.1",
        "SQLAlchemy==1.4.15",
        "WTForms==2.3.3",
        "gunicorn==20.1.0"
    ]

    # Instala cada dependência
    for requirement in requirements:
        subprocess.check_call(["pip", "install", requirement])

if __name__ == "__main__":
    install_requirements()
