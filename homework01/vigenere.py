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
    keyword = keyword.upper()
    key_index = 0

    for char in plaintext:
        if char.isalpha():
            # сдвиг из ключа
            key_char = keyword[key_index % len(keyword)]
            shift = ord(key_char) - ord("A")

            if char.isupper():
                # ЗАГЛАВНЫЕ
                new_code = ord(char) + shift
                if new_code > ord("Z"):
                    new_code -= 26
                ciphertext += chr(new_code)
            else:
                # строчные
                new_code = ord(char) + shift
                if new_code > ord("z"):
                    new_code -= 26
                ciphertext += chr(new_code)

            # Переходим к следующему символу ключа
            key_index += 1
        else:
            # Не буквы оставляем как есть
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
    keyword = keyword.upper()
    key_index = 0

    for char in ciphertext:
        if char.isalpha():
            # сдвиг из ключа
            key_char = keyword[key_index % len(keyword)]
            shift = ord(key_char) - ord("A")

            if char.isupper():
                # ЗАГЛАВНЫЕ
                new_code = ord(char) - shift
                if new_code < ord("A"):
                    new_code += 26
                plaintext += chr(new_code)
            else:
                # строчные
                new_code = ord(char) - shift
                if new_code < ord("a"):
                    new_code += 26
                plaintext += chr(new_code)

            # Переходим к следующему символу ключа
            key_index += 1
        else:
            # Не буквы оставляем как есть
            plaintext += char

    return plaintext
