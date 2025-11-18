def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    for char in plaintext:
        if char.isalpha():
            # Получаем код текущей буквы
            char_code = ord(char)

            # Применяем сдвиг
            new_code = char_code + shift

            # Проверяем не вышли ли за границы алфавита
            if char.isupper():
                if new_code > ord("Z"):
                    # Прыжок от Z к A
                    new_code = new_code - 26
            else:  # строчные буквы
                if new_code > ord("z"):
                    # Прыжок от z к a
                    new_code = new_code - 26

            # Преобразуем код обратно в символ
            new_char = chr(new_code)
            ciphertext += new_char
        else:
            # Не буквы оставляем как есть
            ciphertext += char
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    for char in ciphertext:
        if char.isalpha():
            # Получаем код текущей буквы
            char_code = ord(char)

            # Применяем обратный сдвиг (минус 3)
            new_code = char_code - shift

            # Проверяем, не вышли ли за границы алфавита
            if char.isupper():
                if new_code < ord("A"):
                    # Прыжок от A к Z
                    new_code = new_code + 26
            else:  # строчные буквы
                if new_code < ord("a"):
                    # Прыжок от a к z
                    new_code = new_code + 26

            # Преобразуем код обратно в символ
            new_char = chr(new_code)
            plaintext += new_char
        else:
            # Не буквы оставляем как есть
            plaintext += char

    return plaintext
