import ulid
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



def generate_user_id() -> str:
    new_ulid = str(ulid.new())
    return new_ulid
