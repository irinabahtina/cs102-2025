def encrypt_atbash(plaintext):
    """
    Шифруем текст с помощью шифра Атбаш для английского алфавита.
    """
    encrypted_text = ""

    ALPHABET_SIZE = 26
    LAST_LETTER_INDEX = ALPHABET_SIZE - 1

    # Проходим по каждому символу в исходном тексте
    for char in plaintext:
        # обрабатываем строчные буквы
        if "a" <= char <= "z":
            alphabet_start = "a"
        elif "A" <= char <= "Z":
            alphabet_start = "A"
        else:
            # Если не буква, то оставляем
            encrypted_text += char
            continue

        # Находим позицию буквы в алфавите
        position = ord(char) - ord(alphabet_start)
        # Вычисляем позицию отраженной буквы
        mirrored_position = LAST_LETTER_INDEX - position
        # Получаем отраженную букву
        mirrored_char = chr(ord(alphabet_start) + mirrored_position)
        encrypted_text += mirrored_char

    return encrypted_text


# Пример использования
if __name__ == "__main__":
    # Тестирование функции
    test_cases = [
        "Hello, World",
        "Irina",
        "ABCDEF",
        "Minecraft",
        "vwxyz",
        "?123!",
    ]

    print("Тестирование шифра Атбаш:")

    for text in test_cases:
        encrypted = encrypt_atbash(text)
        print(f"Исходный: '{text}'")
        print(f"Зашифрованный:'{encrypted}'")
