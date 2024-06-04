#!/bin/bash

# echo '**************************************************************************************************'
# echo Clonando repositorio
# echo '**************************************************************************************************'

# # checkear si git esta instalado
# if ! [ -x "$(command -v git)" ]; then
#     echo 'Error: git no está instalado.' >&2
#     exit 1
# fi
# # checkear si existe F-ChatBOC-Front
# if [ -d "F-ChatBOC-Front" ]; then
#     echo 'Error: F-ChatBOC-Front ya existe.' >&2
#     ./F-ChatBOC/chatapp/chatapp/init.sh
    
# fi

# git clone -b despliegue https://github.com/AQM19/F-ChatBOC-Front.git
# cd F-ChatBOC-Front
# cd chatapp

# Función para detectar el sistema operativo
detect_os() {
    case "$OSTYPE" in
        linux*)   echo "Linux" ;;
        msys*)    echo "Windows" ;;
        cygwin*)  echo "Windows" ;;
        *)        echo "unknown" ;;
    esac
}

OS=$(detect_os)

# Creación del entorno virtual y su gestión
echo '**************************************************************************************************'
echo Creando entorno virtual
echo '**************************************************************************************************'

if [ "$OS" = "Linux" ]; then
    python3 -m venv .venv
    source .venv/bin/activate
elif [ "$OS" = "Windows" ]; then
    python -m venv .venv
    source .venv/Scripts/activate
else
    echo "Sistema operativo no soportado."
    exit 1
fi

pip install -r requirements.txt

# Inicio de la api

reflex run
