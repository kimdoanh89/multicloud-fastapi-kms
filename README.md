# multicloud-fastapi-kms

## Setup

- Install packages for using fastapi

```bash
pip install fastapi gunicorn uvicorn pylint
```

- Generate `requirements.txt` with pip

```bash
pip freeze > requirements.txt
```

- Create project on GCP

```bash
gcloud auth login
gcloud projects create fastapi-kms
gcloud projects list
gcloud config set project fastapi-kms
```

- The app is deployed [here](https://fastapi-kms.ey.r.appspot.com/).

