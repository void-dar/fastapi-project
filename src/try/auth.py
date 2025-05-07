import ulid

def generate_user_id():
    new_ulid = ulid.new()
    return new_ulid


generate_user_id()