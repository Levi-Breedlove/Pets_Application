# Pets Application – Django 5.2

# Project Overview
 The Pets Application is a learning project that demonstrates a full Django CRUD workflow—creating, reading, updating, and deleting pets and their veterinary records—then deploys the stack to AWS using Elastic Beanstalk and RDS.

 The application is designed to run on AWS infrastructure, utilizing services such as RDS for the database and S3 for static file storage.


## Prerequisites

| Tool       | Version | Notes                                 |
| ---------- | ------- | ------------------------------------- |
| Python     | 3.12    | Confirm with `python --version`       |
| pip        | ≥23     | `python -m pip install --upgrade pip` |
| virtualenv | any     | or `python -m venv`                   |
| AWS CLI    | 2.x     | `aws configure` set default profile   |
| EB CLI     | 3.x     | `pip install awsebcli`                |
| Git        | ≥2.30   |                                       |

---

## File Structure 

```
Pets_Application/
├── django/
│   ├── hello_app/               # sample landing app
│   │   ├── views.py
│   │   └── urls.py
│   ├── pets_app/                # main CRUD app
│   │   ├── migrations/
│   │   ├── templates/pets_app/
│   │   ├── admin.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   └── views.py
│   ├── pets_project/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── __init__.py
│   ├── manage.py
│   └── requirements.txt
├── media/                       # uploaded pet photos (dev)
├── static/                      # Tailwind CSS build output
├── .ebextensions/               # EB config files (prod only)
└── README.md                    # ← you are here
```

---

## Local Development

```bash
# clone & enter repo
$ git clone https://github.com/Levi-Breedlove/Pets_Application.git
$ cd django

# create virt‑env
$ python -m venv .venv && source .venv/bin/activate

# install deps
$ pip install -r requirements.txt  # Django 5.2, pillow, mysqlclient (optional)

# migrations, sample data 
$ python manage.py migrate

# (Optional) load starter data
$ python manage.py loaddata savedata.json  # located in django/fixtures/

# run Tailwind build (if used)
$ npx tailwindcss -i ./static/src.css -o ./static/styles.css --watch &

# launch dev server
$ python manage.py runserver

# create user for admin console
$ python manage.py createsuperuser
```
Open [http://127.0.0.1:8000](http://127.0.0.1:8000) for the public site and `/admin` for the admin console.

### The Website Loads With Pet Card Fixtures:
![Django Pets Application ](./django/media/pets-grid.png)
---

## Demo Scenarios

| Scenario             | Steps                                                                                                   |
| -------------------- | ------------------------------------------------------------------------------------------------------- |
| **Admin CRUD**       | 1) Sign in at `/admin`  2) Add a pet, upload photo  3) Edit record  4) Delete and confirm list refresh  |
| **Public List View** |                                         |
| **Search**           |                                         |
| **Image upload**     |                                         |

---

## AWS Deployment (Elastic Beanstalk)

The diagram (docs/images/architecture.png) shows a VPC with a public subnet for EB and a private subnet for RDS.

### Preparation

```bash
# at repo root
aws configure                # set AWS creds & default region
cd django
EB_APP=pets-app

# create EB env
eb init $EB_APP --platform "Python 3.12" --region us-west-2
# choose: 1) SSH keypair 2) CodeCommit=No

eb create $EB_APP-prod --instance_type t3.micro --database --database.engine mysql --database.version 8.0 --database.user django --database.password <pwd>
```

EB CLI spins up:

* EC2 (public) running your Django code
* RDS MySQL (private)
* Security groups so EC2 ↔ RDS only

### Deploy

```bash
# collect static then push
eb deploy
```

A URL like `http://pets-app-prod.us-west-2.elasticbeanstalk.com` appears.

### Environment Variables

Set once:

```
# bash
eb setenv DJANGO_SECRET_KEY=prod-secret \
           DB_NAME=pets \
           DB_HOST=<rds-endpoint> \
           DB_USER=django \
           DB_PASSWORD=<pwd> \
           USE_S3=1 USE_SQLITE=0
```

### Static & Media in S3

Add to `settings.py` when `USE_S3=1`:

```
# python
STORAGES = {
    "default": {"BACKEND": "storages.backends.s3boto3.S3Boto3Storage"},
    "staticfiles": {"BACKEND": "storages.backends.s3boto3.S3StaticStorage"},
}
```

Run `eb deploy` again; EB hooks `python manage.py collectstatic` via `.ebextensions/01_collectstatic.config`.

---

## GitHub Actions CI/CD

`.github/workflows/eb-deploy.yml` (simplified):

```yaml
on:
  push:
    branches: [ main ]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v4
      with: { python-version: "3.12" }
    - run: pip install -r django/requirements.txt
    - run: eb deploy pets-app-prod --staged
      env:
        AWS_ACCESS_KEY_ID:   ${{ secrets.AWS_ACCESS_KEY_ID }}
        AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
```

Push to `main` → tests run → auto‑deploy.

---

## Next Steps


---

© 2025 Levi Breedlove – MIT License Amazon Web Services 

