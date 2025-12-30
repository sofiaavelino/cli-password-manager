# CLI Password Manager

A client-side, command-line password manager implemented in Python, featuring
secure master password authentication, encrypted credential storage, and a
PostgreSQL-backed vault running in Docker.

The project is designed as a modular system with a Bash-driven interface and
clear separation between authentication, encryption, database access, and CLI
logic.

---

## Features

- Secure master password authentication using bcrypt
- Encrypted credential storage using symmetric encryption (Fernet)
- Policy-based password generation
- PostgreSQL-backed vault running in Docker
- Configuration-driven database connectivity
- Command-line interface suitable for Bash usage

---

## Architecture Overview

The project is structured into independent modules responsible for distinct
concerns:

- **Authentication**: master password verification
- **Encryption**: encryption and decryption of stored credentials
- **Database**: SQL operations and connection management
- **CLI Interface**: argument parsing and command dispatch
- **Utilities**: password generation and configuration handling

This separation improves security, testability, and maintainability.

---

## Requirements

- Python 3.9+
- Docker
- PostgreSQL (via Docker)
- pip

---

## Database Setup (Docker)

Start a local PostgreSQL instance using Docker:

```bash
docker run --name postgres-db -e POSTGRES_PASSWORD=docker -p 5432:5432 -d postgres
```

The default credentials above are **example values** intended for local development only. You may use your own PostgreSQL instance and credentials.

---

## Configuration

The project requires a `database.ini` file to connect to PostgreSQL.
This file is **generated automatically** using the setup script.

Run:

```bash
chmod +x setup.sh
./setup.sh
```

You will be prompted for PostgreSQL connection details.

Values shown in brackets are **example defaults**.
Press Enter to use them, or provide your own credentials.

The generated `database.ini` file is excluded from version control.

---

## Installation

Create and activate a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

### Usage

Run the CLI entry point:

```bash
python main.py [command] [options]
```

Enter one of the following parameters:

`-a or --add [WEBSITE URL] [USERNAME] [PASSWORD_LENGTH (optional)]`: Generate a random password (default 20 characters) and save the entry.

`-ap or --add_password [WEBSITE_URL] [USERNAME] [PASSWORD]`: Create a new entry with a custom password.

`-uurl or --updateurl [NEW_URL] [OLD_URL]`: Update the URL of an existing entry.

`-uuser or --updateuser [NEW_USERNAME] [URL]`: Update the username of a stored entry.

`-upw or --updatepassword [NEW_PASSWORD (optional)] [URL]`: Update or generate a new password for a stored URL.

`-d or --delete [WEBSITE URL]`: Delete an entry by URL.

`-l or --lookup [WEBSITE URL]`: Look up an entry by URL.

`-li or --list`: List all stored entries in vault.

--- 

## Security Notes

- Master passwords are **never stored in plaintext**
- Authentication uses bcrypt with salted hashes
- Stored credentials are encrypted using Fernet
- Authentication and encryption are handled by separate components
- Configuration files containing credentials are excluded from Git

This project is intended for educational and demonstration purposes and should
not be used as-is for production environments.

---

## Tools and Technologies

- Python
- Bash
- PostgreSQL
- Docker
- bcrypt
- cryptography (Fernet)