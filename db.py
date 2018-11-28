from sqlalchemy import create_engine, Column, Integer, String, CHAR, DateTime, Text, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.functions import func
from sqlalchemy.orm import sessionmaker, scoped_session, Session
import datetime,os

engine = create_engine('mysql+mysqlconnector://root:root@127.0.0.1/bar_db',echo = True)
Base = declarative_base()

_Session : Session= scoped_session(sessionmaker(autocommit=False, autoflush=True, bind=engine))
db_session = _Session
Base.query = db_session.query_property()

class User(Base):
    __tablename__='users'
    u_id=Column(Integer,primary_key=True)
    u_name=Column(String(24),unique=True,nullable=False)
    u_password=Column(String(128),nullable=False,default='')
    u_nickname=Column(String(32))
    u_sex=Column(CHAR,default='')
    u_phone = Column(String(32),unique=True,nullable=False)
    u_birthday=Column(DateTime,server_default=func.now())
    u_create_at=Column(DateTime,server_default=func.now())
    u_introduce = Column(Text)
    u_head_img=Column(String(128))
    u_alive = Column(Integer,default=1) # 1为存活（可发贴，评论），0为死亡（禁言）
    u_permission=Column(Integer,default=0) # 1为管理员，0为普通用户


class Bar(Base):
    __tablename__='bars'
    b_id=Column(Integer,primary_key=True)
    b_name=Column(String(32),nullable=False,unique=True)
    b_path=Column(String(128),nullable=False,)
    b_topic=Column(String(16),nullable=False)
    b_statement=Column(String(255),default='欢迎关注本吧')
    b_head_img=Column(String(128))
    b_banner_img=Column(String(128))
    b_count_users=Column(Integer,default=0)
    b_count_posts=Column(Integer,default=0)


class Bar_relation(Base):
    __tablename__='bars_relation'
    u_id=Column(Integer,primary_key=True)
    b_id=Column(Integer,primary_key=True)
    relation=Column(Integer,default=2)

class Post_relation(Base):
    __tablename__='posts_relation'
    u_id=Column(Integer,primary_key=True)
    p_id=Column(Integer,primary_key=True)
    relation=Column(Integer,default=2)


class Post(Base):
    __tablename__='posts'
    p_id=Column(Integer,primary_key=True)
    p_title=Column(String(64),nullable=False)
    p_content=Column(String(1000),nullable=False)
    p_create_at=Column(DateTime,server_default=func.now())
    p_count_comments=Column(Integer,default=0)
    b_id=Column(Integer,nullable=False)
    u_id=Column(Integer,nullable=False)


class Post_Image(Base):
    __tablename__='post_images'
    i_id=Column(Integer,primary_key=True)
    p_id=Column(Integer,nullable=False)
    img_path=Column(String(128),unique=True,nullable=False)


class Comment(Base):
    __tablename__='comments'
    c_id=Column(Integer,primary_key=True)
    u_id=Column(Integer,nullable=False)
    p_id=Column(Integer,nullable=False)
    c_content=Column(String(255),nullable=False)
    f_id=Column(Integer,nullable=False,default=0)

def close_session(exception=None):
    db_session.close()

