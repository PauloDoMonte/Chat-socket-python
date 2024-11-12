# settings.py

import os
import sys

# Diretório raiz do projeto
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Adiciona o diretório raiz ao sys.path para permitir importações absolutas
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Configurações de rede
SERVER_IP = '82.112.245.62'
SERVER_PORT = 6969
