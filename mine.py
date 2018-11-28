from db import *
from user import *
bp=Blueprint('mine',__name__)

# 以下全是我的帖子那个按钮的东西的函数=====================================
@bp.route('/mypost/page/<int:user_id>/<int:page>/')
@bp.route('/user/mypost/<int:user_id>/',defaults={'page':1})
def my_posts(user_id,page):
    posts_list=[]
    user = db_session.query(User).filter(User.u_id == user_id).first()
    # 帖子信息
    post_list=db_session.query(Post).filter(Post.u_id == user_id).limit(2).offset((page - 1) * 2).all()
    page1=get_page_counts(user_id)
    note=[]
    for j in post_list:
        posts_list.append([j.p_title,j.p_content,j.p_create_at,j.p_id,j.u_id])
        note = db_session.query(User).filter(User.u_id == j.u_id).first()
    current_user=[]
    if is_login():
        current_user=session.get('current_user')
        current_user=db_session.query(User).filter(User.u_name==current_user).first()
    # 帖子图片
    img = db_session.query(Post_Image).all()
    return render_template('my_post.html', posts_list=posts_list, img=img, current_user=current_user, note=note, page=page1 + 1, current_page=page, user=user)


# 我的帖子的删除
@bp.route('/delete_mypost/<int:u_id>/<path:p_id>/',methods=['GET','POST'])
def delete_myposts(u_id,p_id):
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
    db_session.query(Post).filter(Post.p_id ==p_id).filter(Post.u_id == u_id).delete()
    db_session.commit()
    path = request.headers.get('Referer')
    return redirect(path)







# 我的贴吧
@bp.route('/user/mybar/<int:u_id>/')
def my_bar(u_id):
    current_user=[]
    bar_list=[]
    user = db_session.query(User).filter(User.u_id == u_id).first()
    list0 = db_session.query(Bar_relation).filter(Bar_relation.u_id == u_id).filter(Bar_relation.relation == 0).all()
    bar_class=get_all_topics()
    if is_login():
        current_user = session.get('current_user')
        current_user = db_session.query(User).filter(User.u_name == current_user).first()
    for i in list0:
        bar_name = (db_session.query(Bar).filter(Bar.b_id == i.b_id).first()).b_name
        bar_path = (db_session.query(Bar).filter(Bar.b_id == i.b_id).first()).b_path
        bar_statement = (db_session.query(Bar).filter(Bar.b_id == i.b_id).first()).b_statement
        bar_head_img= (db_session.query(Bar).filter(Bar.b_id == i.b_id).first()).b_head_img
        bar_list.append([bar_name,bar_path,bar_statement,bar_head_img])
    return render_template('my_bar.html',user=user,bar_list=bar_list, current_user=current_user,bar_class=bar_class)




# 我的贴吧删除
@bp.route('/delete_mybar/<int:u_id>/<path:b_path>/',methods=['GET','POST'])
def delete_mybar(u_id,b_path):
    # 根据被删除贴吧的信息找到贴吧的b_id
    a=(db_session.query(Bar).filter(Bar.b_path == b_path).first()).b_id
    # 用b_id找到Post表里的p_id
    p_id=(db_session.query(Post).filter(Post.b_id ==a ).first()).p_id
    # 根据p_id删除评论表里对应的一行数据
    db_session.query(Comment).filter(Comment.p_id == p_id).filter(Comment.u_id == u_id).delete()
    # 根据p_id删除帖子表里对应的一行数据
    db_session.query(Post).filter(Post.p_id ==p_id).filter(Post.u_id == u_id).delete()
    # 根据被删除贴吧的b_id找到贴吧关系表里对应的一行数据
    db_session.query(Bar_relation).filter(Bar_relation.b_id==a).delete()
    # 根据p_path找到删除Bars里的一行信息
    db_session.query(Bar).filter(Bar.b_path == b_path).delete()
    db_session.commit()
    path = request.headers.get('Referer')
    return redirect(path)


# 我收藏的帖子
@bp.route('/user/like/<int:u_id>/')
def my_like(u_id):
    # print(u_id,'这是u_id======================================')
    posts_like=[]
    current_user = []
    user = db_session.query(User).filter(User.u_id == u_id).first()
    lst=db_session.query(Post_relation).filter(Post_relation.u_id==u_id,Post_relation.relation==0).all()
    if is_login():
        current_user = session.get('current_user')
        current_user = db_session.query(User).filter(User.u_name == current_user).first()
    for i in lst:
        post=db_session.query(Post).get(i.p_id)
        # print(post, '这是post========================================================')
        if post is None:
            continue
        else:
            post_img=(db_session.query(Post_Image).filter(Post_Image.p_id==i.p_id).first()).img_path
            a=post.b_id
            # print(a,'这是a==========================================')
            b=post.u_id
            u_name=(db_session.query(User).filter(User.u_id==b).first()).u_nickname
            uu_id=(db_session.query(User).filter(User.u_id==b).first()).u_id
            bar_name=(db_session.query(Bar).filter(Bar.b_id==a).first()).b_name
            bar_path=(db_session.query(Bar).filter(Bar.b_id==a).first()).b_path
            posts_like.append([u_name,bar_name,post.p_title,post.p_create_at,post_img,post.p_content,bar_path,post.p_id,uu_id])

    return render_template('my_like.html',user=user,posts_like=posts_like, current_user=current_user)


