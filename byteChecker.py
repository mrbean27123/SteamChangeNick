import ctypes

from loguru import logger

from settings import settings


def replace_russian_with_english(text):
    # Словарь соответствий русских букв английским
    mapping = {
        'А': 'A',
        'В': 'B',
        'Е': 'E',
        'З': '3',
        'К': 'K',
        'М': 'M',
        'Н': 'H',
        'О': 'O',
        'Р': 'P',
        'С': 'C',
        'Т': 'T',
        'Х': 'X',
        'І': 'I',
        'а': 'a',
        'е': 'e',
        'о': 'o',
        'р': 'p',
        'с': 'c',
        'у': 'y',
        'х': 'x',
        'і': 'i',
    }

    # Замена букв в тексте
    result = "".join([mapping.get(char, char) for char in text])
    return result


if __name__ == "__main__":
    counter = 0
    not_corrected_nick = []
    for text in settings.nick_list:
        text_converted = replace_russian_with_english(text)
        print(text + " " + str(len(text.encode('utf-8'))))
        print(text_converted + " " + str(len(text_converted.encode('utf-8'))))
        if len(text_converted.encode('utf-8')) > 32:
            logger.error(text_converted + " " + str(len(text_converted.encode('utf-8'))))
            counter += 1
            not_corrected_nick.append(text_converted + " " + str(len(text_converted.encode('utf-8'))))
    logger.debug(f"Не влезло: {counter}")
    result_nick = "\n".join(not_corrected_nick)
    ctypes.windll.user32.MessageBoxW(0, f"Не влезло: {counter}\n\n{result_nick}", settings.title, 16)