def init_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    add_data(User(u_name='admin',u_password='a621ad1bcb5ceaa8f6b3bc0a8fa1451dd268004adbfcb7e608cb932ccc009950',u_nickname='管理员',u_head_img='img/user2.jpg',u_phone='13855645642',u_permission=1))
    add_data(User(u_name='zhangsan',u_password='a621ad1bcb5ceaa8f6b3bc0a8fa1451dd268004adbfcb7e608cb932ccc009950',u_nickname='张三',u_head_img='img/user.jpg',u_phone='13855645643'))
    add_data(User(u_name='lisi',u_password='a621ad1bcb5ceaa8f6b3bc0a8fa1451dd268004adbfcb7e608cb932ccc009950',u_nickname='李四',u_head_img='img/user4.jpg',u_phone='13855645644'))
    add_data(User(u_name='wangwu',u_password='a621ad1bcb5ceaa8f6b3bc0a8fa1451dd268004adbfcb7e608cb932ccc009950',u_nickname='王五',u_head_img='img/user.jpg',u_phone='13855645645',u_introduce='张三盗我头像！！！'))
    add_data(Bar(b_name='剑灵吧',b_path='bns',b_topic='游戏',b_head_img='img/bar.jpg',b_banner_img='img/bns/bns_bg.jpg',b_statement='师出洪门派，行仗义天下'))
    add_data(Bar(b_name='萌妹御姐吧',b_path='mmyjb',b_topic='美女',b_head_img='img/user2.jpg',b_banner_img='img/mmyjb.jpg',b_statement='遇见最美的自己'))
    add_data(Bar(b_name='英雄联盟吧',b_path='lol',b_topic='游戏',b_head_img='img/lol_head.jpg',b_banner_img='img/lol.jpg',b_statement='全球最大英雄联盟玩家聚集交流平台！'))
    add_data(Bar(b_name='魔方吧',b_path='mofangba',b_topic='思维',b_head_img='img/mofang_head.jpg',b_banner_img='img/mofang.jpg',b_statement='魔方不需要公式。。'))
    add_data(Bar(b_name='Ubuntu吧',b_path='ubuntu',b_topic='系统',b_head_img='img/ubuntu_head.jpg',b_banner_img='img/ubuntu.jpg',b_statement='Ubuntu爱好者的交流平台'))
    add_data(Bar_relation(u_id=1,b_id=1,relation=0))
    add_data(Bar_relation(u_id=1,b_id=4,relation=0))
    add_data(Bar_relation(u_id=1,b_id=5,relation=0))
    add_data(Bar_relation(u_id=3,b_id=2,relation=0))
    add_data(Bar_relation(u_id=2,b_id=3,relation=0))
    add_data(Bar_relation(u_id=2,b_id=1,relation=1))
    add_data(Bar_relation(u_id=3,b_id=1,relation=1))
    add_data(Bar_relation(u_id=4,b_id=1,relation=1))
    add_data(Bar_relation(u_id=3,b_id=3,relation=1))
    add_data(Bar_relation(u_id=4,b_id=5,relation=1))
    add_data(Post(p_title='剑士毕业号出售',p_content='出售电十毕业号，有意的 伽 Q 1111111111 ',b_id=1,p_count_comments=0,u_id=1))
    add_data(Post(p_title='召唤师专属标题',p_content='收泰天首饰材料，卖的来江流市仓库。。。',b_id=1,p_count_comments=0,u_id=4))
    add_data(Post(p_title='LPL战报',p_content='RNG进8强了',b_id=3,p_count_comments=0,u_id=2))
    add_data(Post(p_title='四阶双重介子，不会的看过来',p_content="单层 ，双层 分别使用“巨介子”公式B L' D2 L D F' D2 F D' B' F' R U2 R' U' B U2 B' U F",b_id=4,p_count_comments=0,u_id=1))
    add_data(Post_Image(p_id=4,img_path='posts_imgs/mofang.jpg'))
    add_data(Post_relation(u_id=1,p_id=1,relation=0))
    add_data(Post_relation(u_id=2,p_id=1,relation=1))
    add_data(Post_relation(u_id=3,p_id=1,relation=1))
    add_data(Post_relation(u_id=1,p_id=2,relation=0))
    add_data(Post_relation(u_id=2,p_id=3,relation=0))
    add_data(Post_relation(u_id=3,p_id=3,relation=1))
    print('--------------------------init finished--------------------------')

def add_data(obj):
    db_session.add(obj)
    db_session.commit()


# 通过用户id查询用户
def get_user_by_id(u_id):
    user=db_session.query(User).filter(User.u_id==u_id).first()
    return user

