import jwt
import datetime

SECRET_KEY = 'your-secret-key'  # 设置你的密钥
payload = {
    'user_id': 123,
    'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # 设置过期时间
}

# 使用 pyjwt 的 encode 方法生成 JWT token
token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

print(token)  # 输出生成的 token
