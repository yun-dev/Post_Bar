from flask import Blueprint,render_template,request,session,jsonify,redirect
import db,tools,auth,os,uuid

bp = Blueprint('new',__name__)


# 新建/修改贴吧
@bp.route('/bar/<bar_path>/edit/',methods=['GET','POST'])
@auth.login_required
def bar_edit(bar_path):
    current_user=session.get('current_user')
    user=db.db_session.query(db.User).filter(db.User.u_name==current_user).first()
    if request.method=='GET':
        if bar_path=='0':
            bar=[]
            bar_id=0
            bar_path=0
            bar_head_img='img/bar_head_img.png'
            bar_banner_img='img/bar_banner_img.jpg'
        else:
            bar=db.db_session.query(db.Bar).filter(db.Bar.b_path==bar_path).first()
            bar_id=bar.b_id
            bar_path=bar.b_path
            bar_head_img=bar.b_head_img
            bar_banner_img=bar.b_banner_img
        return render_template("bar_edit.html",user=user,bar=bar,bar_id=bar_id,bar_path=bar_path,bar_head_img=bar_head_img,bar_banner_img=bar_banner_img)
    else:
        bar=db.db_session.query(db.Bar).filter(db.Bar.b_path==bar_path).first()
        b_id=request.form.get('b_id')
        b_name=request.form.get('b_name')
        b_path=request.form.get('b_path')
        b_topic=request.form.get('b_topic')
        b_statement=request.form.get('b_statement')
        if bar:
            b_head_img=bar.b_head_img
            b_banner_img=bar.b_banner_img
        else:
            bar_head_img='img/bar_head_img.png'
            bar_banner_img='img/bar_banner_img.jpg'
            
        head=request.files.get('b_head_img')
        if head:
            b_head_img_data=head.read()
            head_uuid=str(uuid.uuid1())
            b_head_img='bar_head/'+head_uuid+'.jpg'
            with open('static/'+b_head_img,'wb+') as f:
                f.write(b_head_img_data)
            im_head=tools.change_img_dbi('static/'+b_head_img,100,100)
            im_head.save('static/'+b_head_img)

        banner=request.files.get('b_banner_img')
        if banner:
            b_banner_img_data=banner.read()
            banner_uuid=str(uuid.uuid1())
            b_banner_img='bar_banner/'+banner_uuid+'.jpg'
            with open('static/'+b_banner_img,'wb+') as f:
                f.write(b_banner_img_data)
            im_banner=tools.change_img_dbi('static/'+b_banner_img,1024,188)
            im_banner.save('static/'+b_banner_img)

        if b_id=='0':
            new_bar=db.Bar(b_name=b_name,b_path=b_path,b_topic=b_topic,b_head_img=b_head_img,b_banner_img=b_banner_img,b_statement=b_statement)
            db.add_data(new_bar)
            db.add_data(db.Bar_relation(u_id=user.u_id,b_id=new_bar.b_id,relation=0))
        else:
            db.db_session.query(db.Bar).filter(db.Bar.b_id==b_id).update({db.Bar.b_name:b_name,db.Bar.b_path:b_path,db.Bar.b_topic:b_topic,db.Bar.b_head_img:b_head_img,db.Bar.b_banner_img:b_banner_img,db.Bar.b_statement:b_statement})
            db.db_session.commit()
        return redirect('/bar/'+b_path+'/')

# 自动生成贴吧路径
@bp.route('/submit_path/',methods=['GET','POST'])
@auth.login_required
def submit_path():
    b_name=request.get_json().get('b_name')
    b_name=b_name.replace('/','').replace('\\','')
    b_path=tools.create_path(b_name)
    return jsonify({"b_path":b_path})

# 选择贴吧主题
@bp.route("/select_topic/",methods=['GET','POST'])
@auth.login_required
def select_topic():
    topics=db.get_all_topics()
    topics_list=[]
    for t in topics:
        topics_list.append(t[0])
    return jsonify({"topics":topics_list})

# 表单验证
@bp.route("/form_check/",methods=['GET','POST'])
def form_check():
    data=request.get_json()
    b_id=data['b_id']
    b_name=data['b_name']
    b_path=data['b_path']
    name_status=0
    path_status=0
    if b_id!=0:
        bar=db.get_bar_by_id(b_id)
        if db.is_b_name_exist(b_name):
            if bar.b_name!=b_name:
                name_status=1
        if db.is_b_path_exist(b_path):
            if bar.b_path!=b_path:
                path_status=1
    else:
        if db.is_b_name_exist(b_name):
            name_status=1
        if db.is_b_path_exist(b_path):
            path_status=1
    return jsonify({'name_status':name_status,'path_status':path_status})