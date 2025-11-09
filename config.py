"""Application configuration helpers."""
from functools import lru_cache
from typing import List, Optional

from pydantic import BaseSettings, EmailStr, Field, validator


class Settings(BaseSettings):
    """Runtime settings loaded from environment variables."""

    bot_token: str = Field(..., env="TOKEN")

    email_password: str = Field(..., env="EMAIL_PASSWORD")
    email_host: str = Field(..., env="HOST")
    email_from: EmailStr = Field(..., env="EMAIL_FROM")

    email_to: List[EmailStr] = Field(default_factory=list, env="EMAIL_TO")
    email_to_1: Optional[EmailStr] = Field(None, env="EMAIL_TO_1")
    email_to_2: Optional[EmailStr] = Field(None, env="EMAIL_TO_2")
    email_to_3: Optional[EmailStr] = Field(None, env="EMAIL_TO_3")
    email_to_4: Optional[EmailStr] = Field(None, env="EMAIL_TO_4")

    robokassa_merchant_login: str = Field("infsectest_ru", env="ROBOKASSA_MERCHANT_LOGIN")
    robokassa_password1: str = Field("qNI1cl89rPWbFMkb9Ls0", env="ROBOKASSA_PASSWORD1")
    robokassa_base_url: str = Field(
        "https://auth.robokassa.ru/Merchant/Index.aspx", env="ROBOKASSA_BASE_URL"
    )

    payment_description_template: str = Field(
        "Оплата {price} руб за оказание услуги: \"{service}\", объект для проверки: {target}",
        env="PAYMENT_DESCRIPTION_TEMPLATE",
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    @property
    def email_recipients(self) -> List[str]:
        """Return a combined, de-duplicated list of e-mail recipients."""

        recipients = [recipient for recipient in self.email_to if recipient]
        for extra in (self.email_to_1, self.email_to_2, self.email_to_3, self.email_to_4):
            if extra and extra not in recipients:
                recipients.append(extra)
        return recipients

    @validator("email_to", pre=True)
    def _split_email_list(cls, value):  # noqa: D401 - short helper
        """Support comma separated values in EMAIL_TO."""

        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value or []


@lru_cache()
def get_settings() -> Settings:
    """Provide a cached settings instance."""

    return Settings()


settings = get_settings()
