# 1. 
# Вх: список чисел, Возвр: список чисел, где 
# повторяющиеся числа урезаны до одного 
# пример [0, 2, 2, 3] returns [0, 2, 3]. 

def rm_adj(nums):
    return list(sorted(set(nums)))


# 2. Вх: Два списка упорядоченных по возрастанию, Возвр: новый отсортированный объединенный список

def unite_and_sort(nums1, nums2):
    return sorted(nums1 + nums2)


def test(res, expt):
    print('function return:', res)
    print('supposed to return:', expt)
    print('test passed') if res == expt else print('test failed')


def main():
    test(rm_adj([0, 2, 2, 3]), [0, 2, 3])

    test(unite_and_sort([0, 2, 2, 3], [1, 3, 4, 3]), [0, 1, 2, 2, 3, 3, 3, 4])


if __name__ == '__main__':
    main()
