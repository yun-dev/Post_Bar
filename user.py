from flask import Blueprint,render_template,url_for,request,redirect,session
from db import *
import datetime
import time
from auth import *
from os.path import join,sep
import os,uuid
bp = Blueprint('user',__name__)
from PIL import Image

user=db_session.query(User).all()
print(user)


@bp.route('/user/page/<int:user_id>/<int:page>/')
@bp.route('/user/<int:user_id>/',defaults={'page':1})
def user_index(user_id,page):
    create_list=[]
    care_list =[]
    posts_list=[]
    # 自己创建贴吧
    list0 = db_session.query(Bar_relation).filter(Bar_relation.u_id == user_id).filter(Bar_relation.relation == 0).all()
    # 关注的贴吧
    list1 = db_session.query(Bar_relation).filter(Bar_relation.u_id == user_id).filter(Bar_relation.relation == 1).all()
    # 帖子信息
    post_list=db_session.query(Post).filter(Post.u_id == user_id).limit(2).offset((page - 1) * 2).all()


    page1=get_page_counts(user_id)
    # 用户信息
    user=db_session.query(User).filter(User.u_id == user_id).first()
    bar_age=get_age(user.u_id)
    for i in list0:
        print(i.b_id)
        a = (db_session.query(Bar).filter(Bar.b_id == i.b_id).first()).b_name
        b = (db_session.query(Bar).filter(Bar.b_id == i.b_id).first()).b_path
        create_list.append([a,b])
    for k in list1:
        print(k.b_id)
        c = (db_session.query(Bar).filter(Bar.b_id == k.b_id).first()).b_name
        d = (db_session.query(Bar).filter(Bar.b_id == k.b_id).first()).b_path
        care_list.append([c,d])
    note=[]
    for j in post_list:
        posts_list.append([j.p_title,j.p_content,j.p_create_at,j.p_id,j.u_id,j.p_id])
        note = db_session.query(User).filter(User.u_id == j.u_id).first()
    current_user=[]
    if is_login():
        current_user=session.get('current_user')
        current_user=db_session.query(User).filter(User.u_name==current_user).first()
    # 帖子图片
    img = db_session.query(Post_Image).all()


    return render_template('user.html',text=create_list,list=care_list,user=user,bar_age=bar_age,posts_list=posts_list,img=img,current_user=current_user,note=note,page=page1+1,current_page=page)







@bp.route('/user/edit/<int:user_id>/',methods=['GET','POST'])
def user_edit(user_id):
    global images

    user = db_session.query(User).filter(User.u_id == user_id).first()
    return render_template("user_edit.html",user=user)






# 处理提交数据
@bp.route('/submit/<int:u_id>/',methods=['GET','POST'])
def submit(u_id):
    global images
    path = request.files.get('u_head_img')
    if path is None:
        nickname = request.form.get('nickname')
        note = request.form.get('note')
        sex = request.form.get('sex')
        db_session.query(User).filter(User.u_id == u_id).first()
        db_session.query(User).filter(User.u_id == u_id).update({User.u_nickname: nickname, User.u_sex: sex, User.u_introduce: note})
        db_session.commit()
        return redirect('/user/' + str(u_id))
    else:
        img=path.read()
        # print(img,'=================================================')
        head_path=str(uuid.uuid1())
        u_head_img = 'user_head/' +head_path+'.jpg'
        # print(u_head_img, '=================================================')
        with open('static/' + u_head_img, 'wb+') as f:
            f.write(img)
        u_head=change_img_dbi('static/' + u_head_img,100,100)
        u_head.save('static/' + u_head_img)
        # 定义图片的长度和宽度
        # im=Image.open('static/' + u_head_img)
        # width=100
        # height=100
        # resizedIm = im.resize((width,height))
        # resizedIm.save('static/' + u_head_img)
        nickname=request.form.get('nickname')
        note=request.form.get('note')
        sex=request.form.get('sex')
        user=db_session.query(User).filter(User.u_id==u_id).first()
        der='static/'+user.u_head_img
        os.remove(der)
        db_session.query(User).filter(User.u_id==u_id).update({User.u_nickname:nickname,User.u_sex:sex,User.u_introduce:note,User.u_head_img:u_head_img})
        db_session.commit()
        return redirect('/user/'+str(u_id))






# 删除处理
@bp.route('/delete/<int:u_id>/<path:p_id>/',methods=['GET','POST'])
def delete(u_id,p_id):
    imgs_path = get_post_img(p_id)
    for img_path in imgs_path:
        der = 'static/' + img_path.img_path
        try:
            os.remove(der)
        except:
            print('图片不存在')
    # 根据被删除的帖子的用户id和帖子id找到posts里的b_id
    delete_post=db_session.query(Post).filter(Post.p_id == p_id).filter(Post.u_id == u_id).first()
    note = delete_post.b_id
    # 根据被删除帖子的b_id找到bar里的b_id
    db_session.query(Bar).filter(Bar.b_id == note).update({Bar.b_count_posts: Bar.b_count_posts - 1})
    # 根据帖子的p_id删除评论表对应的内容
    db_session.query(Comment).filter(Comment.p_id == p_id).filter(Comment.u_id == u_id).delete()
    # 根据被删除的帖子的p_id删除帖子表对应的内容
    db_session.query(Post_Image).filter(Post_Image.p_id==p_id).delete()
    db_session.query(Post).filter(Post.p_id ==p_id).filter(Post.u_id == u_id).delete()
    db_session.commit()
    path=request.headers.get('Referer')
    return redirect(path)

@bp.route('/guanli_user/',defaults={'page':1})
def guanli_user(page):
    age=''
    user=db_session.query(User).limit(9).offset((page - 1) * 9).all()
    for i in user:
        age = get_page_counts(i.u_id)
    return render_template('user-list.html',user=user,page=age)



