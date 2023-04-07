from collections import Counter
import sys
import pickle

alp = ['\n', ' ', '!', '"', "'", '(', ')', '*', ',', '-', '.', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':',
       ';', '<', '=', '>', '?', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
       'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '\\', '^', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
       'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж',
       'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь',
       'Э', 'Ю', 'Я', 'Ё', 'а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с',
       'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я', 'ё']

typ = sys.argv[1][1]
file = sys.argv[2][:-4]
vigen = False
try:
    vigen = sys.argv[3]
except IndexError:
    pass


def rekod(kod):  # Меняет местами ключи и значения
    res = {}

    for key, val in kod.items():
        res[val] = key

    return res


def detext(f):  # Получение текста
    txt = [ord(i) for i in f.decode('latin-1')]

    return txt


def vigenere(txt, key):  # Шифрование Виженера
    result = ''
    for i, val in enumerate(txt):
        result += alp[(alp.index(val) + alp.index(key[i % len(key)])) % len(alp)]

    return result


def devigenere(txt, key):  # Дешифрование Виженера
    result = ''
    for i, val in enumerate(txt):
        result += alp[(alp.index(val) - alp.index(key[i % len(key)]) + len(alp)) % len(alp)]

    return result


def huffman(txt):  # Кодирование Хаффмана
    d = dict(Counter(txt).most_common())

    def tree(dictionary):  # Рекурсивное строительство дерева
        m = Counter(dictionary).most_common()[:-3:-1]
        del dictionary[m[0][0]]
        del dictionary[m[1][0]]
        dictionary[(m[0], m[1])] = m[0][1] + m[1][1]
        if len(d) > 1:
            return tree(d)
        else:
            return Counter(dictionary).most_common()[0]

    tree = tree(d)
    k = {}

    def kod(t, num=''):  # Получение кода из дерева
        nonlocal k
        e1, e2 = t[0], t[1]
        if type(e1) is tuple and type(e2) is int:
            kod(e1, num)
        elif type(e1) is tuple and type(e2) is tuple:
            kod(e1, num + '0')
            kod(e2, num + '1')
        elif type(e1) is str:
            k[e1] = num

        return k

    return kod(tree)


def encryption(txt_in, kod):  # Шифрование текста
    txt_out = ''

    for let in txt_in:
        txt_out += kod[let]

    sl = ''
    slices = []

    for i in txt_out:
        if len(sl) == 8:
            slices.append(sl)
            sl = ''
        sl += i

    slices.append(sl)
    leng = len(sl)

    result = bytes([int(j, 2) for j in slices])

    return result, leng


def decryption(slices, kod, leng):  # Дешифрование текста
    txt = []
    for i, val in enumerate(slices, start=1):
        sl = bin(val)[2:]
        if len(sl) < 8 and i != len(slices):
            while len(sl) < 8:
                sl = '0' + sl
        elif i == len(slices) and len(sl) < leng:
            while len(sl) < leng:
                sl = '0' + sl
        txt.append(sl)

    txt = ''.join(txt)
    let = ''
    txt_out = ''

    for j in txt:
        let += j
        if let in kod:
            txt_out += kod[let]
            let = ''

    return txt_out


# Шифрование
if typ == 'e':
    with open(f'{file}.txt', 'r', encoding="utf8") as f_r:
        if vigen:
            text = vigenere(f_r.read(), vigen)
        else:
            text = f_r.read()
        code = huffman(text)

    final_text, length = encryption(text, code)

    with open(f'{file}.par', 'wb') as f_w:
        # Список: длина, кодировка, текст
        pickle.dump([pickle.dumps(length), pickle.dumps(rekod(code)), pickle.dumps(final_text)], f_w)
# Дешифрование
elif typ == 'd':
    with open(f'{file}.par', 'rb') as f_d:
        data = pickle.load(f_d)
        length = pickle.loads(data[0])
        code = pickle.loads(data[1])
        text = detext(pickle.loads(data[2]))
        final_text = decryption(text, code, length)

    with open(f'{file}.txt', 'w', encoding='utf8') as f_w:
        f_w.write(final_text)

    if vigen:
        with open(f'{file}.txt', 'r', encoding="utf8") as f_r:
            final_text = devigenere(f_r.read(), vigen)
        with open(f'{file}.txt', 'w', encoding="utf8") as f_w:
            f_w.write(final_text)
