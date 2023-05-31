import telebot
import logging
import time
from random import randint
from telebot import types
import pymorphy2
import json

'''file = open('file.txt', 'w')
file.close()'''

API_TOKEN = 'your_API_token_here'

bot = telebot.TeleBot(API_TOKEN)
morph = pymorphy2.MorphAnalyzer()


file = open('file.txt', 'r')
tmp = file.read()
records = {}
glob_results = {}
if tmp != "":
    for i, j in json.loads(tmp).items():
        records[i] = j[0]
        glob_results[i] = j[1]
else:
    records = {}
    glob_results = {}
file.close()
combo = {}
result = {}
flag_run = {}
task = {}
answer_for_task = {}
result_max = {}
max_number = {}


def set_dics(id, user):
    if user not in records:
        records[user] = 0
        glob_results[user] = 0
    combo[user] = 0
    flag_run[id] = 0
    task[id] = ''
    answer_for_task[id] = ''
    result[id] = 0
    result_max[id] = 0
    max_number[id] = 1


def make_str(tmp):
    tmp_str = str(tmp)
    if tmp >= 10000:
        ans = ''
        k = 0
        for i in range(len(tmp_str) - 1, -1, -1):
            ans = tmp_str[i] + ans
            if k % 3 == 2 and i - 1 >= 0:
                ans = ' ' + ans
            k += 1
        tmp_str = ans
    return tmp_str

    return tmp_str


def random_case():
    number = randint(1, 6)
    if number == 1:
        return 'nomn'
    elif number == 2:
        return 'gent'
    elif number == 3:
        return 'datv'
    elif number == 4:
        return 'accs'
    elif number == 5:
        return 'ablt'
    else:
        return 'loct'


def random_gender():
    number = randint(1, 3)
    if number == 1:
        return 'masc'
    elif number == 2:
        return 'femn'
    else:
        return 'neut'


def case_name(case):
    if case == 'nomn':
        return 'именительный'
    elif case == 'gent':
        return 'родительный'
    elif case == 'datv':
        return 'дательный'
    elif case == 'accs':
        return 'винительный'
    elif case == 'ablt':
        return 'творительный'
    else:
        return 'предложный'


def gender_name(gender):
    if gender == 'masc':
        return 'мужского'
    elif gender == 'femn':
        return 'женского'
    else:
        return 'среднего'


def to_case(arr, case):
    ans = []
    for i in arr:
        word = morph.parse(i)[0]
        for j in morph.parse(i):
            if 'NUMR' in j.tag:
                word = j
                break
        ans.append(word.inflect({case}).word)
    return ans


def agree(arr, number):
    ans = []
    for i in arr:
        word = morph.parse(i)[0]
        ans.append(word.make_agree_with_number(number).word)
    return ans


