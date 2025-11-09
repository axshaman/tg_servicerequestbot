# IST-detector Service Request Bot

A Telegram bot built with [aiogram](https://docs.aiogram.dev) that helps clients request cybersecurity services, pay through Robokassa and notify operators by e-mail. The conversation now guides users through choosing a social network, selecting a service or monitoring plan, capturing contact details and confirming their request before payment.

## Features

- Guided dialogue with validation for social network, service and contact details.
- Support for monitoring subscription plans with inline keyboards.
- Optional e-mail and comment collection prior to confirmation.
- Payment link generation for Robokassa with configurable merchant credentials.
- Automatic e-mail notifications to one or many recipients.
- `/help`, `/services` and `/cancel` commands for better usability.
- Docker image based on Python 3.11 for production deployments.

## Project Structure

```
📂 tg_servicerequestbot
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── main.py
├── loader.py
├── config.py
├── middleware.py
├── service_catalog.py
├── handlers/
│   ├── __init__.py
│   ├── services.py
│   ├── states.py
│   └── images/
├── keyboards/
│   ├── __init__.py
│   └── choise_buttons.py
├── docs/
│   ├── architecture.md
│   └── openapi.yaml
└── README.md
```

## Prerequisites

- Python 3.11+
- A Telegram bot token (`@BotFather`)
- Access to an SMTP server for outbound notifications
- Robokassa merchant credentials (login and password #1)

## Configuration

Create a `.env` file in the project root (see `.gitignore`). Supported variables:

```
TOKEN=<telegram bot token>
EMAIL_PASSWORD=<smtp password>
HOST=<smtp host>
EMAIL_FROM=<sender address>
EMAIL_TO=<comma separated recipient list>
EMAIL_TO_1=<legacy recipient, optional>
EMAIL_TO_2=<legacy recipient, optional>
EMAIL_TO_3=<legacy recipient, optional>
EMAIL_TO_4=<legacy recipient, optional>
ROBOKASSA_MERCHANT_LOGIN=<defaults to infsectest_ru>
ROBOKASSA_PASSWORD1=<defaults to qNI1cl89rPWbFMkb9Ls0>
ROBOKASSA_BASE_URL=<defaults to https://auth.robokassa.ru/Merchant/Index.aspx>
PAYMENT_DESCRIPTION_TEMPLATE=<custom description pattern>
```

> **Tip:** `EMAIL_TO` can be used to define all recipients in a single comma-separated value, while the numbered variables keep compatibility with older deployments.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

Run the bot locally:

```bash
python main.py
```

## Docker Usage

Build and run with Docker Compose:

```bash
docker-compose up --build -d
```

Follow logs:

```bash
docker-compose logs -f
```

## Bot Commands

- `/start` – begin a new service request flow.
- `/services` – display the list of available services and monitoring plans.
- `/help` – show quick usage hints.
- `/cancel` – abort the current conversation and reset the state.

## Documentation

Additional documentation is located in the [`docs/`](docs) directory:

- [`openapi.yaml`](docs/openapi.yaml) – OpenAPI 3.0 description of the service-request workflow for integration scenarios.
- [`architecture.md`](docs/architecture.md) – C4 model overview (context, container and component views) of the bot solution.

## Testing

The project currently relies on manual testing via Telegram. When running locally, interact with the bot using the provided commands to verify the flow, payment link generation and e-mail delivery.

## License

This project is distributed under the MIT License.
