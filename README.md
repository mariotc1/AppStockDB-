# AppStockDB

> **Proyecto de TFG — DAM CFGS · Desarrollo de Aplicaciones Multiplataforma**
> *A full-stack desktop inventory management application built as a Final Grade Project for a Spanish vocational computing degree.*

---

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.1.0-000000?style=flat-square&logo=flask&logoColor=white)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15.11-41CD52?style=flat-square&logo=qt&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=flat-square&logo=mysql&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)
![CI](https://github.com/mariotc1/AppStockDB-/workflows/CI/badge.svg)

**AppStockDB** is a desktop application for managing furniture and household-item inventory across an apartment complex. Staff can track which items are in which rooms, log stock assignments and returns, and consult the full movement history — all from a polished PyQt5 GUI backed by a local Flask REST API and a MySQL database.

---

## About

AppStockDB started as a TFG requirement and grew into a complete full-stack desktop application built from scratch. The goal was to go beyond a simple CRUD form and produce something that demonstrates real architectural thinking, attention to UX, and production-grade concerns like password hashing, role-aware sessions, and exportable reports.

The central architectural decision was to ship the entire backend inside the desktop package. `launcher.py` spawns the Flask API as a child subprocess, then starts the PyQt5 GUI. This means the app is self-contained — no separate server installation required — while keeping the frontend and backend cleanly decoupled through HTTP. The GUI never touches the database directly; every operation goes through the REST API.

The project covers the full stack: database design, API development, and a desktop frontend with animations, theme switching, and a contextual chatbot. It was a deliberate attempt to build something portfolio-worthy rather than just something that passes.

---

## Features

### Auth & Users
- User registration and login with **bcrypt** password hashing
- Password recovery via emailed verification codes (Flask-Mail)
- Session persistence across restarts (no JWT — lightweight session file)
- Profile picture upload and display
- Profile editing (username, email, password)

### Inventory Management
- Full **CRUD** for inventory items (products)
- Category and status tracking per item
- Multi-item stock assignment to rooms/addresses
- Stock returns with automatic quantity restoration
- **Excel export** of current stock and transaction history (via pandas + openpyxl)

### UI / UX
- **Light / Dark theme** toggle with QSS stylesheets (persists across sessions)
- Animated collapsible sidebar
- Rotating logo and typewriter label animations
- Real-time search with `QCompleter` autocomplete
- Contextual **chatbot** popup for in-app help
- Loading screen with progress animation
- Custom styled widgets (bubble cards, circular avatars, password field with toggle)

### Technical
- 18-endpoint **Flask REST API** consumed entirely over localhost HTTP
- **MySQL 8.0** relational database with foreign-key integrity
- Bundleable to a standalone executable with **PyInstaller**
- Docker setup (see Getting Started)
- `requests` for all frontend-to-backend communication

---

## Architecture

```
  [Your machine]                  [Docker containers]
  ┌──────────────────┐            ┌─────────────────────────┐
  │  PyQt5 Desktop   │   HTTP     │  Flask API  (gunicorn)  │
  │  launcher.py     │ ─────────► │  localhost:5001         │
  │  (frontend/)     │ ◄───────── │  (backend/api.py)       │
  └──────────────────┘   JSON     └────────────┬────────────┘
                                               │ connection pool
                                  ┌────────────▼────────────┐
                                  │  MySQL 8.0              │
                                  │  localhost:3307         │
                                  └─────────────────────────┘
                                  + Adminer UI: localhost:8080
```

The three layers are strictly separated:

- **Frontend** — PyQt5 views, dialogs, and widgets. Makes HTTP requests via `requests`. Knows nothing about SQL. Verifies API availability at startup before showing the UI.
- **Backend** — Flask + gunicorn with a MySQL connection pool (5 connections). 18 routes covering auth, CRUD, stock management, history, and file uploads.
- **Database** — MySQL 8.0 in Docker, initialized from `database/schema.sql` on first run.

---

## Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Desktop GUI | PyQt5 | 5.15.11 |
| REST API | Flask | 3.1.0 |
| Database | MySQL | 8.0 |
| ORM / DB driver | mysql-connector-python | 9.2.0 |
| Password hashing | bcrypt | 4.3.0 |
| Data export | pandas + openpyxl | 2.2.3 / 3.1.5 |
| Email | Flask-Mail | 0.10.0 |
| HTTP client | requests | 2.32.3 |
| Packaging | PyInstaller | 6.13.0 |
| Runtime | Python | 3.11+ |

---

## Getting Started

### Option A — Docker (recommended for a quick look)

Spins up the Flask API + MySQL together. The PyQt5 desktop app still runs natively and connects to the Docker-hosted API.

```bash
git clone https://github.com/mariotc1/AppStockDB-.git
cd AppStockDB-

# Copy the Docker env template
cp docker/.env.docker .env

# Build and start MySQL + Flask API
docker compose -f docker/docker-compose.yml --env-file .env up --build
```

The API will be available at `http://localhost:5000`. Then run the GUI with:

```bash
python launcher.py
```

To stop:
```bash
docker compose -f docker/docker-compose.yml down        # keep DB data
docker compose -f docker/docker-compose.yml down -v     # also delete DB volume
```

### Option B — Manual Setup

**1. Clone the repository**

```bash
git clone https://github.com/mariotc1/AppStockDB-.git
cd AppStockDB-
```

**2. Create and activate a virtual environment**

```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Configure the database**

Make sure you have MySQL 8.0 running, then create the database and run the schema:

```bash
mysql -u root -p -e "CREATE DATABASE AppStockDB;"
mysql -u root -p AppStockDB < database/schema.sql
```

**5. Set up environment variables**

```bash
cp .env.example .env
# Edit .env with your own values (see Environment Variables below)
```

**6. Run the application**

```bash
python launcher.py
```

`launcher.py` will start the Flask API in the background and launch the PyQt5 GUI automatically.

---

## Environment Variables

Copy `.env.example` to `.env` and fill in your values. **Never commit your real `.env` file.**

| Variable | Description | Example |
|----------|-------------|---------|
| `DB_HOST` | MySQL host | `127.0.0.1` |
| `DB_PORT` | MySQL port | `3306` |
| `DB_NAME` | Database name | `AppStockDB` |
| `DB_USER` | Database user | `root` |
| `DB_PASSWORD` | Database password | `yourpassword` |
| `MAIL_SERVER` | SMTP server for password recovery | `smtp.gmail.com` |
| `MAIL_PORT` | SMTP port | `587` |
| `MAIL_USERNAME` | Sender email address | `yourapp@gmail.com` |
| `MAIL_PASSWORD` | SMTP password or app password | `yourapppassword` |
| `FLASK_SECRET_KEY` | Flask session secret | `change-me-to-a-random-string` |

---

## API Reference

All endpoints are served at `http://127.0.0.1:5000`. The frontend communicates exclusively through these routes.

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/register` | Register a new user account |
| `POST` | `/login` | Authenticate and start a session |
| `POST` | `/forgot-password` | Send password recovery code by email |

### User Profile

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/get-user/<id>` | Retrieve user data by ID |
| `POST` | `/update-profile` | Update username, email, or password |
| `POST` | `/upload-profile-picture` | Upload and save a profile picture |
| `GET` | `/uploads/<filename>` | Serve a stored profile picture file |

### Products (Inventory)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/productos/listar` | List all inventory items |
| `POST` | `/productos/agregar` | Add a new product |
| `PUT` | `/productos/editar/<id>` | Edit an existing product |
| `DELETE` | `/productos/eliminar/<id>` | Delete a product |
| `GET` | `/productos/exportar` | Export inventory to Excel |

### Stock Assignments

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/productos/asignar_multiples` | Assign multiple items to a room/address |
| `GET` | `/salidas/listar` | List all active stock assignments |
| `PUT` | `/salidas/devolver/<id>` | Return assigned items (restores stock) |
| `DELETE` | `/salidas/eliminar/<id>` | Delete an assignment record |

### Movement History

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/historial/registrar` | Log a movement event |
| `GET` | `/historial/listar` | List full transaction history |
| `DELETE` | `/historial/eliminar/<id>` | Delete a history record |
| `GET` | `/historial/exportar` | Export history to Excel |

---

## Project Structure

```
AppStockDB-/
│
├── launcher.py                  # Entry point: spawns API subprocess, starts GUI
├── requirements.txt             # Runtime Python dependencies (pinned)
├── requirements-dev.txt         # Dev-only dependencies (Sphinx, PyInstaller)
├── .env.example                 # Environment variable template
│
├── backend/                     # Flask REST API
│   ├── api.py                   # All 18 endpoints, DB logic, file handling
│   └── start_api.py             # Flask server runner
│
├── frontend/                    # PyQt5 desktop application
│   ├── config.py                # Centralised config (API_BASE_URL, port)
│   ├── main.py                  # Session loading and main window bootstrap
│   ├── main_window.py           # Main window (sidebar, view router)
│   ├── login_window.py          # Login screen
│   ├── register_window.py       # Registration screen
│   ├── welcome_window.py        # Welcome / splash screen
│   ├── session_loading.py       # Session restore with loading animation
│   │
│   ├── views/                   # Full-page views (one per category)
│   │   ├── room_view.py         # Room inventory view
│   │   ├── appliances_view.py   # Appliances category view
│   │   ├── bathroom_view.py     # Bathroom items view
│   │   ├── common_areas_view.py # Common areas view
│   │   ├── my_profile_view.py   # User profile page
│   │   ├── settings_view.py     # App settings (theme, etc.)
│   │   └── info_view.py         # About / help screen
│   │
│   ├── sub_views/               # Embedded sub-panels within each view
│   │   ├── current_stock_subview.py       # Live stock table
│   │   ├── stock_removal_subview.py       # Assignment management
│   │   └── transaction_history_subview.py # History table with filters
│   │
│   ├── dialogs/                 # Modal dialogs
│   │   ├── add_product_dialog.py
│   │   ├── edit_product_dialog.py
│   │   ├── assign_product_dialog.py
│   │   ├── return_product_dialog.py
│   │   ├── delete_product_dialog.py
│   │   ├── delete_selected_product_dialog.py
│   │   ├── delete_multiple_dialog.py
│   │   ├── delete_movimiento_dialog.py
│   │   ├── loading_screen.py
│   │   └── videoPlayer_dialog.py
│   │
│   ├── styles/                  # Custom PyQt5 widget subclasses
│   │   ├── styled_button.py     # Themed QPushButton
│   │   ├── styled_line_edit.py  # Themed QLineEdit
│   │   ├── password_field.py    # Password input with show/hide toggle
│   │   ├── simple_card.py       # Card container widget
│   │   ├── bubble_widget.py     # Chat bubble widget
│   │   ├── circular_icon.py     # Circular avatar widget
│   │   └── animated_styled_switch.py # Animated toggle switch
│   │
│   ├── animations/              # Reusable animation components
│   │   ├── rotating_logo.py     # Spinning logo (auth screens)
│   │   ├── rotating_logo_mw.py  # Spinning logo (main window)
│   │   ├── typewriter_label.py  # Typewriter text effect
│   │   └── lateral_menu_button.py # Animated sidebar button
│   │
│   ├── themes/                  # QSS stylesheets
│   │   ├── theme_manager.py     # Theme loader and switcher
│   │   ├── light.qss            # Light theme styles
│   │   └── dark.qss             # Dark theme styles
│   │
│   └── chatbot/                 # Contextual help chatbot popup
│       └── chat_popup.py
│
├── database/
│   └── schema.sql               # Full MySQL schema (tables + seed data)
│
├── tests/                       # Test suite
├── docker/                      # Docker and Docker Compose files
├── .github/workflows/           # CI/CD pipelines
├── images/                      # App icons and static assets
├── config/                      # Runtime config (session, theme preference)
├── uploads/                     # Runtime storage for profile pictures
└── docs/                        # Sphinx-generated API documentation
```

---

## Database Schema

The database uses four tables with foreign-key relationships to maintain data integrity.

### `productos` — Inventory Items
Stores every item that can be tracked: `id`, `nombre` (name), `categoria` (category), `estado` (condition), `cantidad` (quantity available). This is the master inventory ledger.

### `usuarios` — User Accounts
Stores staff accounts: `id`, `username`, `email`, `password` (bcrypt hash), `profile_picture` (filename reference). Passwords are never stored in plain text.

### `salidas_stock` — Active Assignments
Records every active stock outflow: `id`, `producto_id` (FK → productos), `cantidad_asignada`, `direccion` (room/address), `fecha_salida`, `usuario_id` (FK → usuarios). Returning items removes the record and restores stock.

### `historial_movimientos` — Transaction History
Immutable audit log: `id`, `tipo_movimiento` (checkout / return / edit / delete), `producto_id`, `cantidad`, `descripcion`, `fecha`, `usuario_id`. Never modified, only appended to or selectively deleted by admins.

---

## Contributing

Contributions, issues, and feature requests are welcome.

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a Pull Request

Please make sure your code follows the existing style and that any new features include appropriate comments.

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgements

This application was developed as a **TFG (Trabajo de Fin de Grado)** for the **DAM CFGS** (Ciclo Formativo de Grado Superior — Desarrollo de Aplicaciones Multiplataforma) vocational degree in Spain.

Building AppStockDB was a genuine learning journey through full-stack desktop development: designing a relational schema, building a REST API, crafting a multi-window GUI, and connecting them all together. The goal was always to build something real — not just something that passes.

Special thanks to the open-source community behind Flask, PyQt5, and the broader Python ecosystem that made this possible.

---

*Built with Python, curiosity, and a lot of coffee.*
