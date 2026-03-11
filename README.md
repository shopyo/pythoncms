# pythoncms

[![First Timers Only](https://img.shields.io/badge/first--timers--only-friendly-blue.svg)](https://www.firsttimersonly.com/)

**The fastest way to start a CMS in Python.** Build production-grade sites with zero-config, modular themes, and a powerful content API.

## 🚀 Quickstart

The new unified CLI makes it easier than ever to get started:

```bash
pip install pythoncms
pythoncms start mysite --run
```

This single command will:
1. Create your project directory.
2. Generate a secure `.env` file.
3. Initialise the database.
4. Seed the default admin user.
5. Start the development server.

Open: `http://localhost:5000/dashboard`  
Login: `admin@domain.com` / `pass`

---

## 🛠️ Unified CLI Commands

Manage your entire project from one place:

- `pythoncms start <name>`: Create a new project.
- `pythoncms run`: Start the dev server.
- `pythoncms initialise`: Set up database and assets.
- `pythoncms seed`: Reset default data.
- `pythoncms --version`: Check your version.

---

## ✨ Features

- 🏗️ **Content Types:** Define custom schemas with JSON.
- 🎨 **Theme Support:** Switch between beautiful, responsive themes instantly.
- 🔐 **Built-in Auth:** Secure admin and user management out of the box.
- 🍱 **Modular Architecture:** Extend functionality with a robust plugin system.
- 🖼️ **Media Management:** Simple upload and resource handling.
- ⚡ **Flask Powered:** Minimal, fast, and easy to customize.

---

## 📸 See it in Action

### Admin Dashboard
![Admin Dashboard](https://github.com/shopyo/pythoncms/raw/main/assets/dashboard_preview.png)

### Page Editor
![Page Editor](https://github.com/shopyo/pythoncms/raw/main/assets/editor_preview.png)

### Website Frontend
![Website Frontend](https://github.com/shopyo/pythoncms/raw/main/assets/frontend_preview.png)

---

## 🛠️ Local Development

If you want to contribute to the core or customize the engine:

1. **Clone and Install:**
   ```bash
   python -m pip install -e .
   ```

2. **Initialize:**
   ```bash
   cd pythoncms
   shopyo initialise
   flask --debug run
   ```

3. **Database Migrations:**
   ```bash
   flask db migrate
   flask db upgrade
   ```

---

## 🎨 Themes & Customization

Themes are located at `/static/themes/`.

### Front Themes
Must include `index.html`, `contact.html`, and `page.html`.

### Back Themes
Must include `base.html`, `login.html`, `register.html`, and `unconfirmed.html`.

---

## 📄 License & Community

- **License:** MIT
- **Discord:** [Join our community](https://discord.com/invite/k37Ef6w)
- **Issues:** [Report a bug](https://github.com/shopyo/pythoncms/issues)

---

*Powered by the Shopyo engine.*
