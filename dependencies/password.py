from werkzeug.security import generate_password_hash, check_password_hash

# --> класс для создания и проверки хэша паролей
class PasswordFunctions:
    def create_password(self, password):
        return generate_password_hash(password)

    def check_password(self, password_hash, password):
        return check_password_hash(password_hash, password)

password_functions = PasswordFunctions()