# 通过吧id查询贴吧
def get_bar_by_id(b_id):
    bar=db_session.query(Bar).filter(Bar.b_id==b_id).first()
    return bar

# 获取用户吧龄
def get_age(user_id):
    user=db_session.query(User).filter(User.u_id==user_id).first()
    create_time=user.u_create_at
    now_time=datetime.datetime.now()
    age=int((now_time-create_time).total_seconds())/(60*60*24*365)
    return round(age,1)

# 获取我创建的吧
def get_my_bars(user_id):
    bars_id=db_session.query(Bar_relation).filter(Bar_relation.u_id==user_id).filter(Bar_relation.relation==0).all()
    bars=[]
    for b in bars_id:
        bar=db_session.query(Bar).filter(Bar.b_id==b.b_id).first()
        bars.append(bar)
    return bars

# 获取我关注的吧
def get_my_concentrated_bars(user_id):
    bars_id=db_session.query(Bar_relation).filter(Bar_relation.u_id==user_id).all()
    bars=[]
    for b in bars_id:
        bar=db_session.query(Bar).filter(Bar.b_id==b.b_id).first()
        bars.append(bar)
    return bars

# 获取所有的吧，按热度排序（关注人数）
def get_all_bars():
    bars=db_session.query(Bar).order_by(Bar.b_count_users.desc()).all()
    return bars

# 获取所有的吧，按热度排序（关注人数）并进行分页
def get_all_bars_hot(page_bar=1,topic='推荐'):
    if topic=='推荐':
        all_bars = db_session.query(Bar).order_by(Bar.b_count_users.desc()).limit(4).offset((page_bar - 1) * 4).all()
    else:
        all_bars=db_session.query(Bar).filter(Bar.b_topic==topic).order_by(Bar.b_count_users.desc()).limit(4).offset((page_bar-1)*4).all()
    return all_bars

# 查询帖子分页数量（每页两条）
def get_bar_page_counts(topic='推荐'):
    if topic=='推荐':
        posts=db_session.query(Bar).all()
    else:
        posts=db_session.query(Bar).filter(Bar.b_topic==topic).all()
    pages=len(posts)
    if pages%4>0:
        page_count=pages//4+1
    else:
        page_count=pages//4
    return page_count

#删除贴吧及服务器中关于帖吧的图片
def delete_someone_bar(b_id):
    bar=db_session.query(Bar).filter(Bar.b_id==b_id).first()
    b_head_img=bar.b_head_img
    b_banner_img=bar.b_banner_img
    try:

        headImg='static/'+b_head_img
        os.remove(headImg)
    except:
        print('图片不存在')
    try:
        bannerImg='static/'+b_banner_img
        os.remove(bannerImg)
    except:
        print('图片不存在')
    bar_posts=db_session.query(Post).filter(Post.b_id==b_id).all()
    for bar_post in bar_posts:
        p_id=bar_post.p_id
        imgs_path = get_post_img(p_id)
        for img_path in imgs_path:
            der = 'static/' + img_path.img_path
            try:
                os.remove(der)
            except:
                print('图片不存在')
        db_session.query(Post_Image).filter(Post_Image.p_id == p_id).delete()
        db_session.query(Comment).filter(Comment.p_id == p_id).delete()
        db_session.query(Post_relation).filter(Post_relation.p_id == p_id).delete()
    db_session.query(Post).filter(Post.b_id==b_id).delete()

    db_session.query(Bar_relation).filter(Bar_relation.b_id==b_id).delete()
    print(b_id, '-------------------------------用户创建吧的id')
    db_session.query(Bar).filter(Bar.b_id==b_id).delete()
    db_session.commit()

