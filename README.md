# Django Video Streaming Backend (PostgreSQL)

This README provides instructions for setting up and running your Django backend, which handles video uploads, conversions to different resolutions, and serves video URLs. It's configured to use PostgreSQL as its database.

> [!NOTE]
> The corresponding frontend for this backend can be found here:
> **https://github.com/43and18zeroes/videoflix_frontend**

---

## 1. Prerequisites

Before you begin, ensure you have the following installed on your system:

* **Python 3.8+**: [Download Python](https://www.python.org/downloads/)
* **pip**: Python package installer (usually comes with Python)
* **PostgreSQL**: [Download PostgreSQL](https://www.postgresql.org/download/)
* **FFmpeg**: For video conversion. See [FFmpeg Setup](#4-ffmpeg-setup) for installation details.

---

## 2. Setup Instructions

### Clone the Repository

First, clone your backend repository:

```bash
git clone https://github.com/43and18zeroes/videoflix_backend
cd videoflix_backend

sudo apt-get install python3-venv

sudo python3 -m venv env

source env/bin/activate

pip install -r requirements.txt
```


### Setup PostgreSQL

```bash
sudo apt install postgresql postgresql-contrib

sudo service postgresql start

sudo service postgresql status

sudo su postgres

psql
```


```bash
CREATE DATABASE videoflix_database;
CREATE USER postgres WITH PASSWORD 'n1n3!Cl34n1n6';
ALTER ROLE postgres SET client_encoding TO 'utf8';
ALTER ROLE postgres SET default_transaction_isolation TO 'read committed';
ALTER ROLE postgres SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE videoflix_database TO postgres;
```

Exit with CMD + D

```bash
exit
```

In some cases it necessary to reset the password:

```bash
sudo su postgres

ALTER ROLE postgres WITH PASSWORD 'n1n3!Cl34n1n6';
```

Exit with CMD + D

```bash
exit
```

Migration:

```bash
python manage.py makemigrations
python manage.py migrate
```