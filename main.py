import telebot
from bs4 import BeautifulSoup
import requests
import urllib
import lxml
dletkod = {}
abc = ('й ц у к е н г ш щ з х ъ ф ы в а п р о л д ж э я ч с м и т ь б ю')
cba = ('E9%F6%F3%EA%E5%ED%E3%F8%F9%E7%F5%FA%F4%FB%E2%E0%EF%F0%EE%EB%E4%E6%FD%FF%F7%F1%EC%E8%F2%FC%E1%FE')
cba = cba.split('%')
for i in enumerate(cba):
    i = i[0]
    cba[i] = '%' + cba[i]
abc = abc.split(' ')
for (letter, kod) in zip(abc, cba):
    dletkod[letter] = kod
bot = telebot.TeleBot("1636066224:AAHbWsMnOTsNYUGScjo2dpugBOMaf0bp0R8")
@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.send_message(message.from_user.id, 'Для поиска в запросе ОБЯЗАТЕЛЬНО должно присутствовать НАЗВАНИЕ стиха, '
                                           'вводите свой запрос отправляете и вуаля')
@bot.message_handler(content_types=['text'])
def welcome(message):
    all_text = ''
    xxx = ''
    i = 1
    mt = message.text.lower()
    for let in mt:
        if let == ' ':
            xxx += '+'
        else:
            try:
                xxx += dletkod[let]
            except Exception as e:
                pass
    url = "https://ilibrary.ru/search.phtml?q=" + xxx
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "lxml")
    #print(soup.prettify())
    try:
        xxx = soup.find('li').find('a').get('href')
    except Exception as e:
        bot.send_message(message.from_user.id, 'Ничо не нашлось')
    else:
        url = "https://ilibrary.ru" + xxx
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "lxml")
        all_text = all_text \
                   + '*' + soup.find('div', 'author').get_text() + '*\n\n' \
                   + '*' +soup.find('div', 'title').get_text() + '*\n\n'
        for text in soup.find_all('span', 'pmm'):
            all_text = all_text + str(i) + text.get_text() + '\n'
            i += 1
        print(all_text)
        if len(all_text) >= 4000:
             while len(all_text) > 0:
                 try:
                     bot.send_message(message.from_user.id, all_text[:4000], parse_mode="MARKDOWN")
                     all_text = all_text[4000:]
                 except Exception as e:
                     bot.send_message(message.from_user.id, 'Попробуйте изменить запрос (например указать автора)')
                     pass
        else:
            try:
                bot.send_message(message.from_user.id, all_text, parse_mode="MARKDOWN")
            except Exception as e:
                bot.send_message(message.from_user.id, 'Попробуйте изменить запрос (например указать автора)')
                pass
bot.polling()
