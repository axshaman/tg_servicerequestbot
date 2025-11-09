"""Domain catalog with supported services and social networks."""
from dataclasses import dataclass
from typing import Dict, Iterable, Optional, Tuple


def _normalise(value: str) -> str:
    return value.strip().lower().replace("ё", "е")


@dataclass(frozen=True)
class SocialNetwork:
    code: str
    label: str
    aliases: Tuple[str, ...]

    def matches(self, candidate: str) -> bool:
        candidate_normalised = _normalise(candidate)
        return candidate_normalised in {self.code, *(alias for alias in self.aliases)}


@dataclass(frozen=True)
class SubscriptionPlan:
    code: str
    label: str
    price: int
    description: str


@dataclass(frozen=True)
class ServiceOption:
    code: str
    label: str
    price: Optional[int]
    description: str
    payment_hint: str
    phone_prompt: str
    aliases: Tuple[str, ...]
    subscription_plans: Tuple[SubscriptionPlan, ...] = ()

    def requires_plan(self) -> bool:
        return bool(self.subscription_plans)


DEFAULT_PAYMENT_HINT = (
    "Оплата осуществляется через авторизованный сервис Робокасса, являющийся одним из ведущих в РФ, что гарантирует безопасность"
    " платежей ⚒"
)
DEFAULT_PHONE_PROMPT = "Введите номер телефона ☎️ привязанный к выбранному аккаунту"

SOCIAL_NETWORKS: Tuple[SocialNetwork, ...] = (
    SocialNetwork("вконтакте", "Вконтакте", ("vk", "вк", "vkontakte")),
    SocialNetwork("instagram", "Instagram", ("inst", "инстаграм", "instagram")),
    SocialNetwork("facebook", "Facebook", ("fb", "фейсбук")),
    SocialNetwork("email", "Email", ("e-mail", "почта")),
    SocialNetwork(
        "web-сайты и cms системы",
        "WEB-сайты и CMS системы",
        ("web", "сайт", "cms", "web-сайты", "web-сайты и cms системы"),
    ),
)

SUBSCRIPTION_PLANS: Tuple[SubscriptionPlan, ...] = (
    SubscriptionPlan("monthly", "Ежемесячно за 250 руб/мес", 250, "Базовый мониторинг с отчетом раз в месяц."),
    SubscriptionPlan("weekly", "Еженедельно за 800 руб/мес", 800, "Подробные отчеты каждую неделю."),
    SubscriptionPlan("daily", "Ежедневно за 4500 руб/мес", 4500, "Максимальная скорость реакции и ежедневные отчеты."),
)

SERVICE_OPTIONS: Tuple[ServiceOption, ...] = (
    ServiceOption(
        code="intrusion_check",
        label="Узнать, пытались ли взломать",
        price=3000,
        description=(
            "Я помогу узнать, заказывали ли взлом Вашего аккаунта в Darknet или у профессиональных хакеров 🖥. "
            "Предоставлю Вам информацию по целевым атакам, их датам и успешности."
        ),
        payment_hint=DEFAULT_PAYMENT_HINT,
        phone_prompt=DEFAULT_PHONE_PROMPT,
        aliases=("узнать, пытались ли взломать", "взлом", "инцидент"),
    ),
    ServiceOption(
        code="security_risk",
        label="Анализ рисков безопасности",
        price=300,
        description="Будет произведен анализ Вашего аккаунта на возможные риски несанкционированного доступа 🗝",
        payment_hint=DEFAULT_PAYMENT_HINT,
        phone_prompt=DEFAULT_PHONE_PROMPT,
        aliases=("анализ рисков безопасности", "риски", "безопасность"),
    ),
    ServiceOption(
        code="leak_analysis",
        label="Анализ утечек",
        price=300,
        description="Проверьте, взламывали ли Ваш аккаунт и есть ли риск утечки данных",
        payment_hint=DEFAULT_PAYMENT_HINT,
        phone_prompt=DEFAULT_PHONE_PROMPT,
        aliases=("анализ утечек", "утечки", "утечка"),
    ),
    ServiceOption(
        code="monitoring",
        label="Мониторинг",
        price=None,
        description=(
            "Укажите периодичность мониторинга информационной безопасности Вашего аккаунта. "
            "Отчеты будут предоставляться в формате Secret Chat. Первый отчет через 2 дня после заказа 👇"
        ),
        payment_hint=DEFAULT_PAYMENT_HINT,
        phone_prompt=DEFAULT_PHONE_PROMPT,
        aliases=("мониторинг", "наблюдение"),
        subscription_plans=SUBSCRIPTION_PLANS,
    ),
    ServiceOption(
        code="investigation",
        label="Расследование",
        price=30000,
        description=(
            "Если у Вас произошел инцидент несанкционированного доступа 🕷. "
            "Мы поможем найти злоумышленника и предоставим расширенные сведения, которые помогут разобраться в ситуации."
        ),
        payment_hint=DEFAULT_PAYMENT_HINT,
        phone_prompt=DEFAULT_PHONE_PROMPT,
        aliases=("расследование", "инцидент расследование", "investigation"),
    ),
)


def _build_alias_map(items: Iterable) -> Dict[str, object]:
    alias_map: Dict[str, object] = {}
    for item in items:
        raw_aliases = {item.code, item.label}
        if isinstance(item, (SocialNetwork, ServiceOption)):
            raw_aliases.update(item.aliases)
        for value in raw_aliases:
            alias_map[_normalise(value)] = item
    return alias_map


SOCIAL_NETWORK_MAP = _build_alias_map(SOCIAL_NETWORKS)
SERVICE_OPTION_MAP = _build_alias_map(SERVICE_OPTIONS)


def resolve_social_network(candidate: str) -> Optional[SocialNetwork]:
    return SOCIAL_NETWORK_MAP.get(_normalise(candidate))


def resolve_service_option(candidate: str) -> Optional[ServiceOption]:
    return SERVICE_OPTION_MAP.get(_normalise(candidate))
