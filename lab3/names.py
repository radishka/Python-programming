import sys
from bs4 import BeautifulSoup


# Вход: nameYYYY.html, Выход: список начинается с года, продолжается имя-ранг в алфавитном порядке.
# '2006', 'Aaliyah 91', Aaron 57', 'Abagail 895', ' и т.д.
def extr_name(filename):
    with open(filename, "r") as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'lxml')

        table = soup.find("table", summary="Popularity for top 1000")
        input = soup.find("input", id="yob")
        year = input.get("value")

        table_raws = table.find_all("tr")
        names = []

        for i in range(1, len(table_raws) - 2):
            name1 = []
            name2 = []

            raws = table_raws[i].find_all("td")

            name1.append(int(raws[0].text))
            name1.append(raws[1].text)

            name2.append(int(raws[0].text))
            name2.append(raws[2].text)

            names.append(name1)
            names.append(name2)

    names = sorted(names, key=lambda x: x[1])
    names.insert(0, year)

    return names


# для каждого переданного аргументом имени файла, вывести имена  extr_name
# напечатать ТОП-10 муж и жен имен из всех переданных файлов
def main():
    args = sys.argv[1:]
    if not args:
        print('use: [--file] file [file ...]')
        sys.exit(1)

    names = []

    for arg in args:
        result = extr_name(arg)
        print(result)

        result.pop(0)

        for i in range(0, 20):
            sorted_names = sorted(result, key=lambda x: x[0])[i]
            print(str(sorted_names[0]) + " " + str(sorted_names[1]))

        names.extend(result)


if __name__ == '__main__':
    main()
