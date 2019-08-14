import hashlib

from flask import request
from flask import redirect
from flask import jsonify
from flask import session
from flask import render_template
from flask import make_response



from . import main
from app import csrf      #从main中引入csrf
from app.models import *
from .forms import TeacherForm #导入定义好的表单
from app import cache


def setPassWord(password):
    # password += BaseConfig.SECRET_KEY  #利用加盐方式，给秘钥加盐
    md5 = hashlib.md5()
    md5.update(password.encode())
    return md5.hexdigest()

#设置校验装饰器
def loginVaild(func):
    def inner(*args,**kwargs):
        username = request.cookies.get('username')
        id = request.cookies.get('user_id')
        session_username = session.get('username')
        if username and id and session_username:
            if username ==session_username:
                return func(*args,**kwargs)
        return redirect('/login/')
    return inner


@main.route('/register/',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        form_data = request.form
        username = form_data.get('username')
        password = form_data.get('password')
        identity = form_data.get('identity')
        user = User()
        user.username = username
        user.password = setPassWord(password)
        user.identity = identity
        user.save()
        return redirect('/login/')
    return render_template('register.html',**locals())


#登录
# @cache.cached(timeout=50)  #设置缓存
@main.route('/login/',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        form_data = request.form
        username = form_data.get('username')
        password = form_data.get('password')

        user = User.query.filter_by(username=username).first()
        #对身份进行识别判断是教师还是学生
        identity = user.identity
        #对教师表或者学生表的id来进行识别
        identity_id= user.identity_id

        if user:
            db_password = user.password
            send_password = setPassWord(password)
            if db_password == send_password:
                response = redirect('/index/')


                response.set_cookie('username',username)
                response.set_cookie('user_id',str(user.id))
                response.set_cookie('identity',str(identity))
                session['username'] = username
                #判断用户用没有填写详细信息，如果填写的话，那么identity_id有值。
                if user.identity_id:
                    response.set_cookie('identity_id',str(user.identity_id))
                else:
                    response.set_cookie('identity_id','')
                return response
    return render_template('login.html',**locals())

#首页面
@csrf.exempt  #不受csrf影响，不携带csrf也可以进入
@main.route('/index/',methods=['GET','POST'])
@loginVaild
# @cache.cached(timeout=50)  #设置缓存
def index():
    #获取进入index页面的人员身份
    identity= request.cookies.get('identity')
    identity_id = request.cookies.get('identity_id')


    #如果是post方式提交的话
    if request.method == 'POST':
        #如果人物的身份是教师的话
        if identity == '1':
            user_form = request.form

            #添加教师表
            teacher = Teacher()
            teacher.name = user_form.get('username')
            teacher.age = user_form.get('age')
            teacher.gender = user_form.get('gender')
            teacher.course_id = int(user_form.get('course'))
            teacher.save()

            #更新user表
            user_id = request.cookies.get('user_id')
            user = User.query.get(int(user_id))
            user.identity_id = int(teacher.id)
            user.save()

            #表单填写完成之后设置返回和保存dentity_id的cookie
            # print('*'*20,user.identity_id)
            response = make_response(render_template('index.html'),**locals())
            #
            # response = redirect('/index/')
            response.set_cookie('identity_id',str(user.identity_id))
            return response
    else:
        #如果进入的是教师的并且没有完善信息的话，就把所有课程返回给教师，供教师注册
        if identity == '1':
            if identity_id:
                # user = request.cookies.get('user_id')
                identity_id = request.cookies.get('identity_id')
                teacher = Teacher.query.get(int(identity_id))
                print('*'*20,teacher.id)
                return render_template('index.html', **locals())

            else:
                course = Course.query.all()
                cou_dict = {}
                for cou in course:
                    cou_id = str(cou.id)
                    label = cou.label
                    cou_dict[cou_id] = label


    return render_template('index.html',**locals())

#退出
@main.route('/logout/',methods=['GET','POST'])
def logout():
    response = redirect('/login/')
    for key in request.cookies:
        response.delete_cookie(key)
    del session['username']
    return  response

#添加教师
@csrf.exempt   #不受csrf影响
@main.route('/add_teacher/',methods=['GET','POST'])
def add_teacher():
    teacher_form = TeacherForm()   #使用forms.py中定义好的表单
    if request.method == 'POST':
        #获取前台传来的表单
        name = request.form.get('name')   #获取名字和forms的字段名一样
        age = request.form.get('age')
        gender = request.form.get('gender')
        course = request.form.get('course')

        #保存数据到teacher表
        teacher = Teacher()
        teacher.name = name
        teacher.age = age
        teacher.gender = gender
        teacher.course_id = int(course)
        teacher.save()
    return render_template('add_teacher.html',**locals())

#错误跳转的页面
# @csrf.error_handler #开启csrf
@main.route('/csrf_403/',methods=['GET','POST'])
def csrf_403():  #reason为错误信息
    # print(reason)
    return render_template('csrf_403.html',**locals())


# @csrf.error_handler
@main.route('/UserVaild/',methods=['GET','POST'])
def UserVaild():


    ###POST提交方式
    result= {'code':'','data':''}
    # print('*' * 20, 'POST')
    if request.method == 'POST':
        print('*'*20,'POST')
        data = request.form.get('username')
        if data:
            user = User.query.filter_by(username=data).first()
            if user:
                result['code'] = 400
                result['data'] = '用户已存在'
            else:
                result['code'] = 200
                result['data'] = '用户未存在，可以注册'
    else:
        result['code'] = 400
        result['data'] = '请求方式错误'
    return jsonify(result)


    ###GET提交方式
    # result= {'code':'','data':''}
    # # print('*' * 20, 'POST')
    # if request.method == 'POST':
    #     print('*'*20,'POST')
    #     data = request.form.get('username')
    #     if data:
    #         user = User.query.filter_by(username=data).first()
    #         if user:
    #             result['code'] = 400
    #             result['data'] = '用户已存在'
    #         else:
    #             result['code'] = 200
    #             result['data'] = '用户未存在，可以注册'
    # else:
    #     result['code'] = 400
    #     result['data'] = '请求方式错误'
    # return jsonify(result)



    # return jsonify({'key':'value'})

#清除缓存
@csrf.exempt
@main.route('/clearCache/',methods=['GET','POST'])
def clearCache():
    cache.clear()
    return 'cache is cleared'