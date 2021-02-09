# 1.
# Вх: список строк, Возвр: кол-во строк
# где строка > 2 символов и первый символ == последнему

def me(words):
    count = 0
    strings = words.split(' ')

    for s in strings:
        if len(s) > 2 and s[0] == s[-1]:
            count += 1

    return count


# 2. 
# Вх: список строк, Возвр: список со строками (упорядочено)
# за искл всех строк начинающихся с 'x', которые попадают в начало списка.
# ['tix', 'xyz', 'apple', 'xacadu', 'aabbbccc'] -> ['xacadu', 'xyz', 'aabbbccc', 'apple', 'tix']

def fx(words):
    xList = []
    list = []

    for element in words:
        if element[0] == 'x':
            xList.append(element)
        else:
            list.append(element)

    return sorted(xList) + sorted(list)


# 3. 
# Вх: список непустых кортежей, 
# Возвр: список сортир по возрастанию последнего элемента в каждом корт.
# [(1, 7), (1, 3), (3, 4, 5), (2, 2)] -> [(2, 2), (1, 3), (3, 4, 5), (1, 7)]

def sortCortege(corteges):
    return sorted(corteges, key=lambda cortege: cortege[-1])


def test(res, expt):
    print('function return:', res)
    print('supposed to return:', expt)
    print('test passed') if res == expt else print('test failed')


def main():
    test(me('one two three nan'), 1)
    test(fx(['tix', 'xyz', 'apple', 'xacadu', 'aabbbccc']), ['xacadu', 'xyz', 'aabbbccc', 'apple', 'tix'])
    test(sortCortege([(1, 7), (1, 3), (3, 4, 5), (2, 2)]), [(2, 2), (1, 3), (3, 4, 5), (1, 7)])


if __name__ == '__main__':
    main()
