import random
from docx import Document
import hashlib
from sympy import mod_inverse


def find_inverse(number, modulus):
    return pow(number, -1, modulus)


class Point:
    def __init__(self, x, y, curve_config):
        a = curve_config['a']
        b = curve_config['b']
        p = curve_config['p']

        if (y ** 2) % p!= (x ** 3 + a * x + b) % p:
            raise Exception("The point is not on the curve")

        self.x = x
        self.y = y
        self.curve_config = curve_config

    def __str__(self):
        return f"Point({self.x}, {self.y})"

    def is_equal_to(self, point):
        return self.x == point.x and self.y == point.y

    def lambda_for_addition(self, point):
        p = self.curve_config['p']
        if self.is_equal_to(point):
            return (3 * point.x ** 2) * find_inverse(2 * point.y, p) % p
        else:
            return (point.y - self.y) * find_inverse(point.x - self.x, p) % p

    def add(self, point):
        p = self.curve_config['p']
        slope = self.lambda_for_addition(point)
        x = (slope ** 2 - point.x - self.x) % p
        y = (slope * (self.x - x) - self.y) % p
        return Point(x, y, self.curve_config)

    def multiply(self, times):
        current_point = self
        current_coefficient = 1

        previous_points = []
        while current_coefficient < times:
            previous_points.append((current_coefficient, current_point))
            if 2 * current_coefficient <= times:
                current_point = current_point.add(current_point)
                current_coefficient *= 2
            else:
                next_point = self
                next_coefficient = 1
                for (previous_coefficient, previous_point) in previous_points:
                    if previous_coefficient + current_coefficient <= times:
                        if previous_point.x!= current_point.x:
                            next_coefficient = previous_coefficient
                            next_point = previous_point
                current_point = current_point.add(next_point)
                current_coefficient += next_coefficient
        return current_point


curve_config = {
    'a': 0,
    'b': 7,
    'p': 115792089237316195423570985008687907853269984665640564039457584007908834671663,
}

n = 115792089237316195423570985008687907852837564279074904382605163141518161494337
x=55066263022277343669578718895168534326250603453777594175500187360389116729240
y=32670510020758816978083085130507043184471273380659243275938904335757337482424
gp_point = Point(x, y, curve_config)


def sign_message(message, private_key):
    k = random.randint(1,n)
    r_point = gp_point.multiply(k)
    r = r_point.x % n
    if r == 0:
        return sign_message(message, private_key)
    k_inverse = find_inverse(k, n)
    s = k_inverse * (message + r * private_key) % n
    return r, s


def verify_signature(signature, message, public_key):
    r, s = signature
    if s == 0:
        return False

    s_inverse = mod_inverse(s, n)
    u = (message * s_inverse) % n
    v = (r * s_inverse) % n

    c_point = gp_point.multiply(u).add(public_key.multiply(v))
    return c_point.x % n == r



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