#删除用户
def deiete_user(u_id):

    u_img=db_session.query(User).filter(User.u_id==u_id).first()
    der='static/'+u_img.u_head_img
    try:
        os.remove(der)
    except:
        print('图片不存在')
    u_p=db_session.query(Bar_relation).filter(Bar_relation.u_id==u_id).filter(Bar_relation.relation==0).all()
    for i in u_p:
        delete_someone_bar(i.b_id)
    db_session.query(User).filter(User.u_id==u_id).delete()
    db_session.commit()


# 判断吧名是否存在
def is_b_name_exist(b_name):
    bar=db_session.query(Bar).filter(Bar.b_name==b_name).first()
    if bar:
        return True
    return False

# 判断吧的路径是否存在
def is_b_path_exist(b_path):
    bar=db_session.query(Bar).filter(Bar.b_path==b_path).first()
    if bar:
        return True
    return False

# 获取所有主题
def get_all_topics():
    all_topics=db_session.query(Bar.b_topic).group_by(Bar.b_topic).all()
    return all_topics

# 点击关注
def attention(u_id,b_id,relation):
    b_r=Bar_relation(u_id=u_id,b_id=b_id,relation=relation)
    db_session.query(Bar).filter(Bar.b_id==b_id).update({Bar.b_count_users:Bar.b_count_users+1})
    add_data(b_r)

# 点击取消关注
def cancel_attention(u_id,b_id):
    db_session.query(Bar_relation).filter(Bar_relation.u_id==u_id).filter(Bar_relation.b_id==b_id).delete()
    db_session.query(Bar).filter(Bar.b_id==b_id).update({Bar.b_count_users:Bar.b_count_users-1})
    db_session.commit()

# 查询关注状态，未关注则返回 None
def attention_status(u_id,b_id):
    data=db_session.query(Bar_relation).filter(Bar_relation.u_id==u_id).filter(Bar_relation.b_id==b_id).first()
    if data is not None:
        return data.relation
    return None

# 查询所有帖子，按热度或者最新发布排序,每页10条，默认第1页
# order_by_hot 默认为False，此时按最新发布时间排序；若为True，则按热度（回复数量）降序
#  b_id默认空,
def get_all_posts(page_index=1,order_by_hot=False,b_id=None):
    if b_id is None:
        if order_by_hot==True:
            all_posts=db_session.query(Post).order_by(Post.p_count_comments.desc()).limit(2).offset((page_index-1)*2).all()
        else:
            all_posts=db_session.query(Post).order_by(Post.p_create_at.desc()).limit(2).offset((page_index-1)*2).all()
    else:
        if order_by_hot==True:
            all_posts=db_session.query(Post).filter(Post.b_id==b_id).order_by(Post.p_count_comments.desc()).limit(2).offset((page_index-1)*2).all()
        else:
            all_posts=db_session.query(Post).filter(Post.b_id==b_id).order_by(Post.p_create_at.desc()).limit(2).offset((page_index-1)*2).all()
    return all_posts

# 查询用户发布的所有帖子，按最新发布时间排序，每页10条，默认第1页
def get_user_all_posts(u_id,page_index=1):
    all_posts=db_session.query(Post).filter(Post.u_id==u_id).limit(2).offset((page_index-1)*2).all()
    return all_posts

# 查询帖子分页数量（每页两条）
#b_id默认为空
def get_page_counts(u_id=None,b_id=None):
    if b_id is None:
        if u_id is None:
            posts=db_session.query(Post).all()
        else:
            posts=db_session.query(Post).filter(Post.u_id==u_id).all()
        pages=len(posts)
        if pages%2>0:
            page_count=pages//2+1
        else:
            page_count=pages//2
    else:
        if u_id is None:
            posts=db_session.query(Post).filter(Post.b_id==b_id).all()
        else:
            posts=db_session.query(Post).filter(Post.u_id==u_id).filter(Post.b_id==b_id).all()
        pages=len(posts)
        if pages%2>0:
            page_count=pages//2+1
        else:
            page_count=pages//2
    return page_count

