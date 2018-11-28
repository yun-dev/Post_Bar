from flask import Blueprint,render_template,request,session,jsonify,redirect,url_for
import db,tools,auth,os

bp = Blueprint('bar',__name__)


@bp.route('/post_page/<bar_path>/<int:page>/')
@bp.route('/bar/<bar_path>/',defaults={'page':1})
def bar_index(bar_path,page):
    chang = len(db.get_all_bars_hot(page_bar=page, topic='推荐'))
    print('第几页-----------------------------',page)
    select_bar_info =db.db_session.query(db.Bar).filter(db.Bar.b_path == bar_path).first()
    b_id = select_bar_info.b_id
    select_posts_info=db.db_session.query(db.Post).filter(db.Post.b_id == b_id).all()
    list1 = []
    list_sum = []
    list_img=[]
    for i in select_posts_info:
        a = i.u_id
        p_id=i.p_id
        if a in list1:
            pass
        else:
            list1.append(a)
    count=0
    user=[]
    user_img=None
    for k in list1:
        sum_user = db.db_session.query(db.Post).filter(db.Post.b_id == b_id).filter(db.Post.u_id == k).count()
        list_sum.append(sum_user)
        count = max(list_sum)
        u_id_suoyin= list_sum.index(count)
        u_id = list1[u_id_suoyin]
        user=db.get_user_by_id(u_id)
        print(type(user),'----------------------------------------------------------------------你猜我是啥')
        print('本吧牛人',user.u_name)
        user_img=db.get_user_by_id(u_id).u_head_img

    if auth.is_login():
        current_user=session.get('current_user')
        select_user_info=db.db_session.query(db.User).filter(db.User.u_name==current_user).first()
        u_id=select_user_info.u_id
        attetion_bar_state = db.db_session.query(db.Bar_relation).filter(db.Bar_relation.b_id == b_id).filter(db.Bar_relation.u_id==u_id).first()
        return render_template("bar.html", select_bar_info=select_bar_info, attetion_bar_state=attetion_bar_state,select_user_info=select_user_info,max_sum=count,user=user,select_posts_info=select_posts_info,imgs_path=list_img,user_img=user_img,page=page,current_user=current_user,chang=chang)
    else:
        select_bar_info = db.db_session.query(db.Bar).filter(db.Bar.b_path == bar_path).first()
        return render_template("bar.html",select_bar_info=select_bar_info,max_sum=count,user=user,select_posts_info=select_posts_info,user_img=user_img,page=page,chang=chang)


@bp.route('/delete_post/<int:p_id>/<int:b_id>/')
def delete_post(p_id,b_id):
    last_url=request.headers.get('Referer')
    if last_url.find('/post/'+str(p_id))>=0:
        last_url='/bar/'+(db.get_bar_by_id(b_id).b_path)

    print(last_url,'网页上的路由________________________________________________')
    db.delete_someone_post(p_id, b_id)
    return redirect(last_url)

@bp.route('/bar_page/<topic>/<int:page>')
@bp.route('/bar_list/<topic>/',defaults={'page':1})
@bp.route('/bar_list',defaults={'topic':'推荐','page':1})
def bar_list(topic,page):
    global select_topic_bars

    topic_html=topic
    select_topic_bars=[]
    if topic=='推荐':
        select_topic_bars=db.db_session.query(db.Bar).all()
    else:
        select_topic_bars = db.db_session.query(db.Bar).filter(db.Bar.b_topic == topic).all()
    if auth.is_login():
        current_user=session.get('current_user')
        select_users_info=db.db_session.query(db.User).filter(db.User.u_name==current_user).first()
        select_barRelation_info=db.db_session.query(db.Bar_relation).filter(db.Bar_relation.u_id==select_users_info.u_id).all()
        list_b_id=[]
        list_b_topic=[]
        list_bars_info=[]
        for barBelation in select_barRelation_info:
            b_id=barBelation.b_id
            select_bars_info = db.db_session.query(db.Bar).filter(db.Bar.b_id ==b_id).first()
            list_b_id.append(b_id)
            list_bars_info.append(select_bars_info)

        for bar_info in list_bars_info:
            b_name=bar_info.b_name
            if b_name not in list_b_topic:
                list_b_topic.append(b_name)

        return render_template("bar_list.html", select_user_info=select_users_info,select_barRelation_info=select_barRelation_info,list_b_topic=list_b_topic,topic_html=topic_html,select_topic_bars=select_topic_bars,current_user=current_user,page=page)

    else:

        return render_template("bar_list.html",topic_html=topic_html,select_topic_bars=select_topic_bars,page=page)

@bp.route("/delete_bar/<int:b_id>/", methods=['POST','GET'])
def delete(b_id):
    last_url=request.headers.get('Referer')
    db.delete_someone_bar(b_id)
    print(b_id, '-------------------------------用户创建吧的id')
    return redirect(last_url)
@bp.route('/list_new_t/<int:page>')
@bp.route('/list_new_t/',defaults={'page':1})
def list_new_t(page):
    if auth.is_login():
        current_user=session.get('current_user')
        currentUser=db.db_session.query(db.User).filter(db.User.u_name==current_user).first()
        bar=db.db_session.query(db.Bar).limit(8).offset((page - 1) * 8).all()
        age = ''
        user = db.db_session.query(db.User).limit(9).offset((page - 1) * 9).all()
        posts= db.db_session.query(db.Post).limit(9).offset((page - 1) * 9).all()
        for i in user:
            age = db.get_page_counts(i.u_id)

        return render_template('list_new_t.html',bar=bar,page=page,user=user,age=age,posts=posts,currentUser=currentUser)
    else:
        return redirect('/')

#删除人
@bp.route("/delete_user/<int:u_id>/")
def delete_some_user(u_id):
    last_url=request.headers.get('Referer')
    db.deiete_user(u_id)
    print(u_id, '-------------------------------用户创建吧的id')
    return redirect(last_url)