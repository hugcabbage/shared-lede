"""Use the crypt method to generate a cryptographic certificate, 
which can also be used to verify whether the cryptographic certificate is correct
"""
import time
from purecrypt import Crypt, Method


def crypt_str(plaintext, user='root') -> str:
    """generate crypt string"""

    salt = Crypt.generate_salt(Method.MD5)
    ciphertext = Crypt.encrypt(plaintext, salt).replace('\\', '\\\\')
    part1 = user
    part2 = ciphertext
    part3 = int(time.time()) // 86400
    part_end = '0:99999:7:::'
    login_cred = f'{part1}:{part2}:{part3}:{part_end}'
    return login_cred


def validate_cipher(plaintext, ciphertext):
    """validate cipher"""

    # ciphertext example: $1$MCGAgYw.$Ip1GcyeUliId3wzVcKR/e/
    assert Crypt.is_valid(plaintext, ciphertext), 'password does not match'
    print('password matches')
