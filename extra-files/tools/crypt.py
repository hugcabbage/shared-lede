# 生成密文凭证
def crypt_root(plaintext):
    import time
    from purecrypt import Crypt, Method
    salt = Crypt.generate_salt(Method.MD5)
    ciphertext = Crypt.encrypt(plaintext, salt).replace('\\', '\\\\')
    part1 = 'root'
    part2 = ciphertext
    part3 = int(time.time()) // 86400
    part_end = '0:99999:7:::'
    login_cred = f'{part1}:{part2}:{part3}:{part_end}'
    return login_cred
