def encrypt_atbash(plaintext):
    """
    Шифруем текст с помощью шифра Атбаш для английского алфавита.
    """
    encrypted_text = ""

    # Проходим по каждому символу в исходном тексте
    for char in plaintext:
        # обрабатываем строчные буквы
        if "a" <= char <= "z":
            # Находим позицию буквы
            position = ord(char) - ord("a")
            # Вычисляем позицию отраженной буквы
            mirrored_position = 25 - position
            # Получаем отраженную букву
            mirrored_char = chr(ord("a") + mirrored_position)
            encrypted_text += mirrored_char

        # ОБРАБАТЫВАЕМ ЗАГЛАВНЫЕ
        elif "A" <= char <= "Z":
            position = ord(char) - ord("A")
            mirrored_position = 25 - position
            mirrored_char = chr(ord("A") + mirrored_position)
            encrypted_text += mirrored_char

        # Все остальные символы оставляем
        else:
            encrypted_text += char

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
