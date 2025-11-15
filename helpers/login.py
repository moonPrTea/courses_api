from serializers import ValidationAnswer
import re


async def check_input_username (username: str) -> ValidationAnswer:
    impossible_names = ['admin', 'username', 'root', 'moderator']
    if len(username) < 5:
        return ValidationAnswer(success=False, detail="Длина имени пользователя должна быть больше 5 символов")
    elif len(username) > 20:
        return ValidationAnswer(success=False, detail="Длина имени пользователя должна быть меньше 20 символов")
    
    for item in impossible_names:
        if item in username:
            return ValidationAnswer(success=False, detail="Недопустимое имя пользователя")
    
    print(username.isdigit())
    if username.isdigit():
        return ValidationAnswer(success=False, detail="Имя не может содержать только цифры")
    
    if username[0].isdigit():
        return ValidationAnswer(success=False, detail="Имя не может начинаться с цифры")
    
    return ValidationAnswer(success=True, detail="Имя пользователя проверено")



async def check_input_email (email: str) -> tuple[bool, str]:
    if len(email) > 254:
        return ValidationAnswer(success=False, detail="Длина почты слишком большая")
    
    if '@' not in email:
        return ValidationAnswer(success=False, detail="Почта должна содержать символ @")
    
    username_part, domain = email.split('@', 1) # --> проверка общего домена и локальной части почты
    
    if not username_part:
        return ValidationAnswer(success=False, detail="Локальная часть пустая")
    
    if len(username_part) > 64:
        return ValidationAnswer(success=False, detail="Локальная часть содержит больше 64 символов")
    
    allowed_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._%+-"
    for elem in username_part:
        if elem not in allowed_chars:
            return ValidationAnswer(success=False, detai=f"Неверный ввод символа '{elem}' в локальной части")
    
    if not domain:
        return ValidationAnswer(success=False, detail="Домен почты не может быть пустым")
    
    if len(domain) > 255:
        return ValidationAnswer(success=False, detail="Домен почты не может быть больше 255 символов")
    
    if '.' not in domain:
        return ValidationAnswer(success=False, detail="Домен должен содержать точку")
    
    domain_parts = domain.split('.') # --> прооверка адреса сервера
    if len(domain_parts) < 2:
        return ValidationAnswer(success=False, detail="Домен должен содержать 2 части, разделенные точкой")
    
    for i, part in enumerate(domain_parts):
        if not part:
            return ValidationAnswer(success=False, detail="Адрес сервера не может быть пустым")
        
        if len(part) > 63:
            return ValidationAnswer(status=False, detail=f"Адрес сервера '{part}' слишком длинный")
    
        domain_allowed_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-"
        for char in part:
            if char not in domain_allowed_chars:
                return ValidationAnswer(success=False, detail=f"Неверный ввод символа '{elem}' в домене")
        if part.startswith('-') or part.endswith('-'):
            return ValidationAnswer(success=False, detail="Домен не может начинаться/заканчиваться '-'")
    
    domen_zone = domain_parts[-1] # --> проверка доменной зоны или TLD
    if len(domen_zone) < 2:
        return ValidationAnswer(success=False, detail="Доменная зона должна содержать 2 символа")
    
    if not domen_zone.isalpha():
        return ValidationAnswer(success=False, detail="Доменная зона не может содержать цифры")
    
    return ValidationAnswer(success=True, detail="Почта проверена")
    
async def check_input_password(pswrd: str):
    if len(pswrd) < 8:
        return ValidationAnswer(success=False, detail="Длина пароля не может быть менее 8 символов")
    
    if len(pswrd) > 100:
        return ValidationAnswer(success=False, detail="Длина пароля превышает 100 символов")
    
    if not re.search(r"\d", pswrd):
        return ValidationAnswer(success=False, detail="Пароль должен содержать цифру")
    
    if not re.search(r"[A-Z]", pswrd):
        return ValidationAnswer(success=False, detail="Пароль должен содержать заглавную букву")
    
    if not re.search(r"[a-z]", pswrd):
        return ValidationAnswer(success=False, detail="Пароль должен содержать буквы")
    
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", pswrd):
        return ValidationAnswer(success=False, detail="Пароль должен содержать хотя бы один специальный символ")
    return ValidationAnswer(success=True, detail="Пароль проверен")