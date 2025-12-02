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

    # Очищаем ключ, оставляем только буквы
    clean_keyword = ""
    for char in keyword:
        if char.isalpha():
            clean_keyword += char

    if not clean_keyword:
        clean_keyword = "A"

    for char in plaintext:
        if char.isalpha():
            # Получаем текущую букву ключа
            key_char = clean_keyword[key_index % len(clean_keyword)]

            # Вычисляем сдвиг (всегда в нижнем регистре для ключа)
            key_char_lower = key_char.lower()
            shift = ord(key_char_lower) - ord("a")

            # Шифруем
            if char.isupper():
                base = ord("A")
                encrypted_char = chr((ord(char) - base + shift) % 26 + base)
            else:
                base = ord("a")
                encrypted_char = chr((ord(char) - base + shift) % 26 + base)

            ciphertext += encrypted_char
            key_index += 1
        else:
            # Небуквенные символы остаются без изменений
            ciphertext += char
            key_index += 1

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

    # Очищаем ключ, оставляем только буквы
    clean_keyword = ""
    for char in keyword:
        if char.isalpha():
            clean_keyword += char

    if not clean_keyword:
        clean_keyword = "A"

    for char in ciphertext:
        if char.isalpha():
            # Получаем текущую букву ключа
            key_char = clean_keyword[key_index % len(clean_keyword)]

            # Вычисляем сдвиг (всегда в нижнем регистре для ключа)
            key_char_lower = key_char.lower()
            shift = ord(key_char_lower) - ord("a")

            # Дешифруем
            if char.isupper():
                base = ord("A")
                decrypted_char = chr((ord(char) - base - shift) % 26 + base)
            else:
                base = ord("a")
                decrypted_char = chr((ord(char) - base - shift) % 26 + base)

            plaintext += decrypted_char
            key_index += 1
        else:
            # Небуквенные символы остаются без изменений
            plaintext += char
            key_index += 1

    return plaintext