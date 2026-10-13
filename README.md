# Yadino — Smart Education Platform

<p align="center">
  <strong>An educational prototype for learning profiles, personalized activity recommendations, and feedback</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/Django-Web%20Framework-092E20?logo=django&logoColor=white" alt="Django">
  <img src="https://img.shields.io/badge/Status-Prototype-orange" alt="Prototype">
  <img src="https://img.shields.io/badge/AI-Demo%20Recommender-blueviolet" alt="Demo recommender">
</p>

**Yadino** is a Django-based educational prototype that demonstrates a simple learning-support workflow:

1. A student completes a questionnaire.
2. The application creates a learning profile from the submitted answers.
3. The system suggests learning strategies and activities.
4. A learning plan presents recommended activities.
5. Feedback can be recorded to help evaluate the experience.

> **Project status:** This repository is a development/demo prototype. Its current database and training data are synthetic. It has not been established as a validated educational or psychological assessment system and should not be used to make high-stakes decisions about students.

## Contents

- [Features](#features)
- [Technology stack](#technology-stack)
- [How the workflow works](#how-the-workflow-works)
- [Requirements](#requirements)
- [Installation](#installation)
- [Database setup and demo data](#database-setup-and-demo-data)
- [Train the demonstration recommender](#train-the-demonstration-recommender)
- [Run the application](#run-the-application)
- [Application routes](#application-routes)
- [Project structure](#project-structure)
- [Configuration and security](#configuration-and-security)
- [Privacy, fairness, and responsible use](#privacy-fairness-and-responsible-use)
- [Further documentation](#further-documentation)
- [Future development ideas](#future-development-ideas)

## Features

- **Questionnaire workflow:** collect sample answers from a student.
- **Learning profile:** display profile features and related recommendations.
- **Learning plan:** organize suggested learning activities.
- **Feedback endpoint:** accept feedback or activity-status data.
- **Django administration:** provide an administrative interface for development.
- **Machine-learning demonstration:** train a recommender using synthetic example data.
- **Technical documentation:** describe the API, database, and ML components in separate documents.

The features above describe the prototype's intended workflow; they do not imply that its recommendations have been validated for real-world educational outcomes.

## Technology stack

| Technology | Role |
| --- | --- |
| Python | Application and ML code |
| Django | Web framework, routing, views, and administration |
| HTML templates | Server-rendered pages |
| CSS / JavaScript | Front-end presentation and interactions |
| CSV | Demonstration training data |
| Joblib / JSON | Saved demonstration model and metrics |

Check `requirements.txt` for the project's actual Python dependencies.

## How the workflow works

```text
Student
   |
   v
Questionnaire
   |
   v
Answer processing
   |
   v
Learning profile
   |
   v
Recommendation / learning plan
   |
   v
Student activity and feedback
```

This diagram is a conceptual overview of the prototype, not a claim that the recommendation model is clinically or educationally validated.

## Requirements

- Python **3.10 or newer** (Python 3.11 or 3.12 is a reasonable choice for a compatible environment)
- `pip`
- Python virtual environment support
- Git, if you want to clone the repository

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/alipourfereydoon/smart_educations.git
cd smart_educations
```

If you already downloaded the repository, open a terminal in the project directory instead.

### 2. Create and activate a virtual environment

**Windows PowerShell**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can use the virtual environment's Python executable directly, or follow the Python documentation for your system's execution policy.

**Windows Command Prompt**

```bat
python -m venv .venv
.venv\Scripts\activate.bat
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Create your environment file

Copy `.env.example` to `.env`.

**Windows PowerShell**

```powershell
Copy-Item .env.example .env
```

**macOS / Linux**

```bash
cp .env.example .env
```

Review the environment variables before running the application. Use a unique, secret `SECRET_KEY` for any shared or deployed environment. Do not commit `.env` or real credentials to Git.

## Database setup and demo data

Run the following commands from the directory containing `manage.py`:

```bash
python manage.py makemigrations education
python manage.py migrate
python manage.py seed_demo
```

The `seed_demo` command creates example records for the demonstration workflow, including a sample student, questions, strategies, synthetic answers, an assessment, and a plan.

Use only the demo credentials documented in the command's source code, and **never reuse demo passwords in a real deployment**. If a password has been published in a public repository, treat it as compromised and replace it.

## Train the demonstration recommender

Run:

```bash
python ml_engine/train_model.py
```

The training script reads the synthetic dataset at `ml_engine/training_data.csv` and writes demonstration artifacts, including:

- `ml_engine/artifacts/recommender.joblib`
- `metrics.json` (location as defined by the script)

These outputs are for experimentation and development. Metrics obtained from synthetic data do not establish real-world accuracy, educational benefit, or fairness.

## Run the application

Start Django's development server:

```bash
python manage.py runserver
```

Open this address in your browser:

**http://127.0.0.1:8000/**

The Django development server is intended for local development, not production hosting.

## Application routes

| Route | Method | Purpose |
| --- | --- | --- |
| `/` | `GET` | Home page and sample student |
| `/questionnaire/<student_id>/` | `GET`, `POST` | Display a questionnaire and submit answers |
| `/profile/<student_id>/` | `GET` | Show the learning profile, feature scores, and recommendations |
| `/plan/<student_id>/` | `GET` | Show a learning plan and its activities |
| `/api/feedback/<plan_item_id>/` | `POST` | Submit JSON feedback or activity status |
| `/admin/` | `GET` | Django administration interface |

For request and response details, see [`docs/API.md`](docs/API.md). For the data model, see [`docs/DATABASE.md`](docs/DATABASE.md).

## Project structure

```text
smart_educations/
├── education/       # Django models, views, and application services
├── templates/       # HTML templates
├── static/          # CSS and JavaScript assets
├── ml_engine/       # Feature engineering, model code, and synthetic data
├── docs/            # Technical documentation
├── manage.py        # Django management entry point
├── requirements.txt # Python dependencies
├── .env.example     # Example environment configuration
└── README.md        # Project overview and setup guide
```

This is a high-level guide. The exact files and folders may change as the project develops.

## Configuration and security

Before making the application accessible to other people or deploying it, review and complete the following items:

- Set `DEBUG=False`.
- Generate a strong, unique `SECRET_KEY` and store it outside source control.
- Configure `ALLOWED_HOSTS` for the intended domains.
- Use HTTPS and secure cookie settings.
- Add authentication and authorization checks to student pages, APIs, and the admin interface.
- Verify that each user can access only records they are authorized to view or change.
- Apply request throttling where appropriate.
- Keep dependencies updated and review them for known vulnerabilities.
- Configure secure logging, backups, and a data-retention/deletion process.
- Review CSRF protection for forms and API requests. The feedback endpoint is expected to receive a valid CSRF token when CSRF protection applies.
- Do not use Django's development server as a production server.

**Important prototype limitation:** the repository's current example configuration may not include authentication or ownership-based access controls on all student-facing routes. Do not deploy it with real student information until these controls have been implemented and tested.

## Privacy, fairness, and responsible use

Educational information can be sensitive, especially when it concerns children. Before conducting a real pilot:

- Collect only the data needed for a clearly stated purpose.
- Obtain appropriate consent and follow applicable privacy and education laws.
- Separate directly identifying information from model-training data where feasible.
- Restrict access and provide a process for correcting or deleting records.
- Evaluate recommendation quality with representative, appropriately collected data.
- Test for bias across language, culture, disability, and other relevant circumstances.
- Explain recommendations in understandable language and allow human review and challenge.
- Keep teachers and appropriate guardians involved in consequential decisions.
- Do not present learning-profile outputs as a medical or psychological diagnosis.
- Do not use this demonstration model to make high-stakes or fully automated decisions about students.

## Further documentation

- [ML documentation](docs/ML.md) — machine-learning workflow and implementation notes.
- [API documentation](docs/API.md) — endpoint payloads and usage details.
- [Database documentation](docs/DATABASE.md) — data model and database design.

## Future development ideas

Potential next steps for turning the prototype into a more complete project include:

- Add secure sign-in and role-based permissions for students, teachers, and administrators.
- Improve questionnaire design and document how each profile feature is calculated.
- Compare transparent rule-based recommendations with ML-based recommendations.
- Evaluate the model using real, consented, anonymized, and representative data.
- Add automated tests for views, permissions, API validation, and recommendation logic.
- Improve accessibility, mobile responsiveness, and multilingual support.
- Add monitoring and clear explanations for recommendation quality and limitations.
- Document setup, architecture, evaluation methodology, and known limitations as the implementation evolves.

## License

No license is specified here. Check the repository for a `LICENSE` file before reusing, modifying, or distributing the code.
