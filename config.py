__email = '56;<:7576:<'
__password = 'kwnjsifsiqt{j<<=6=:'


def get_email():
    return __decrypt_pass(__email)


def get_pass():
    return __decrypt_pass(__password)


def __decrypt_pass(encrypt_pass):
    passw = ''
    for c in encrypt_pass:
        passw += chr(ord(c) - 5)
    return passw


def __encrypt_pass(raw_pass):
    en_pass = ''
    for c in raw_pass:
        en_pass += chr(ord(c) + 5)
    return en_pass

if __name__ == '__main__':
    print __encrypt_pass('your_pass_word')