# Telegram Bot Constructor (Backend) 🤖


<p align="center">
  <img src="https://img.shields.io/badge/Flask-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
</p>
A versatile and lightweight Flask-based backend framework for building Telegram chatbots. The architecture is engineered for effortless portability and multi-server exporting: it utilizes a JSON-driven configuration instead of a Redis dependency, allowing the entire application to spin up with a single command.

---

## 🚀 Key Features

* **No-Redis && DB Architecture:** The entire bot workflow state machine and node layout are declared entirely within `data.json`.
* **Node-Based System:** Chatbot dialogue trees and conditional branching are handled dynamically via a dedicated routing system.
* **Minimalist Deployment:** Specially optimized to run reliably on resource-constrained servers or within lightweight Docker environments.
* **Dynamic Placeholders:** Native support for template matching and variable substitution inside message bubbles.

---

## 🏗️ Project Architecture & Components

* `bot.py` — Application entry point, handling Flask server initialization and the Telegram client polling/webhook setup.
* `data.json` — The central configuration file defining the bot's conversational nodes and routing logic.
* `service/` — The core business logic directory:
  * `nodes/` — Modules managing user transitions through the visual layout node-tree.
  * `answers/` — Components handling text validation and parsing of inbound user responses.
  * `replace_placeholders.py` — Engine responsible for injecting dynamic user attributes into automated texts.
* `db/` — Database abstraction layers capturing persistent user sessions and interaction states.
* `utils/config.py` — Configurations loader for tokens, environment parameters, and runtime variables.

---

## 📦 Getting Started & Setup

### 1. Environment Preparation
Ensure you have **Python 3.10 or higher** installed on your system.

```bash
# Clone the repository (if applicable)
# git clone <url> && cd <project_dir>

# Initialize a clean virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate
```

### 2. Dependency Installation
```bash
pip install -r requirements.txt
```

### 3. Configuration Setup
Create a `.env` file in the root folder (or directly update `utils/config.py`) to store your secure `TELEGRAM_TOKEN`. All visual dialogue steps can be tailored inside `data.json`.

### 4. Running the Bot
*Note: Admin privileges (`sudo`) might be required if your server environment requires binding to low-numbered ports (under 1024) or special system resources.*

```bash
sudo ./venv/bin/python bot.py
```
> **⚠️ Crucial:** To completely avoid module conflicts with the host system, always execute the project interpreter directly out of the local path: `./venv/bin/python`.

---

## 📄 License

This software is distributed on an "As-Is" basis. You are fully welcome to copy, modify, and restructure this codebase for your custom infrastructure setups.
