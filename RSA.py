import random
from itertools import islice
import hashlib
from docx import Document

def NOD(m,n):
    multiplier = 1

    while m != n:
        if m % 2 == 0 and n % 2 == 0:
            multiplier = multiplier * 2
            n = n / 2
            m = m / 2
        elif m % 2 != 0 and n % 2 != 0:
            if n > m:
                n = n - m
            elif m > n:
                m = m - n
        else:
            if n % 2 == 0:
                n = n / 2
            elif m % 2 == 0:
                m = m / 2

    return int(multiplier * n)

def primes():
    if hasattr(primes, "D"):
        D = primes.D
    else:
        primes.D = D = {}

    def sieve():
        q = 2
        while True:
            if q not in D:
                yield q
                D[q * q] = [q]
            else:
                for p in D[q]:
                    D.setdefault(p + q, []).append(p)
                del D[q]

            q += 1

    return sieve()



def a_random_number(n,simple):
    prov=False
    while prov==False:

        random_number = list(bin(random.getrandbits(n))[2:])
        random_number[0] = '1'
        random_number[-1] = '1'
        random_number = ''.join(random_number)
        while int(random_number, 2)==0 or int(random_number, 2)==1:
            random_number = list(bin(random.getrandbits(n))[2:])
            random_number[0] = '1'
            random_number[-1] = '1'
            random_number = ''.join(random_number)
        random_number = int(random_number, 2)
        i=0
        f=True
        while i<len(simple) and f==True:
            if random_number%simple[i]==0 and random_number!=simple[i]:
                f=False
            else:
                i+=1
        if f==True:
            prov=True
    return random_number


def find_s_and_t(N):
    # Проверяем, что N является нечетным числом
    if N % 2 == 0:
        print("N должно быть нечетным числом.")
        return

    # Ищем s и t
    for s in range(1, N):
        # Вычисляем t как (N - 1) / 2^s
        t = (N - 1) / (2 ** s)
        # Проверяем, что t является целым числом
        if t.is_integer():
            # Если t является целым числом, то мы нашли подходящие значения s и t
            return s, int(t)

    # Если подходящих значений s и t не найдено
    print("Не найдено подходящих значений s и t.")
    return


def The_algorithm_of_prime_numbers(N, k=6):
    if N <= 1:
        return False
    if N <= 3:
        return True
    if N % 2 == 0:
        return False

    s = 0
    t = N - 1
    while t % 2 == 0:
        t //= 2
        s += 1

    for _ in range(k):
        a = random.randint(2, N - 2)
        x = pow(a, t, N)

        if x == 1 or x == N - 1:
            continue

        for _ in range(s - 1):
            x = pow(x, 2, N)
            if x == 1:
                return False
            if x == N - 1:
                break
        else:
            return False

    return True

def finding_the_e_value(d,m):
    e=0
    while e*d%m!=1:
        e+=1
    return e


def key_generation():
    simple = list(islice(primes(), 0, 303))

    bits = 12
    check = False
    while check == False:
        p = a_random_number(bits, simple)
        check = The_algorithm_of_prime_numbers(p, k=6)
    check = False
    while check == False:
        q = a_random_number(bits, simple)
        check = The_algorithm_of_prime_numbers(q, k=6)
    n = p * q
    m = (p - 1) * (q - 1)

    # Использование a_random_number для генерации d
    d = a_random_number(bits, simple)
    while NOD(d, m) != 1:
        d = a_random_number(bits, simple)

    e = finding_the_e_value(d, m)

    return d, e, n



def get_document_hash(document_path):
    # Открытие документа
    doc = Document(document_path)

    # Сбор текста из документа
    document_text = ""
    for paragraph in doc.paragraphs:
        document_text += paragraph.text + "\n"

    # Создание хеша из текста документа
    document_hash = hashlib.sha256(document_text.encode()).hexdigest()

    return document_hash


def sign_document(document_hash, d, n):
    """Подпись хеша документа, разделенного на блоки."""
    block_size = len(str(n)) // 2  # Размер блока в символах
    signatures = []
    for i in range(0, len(document_hash), block_size):
        block_hex = document_hash[i:i+block_size]
        block_int = int(block_hex, 16)
        signature_int = pow(block_int, d, n)
        signatures.append(hex(signature_int)[2:])
    return signatures

def verify_document_signature(document_hash, signatures, e, n):
    """Проверка подлинности подписи документа, разделенного на блоки."""
    block_size = len(str(n)) // 2  # Размер блока в символах
    blocks = [document_hash[i:i+block_size] for i in range(0, len(document_hash), block_size)]
    for block, signature in zip(blocks, signatures):
        block_int = int(block, 16)
        signature_int = int(signature, 16)
        if pow(signature_int, e, n)!= block_int:
            return False
    return True



