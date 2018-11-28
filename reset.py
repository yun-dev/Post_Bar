from flask import Blueprint, render_template, session, redirect, request, jsonify
from urllib import request as req
import time
import json, random, requests
from functools import wraps
from db import *
from code_number import *

bp = Blueprint('reset', __name__)
n = None
r_number = None
phone = None

@bp.route('/resetting/')
def resetting():
    return render_template('resetting.html')


@bp.route('/newcode/')
def newcode():
    return render_template('newcode.html')


@bp.route('/newcode2/')
def newcode2():
    return render_template('newcode2.html')


@bp.route('/reset_number',methods=['post'])
def reset_number():
    global r_number,phone
    r_number = random.randint(10000, 99999)
    users = request.get_json()
    phone = users.get('number')
    return_number_qw(users['number'],r_number)
    return jsonify({'status': 0})


@bp.route('/phone_number/',methods=['post'])
def phone_number():
    global r_number
    reset_number = request.get_json()
    number = reset_number.get('pwd')
    if number == str(r_number):
        return jsonify({'status':0})
    else:
        error = '验证码输入错误'
        return jsonify({'status': 101,'error':error})


@bp.route('/new_mesg/',methods=['post'])
def new_mesg():
    global phone_number
    user = request.get_json()
    pwd = user.get('pwd')
    pwd1 = user.get('pwd1')
    if pwd =='' or pwd1 =='':
        error = '密码不能为空'
        return jsonify({'status': 101, 'error': error})
    elif pwd != pwd1:
        error = '两次密码输入不符'
        return jsonify({'status': 101, 'error': error})
    else:
        db_session.query(User).filter(User.u_phone == phone_number).update(
            {User.u_password:pwd})
        db_session.commit()
        return jsonify({'status': 0})

