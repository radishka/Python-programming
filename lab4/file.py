"""
Прочитать из файла (имя - параметр командной строки)
все слова (разделитель пробел)

Создать "Похожий" словарь который отображает каждое слово из файла
на список всех слов, которые следуют за ним (все варианты).

Список слов может быть в любом порядке и включать повторения.
например "and" ['best", "then", "after", "then", ...] 

Считаем , что пустая строка предшествует всем словам в файле.

С помощью "Похожего" словаря сгенерировать новый текст
похожий на оригинал.
Т.е. напечатать слово - посмотреть какое может быть следующим 
и выбрать случайное.

В качестве теста можно использовать вывод программы как вход.парам. для следующей копии
(для первой вход.парам. - файл)

Файл:
He is not what he should be
He is not what he need to be
But at least he is not what he used to be
  (c) Team Coach


"""

import random
import sys


def mem_dict(filename):
    with open(str(filename), encoding='utf-8') as f:
        values = f.read().split()
        for value in values:
            values[values.index(value)] = value.lower()

        unique_values = list(set(values))

        dictionary = {}

        for value in unique_values:
            copy_values = unique_values.copy()
            copy_values.remove(value)
            dictionary[value] = copy_values

        previous_word = unique_values[random.randrange(0, len(dictionary) - 1, 1)]
        print(previous_word.title(), end='')

        for i in range(0, len(dictionary)):
            index = random.randrange(0, len(dictionary) - 2, 1)
            word = dictionary[previous_word][index]
            print(' ' + word, end='')
            previous_word = word
        print('.')

    return


def main():
    args = sys.argv[1:]
    if not args:
        print('use: [--file] file [file ...]')
        sys.exit(1)

    for arg in args:
        try:
            mem_dict(arg)
        except FileNotFoundError:
            print('file not found:', arg)
        except PermissionError:
            print('permission denied:', arg)


if __name__ == '__main__':
    main()
