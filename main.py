from RSA import *
from ECDSA import *
from Counting_memory import *
import time

s='0'
while s!='':
    s=(input('Какой алгоритм используем? 1- RSA 2 - ECDSA: '))
    if s=='1':
        storona = "C"
        while storona != '':
            storona = input('От лица какой стороны мы действуем A или B? ')
            try:
                if storona == 'A':
                    start_time = time.time()  # Начало отсчета времени
                    d, e, n = key_generation()
                    end_time = time.time()  # Конец отсчета времени
                    print(f"Время генерации ключей RSA: {end_time - start_time} секунд")

                    document_path = input('Введите путь к вашему документу: ')
                    document_hash = get_document_hash(document_path)
                    print("Хэш документа:", document_hash)

                    # Подпись хеша документа
                    start_time = time.time()  # Начало отсчета времени
                    signatures = sign_document(document_hash, d, n)
                    print('Подпись:', signatures)
                    end_time = time.time()  # Конец отсчета времени
                    print(f"Время создания подписи RSA: {end_time - start_time} секунд")

                    # Сборка полной подписи и хеша
                    full_signature_and_hash = verify_document_signature(document_hash, signatures, e, n)
                elif storona == 'B':
                    document_path1 = input('Введите путь к вашему документу: ')
                    document_hash1 = get_document_hash(document_path1)
                    print("Хэш документа:", document_hash1)

                    # Проверка подлинности подписи
                    start_time = time.time()  # Начало отсчета времени
                    is_valid = verify_document_signature(document_hash1, signatures, e, n)
                    print("Проверка подписи:", is_valid)
                    end_time = time.time()  # Конец отсчета времени
                    print(f"Время верификации подписи RSA: {end_time - start_time} секунд")
            except:
                print('Вероятнее всего Вы ввели неверный путь')
    else:
        storona = "C"
        while storona != '':
            storona = input('От лица какой стороны мы действуем A или B? ')
            try:
                if storona == 'A':
                    start_time = time.time()  # Начало отсчета времени
                    private_key = random.randint(1000, curve_config['p'] - 1)  # любое рандомное число
                    end_time = time.time()  # Конец отсчета времени
                    print(f"Время генерации ключей ECDSA: {end_time - start_time} секунд")
                    document_path = input('Введите путь к вашему документу: ')
                    document_hash = get_document_hash(document_path)
                    print("Хэш документа:", document_hash)
                    message = int(document_hash, 16)  # любое целое число
                    public_key = gp_point.multiply(private_key)
                    start_time = time.time()  # Начало отсчета времени
                    signature = sign_message(message, private_key)
                    print('Подпись: ', signature)
                    end_time = time.time()  # Конец отсчета времени
                    print(f"Время создания подписи ECDSA: {end_time - start_time} секунд")
                elif storona == 'B':
                    ddocument_path = input('Введите путь к вашему документу: ')
                    document_hash = get_document_hash(document_path)
                    print("Хэш документа:", document_hash)
                    start_time = time.time()  # Начало отсчета времени
                    message = int(document_hash, 16)  # любое целое число
                    print('Проверка подписи: ', verify_signature(signature, message, public_key))
                    end_time = time.time()  # Конец отсчета времени
                    print(f"Время верификации подписи ECDSA: {end_time - start_time} секунд")

            except:
                print('Вероятнее всего Вы ввели неверный путь')


if __name__ == "__main__":
    print('\nПамять, затрачиваемая на RSA')
    sign_RSA()
    print('Память, затрачиваемая на ECDSA')
    sign_ECDSA()
