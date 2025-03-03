# Telegram Bot for Service Requests and Payments

## Overview

This project is a Telegram bot designed to collect service requests from users and direct them to a payment gateway. The bot offers various cybersecurity-related services, such as security risk analysis, monitoring, and account breach investigations.

## Project Structure

```
📂 project-root
│── 📄 Dockerfile               # Configuration for Docker container
│── 📄 docker-compose.yml        # Docker Compose configuration
│── 📄 req.txt                   # Dependencies
│── 📄 main.py                    # Main script to run the bot
│── 📄 loader.py                  # Bot initialization
│── 📄 middleware.py               # Middleware setup
│── 📄 config.py                   # Configuration file for environment variables
│── 📄 README.md                   # Documentation file
│── 📂 handlers                    # Folder for bot handlers
│   │── 📂 images                  # Folder for images
│   │── 📄 __init__.py             # Init file for handlers module
│   │── 📄 api_queries.py          # API request handling
│   │── 📄 services.py             # Bot services logic
│   │── 📄 states.py               # Bot state management
│── 📂 keyboards                   # Folder for bot keyboards
│   │── 📄 __init__.py             # Init file for keyboards module
│   │── 📄 choise_buttons.py       # Keyboard buttons configuration
│── 📄 .env                        # Environment variables (not included in repo for security)
│── 📄 .env.example                # Example of environment configuration
│── 📄 .gitignore                  # Git ignore file
```

## Dependencies

The bot is built using the `aiogram` library for Telegram bot integration. All required dependencies are listed in `req.txt`:

```
aiogram==2.13
aiohttp==3.7.4.post0
alembic==1.6.5
...
python-dotenv==0.17.1
requests==2.24.0
```

To install dependencies, run:

```sh
pip install -r req.txt
```

## Configuration

Before running the bot, set up the `.env` file with the following variables:

```
TOKEN=your-telegram-bot-token
email_password=your-email-password
HOST=email-server-host
EMAIL_FROM=your-email-address
EMAIL_TO_1=recipient-email
EMAIL_TO_2=recipient-email
EMAIL_TO_3=recipient-email
EMAIL_TO_4=recipient-email
```

## Running the Bot

1. Install dependencies:

    ```sh
    pip install -r req.txt
    ```

2. Run the bot:

    ```sh
    python main.py
    ```

## Running with Docker

To deploy the bot using Docker:

1. Build and run the container:

    ```sh
    docker-compose up --build -d
    ```

2. Check logs:

    ```sh
    docker-compose logs -f
    ```

The bot runs inside a container using the configuration specified in `docker-compose.yml`:

```yaml
version: "3.1"
services:
  infsectest_bot:
    container_name: infsectest_bot
    build:
      context: .
    command: python main.py
    restart: always
    volumes:
      - .:/src
    env_file:
      - '.env'
    networks: 
      - infsectest_botnet

networks: 
  infsectest_botnet:
    driver: bridge
```

## Usage

1. Start the bot by running `/start`.
2. Select the desired service.
3. Provide necessary details (e.g., account ID, phone number).
4. Click on the provided payment link.
5. After payment, the bot will process the request and send a report.

## Features

- Secure payment integration with **Robokassa**.
- Provides cybersecurity-related services.
- Saves request details and sends them via email.
- Supports multiple recipients for email notifications.
- Uses **Docker** for easy deployment.

## License

This project is licensed under the MIT License.

---

For further development or integration, refer to the source code in `services.py`, `api_queries.py`, and `choise_buttons.py`.

