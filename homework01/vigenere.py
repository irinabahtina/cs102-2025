def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    key_index = 0

    # Приводим ключ к нижнему регистру для единообразия
    keyword = keyword.lower()

    for char in plaintext:
        if char.isalpha():
            # Берем текущий символ ключа
            key_char = keyword[key_index % len(keyword)]
            shift = ord(key_char) - ord("a")

            if char.isupper():
                new_code = ord(char) + shift
                if new_code > ord("Z"):
                    new_code -= 26
                ciphertext += chr(new_code)
            else:
                new_code = ord(char) + shift
                if new_code > ord("z"):
                    new_code -= 26
                ciphertext += chr(new_code)

            # Увеличиваем индекс ключа только для букв
            key_index += 1
        else:
            # Небуквенные символы добавляем без изменений
            # Не увеличиваем key_index
            ciphertext += char
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    key_index = 0

    # Приводим ключ к нижнему регистру для единообразия
    keyword = keyword.lower()

    for char in ciphertext:
        if char.isalpha():
            # Берем текущий символ ключа
            key_char = keyword[key_index % len(keyword)]
            shift = ord(key_char) - ord("a")

            if char.isupper():
                new_code = ord(char) - shift
                if new_code < ord("A"):
                    new_code += 26
                plaintext += chr(new_code)
            else:
                new_code = ord(char) - shift
                if new_code < ord("a"):
                    new_code += 26
                plaintext += chr(new_code)

            # Увеличиваем индекс ключа только для букв
            key_index += 1
        else:
            # Небуквенные символы добавляем без изменений
            # Не увеличиваем key_index
            plaintext += char

    return plaintext
