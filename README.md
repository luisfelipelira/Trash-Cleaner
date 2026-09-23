# Trash Cleaner

Jogo local desenvolvido com Pygame. O ponto de entrada principal é `menu.py`.

## Requisitos

- Python 3.11 recomendado (64 bits)
- Tkinter, normalmente incluído no instalador oficial do Python para Windows

## Instalação no Windows (PowerShell)

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Não reutilize a pasta `venv` antiga do repositório: ambientes virtuais não são portáteis e devem ser recriados localmente.

## Execução

Com o ambiente virtual ativado:

```powershell
python menu.py
```

Na primeira execução, o vídeo de introdução é reproduzido antes da abertura do menu.
