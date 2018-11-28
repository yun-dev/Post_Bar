from flask import Blueprint,render_template,request,redirect,session,json,jsonify
import db,auth,uuid,os,base64

bp = Blueprint('post',__name__)

# 帖子详情
@bp.route('/post/<int:post_id>/')
def post_detail(post_id):
    current_user=[]
    if auth.is_login:
        current_user=session.get('current_user')
        current_user=db.db_session.query(db.User).filter(db.User.u_name==current_user).first()
    post=db.db_session.query(db.Post).filter(db.Post.p_id==post_id).first()
    bar=db.get_bar_by_id(post.b_id)
    comments=db.get_all_comments(post_id)
    return render_template("post_detail.html",user=current_user,post=post,bar=bar,comments=comments)

# 发帖
@bp.route('/new_post/',methods=['GET','POST'])
@auth.login_required
def new_post():
    data = json.loads(request.get_data('data'))
    title = data.get('title')
    content=data.get('content')
    bar_path=data.get('bar_path')
    imgs_list=data.get('imgs')
    imgs=[]
    for i in imgs_list:
        img_base64=(i['base64'])[23:]
        try:
            img_data=base64.b64decode(img_base64)
        except:
            pass
        img_path=str(uuid.uuid1())
        post_img='posts_imgs/'+img_path+'.jpg'
        imgs.append(post_img)
        with open('static/'+post_img,'wb+') as f:
            f.write(img_data)
    bar=db.db_session.query(db.Bar).filter(db.Bar.b_path==bar_path).first()
    current_user=db.db_session.query(db.User).filter(db.User.u_name==session.get('current_user')).first()
    db.add_post(title,content,bar.b_id,current_user.u_id,imgs)
    return jsonify({'status':0})

# 发评论
@bp.route('/new_comment/',methods=['GET','POST'])
def new_comment():
    if not auth.is_login():
        return jsonify({'status':'not_login'})
    current_user=session.get('current_user')
    current_user=db.db_session.query(db.User).filter(db.User.u_name==current_user).first()
    u_id=current_user.u_id
    data=request.get_json()
    p_id=data['p_id']
    c_content=data['c_content']
    f_id=data['f_id']
    db.add_comment(u_id,p_id,c_content,f_id)
    all_comments=db.get_all_comments(p_id)
    comments=[]
    for i in all_comments:
        commit_user=db.get_user_by_id(i.u_id)
        if i.f_id==0:
            comments.append([i.c_id,i.u_id,i.p_id,i.c_content,i.f_id,commit_user.u_head_img,commit_user.u_nickname,0,0])
        else:
            f_user=db.get_user_by_f_id(i.f_id)
            comments.append([i.c_id,i.u_id,i.p_id,i.c_content,i.f_id,commit_user.u_head_img,commit_user.u_nickname,f_user.u_id,f_user.u_nickname])
    post_obj=db.db_session.query(db.Post).filter(db.Post.p_id==p_id).first()
    post=[post_obj.p_id,post_obj.p_title,post_obj.p_content,post_obj.p_create_at,post_obj.p_count_comments,post_obj.b_id,post_obj.u_id]
    return jsonify({'comments':comments,'post':post})

# 删评论
@bp.route('/delete_comment/',methods=['GET','POST'])
def delete_comment():
    data=request.get_json()
    c_id=data.get('c_id')
    p_id=data.get('p_id')
    db.delete_comment(c_id,p_id)
    return jsonify({'status':0})