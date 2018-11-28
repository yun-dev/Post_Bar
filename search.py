from flask import Blueprint,render_template,request,jsonify,session
import db,tools,auth,os,uuid

bp = Blueprint('search',__name__)

# 搜索实时提示
@bp.route('/search/',methods=['GET','POST'])
def search_tip():
    data=request.get_json()
    keyword=data.get('keyword')
    search_data=db.search(keyword)
    bar=[]
    post=[]
    for b in search_data.get('bar'):
        bar.append([b.b_name,b.b_statement])
    for p in search_data.get('post'):
        post.append([p.p_title,p.p_content])
    return jsonify({'bar':bar,'post':post})

@bp.route('/submit_search/',methods=['GET','POST'])
def submit_search():
    user=db.User()
    if auth.is_login:
        user=db.db_session.query(db.User).filter(db.User.u_name==session.get('current_user')).first()
    keyword=request.form.get('search_input')
    search_data=db.search(keyword)
    bars=search_data.get('bar')
    posts=search_data.get('post')
    return render_template('search.html',user=user,bars=bars,posts=posts,old_keyword=keyword)
