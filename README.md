# Backend for AlumNUS

The backend works as a REST API for the AlumNUS website. It is built using FastAPI and deployed on Fly.io.

The current version of the API is available at https://alumnus.fly.dev/docs/ or https://alumnus.fly.dev/redoc/.

There is no need to build the backend locally as it is already deployed on Fly.io. However, if you wish to do so, follow the instructions below.

## Setup

### Python Modules

1. Install Python 3.10
2. Run `pip install -r requirements.txt`

### Firebase

1. Create a new Firebase project
2. Create a new Firestore database
3. Save your service account keys as `<app-name>_service_account_keys.json` in the root directory of the project
4. Save your Firebase config as `firebase_config.json` in the root directory of the project

### Flyctl

1. Install flyctl CLI from https://fly.io/docs/getting-started/installing-flyctl/
2. Login to flyctl CLI with `flyctl auth login`
3. Create a new app with `flyctl apps create <app-name>`
4. Launch the app with `flyctl launch`
5. Deploy the app with `flyctl deploy`

Your application should be up and running now! Your API URL is `https://<app-name>.fly.dev/`, and the docs are available at `https://<app-name>.fly.dev/docs/` or `https://<app-name>.fly.dev/redoc/`. Make sure to update the API URL in the frontend accordingly.
