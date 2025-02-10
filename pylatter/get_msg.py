import numpy as np
from flask_cors import CORS
from models import app, db, User, Jingli, Guzhang, Fuwu
import datetime
import jwt
from functools import wraps
from flask import request, jsonify

cors = CORS(app, resources={r"/*": {"origins": "*"}})
SECRET_KEY = 'secret_tzx'

# 用户登录验证
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    # 这里用静态用户名和密码作为示例，实际中需要验证用户名和密码
    if username == 'user' and password == 'password':
        payload = {
            'sub': username,  # 'sub' 标识主体
            'iat': datetime.datetime.utcnow(),  # 签发时间
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # 过期时间
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return jsonify({'token': token})

    return jsonify({'message': 'Invalid credentials'}), 401

# 验证 token 装饰器
def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]  # 获取 'Bearer <token>'

        if not token:
            return jsonify({'message': 'Token is missing!'}), 403

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401

        return f(*args, **kwargs)

    return decorated_function

# 保护 API 路由
@app.route('/protected', methods=['GET'])
@token_required
def protected():
    return jsonify({'message': 'This is a protected route.'})


@app.route('/')
def hello_world():
    return 'hello world!'


@app.route('/getUser', methods=['POST'])
def getUser():
    data = request.get_json(silent=True)
    account = data['account']
    user = User.query.get_or_404(int(account))
    if user:
        if user.pwd == data['pwd']:
            msg = user.account
        else:
            msg = 405
    else:
        msg = 404
    res = {
        "msg": msg
    }
    return jsonify(res)


@app.route('/getJingli', methods=['GET', 'POST'])   # /getJingli 是传递给前端的路径名
def getJingli():
    jinglis = Jingli.query.order_by(Jingli.id.desc()).all()
    res = {
        "msg": Jingli.repr(None, jinglis=jinglis)
    }
    return jsonify(res)


# delJingli 删除经理
@app.route("/delJingli", methods=['GET', 'POST'])
def delJingli():
    data = request.get_json(silent=True)  # {'id': 1}
    id = data['id']
    jingli = Jingli.query.get_or_404(int(id))
    db.session.delete(jingli)
    db.session.commit()
    res = {
        "msg": 200
    }
    return jsonify(res)


@app.route('/updateJingli', methods=['GET', 'POST'])
def updateJingli():
    data = request.get_json(silent=True)
    # print(data)
    id = data['id']
    jingli = Jingli.query.get_or_404(int(id))
    jingli.name = data['name']
    jingli.serviceArea = data["serviceArea"]

    # update
    db.session.add(jingli)
    db.session.commit()
    res = {
        "msg": 200
    }
    return jsonify(res)


@app.route('/addJingli', methods=['GET', 'POST'])
def addJingli():
    data = request.get_json(silent=True)
    # print(data)
    jingli = Jingli(
        name=data['name'],
        serviceArea=data["serviceArea"],
    )
    db.session.add(jingli)
    db.session.commit()

    res = {
        "msg": 200
    }
    return jsonify(res)


# 统计各工单每月数量
def countGongdans(gongdans, count=None):
    if count is None:
        count = [0 for i in range(12)]
    for g in gongdans:
        i = g.startTime.month - 1
        count[i] += 1
    return count


@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    data = request.get_json(silent=True)
    jingli = Jingli.query.get_or_404(data['id'])

    # 统计各工单每月数量
    count_guz = countGongdans(jingli.guzhangs)
    count_fuw = countGongdans(jingli.fuwus)
    print(count_guz, count_fuw)

    # 统计故障工单每个分类比例
    pie = {}
    for g in jingli.guzhangs:
        yiji = g.fenlei
        pie[yiji] = pie.get(yiji, 0) + 1
    pie2 = [{'name': k, 'value': round(v / len(jingli.guzhangs), 2)} for k, v in pie.items()]

    # 发送信息
    msg = {
      'bar': {
        'x': [str(i+1)+'月' for i in range(12)],
        'legend': ['故障工单', '非故障工单'],
        'y': [count_guz, count_fuw],
      }, 'pie': pie2
    }
    res = {
        "msg": msg
    }
    return jsonify(res)


# 启动运行
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)  # 这里可通过 host 指定在公网IP上运行
