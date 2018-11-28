from flask import Flask, render_template,session,request,redirect,jsonify
import auth,db,bar,user,post,new,mine,reset,search

app = Flask(__name__)

app.secret_key = 'post_bar'

app.register_blueprint(auth.bp)
app.register_blueprint(bar.bp)
app.register_blueprint(user.bp)
app.register_blueprint(post.bp)
app.register_blueprint(new.bp)
app.register_blueprint(mine.bp)
app.register_blueprint(reset.bp)
app.register_blueprint(search.bp)

app.teardown_appcontext(db.close_session)

app.add_template_global(db.get_user_by_id)
app.add_template_global(db.get_user_by_f_id)
app.add_template_global(db.get_bar_by_id)
app.add_template_global(db.get_all_bars)
app.add_template_global(db.get_all_topics)
app.add_template_global(db.attention_status)
app.add_template_global(db.get_all_posts)
app.add_template_global(db.get_user_all_posts)
app.add_template_global(db.get_page_counts)
app.add_template_global(db.get_post_img)
app.add_template_global(db.get_bars_by_topic)
app.add_template_global(db.get_all_bars_hot)
app.add_template_global(db.get_bar_page_counts)

# 主页
@app.route('/page/<int:page>/')
@app.route('/',defaults={'page':1})
def index(page):
    if auth.is_login():
        current_user=session.get('current_user')
        current_user=db.db_session.query(db.User).filter(db.User.u_name==current_user).first()
        age=db.get_age(current_user.u_id)
        my_created_bars=db.get_my_bars(current_user.u_id)
        my_concentrated_bars=db.get_my_concentrated_bars(current_user.u_id)
        return render_template('index.html',user=current_user,age=age,my_created_bars=my_created_bars,my_concentrated_bars=my_concentrated_bars,current_page=page)
    return render_template('index.html',user=db.User(),current_page=page)

# 点击关注/取消关注按钮
@app.route('/concentrate_a_bar/<int:b_id>/')
@auth.login_required
def concentrate_a_bar(b_id):
    last_url=request.headers.get('Referer')
    current_user=session.get('current_user')
    u_id=(db.db_session.query(db.User).filter(db.User.u_name==current_user).first()).u_id
    if 'cancel' in request.args:
        db.cancel_attention(u_id,b_id)
    else:
        db.attention(u_id,b_id,1)
    return redirect(last_url)


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)