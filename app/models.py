from app import models

class BaseModel(models.Model):
    __abstract__ = True  #抽象表为True，代表当前类为抽类，当前对象不被创建。
    id = models.Column(models.Integer,primary_key=True,autoincrement=True)

    #设置保存对象的方法
    def save(self):
        db = models.session() #设置session
        db.add(self)          #把对象添加到db
        db.commit()           #提交保存到数据库

    #设置删除对象的方法
    def delete_obj(self):
        db = models.session()  #设置session
        db.delete(self)        #把对象删除
        db.commit()            #提交保存到数据库

class User(BaseModel):
    __tablename__ = 'user'
    username = models.Column(models.String(32))
    password = models.Column(models.String(32))
    identity = models.Column(models.Integer) #0学生 1 教师
    identity_id = models.Column(models.Integer,default=0)

class Students(BaseModel): #继承BaseModel中的方法
    """
    学员表
    """
    __tablename__ = 'students'                #设置数据表的名称
    name = models.Column(models.String(32))   #设置对应的字段
    age = models.Column(models.Integer)
    gender = models.Column(models.Integer)    #0男 1女 -1未知

# class Stu_Cou(BaseModel):
#     """
#     课程学员关联表
#     """
#     __tablename__ = 'stu_cou'
#     course_id = models.Column(models.Integer,models.ForeignKey('course.id'))
#     student_id = models.Column(models.Integer,models.ForeignKey('students.id'))

#创建数据表
Stu_Cou = models.Table(
    'stu_cou',
    models.Column('id',models.Integer,primary_key=True,autoincrement=True),
    models.Column('course_id',models.Integer,models.ForeignKey('course.id')),
    models.Column('student_id',models.Integer,models.ForeignKey('students.id')),
)

class Course(BaseModel):
    """
    课程表
    """
    __tablename__ = 'course'
    label = models.Column(models.String(32))
    description = models.Column(models.Text)

    #设置双向映射
    to_teacher = models.relationship(  #执行映射表的字段
        'Teacher',                  #映射表，映射到谁
        backref = 'to_course_data'       #反向映射字段
    )

    #多对多
    to_student = models.relationship(
        'Students',
        secondary = Stu_Cou,
        backref = models.backref('to_course',lazy='dynamic'),  #stu_cou course
        lazy = 'dynamic',  #stu_cou student
        #select  访问该字段的时候加载所有映射数据
        #joined  对关联的两个表student和teacher表进行join查询
        #dynamic 不加载数据,为了防止数据多的时候查询卡
    )


class Grade(BaseModel):
    """
    课程，学员
    """
    __tablename__ = 'grade'
    grade = models.Column(models.Float,default=0)
    course_id = models.Column(models.Integer,models.ForeignKey('course.id'))
    student_id = models.Column(models.Integer,models.ForeignKey('students.id'))

#考勤
class Attendance(BaseModel):
    """
    考勤表,记录是否请假
    """
    __tablename__ = 'attendance'
    att_time = models.Column(models.Date)
    status = models.Column(models.Integer,default=1)  #0迟到，1是正常出勤，2早退，3请假，4旷课
    student_id = models.Column(models.Integer,models.ForeignKey('students.id')) #考勤，学生多对一映射


class Teacher(BaseModel):
    """
    教师表
    教师与课程多对一
    """
    __tablename__ = 'teachers'
    name = models.Column(models.String(32))
    age = models.Column(models.Integer)
    gender = models.Column(models.Integer) #0男 1女 -1未知
    course_id = models.Column(models.Integer,models.ForeignKey('course.id')) #教师，课程多对一映射


