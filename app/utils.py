from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# def find_post(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p
        

# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p["id"] == id:
#             return i
