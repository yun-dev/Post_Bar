from flask import Blueprint, render_template, session, redirect, request, jsonify
from urllib import request as req
import time, re
import json, random, requests
from functools import wraps
from db import *
from tools import *
from code_number import *

bp = Blueprint('auth', __name__)
n = None
r_number = None


@bp.route('/login/')
def login():
    print(session,"---------------------")
    if session.get('remberu_user') and session.get('remberu_pwd'):
        return render_template("login.html",name=session.get('remberu_user'),pwd=session.get('remberu_pwd'))
    else:
        return render_template("login.html")


# 用户登录
@bp.route('/user_login/', methods=['post'])
def user_login():
    user = request.get_json()
    username = user.get('user')
    userpwd = user.get('pwd')
    status = int(user.get('status'))
    u = db_session.query(User).filter(User.u_name == username).first()
    if userpwd == '' or userpwd == '':
        error = '用户名或密码不能为空'
        return jsonify({'status': 102, 'error': error})
    if u != None:
        p = u.u_password
        if p == security_password(userpwd):
            session['current_user'] = username
            if status == 1:
                session['remberu_user'] = username
                session['remberu_pwd'] = userpwd
            else:
                if session.get('remberu_user') and session.get('remberu_pwd'):
                    del session['remberu_user']
                    del session['remberu_pwd']
            return jsonify({'status': 0})
        else:
            error = '密码输入错误'
            return jsonify({'status': 101, 'error': error})
    else:
        error = '用户不存在'
        return jsonify({'status': 100, 'error': error})


@bp.route('/logout/')
def logout():
    del session['current_user']
    return redirect('/')


# 发送验证码
@bp.route('/return_number',methods=['post'])
def return_number():
    global  r_number
    r_number = random.randint(10000, 99999)
    r_number = 12345
    users = request.get_json()
    return_number_qw(users['number'],r_number)
    return jsonify({'status': 0})


@bp.route('/register/')
def register():
    return render_template("register1.html")


@bp.route('/register2/')
def register2():
    global n
    img_loads = (db_session.query(User).filter(User.u_id == n).first()).u_head_img
    if img_loads == None:
        return render_template("register2.html", img='img/baidu.jpg')
    else:
        return render_template("register2.html", img=img_loads)


@bp.route('/register3/')
def register3():
    return render_template('register3.html')


# 用户名，密码，手机号注册
@bp.route('/new_mesg/', methods=['post'])
def new_mesg():
    global n, r_number
    users = request.get_json()
    user_name = users.get('user')
    user_pwd = users.get('pwd')
    user_pwd1 = users.get('pwd1')
    user_number = users.get('number')
    user_phone = users.get('phone')
    r = re.match('^[\u4e00-\u9fa5_a-zA-Z0-9]+$', user_name)
    m = re.match('^[0-9A-Za-z_-]+$', user_pwd)
    res = req.urlopen(
        "http://apis.juhe.cn/mobile/get?phone=" + users['number'] + "&key=90db363c1c636731a410df9b1bb838c1")
    phone_numbers = res.read().decode()
    result = json.loads(phone_numbers)
    err = result['error_code']
    userid = db_session.query(User).filter(User.u_name == user_name).first()
    userphone = db_session.query(User).filter(User.u_phone == user_number).first()
    if user_name == '' or user_pwd == '' or user_number == '':
        status = 100
        error = '用户名,密码,手机号不能为空'
        return jsonify({'status': status, 'error': error})
    elif userid != None:
        error = '用户名已存在'
        return jsonify({'status': 104, 'error': error})
    elif len(user_name) < 6 or len(user_name) > 24:
        error = '用户名长度需6~24位'
        return jsonify({'status': 104, 'error': error})
    elif len(user_pwd) < 6 or len(user_pwd) > 18:
        error = '用户密码需6~18位'
        return jsonify({'status': 104, 'error': error})
    elif r == None:
        error = '用户名需由中英文及下划线组成'
        return jsonify({'status': 106, 'error': error})
    elif m == None:
        error = '用户密码要以数字字母下划线组成'
        return jsonify({'status': 106, 'error': error})
    elif user_pwd != user_pwd1:
        status = 101
        error = '两次密码输入不符'
        return jsonify({'status': status, 'error': error})
    elif err == 201103:
        error = '手机号查询无结果'
        return jsonify({'status': 102, 'error': error})
    elif err == 201102:
        error = '错误的手机号码'
        return jsonify({'status': 102, 'error': error})
    elif err == 201101:
        error = '手机号码不能为空'
        return jsonify({'status': 102, 'error': error})
    elif userphone != None:
        error = '手机号码已存在'
        return jsonify({'status': 105, 'error': error})
    elif str(r_number) != user_phone:
        error = '验证码输入错误'
        return jsonify({'status': 103, 'error': error})
    else:
        pwds = security_password(user_pwd)
        status = 0
        add_data(User(u_name=user_name, u_password=pwds, u_phone=user_number))
        u = db_session.query(User).filter(User.u_name == user_name, User.u_password == pwds).first()
        n = u.u_id
        return jsonify({'status': status})


# 用户注册信息
@bp.route('/new_mesgs/', methods=['post'])
def new_mesgs():
    global n
    users = request.get_json()
    fakename = users.get('fakename')
    bir = users.get('bir')
    sex = users.get('sex')
    tag = users.get('tag')
    f = db_session.query(User).filter(User.u_nickname == fakename).first()
    if fakename == '' or sex == '' or bir == '':
        error = '昵称,性别,生日不能为空'
        return jsonify({'status': 101, 'error': error})
    elif len(fakename)>10:
        error = '昵称过长'
        return jsonify({'status': 101, 'error': error})
    elif f == None:
        db_session.query(User).filter(User.u_id == n).update(
            {User.u_nickname: fakename, User.u_sex: sex, User.u_introduce: tag, User.u_birthday: bir})
        db_session.commit()
        return jsonify({'status': 0})

    else:
        error = '昵称已存在'
        return jsonify({'status': 101, 'error': error})


# 截图界面
@bp.route('/testimg/')
def testimgs():
    return render_template('screenshot.html')


# 头像截图
@bp.route('/new_mesgss/', methods=['post'])
def uploadimge():
    global n
    t = str(time.time())
    updote = request.files['files']
    data = updote.read()
    with open('static/img/' + str(n) + t + '.jpg', 'wb+') as f:
        f.write(data)
    img_load = 'img/' + str(n) + t + '.jpg'
    db_session.query(User).filter(User.u_id == n).update(
        {User.u_head_img: img_load})
    db_session.commit()
    return jsonify({'status': 0})


@bp.app_template_global()
def is_login():
    return 'current_user' in session


def login_required(view_func):
    @wraps(view_func)
    def wrapped_view(**kwargs):
        if not is_login():
            return redirect('/login')
        return view_func(**kwargs)

    return wrapped_view


# @bp.route('/rember_user/',methods=['post'])
# def rember_user():
#     user = request.get_json()
#     username = user.get('user')
#
#     userpwd = user.get('pwd')
#
#     status = user.get('status')
#
#     u = db_session.query(User).filter(User.u_name == username).first()
#
#     if u != None:
#         p = u.u_password
#
#         if p == security_password(userpwd):
#             if status==1:
#                 if session.get('remberu_user') == None and session.get('remberu_pwd') == None:
#                     session['remberu_user'] = username
#                     session['remberu_pwd'] = userpwd
#             else:
#                 if session.get('remberu_user') and session.get('remberu_pwd'):
#                     del session['remberu_user']
#                     del session['remberu_pwd']
#             return jsonify({'status': 0})
