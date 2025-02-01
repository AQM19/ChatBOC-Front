# ChatBOC app UI

Una aplicación web Python fácil de usar y altamente personalizable diseñada para demostrar LLM en formato Llama3.

<div align="center">
<img src="./docs/demo.gif" alt="icon"/>
</div>

# Inicialización en un click

Para iniciar la aplicación ejecutar en consola:

### 1. Descarga fichero install

```bash
chmod +x install.sh
./install.sh
```
#
El Script realiza:

#### 🧬 1. Clona el Repo

```bash
git clone https://github.com/reflex-dev/reflex-chat.git
```

#### 📦 2. Instalar dependencias

Para lanzar la aplicación se necesita lo siguiente:

- Python 3.7+
- Node.js 12.22.0+ \(No JavaScript knowledge required!\)
- Pip dependencies: `reflex`, `flask`, `flask_jwt_extended`,`loguru`,`python-dotenv`

Install `pip` con las dependencias en `requirements.txt`:

```bash
pip install -r requirements.txt
```

#### 🚀 3. Ejecutar app

Inicialización y ejecución de la app:

```
reflex init
reflex run
```

# Características

- 100% Python-based. Reflex IU
- Crear y borrar chats
- Respuesta de Llama3 al contexto del BOC (boletín oficial de cantabria)
- Fácil cambio a otro modelo LLM
- Diseño responsive


# Licencia

El cógido de la app tiene licencia MIT License.
