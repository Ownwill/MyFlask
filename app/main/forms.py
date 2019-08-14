import wtforms                  #定义字段
from flask_wtf import FlaskForm #定义表单
from wtforms import validators  #定义校验
from app.models import Course #引入课程模型

# course_list = [(c.id,c.label) for c in Course.query.all()] #设置课程列表

course_list = []

class TeacherForm(FlaskForm): #设置类继承表单的方法
    """
       form字段的参数
       label=None, 表单的标签
       validators=None, 校验，传入校验的方法
       filters=tuple(), 过滤
       description='',  描述
       id=None, html id
       default=None, 默认值
       widget=None,
       render_kw=None,
       """
    name = wtforms.StringField('教师姓名',
                               render_kw={
                                   'class':'form-control',
                                   'placeholder':'教师姓名',
                               }, #定义前台表单的样式
                               validators = [
                                   validators.DataRequired('姓名不可以为空')
                               ] #设置校验
                               )
    age = wtforms.IntegerField('教师年龄',
                               render_kw={
                                   'class': 'form-control',
                                   'placeholder': '教师年龄',
                               },
                                validators = [
                                    validators.DataRequired('年龄不可以为空')
                                ]
                               )
    gender = wtforms.IntegerField('教师性别',
                                  render_kw={
                                      'class': 'form-control',
                                      'placeholder': '教师性别',
                                  },
                                  validators=[
                                      validators.DataRequired('性别不可以为空')
                                  ]
                                  )
    course = wtforms.SelectField(  #下拉列表对应的字段
        '学科',
        choices=course_list,
        render_kw={
            'class': 'form-control',
        },
    )