def from_number_to_string(number, case, gender):
    a = ['', 'один', 'два', 'три', 'четыре', 'пять', 'шесть',
         'семь', 'восемь', 'девять']
    b = ['десять', 'одиннадцать', 'двенадцать', 'тринадцать',
         'четырнадцать', 'пятнадцать', 'шестнадцать',
         'семнадцать', 'восемнадцать', 'девятнадцать']
    c = ['двадцать', 'тридцать', 'сорок', 'пятьдесят',
         'шестьдесят', 'семьдесят', 'восемьдесят', 'девяносто']
    d = ['сто', 'двести', 'триста', 'четыреста', 'пятьсот',
         'шестьсот', 'семьсот', 'восемьсот', 'девятьсот']
    len_number = len(str(number))
    if len_number == 1:
        if number == 1:
            if gender == 'masc':
                return to_case(['один'], case)
            elif gender == 'femn':
                return to_case(['одна'], case)
            else:
                return to_case(['одно'], case)
        elif number == 2:
            if gender == 'masc' or gender == 'neut':
                return to_case(['два'], case)
            else:
                return to_case(['две'], case)
        else:
            return to_case([a[number]], case)
    elif len_number == 2:
        if number <= 19:
            return to_case([b[number - 10]], case)
        elif number % 10 == 0:
            return to_case([c[number // 10 - 2]], case)
        else:
            return to_case([c[number // 10 - 2]] + from_number_to_string(number % 10, case, gender), case)
    elif len_number == 3:
        if number % 100 == 0:
            return to_case([d[number // 100 - 1]], case)
        else:
            return to_case([d[number // 100 - 1]] + from_number_to_string(number % 100, case, gender), case)
    elif len_number <= 6:
        if number % 1000 == 0:
            if case == 'nomn' or case == 'accs':
                return from_number_to_string(number // 1000, case, 'femn') + agree(['тысяча'], number // 1000)
            else:
                return from_number_to_string(number // 1000, case, 'femn') + to_case(
                    agree(to_case(['тысяча'], case), number // 1000), case)
        else:
            if case == 'nomn' or case == 'accs':
                return from_number_to_string(number // 1000, case, 'femn') + agree(['тысяча'],
                                                                                   number // 1000) + from_number_to_string(
                    number % 1000, case, gender)
            else:
                return from_number_to_string(number // 1000, case, 'femn') + to_case(
                    agree(to_case(['тысяча'], case), number // 1000), case) + from_number_to_string(number % 1000, case,
                                                                                                    gender)
    elif len_number <= 9:
        if number % 1000000 == 0:
            if case == 'nomn' or case == 'accs':
                return from_number_to_string(number // 1000000, case, 'masc') + agree(['миллион'], number // 1000000)
            else:
                return from_number_to_string(number // 1000000, case, 'masc') + to_case(
                    agree(to_case(['миллион'], case), number // 1000000), case)
        else:
            if case == 'nomn' or case == 'accs':
                return from_number_to_string(number // 1000000, case, 'masc') + agree(['миллион'],
                                                                                      number // 1000000) + from_number_to_string(
                    number % 1000000, case, gender)
            else:
                return from_number_to_string(number // 1000000, case, 'masc') + to_case(
                    agree(to_case(['миллион'], case), number // 1000000), case) + from_number_to_string(
                    number % 1000000, case, gender)
    elif len_number <= 12:
        if number % 1000000000 == 0:
            if case == 'nomn' or case == 'accs':
                return from_number_to_string(number // 1000000000, case, 'masc') + agree(['миллиард'],
                                                                                         number // 1000000000)
            else:
                return from_number_to_string(number // 1000000000, case, 'masc') + to_case(
                    agree(to_case(['миллиард'], case), number // 1000000000), case)
        else:
            if case == 'nomn' or case == 'accs':
                return from_number_to_string(number // 1000000000, case, 'masc') + agree(['миллиард'],
                                                                                         number // 1000000000) + from_number_to_string(
                    number % 1000000000, case, gender)
            else:
                return from_number_to_string(number // 1000000000, case, 'masc') + to_case(
                    agree(to_case(['миллиард'], case), number // 1000000000), case) + from_number_to_string(
                    number % 1000000000, case, gender)


def generate_task(message):
    while True:
        id = message.chat.id
        tmp = randint(5, max_number[id])
        tmp_str = make_str(tmp)
        case = random_case()
        gender = random_gender()
        print(message.from_user.first_name, message.from_user.last_name, tmp_str, case, gender)

        x = ' '.join(from_number_to_string(tmp, case, gender))
        question = 'Напишите число ' + tmp_str + ' в форме ' + ' '.join(to_case([case_name(case)], 'gent')) + ' падежа'
        if ((case == 'accs' or case == 'nomn') and (tmp % 10 == 2 and tmp % 100 != 12)) or (
                tmp % 10 == 1 and tmp % 100 != 11):
            question += ', ' + gender_name(gender) + ' рода'
        question += ' словами (без цифр).'
        if case == 'loct':
            question += ' Предлог писать не нужно.'

        if question != task[id]:
            task[id] = question
            answer_for_task[id] = x
            break


def generate_task_cooler(max_number):
    global task, answer_for_task
    nouns_masc_anim = ["друг", "брат", "сын", "знакомый"]
    nouns_masc_inanim = ["стол", "стул", "шкаф", "торт"]
    nouns_fem_anim = ["подружка", "сестра", "дочь", "знакомая"]
    nouns_masc_inanim = ["табуретка", "тумбочка", "машина", "квартира"]
    while True:
        tmp = randint(1, max_number)
        tmp_str = str(tmp)

        '''tmp_str = ''
        for i in range(len(str(tmp))):
            tmp_str = str(tmp)[-i] + tmp_str
            if i % 3 == 2 and i + 1 < len(str(tmp)):
                tmp_str = '.' + tmp_str'''
        number_of_case = randint(1, 4)
        num_str = from_number_to_string(tmp)
        question = ''
        x = ''
        if number_of_case == 1:
            x = ' '.join(to_case(num_str, 'gent'))
            question = f'Поставьте {tmp_str} в родительный падеж.'
        elif number_of_case == 2:
            x = ' '.join(to_case(num_str, 'datv'))
            question = f'Поставьте {tmp_str} в дательный падеж.'
        elif number_of_case == 3:
            x = ' '.join(to_case(num_str, 'accs'))
            question = f'Поставьте {tmp_str} в винительный падеж.'
        elif number_of_case == 4:
            x = ' '.join(to_case(num_str, 'ablt'))
            question = f'Поставьте {tmp_str} в творительный падеж.'
        else:
            x = ' '.join(to_case(num_str, 'loct'))
            question = f'Поставьте {tmp_str} в предложный падеж.'
        if question != task:
            task = question
            answer_for_task = x
            break


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, "Я бот, помогающий тренировать правописание числительных и их склонение.\n"
                                      "Правила склонения числительных можно получить по команде /rules.\n"
                                      "У меня есть четыре уровня тренировки.\n"
                                      "Простой вызывается командой /game1, и в нем потребуется склонять числа меньше тысячи;\n"
                                      "cредний вызывается командой /game2, и в нем потребуется склонять числа меньше миллиона;\n"
                                      "cложный вызывается командой /game3, и в нем потребуется склонять числа меньше миллиарда;\n"
                                      "oчень сложный вызывается командой /game4, и в нем потребуется склонять числа меньше триллиона.\n"
                                      "Чтобы завершить тренировку, вызовите /stop.\n"
                                      "А ещё командой /results можно увидеть таблицу с результатами всех пользователей.\n")


@bot.message_handler(commands=['start'])
def starting(message):
    set_dics(id, message.from_user.first_name)
    bot.send_message(message.chat.id, "Привет, " + message.from_user.first_name + '!')
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAALwrF7k_QnoF-kAAQEKhLSJlu0CUWUdgQACNQEAAjDUnRG0uDX9ZqC2fBoE')
    time.sleep(2)
    bot.send_message(message.chat.id, "Я бот, помогающий тренировать правописание числительных и их склонение.\n"
                                      "Правила склонения числительных можно получить по команде /rules.\n"
                                      "У меня есть четыре уровня тренировки.\n"
                                      "Простой вызывается командой /game1, и в нем потребуется склонять числа меньше тысячи;\n"
                                      "cредний вызывается командой /game2, и в нем потребуется склонять числа меньше миллиона;\n"
                                      "cложный вызывается командой /game3, и в нем потребуется склонять числа меньше миллиарда;\n"
                                      "oчень сложный вызывается командой /game4, и в нем потребуется склонять числа меньше триллиона.\n"
                                      "Чтобы завершить тренировку, вызовите /stop.\n"
                                      "А ещё командой /results можно увидеть таблицу с результатами всех пользователей.\n")

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == '1':
        bot.send_photo(call.message.chat.id, open('ChisloBot-1-4.png', 'rb'));

    elif call.data == '2':
        bot.send_photo(call.message.chat.id, open('ChisloBot-5-20+30.png', 'rb'));
    elif call.data == '3':
        bot.send_photo(call.message.chat.id, open('ChisloBot-50+60+70+80.png', 'rb'));
    elif call.data == '4':
        bot.send_photo(call.message.chat.id, open('ChisloBot-40+90+100.png', 'rb'));
    elif call.data == '5':
        bot.send_photo(call.message.chat.id, open('ChisloBot-100s.png', 'rb'));
    elif call.data == '6':
        bot.send_photo(call.message.chat.id, open('ChisloBot-999-.png', 'rb'));
    elif call.data == '7':
        bot.send_photo(call.message.chat.id, open('ChisloBot-1000+.png', 'rb'));
    elif call.data == '8':
        bot.send_message(call.message.chat.id, 'А теперь готовы начать тренировку? Напомню:\n'
                                               "У меня есть четыре уровня тренировки.\n"
                                      "Простой вызывается командой /game1, и в нем потребуется склонять числа меньше тысячи;\n"
                                      "cредний вызывается командой /game2, и в нем потребуется склонять числа меньше миллиона;\n"
                                      "cложный вызывается командой /game3, и в нем потребуется склонять числа меньше миллиарда;\n"
                                      "oчень сложный вызывается командой /game4, и в нем потребуется склонять числа меньше триллиона.\n"
                                      "Чтобы завершить тренировку, вызовите /stop.\n")
    else:
        bot.send_message(call.message.chat.id, 'Что вы натворили!!!')

@bot.message_handler(commands=['rules'])
def print_rules(message):
    keyboard = types.InlineKeyboardMarkup()
    key1 = types.InlineKeyboardButton(text='1, 2, 3 и 4', callback_data='1')
    key2 = types.InlineKeyboardButton(text='5 – 20 и 30', callback_data='2')
    key3 = types.InlineKeyboardButton(text='50, 60, 70, 80', callback_data='3')
    key4 = types.InlineKeyboardButton(text='40, 90, 100', callback_data='4')
    key5 = types.InlineKeyboardButton(text='сотни', callback_data='5')
    key6 = types.InlineKeyboardButton(text='составные меньше 1000', callback_data='6')
    key7 = types.InlineKeyboardButton(text='1000 и больше', callback_data='7')

    key_return = types.InlineKeyboardButton(text='Назад', callback_data='8')
    keyboard.add(key1)
    keyboard.add(key2)
    keyboard.add(key3)
    keyboard.add(key4)
    keyboard.add(key5)
    keyboard.add(key6)
    keyboard.add(key7)
    keyboard.add(key_return)
    bot.send_message(message.chat.id, 'Числительные делятся на порядковые, количественные и собирательные.\n'
                                      'Порядковые обозначают номер – например, "второй", "пятьдесят седьмой" или "сто семьдесят девятый".\n'
                                      'У порядковых числительных склоняется только последнее слово и склоняется как обычное прилагательное ("белого" – "второго", "белым" – "пятьдесят седьмым)".\n'
                                      'Собирательные числительные пока не описаны в этом боте, обязательно добавим.\n'
                                      'А количественные числительные можно поделить по склонению на несколько групп:\n', reply_markup=keyboard)




@bot.message_handler(commands=['results'])
def print_table_res(message):
    file = open('file.txt', 'r')
    if message.chat.id not in flag_run:
        set_dics(message.chat.id, message.from_user.first_name)
    if flag_run[message.chat.id]:
        bot.send_message(message.chat.id, "Нет уж, сначала доиграйте, а потом смотрите результаты.")
        return
    tmp1 = file.read()
    tmp = []
    if tmp1 != "":
        for i, j in json.loads(tmp1).items():
            tmp.append((i, j))
    else:
        tmp = []
    if len(tmp) == 0:
        bot.send_message(message.chat.id, 'Никто ещё ничего не сделал.')
    else:
        tmp.sort(key=lambda x: x[1][0])
        mes = "Имя пользователя      Подряд правильных      Всего правильных\n"
        for i in tmp:
            mes += f'{i[0]}' + ' ' * (33 - len(i[0]) - len(str(i[1][0])) // 2)\
                   + f'{i[1][0]}' + ' ' * (46 - len(str(i[1][0])) // 2 - len(str(i[1][1])) // 2)\
                   + f'{i[1][1]}'
            # mes += f'{i[0]}:          {i[1][0]},                     {i[1][1]}\n'
        bot.send_message(message.chat.id, mes + '\n')


@bot.message_handler(commands=['game1'])
def start_game1(message):
    set_dics(message.chat.id, message.from_user.first_name)
    if (flag_run[message.chat.id]):
        bot.send_message(message.chat.id,
                         'Вы еще не завершили предыдущую тренировку.\n Завершите её командой /stop и снова начните эту.')
        return
    bot.send_message(message.chat.id,
                     'Начинаем простую тренировку (1-й уровень). Завершить её можно командой /stop.\nУдачи!')
    time.sleep(1)
    flag_run[message.chat.id] = 1
    result_max[message.chat.id] = 0
    result[message.chat.id] = 0
    max_number[message.chat.id] = 999
    generate_task(message)
    bot.send_message(message.chat.id, task[message.chat.id])


@bot.message_handler(commands=['game2'])
def start_game2(message):
    set_dics(message.chat.id, message.from_user.first_name)
    if (flag_run[message.chat.id]):
        bot.send_message(message.chat.id,
                         'Вы еще не завершили предыдущую тренировку.\n Завершите её командой /stop и снова начните эту.')
        return
    bot.send_message(message.chat.id,
                     'Начинаем тренировку средней сложности (2-й уровень). Завершить её можно командой /stop.\nУдачи!')
    time.sleep(1)
    flag_run[message.chat.id] = 1
    result_max[message.chat.id] = 0
    result[message.chat.id] = 0
    max_number[message.chat.id] = 999999
    generate_task(message)
    bot.send_message(message.chat.id, task[message.chat.id])


@bot.message_handler(commands=['game3'])
def start_game3(message):
    set_dics(message.chat.id, message.from_user.first_name)
    if (flag_run[message.chat.id]):
        bot.send_message(message.chat.id,
                         'Вы еще не завершили предыдущую тренировку.\n Завершите её командой /stop и снова начните эту.')
        return
    bot.send_message(message.chat.id,
                     'Начинаем сложную тренировку (3-й уровень). Завершить её можно командой /stop.\nУдачи!')
    time.sleep(1)
    flag_run[message.chat.id] = 1
    result_max[message.chat.id] = 0
    result[message.chat.id] = 0
    max_number[message.chat.id] = 999999999
    generate_task(message)
    bot.send_message(message.chat.id, task[message.chat.id])


@bot.message_handler(commands=['game4'])
def start_game4(message):
    set_dics(message.chat.id, message.from_user.first_name)
    if (flag_run[message.chat.id]):
        bot.send_message(message.chat.id,
                         'Вы еще не завершили предыдущую тренировку.\n Завершите её командой /stop и снова начните эту.')
        return
    bot.send_message(message.chat.id,
                     'Начинаем тренировку повышенной сложности (4-й уровень). Завершить её можно командой /stop.\nУдачи!')
    time.sleep(1)
    flag_run[message.chat.id] = 1
    result_max[message.chat.id] = 0
    result[message.chat.id] = 0
    max_number[message.chat.id] = 999999999999
    generate_task(message)
    bot.send_message(message.chat.id, task[message.chat.id])


@bot.message_handler(commands=['stop'])
def stop_game(message):
    id = message.chat.id
    file = open("file.txt", "w")
    tmp = {}
    for i in records.keys():
        tmp[i] = [records[i], glob_results[i]]
    file.write(json.dumps(tmp))
    file.close()
    if (not flag_run[id]):
        return
    bot.send_message(id, 'Тренировка окончена.')
    if result_max[id] == 0:
        bot.send_message(id, 'Вы не ответили ни на один вопрос.')
    elif result[id] == 0:
        bot.send_message(id, 'Вы не ответили верно ни на один вопрос из ' + str(result_max[id]))
    elif result[id] / result_max[id] < 0.25:
        bot.send_message(id, 'Вы ответили верно на ' + str(result[id]) + ' ' + agree(['вопрос'], result[id])[
            0] + ' из ' + str(result_max[id]) + '.\n' + 'Можно и лучше.')
    elif result[id] / result_max[id] < 0.5:
        bot.send_message(id, 'Вы ответили верно на ' + str(result[id]) + ' ' + agree(['вопрос'], result[id])[
            0] + ' из ' + str(result_max[id]) + '.\n' + 'Можно и лучше.')
    elif result[id] / result_max[id] < 0.75:
        bot.send_message(id, 'Вы ответили верно на ' + str(result[id]) + ' ' + agree(['вопрос'], result[id])[
            0] + ' из ' + str(result_max[id]) + '.\n' + 'Неплохо! В следующий раз должно быть ещё лучше.')
    elif result[id] / result_max[id] < 1:
        bot.send_message(id, 'Вы ответили верно на ' + str(result[id]) + ' ' + agree(['вопрос'], result[id])[
            0] + ' из ' + str(result_max[id]) + '.\n' + 'Хорошо, даже очень!')
    else:
        bot.send_message(message.chat.id, 'Вы ответили верно на все вопросы – ' + str(result[id]) + ' / ' + str(
            result_max[id]) + '.\n' + 'Идеально!')
    flag_run[id] = 0


@bot.message_handler(content_types=['text'])
def check_answer(message):
    id = message.chat.id
    if id not in flag_run:
        set_dics(id, message.from_user.first_name)
    if flag_run[id] == 1:
        answer_for_task[id] = answer_for_task[id].lower()
        message.text = message.text.lower()
        answer_for_task[id] = answer_for_task[id].replace('ё', 'е')
        message.text = message.text.replace('ё', 'е')
        answer_for_task[id] = answer_for_task[id].replace('восьмью', 'восемью')
        message.text = message.text.replace('восьмью', 'восемью')
        if answer_for_task[id] == message.text:
            combo[message.from_user.first_name] += 1
            if combo[message.from_user.first_name] \
                    > records[message.from_user.first_name]:
                records[message.from_user.first_name]\
                    = combo[message.from_user.first_name]
            result[id] += 1
            glob_results[message.from_user.first_name] += 1
            result_max[id] += 1
            bot.send_message(id, f'Правильно! Уже {result[id]} {morph.parse("правильный")[0].make_agree_with_number(result[id]).word} {morph.parse("ответ")[0].make_agree_with_number(result[id]).word}.')
            generate_task(message)
            time.sleep(1)
            bot.send_message(id, task[id])
        else:
            result_max[id] += 1
            combo[message.from_user.first_name] = 0
            bot.send_message(id, 'К сожалению, это неверно. Правильный ответ:')
            bot.send_message(id, answer_for_task[id])
            generate_task(message)
            bot.send_message(id, task[id])
    else:
        bot.send_message(id, 'Если что-то непонятно, вызовите /help')

print('Поехали!')

def congratulate_grisha():
    misha_id = 839506170
    grisha_id = 1198720177
    bot.send_message(grisha_id, "Привет, дорогой Гриша!\nС днём рождения!")
    bot.send_sticker(grisha_id, "CAACAgIAAxkBAAEHcXRj0WT7akHhMZZ8oelUNmy2JUBd8gACWwAD-tTmHWOVBw8epntdLQQ")
    time.sleep(10)
    congratulation_text = "В начале 9 класса ты уезжал на сборы по физике, а я — в Сириус. Это казалось долгим.\nА теперь мы буквально не виделись целый год (и три дня). Но всё же, спасибо тебе за те времена:\nза пельмени в столовой,\n1 = 0 = палочку,\nи вот за ЧислоБота."
    congratulation_text += "\nА теперь нам ещё и по 10000 лет. Много как-то, да?"
    congratulation_text += "\nНу да ладно, это не важно. Пусть будет больше хорошего и меньше плохого, успехов тебе, и, надеюсь, мы всё-таки встретимся!"
    bot.send_message(grisha_id,  congratulation_text)
    time.sleep(10)
    bot.send_photo(grisha_id, open('GrishaMishaPhoto.jpg', 'rb'));
congratulate_grisha()
bot.polling(none_stop=True)

file.close()
