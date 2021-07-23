import os
import functools

from flask import (
    Flask, render_template, request,
    redirect, url_for, flash, g, session
)
from werkzeug.security import check_password_hash

from online_clearance.models import db
from online_clearance import students, staffs, admin
from online_clearance.forms import LoginForm
from online_clearance.models import Students, Staffs, Admin

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        {
            # 'SQLALCHEMY_DATABASE_URI': 'mysql://admin:ybuc12345@127.0.0.1:3306/ybuc_clearance',
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///'+os.path.join(app.instance_path, 'data.db'),
            'SECRET_KEY': 'dev',
            'SQLALCHEMY_TRACK_MODIFICATIONS': False
        }
    )

    db.init_app(app)
    if test_config:
        app.config.from_mapping(test_config)
    else:
        app.config.from_pyfile('config.py', silent=True)

    try:
        os.makedirs(app.instance_path)
    except:
        pass

    
    @app.route('/hello')
    def hello():
        return "Hello World"


    @app.route('/')
    def index():
        return render_template('index.html')


    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
        # if request.method == 'POST':
            if request.form['action'] == 'student':
                username = request.form.get('username', '')
                password = request.form.get('password', '')
                user = Students.query.filter(Students.reg_no == username).first()

                if not user:
                    error = "Incorrect Username"
                    flash(error, 'danger')
                elif not check_password_hash(user.password, password):
                    error = "Incorrect Password"
                    flash(error, 'danger')
                else:
                    session.clear()
                    session['user_no'] = user.reg_no
                    session['role'] = 'student'
                    session['user_home'] = 'students.index'
                    return redirect(url_for('students.index'))
            else:
                username = request.form.get('username', '')
                password = request.form.get('password', '')
                user = Staffs.query.filter(Staffs.staff_no==username).first()

                if not user:
                    error = "Incorrect Username"
                    flash(error, 'danger')
                elif not check_password_hash(user.password, password):
                    error = "Incorrect Password"
                    flash(error, 'danger')
                else:
                    session.clear()
                    session['user_no'] = user.staff_no
                    session['role'] = 'staff'
                    session['user_home'] = 'staffs.index'
                    return redirect(url_for('staffs.index'))
        
        return render_template('login.html', form=form)


    @app.route('/logout', methods=['GET'])
    def logout():
        session.clear()
        return redirect(url_for('index'))

    @app.before_request
    def load_logged_in_user():
        user_no = session.get('user_no')
        if user_no is not None:
            g.user_home = session.get('user_home')
            if session.get('role') == 'student':
                user = Students.query.filter_by(reg_no=user_no).first()
                g.user = user
            elif session.get('role') == 'staff':
                user = Staffs.query.filter_by(staff_no=user_no).first()
                g.user = user
            else:
                user = Admin.query.filter_by(id=user_no).first()
                g.user = user
        else:
            g.user = None

    app.register_blueprint(students.bp)
    app.register_blueprint(staffs.bp)
    app.register_blueprint(admin.bp)


    return app
