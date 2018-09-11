import jwt

# For jwt
key = 'lknawevuiasodnv'

# Authorization
def auth(token):
    try:
        user = jwt.decode(token, key, algorithm='HS256')['user']
        return user
    except:
        return False

