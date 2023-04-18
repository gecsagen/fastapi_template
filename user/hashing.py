from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


#  класс хэша
class Hasher:
    @staticmethod
    def verify_password(plain_password, hashed_password):
        """верификация пароля"""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """получение хэша пароля"""
        return pwd_context.hash(password)
