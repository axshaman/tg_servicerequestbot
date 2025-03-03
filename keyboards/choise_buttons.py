from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton


button_vzlom = KeyboardButton('Узнать, пытались ли взломать')
button_utechka = KeyboardButton('Анализ рисков безопасности')
button_safe = KeyboardButton('Мониторинг')
button_attempts = KeyboardButton('Анализ утечек')
button_invest = KeyboardButton('Расследование')
# button_vzlom = KeyboardButton('1️⃣ Узнать, пытались ли взломать')
# button_utechka = KeyboardButton('2️⃣ Анализ рисков безопасности')
# button_safe = KeyboardButton('3️⃣ Мониторинг')
# button_attempts = KeyboardButton('4️⃣ Анализ')
# button_invest = KeyboardButton('5️⃣ Расследование')
choise = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button_vzlom).add(button_utechka).row(button_attempts, button_safe, button_invest)


button_link = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton('Перейти к оплате 💵 ', url=''))

accoun = InlineKeyboardMarkup(row_width=2)
acc = (InlineKeyboardButton(text='Указать аккаунт📱', callback_data='account'))
accoun.insert(acc)


accoun = InlineKeyboardMarkup(row_width=2)
recv = (InlineKeyboardButton(text='Указать аккаунт📱', callback_data='account'))
accoun.insert(acc)
# choice = InlineKeyboardMarkup(row_width=2)

# accept = InlineKeyboardButton(text='Подтвердить ✅', callback_data='accept')
# choice.insert(accept)


button_vk = KeyboardButton('Вконтакте')
button_inst = KeyboardButton('Instagram')
button_face = KeyboardButton('Facebook')
button_email = KeyboardButton('Email')
button_site = KeyboardButton('WEB-сайты и CMS системы')

# button_vk = KeyboardButton('1️⃣ Вконтакте')
# button_inst = KeyboardButton('2️⃣ Instagram')
# button_face = KeyboardButton('3️⃣ Facebook')
# button_email = KeyboardButton('4️⃣ Email')
# button_site = KeyboardButton('5️⃣ WEB-сайты и CMS системы')

choise2 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(button_vk, button_inst).row(button_face, button_email).add(button_site)


# button_month = KeyboardButton('Ежемесячно за 250 руб/мес')
# button_week = KeyboardButton('Еженедельно за 800 руб/мес')
# button_day = KeyboardButton('Ежедневно за 4500 руб/мес')

# choise3 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button_month).add(button_week).add(button_day)




# markup_request = ReplyKeyboardMarkup(resize_keyboard=True).add(
#     KeyboardButton('Отправить свой контакт ☎️', request_contact=True)
# ).add(
#     KeyboardButton('Отправить свою локацию 🗺️', request_location=True)
# )



button_3000 = InlineKeyboardMarkup(row_width=2)
choise3000 = InlineKeyboardButton(text='Оплатить 3000 руб', callback_data='choise3000')
button_3000.insert(choise3000)

button_300 = InlineKeyboardMarkup(row_width=2)
choise300 = InlineKeyboardButton(text='Оплатить 300 руб', callback_data='choise300')
button_300.insert(choise300)

button_30000 = InlineKeyboardMarkup(row_width=2)
choise30000 = InlineKeyboardButton(text='Оплатить 30000 руб', callback_data='choise30000')
button_30000.insert(choise30000)



choise250 = InlineKeyboardButton(text='Ежемесячно за 250 руб/мес', callback_data='choise250')
choise800 = InlineKeyboardButton(text='Еженедельно за 800 руб/мес', callback_data='choise800')
choise4500 = InlineKeyboardButton(text='Ежедневно за 4500 руб/мес', callback_data='choise4500')

button_change = InlineKeyboardMarkup(row_width=3).row(choise250).row(choise800).row(choise4500)




button_month = KeyboardButton('Ежемесячно за 250 руб/мес')
button_week = KeyboardButton('Еженедельно за 800 руб/мес')
button_day = KeyboardButton('Ежедневно за 4500 руб/мес')

choise3 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button_month).add(button_week).add(button_day)