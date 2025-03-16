from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,BooleanField,DateField
from wtforms.validators import DataRequired, Length, EqualTo,Email
from datetime import date

class RegistrationForm(FlaskForm):
    username = StringField('用户名', validators=[
        DataRequired(),
        Length(min=4, max=20, message="用户名需为4-20位字符")
    ])
    password = PasswordField('密码', validators=[
        DataRequired(),
        Length(min=8, message="密码至少8位")
    ])
    confirm_password = PasswordField('确认密码', validators=[
        DataRequired(),
        EqualTo('password', message="两次密码不一致")
    ])
    submit = SubmitField('注册')

class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[
        DataRequired(message="用户名不能为空")
    ])
    password = PasswordField('密码', validators=[
        DataRequired(message="密码不能为空")
    ])
    remember = BooleanField('记住我')
    submit = SubmitField('登录')

class AddDeviceForm(FlaskForm):
    name = StringField('设备名称', validators=[DataRequired()])
    submit = SubmitField('添加设备')

class BorrowForm(FlaskForm):
    return_date = DateField(
        '预计归还日期',
        validators=[DataRequired(message="请选择归还日期")],
        default=date.today  # 默认今日
    )
    submit = SubmitField('确认借出')