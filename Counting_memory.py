from memory_profiler import profile
from RSA import *
from ECDSA import *
import time

@profile
def sign_RSA():
    d, e, n = key_generation()

    document_path = 'example.docx'
    document_hash = get_document_hash(document_path)

    # Подпись хеша документа
    signatures = sign_document(document_hash, d, n)


    # Сборка полной подписи и хеша
    full_signature_and_hash = verify_document_signature(document_hash, signatures, e, n)
    document_path1 = 'example.docx'
    document_hash1 = get_document_hash(document_path1)

    # Проверка подлинности подписи
    is_valid = verify_document_signature(document_hash1, signatures, e, n)
    pass

@profile
def sign_ECDSA():
    private_key = random.randint(1000, curve_config['p'] - 1)  # любое рандомное число
    document_path = 'example.docx'
    document_hash = get_document_hash(document_path)

    message = int(document_hash, 16)  # любое целое число
    public_key = gp_point.multiply(private_key)
    signature = sign_message(message, private_key)

    ddocument_path = 'example.docx'
    document_hash = get_document_hash(document_path)
    message = int(document_hash, 16)  # любое целое число
    pass