# 查询某个帖子的图片
def get_post_img(p_id,count=0):
    imgs_path=db_session.query(Post_Image).filter(Post_Image.p_id == p_id).all()
    if count!=0:
        if len(imgs_path)>count:
            return imgs_path[0:3]
    return imgs_path

# 根据主题查询贴吧
def get_bars_by_topic(topic):
    bars=db_session.query(Bar).filter(Bar.b_name==topic).all()
    return bars

# 发表一个帖子
    # imgs  传入图片路径列表
def add_post(title,content,b_id,u_id,imgs=[]):
    post=Post(p_title=title,p_content=content,b_id=b_id,u_id=u_id)
    db_session.query(Bar).filter(Bar.b_id==b_id).update({Bar.b_count_posts:Bar.b_count_posts+1})
    add_data(post)
    for img in imgs:
        post_img=Post_Image(p_id=post.p_id,img_path=img)
        add_data(post_img)

# 删除帖子及服务器中关于帖子图片
def delete_someone_post(p_id,b_id):
    imgs_path = get_post_img(p_id)
    for img_path in imgs_path:
        der = 'static/' + img_path.img_path
        try:
            os.remove(der)
        except:
            print('图片不存在')
    db_session.query(Comment).filter(Comment.p_id == p_id).delete()
    db_session.query(Post_Image).filter(Post_Image.p_id == p_id).delete()
    db_session.query(Post_relation).filter(Post_relation.p_id == p_id).delete()
    db_session.query(Post).filter(Post.p_id == p_id).delete()
    db_session.query(Bar).filter(Bar.b_id == b_id).update({Bar.b_count_posts: Bar.b_count_posts - 1})
    db_session.commit()

# 发表评论
def add_comment(u_id,p_id,c_content,f_id):
    c=Comment(u_id=u_id,p_id=p_id,c_content=c_content,f_id=f_id)
    db_session.query(Post).filter(Post.p_id==p_id).update({Post.p_count_comments:Post.p_count_comments+1})
    add_data(c)
    pass

# 删除评论
def delete_comment(c_id,p_id):
    db_session.query(Post).filter(Post.p_id==p_id).update({Post.p_count_comments:Post.p_count_comments-1})
    def delete_child_commit(comment_id):
        lst=db_session.query(Comment).filter(Comment.f_id==comment_id).all()
        if lst:
            for i in lst:
                delete_child_commit(i.c_id)
        else:
            db_session.query(Comment).filter(Comment.c_id==comment_id).delete()
    db_session.query(Comment).filter(Comment.c_id==c_id).delete()
    db_session.commit()

# 获取帖子的评论
def get_all_comments(p_id):
    all_comments=db_session.query(Comment).filter(Comment.p_id==p_id).filter(Comment.f_id==0).all()
    comments=[]
    def select_comment(lst):
        for c in lst:
            comments.append(c)
            f=db_session.query(Comment).filter(Comment.p_id==p_id).filter(Comment.f_id==c.c_id).all()
            if f:
                select_comment(f)
        return comments
    return select_comment(all_comments)

# 查询父id对应的评论人
def get_user_by_f_id(f_id):
    f_comment=db_session.query(Comment).filter(Comment.c_id==f_id).first()
    user=db_session.query(User).filter(User.u_id==f_comment.u_id).first()
    if user:
        return user
    return []

# 搜索引擎
def search(keyword):
    bar_data=db_session.query(Bar).filter(Bar.b_name.like('%'+keyword+'%')).all()
    bar_data+=db_session.query(Bar).filter(Bar.b_statement.like('%'+keyword+'%')).all()
    post_data=db_session.query(Post).filter(Post.p_title.like('%'+keyword+'%')).all()
    post_data+=db_session.query(Post).filter(Post.p_content.like('%'+keyword+'%')).all()
    result={'bar':bar_data,'post':post_data}
    return result

if __name__=='__main__':
    init_db()