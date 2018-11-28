from hashlib import md5,sha256
from pypinyin import lazy_pinyin
from PIL import Image
import db

def security_password(pwd):
    """
    pwd: 传入明文密码
    return: 返回 md5、哈希256加密后的密文
    """
    one=md5(pwd.encode()).digest()
    salt='this is my post_bar'
    two=sha256((salt+str(one)+salt).encode()).hexdigest()
    security_code=sha256((salt+str(two)+salt).encode()).hexdigest()
    return security_code

def create_path(word):
    """
    word: 传入中文
    return: 返回中文对应的拼音
    """
    lst=lazy_pinyin(word)
    result=""
    for i in lst:
        result+=i
    while True:
        if not db.is_b_path_exist(result):
            return result
        result+="-copy"

def change_img_dbi(image,width,height):
    """
    image: 图片路径
    width: 想要的图片长度
    height: 想要的图片高度
    return: 返回 PIL.Image.Image 对象
    """
    rate=width/height
    im=Image.open(image)
    im = im.convert('RGB')
    old_width=im.size[0]
    old_height=im.size[1]
    print('原图：',old_width,'------',old_height)
    w_h=old_width/old_height
    if w_h>rate:
        new_width=int(old_height*rate)
        new_height=old_height
        l=(old_width-new_width)//2
        u=0
        r=new_width+(old_width-new_width)//2
        d=new_height
    elif w_h<rate:
        new_width=old_width
        new_height=int(old_width/rate)
        l=0
        u=(old_height-new_height)//2
        r=new_width
        d=new_height+(old_height-new_height)//2
    else:
        new_width=old_width
        new_height=old_height
        l=0
        u=0
        r=new_width
        d=new_height
    print('左上右下: ',l,'   ',u,'   ',r,'   ',d)
    region = im.crop((l,u,r,d))
    return region

if __name__ == '__main__':
    print(security_password('123'))