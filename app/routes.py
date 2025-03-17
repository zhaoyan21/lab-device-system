
from datetime import datetime
from functools import wraps
from flask import render_template, request, redirect, url_for, flash
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from app.Model import db, User, Device, Borrowrecord
from app.__init__ import create_app
from app.forms import RegistrationForm, LoginForm, AddDeviceForm, BorrowForm

app = create_app()
bcrypt = Bcrypt()
bcrypt.init_app(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if  current_user.role.lower() != 'admin':
            flash('无权访问此页面', 'danger')
            print(current_user.role)
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function
@app.route('/base',methods=['GET','POST'])
def base():
    return render_template("base.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()  # 创建表单实例
    if form.validate_on_submit():
        # 处理注册逻辑
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('注册成功！','success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route("/login",methods=['GET','POST'])
def login():
    form=LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if form.validate_on_submit():
        # 查询用户
        user = User.query.filter_by(username=form.username.data).first()

        # 验证用户是否存在且密码正确
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=form.remember.data)  # 处理“记住我”
            flash('欢迎使用本系统', 'success')
            next_page = request.args.get('next')  # 获取重定向路径
            return redirect(next_page or url_for('dashboard'))
        else:
            flash('用户名或密码错误', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required  # 需要登录才能访问
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/add_device', methods=['GET', 'POST'])
@login_required
@admin_required
def add_device():
    form = AddDeviceForm()
    if form.validate_on_submit():
        device = Device(
            name=form.name.data,
        )
        db.session.add(device)
        db.session.commit()
        flash('设备添加成功', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_device.html', form=form)

@app.route('/dashboard',methods=['GET','POST'])
@login_required
def dashboard():
    search_keyword = request.args.get('search', '')
    status_filter = request.args.get('status', '')

    # 构建基础查询
    query = Device.query

    # 应用搜索过滤
    if search_keyword:
        query = query.filter(Device.name.ilike(f'%{search_keyword}%'))  # 模糊匹配名称

    # 应用状态过滤
    if status_filter:
        query = query.filter(Device.status == status_filter)

    # 执行查询
    devices = query.all()
    return render_template('dashboard.html', username=current_user.username, devices=devices)


@app.route('/borrow/<int:device_id>', methods=['GET', 'POST'])
@login_required
def borrow(device_id):
    device = Device.query.get_or_404(device_id)
    form = BorrowForm()
    if device.status != 'available':
        flash('该仪器当前不可借', 'warning')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        # 处理借出表单（预计归还时间等）
        try:
            return_date= datetime.strptime(request.form['return_date'], '%Y-%m-%d')
        except ValueError:
            flash('日期格式错误，请使用 YYYY-MM-DD 格式', 'danger')
            return redirect(url_for('borrow', device_id=device_id))
        record = Borrowrecord(user_id=current_user.id, device_id=device.id,borrow_date=datetime.utcnow(),return_date=return_date)
        device.status = 'borrowed'
        db.session.add(record)
        db.session.commit()
        flash('借出成功！', 'success')
        return redirect(url_for('dashboard'))

    return render_template('borrow_form.html', device=device, form=form)

@app.route('/device/admin/<int:device_id>',methods=['GET','POST'])
@login_required
@admin_required
def admin_device(device_id):
    device = Device.query.get_or_404(device_id)
    # 定义状态切换顺序：available → borrowed → maintenance → available
    status_order = ['available', 'borrowed', 'maintenance']
    current_index = status_order.index(device.status)
    new_index = (current_index + 1) % len(status_order)
    device.status = status_order[new_index]

    try:
        db.session.commit()
        flash(f'设备 [{device.name}] 状态已更新为 {device.status}', 'success')
    except Exception as e:
        db.session.rollback()
        flash('状态更新失败', 'danger')

    return redirect(url_for('dashboard'))


@app.route('/device/delete/<int:device_id>', methods=['POST'])
@login_required
@admin_required
def delete_device(device_id):
    device = Device.query.get_or_404(device_id)

    try:
        # 删除关联的借还记录
        Borrowrecord.query.filter_by(device_id=device.id).delete()
        # 再删除设备
        db.session.delete(device)
        db.session.commit()
        flash(f'设备 [{device.name}] 已删除', 'success')
    except Exception as e:
        db.session.rollback()
        flash('删除失败', 'danger')

    return redirect(url_for('dashboard'))



@app.route('/create-db')
def create_db():
    with app.app_context():
        db.drop_all()
        db.create_all()

        use1 = User(username='1727919865', password_hash='$2b$12$AD6MBraRnTjFyAmy4ypN5.Xz7M7OeURaICnrjWkcqEIdDYoeNZuXe', role='admin')
        db.session.add_all([use1])
        db.session.commit()

    return "Database tables created!"
@app.route('/test')
def test():
    return render_template('test.html')


@app.errorhandler(404)
def handle_404_error(err):
    return render_template('404.html')
if __name__ == '__main__':
    app.run()
