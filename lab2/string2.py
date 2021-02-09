# 1.
# Вх: строка. Если длина > 3, добавить в конец "ing", 
# если в конце нет уже "ing", иначе добавить "ly".

def v(s):
    if s.endswith('ing') and len(s) > 3:
        s = s + 'ly'
    elif len(s) > 3:
        s = s + 'ing'

    return s


# 2. 
# Вх: строка. Заменить подстроку от 'not' до 'bad'. ('bad' после 'not')
# на 'good'.
# Пример: So 'This music is not so bad!' -> This music is good!

def nb(s):

    start = str.find(s, 'not')
    end = str.rfind(s, 'bad')

    return 'good' + s[end+3:] if start == 0 else s[0:start] + 'good' + s[end+3:]


def test(res, expt):
    print('function return:', res)
    print('supposed to return:', expt)
    print('test passed') if res == expt else print('test failed')


def main():

    test(v('ab'), 'ab')
    test(v('abcd'), 'abcding')
    test(v('abcing'), 'abcingly')

    test(nb('This music is not so bad!'), 'This music is good!')


if __name__ == '__main__':
    main()
