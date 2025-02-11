from flask import Flask
from flask_sqlalchemy import SQLAlchemy  # flask的一个数据库ORM（对象关系映射）库，封装了一系列对数据库的操作API
from flask_cors import *
import pymysql
pymysql.install_as_MySQLdb()


def creat_app():  #  配置flask-sqlalchemy连接MySQL数据库
    app2 = Flask(__name__)  #创建应用程序对象
    CORS(app2, supports_credentials=True)  # 设置跨域
    app2.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:12345678@127.0.0.1/dianli"
    # 如果设置成 True (默认情况)，Flask-SQLAlchemy 将会追踪对象的修改并且发送信号。
    app2.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    return app2


# 绑定app至SQLAlchemy
app = creat_app()
db = SQLAlchemy(app)  # 创建数据库对象


# 定义数据表的model类User，以完成数据库表和数据对象之间的关系映射
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)  # 编号id
    account = db.Column(db.String(20), nullable=False)  # 账号非空
    pwd = db.Column(db.String(100), nullable=False)  # 密码非空
    add_time = db.Column(db.DateTime, nullable=False)  # 注册时间

    def __init__(self, account, pwd, add_time):
        self.account = account
        self.pwd = pwd
        self.add_time = add_time

    # 查询时的返回
    def __repr__(self):
        return "<User %r>" % self.account

    # 检查密码是否正确
    def check_pwd(self, pwd):
        return True


# 定义数据表的model类Jingli，以完成数据库表和数据对象之间的关系映射
class Jingli(db.Model):
    __tablename__ = "jingli"
    id = db.Column(db.Integer, primary_key=True)  # "主键ID",
    name = db.Column(db.String(32))  # "台区经理姓名",
    serviceArea = db.Column(db.String(256))  # "服务地区",
    guzhangs = db.relationship('Guzhang', backref='Jingli')
    fuwus = db.relationship('Fuwu', backref='Jingli')

    def repr(self, jinglis=None):
        if not jinglis:
            return "error0101: jingli is None"
        res = []

        for item in jinglis:
            res.append({'id': item.id, 'name': item.name, 'serviceArea': item.serviceArea})
        return res


class Guzhang(db.Model):
    __tablename__ = "guzhang"
    id = db.Column(db.Integer, primary_key=True)  # "主键ID",
    startTime = db.Column(db.DateTime)  # "开始时间",
    endTime = db.Column(db.DateTime)  # "结束时间",
    address = db.Column(db.String(128))   # "故障地址",
    fenlei = db.Column(db.String(32))   # "一级分类",
    sanji = db.Column(db.String(32))   #  "三级分类",
    jingli_id = db.Column(db.Integer(), db.ForeignKey('jingli.id'))

    def repr(self, guzhang=None):
        if not guzhang:
            return "error0101: guzhang is None"
        res = []
        for item in guzhang:
            res.append({'id': item.id, 'startTime': item.startTime, 'endTime': item.endTime,
                        'address': item.address, 'fenlei': item.fenlei, 'sanji': item.sanji})
        return res


class Fuwu(db.Model):
    __tablename__ = "fuwu"
    id = db.Column(db.Integer, primary_key=True)  # "主键ID",
    startTime = db.Column(db.DateTime)  # "开始时间",
    address = db.Column(db.String(128))  # "联系地址",
    jingli_id = db.Column(db.Integer(), db.ForeignKey('jingli.id'))

    def repr(self, fuwu=None):
        if not fuwu:
            return "error0101: fuwu is None"
        res = []
        for item in fuwu:
            res.append({'id': item.id, 'gongdanbianhao': item.gongdanbianhao, 'jiedandengjishijian': item.jiedandengjishijian,
                        'baoxiuneirong': item.baoxiuneirong, 'address': item.address})
        return res

class Task(db.Model):
    __tablename__ = 'tasks'
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    exec_command = db.Column(db.Text, nullable=False)
    check_command = db.Column(db.Text, nullable=False)
    status = db.Column(db.Enum('pending', 'running', 'completed', 'failed'), default='pending')
    
    dependencies = db.relationship('Task', 
                                   secondary='task_dependencies',
                                   primaryjoin='Task.task_id==task_dependencies.c.task_id',
                                   secondaryjoin='Task.task_id==task_dependencies.c.dependency_id',
                                   backref='dependents')

    def __init__(self, name, exec_command, check_command):
        self.name = name
        self.exec_command = exec_command
        self.check_command = check_command


class TaskDependency(db.Model):
    __tablename__ = 'task_dependencies'
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.task_id'), primary_key=True)
    dependency_id = db.Column(db.Integer, db.ForeignKey('tasks.task_id'), primary_key=True)

    task = db.relationship("Task", foreign_keys=[task_id])
    dependency = db.relationship("Task", foreign_keys=[dependency_id])

class TaskExecutionLog(db.Model):
    __tablename__ = 'task_execution_logs'
    log_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.task_id'), nullable=False)
    execution_time = db.Column(db.DateTime, default=db.func.current_timestamp())  # 默认当前时间
    status = db.Column(db.Enum('started', 'completed', 'failed'), nullable=False)  # 执行状态
    message = db.Column(db.Text)  # 执行消息

    # 关联任务
    task = db.relationship('Task', backref=db.backref('execution_logs', lazy=True))

    def __init__(self, task_id, status, message):
        self.task_id = task_id
        self.status = status
        self.message = message

# 执行创建表语句
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
