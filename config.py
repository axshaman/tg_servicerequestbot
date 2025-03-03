import os
import dotenv


dotenv.load_dotenv()
TOKEN = os.getenv("TOKEN")
EMAIL_PASSWORD = os.getenv("email_password")
HOST = os.getenv("HOST")
EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_TO_1 = os.getenv("EMAIL_TO_1")
EMAIL_TO_2 = os.getenv("EMAIL_TO_2")
EMAIL_TO_3 = os.getenv("EMAIL_TO_3")
EMAIL_TO_4 = os.getenv("EMAIL_TO_4")
