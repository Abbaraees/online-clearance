import functools
from datetime import date

from flask import (
    Blueprint, render_template, url_for, redirect, g, request,
    flash, session
)
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash

from online_clearance import db
from online_clearance.models import Admin, Staffs, Students
from online_clearance.forms import AdminRegistrationForm, LoginForm, StaffRegisterForm, StudentRegisterForm


bp = Blueprint('admin', __name__, url_prefix='/admin')

def login_required(view):
        @functools.wraps(view)
        def wrapped_view(**kwargs):
            if g.user is None:
                return redirect(url_for('admin.login'))
            elif not isinstance(g.user, Admin):
                return abort(401)

            return view(**kwargs)
            
        return wrapped_view


@bp.route('/')
@login_required
def index():
    return render_template('admin/index.html')


@bp.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        error = None
        user = Admin.query.filter_by(username=username).first()
        if not username:
            error = 'Username is required'
        elif not password:
            error = 'password is required'
        else:
            if user is None:
                error = "User is not registered"
            elif not check_password_hash(user.password, password):
                error = "Invalid Password"
            else:
                session.clear()
                session['role'] = 'admin'
                session['user_no'] = user.id
                session['user_home'] = 'admin.index'
                return redirect(url_for('admin.index'))
                
        flash(error, 'danger')

    return render_template('login.html', form=LoginForm(), admin=True)


@bp.route('/register', methods=['POST', 'GET'])
@login_required
def register():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        error = None

        if not username:
            error = 'Username is required'
        elif not password:
            error = 'password is required'
        elif Admin.query.filter_by(username=username).first():
            error = 'Username Already Exists'
        else:
            user = Admin(username=username, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()

            return redirect(url_for('admin.login'))

        flash(error, 'danger')

    return render_template('admin/register.html', form=AdminRegistrationForm())


@bp.route('/staffs')
@login_required
def staffs():
    all_staffs = Staffs.query.paginate(per_page=10)
    return render_template('admin/staffs_list.html', staffs=all_staffs)


@bp.route('/new_staff', methods=['GET', 'POST'])
@login_required
def new_staff():
    if request.method == 'POST':
        first_name = request.form.get('first_name', '')
        surname = request.form.get('surname', '')
        other_name = request.form.get('other_name', '')
        dob = request.form.get('dob', '')
        state = request.form.get('state', '')
        lga = request.form.get('lga', '')
        gender = request.form.get('gender', '')
        staff_no = request.form.get('staff_no', '')
        role = request.form.get('role', '')
        department = request.form.get('department', '')
        password = request.form.get('password', '')

        user = Staffs.query.filter_by(staff_no=staff_no).first()

        if user:
            error = "User Already Exists"
        else:
            new = Staffs(first_name=first_name, surname=surname, other_name=other_name,
                dob = date.fromisoformat(dob), state=state, lga=lga, gender=gender, staff_no=staff_no, role=role,
                password = generate_password_hash(password), department=department
            )

            db.session.add(new)
            db.session.commit()
            flash("Staff Added Successfully", 'success')
            
            return redirect(url_for('admin.staffs'))

        flash(error)

    return render_template('admin/register_staff.html', form=StaffRegisterForm())


@bp.route('/staff_info/<int:id>', methods=['GET', 'POST'])
@login_required
def staff_info(id):
    staff = Staffs.query.filter_by(id=id).first_or_404()
    return render_template('admin/staff_info.html', staff=staff)


@bp.route('/update_staff_info/<int:id>', methods=['GET', 'POST'])
@login_required
def update_staff_info(id):
    staff = Staffs.query.filter_by(id=id).first_or_404()
    if request.method == 'POST':
        first_name = request.form.get('first_name', '')
        surname = request.form.get('surname', '')
        other_name = request.form.get('other_name', '')
        dob = request.form.get('dob', '')
        state = request.form.get('state', '')
        lga = request.form.get('lga', '')
        gender = request.form.get('gender', '')
        staff_no = request.form.get('staff_no', '')
        role = request.form.get('role', '')
        department = request.form.get('department', '')
        password = request.form.get('password', '')

        staff.first_name = first_name
        staff.surname = surname
        staff.other_name = other_name
        staff.dob = date.fromisoformat(dob)
        staff.state = state
        staff.lga = lga
        staff.gender = gender
        staff.staff_no = staff_no
        staff.department = department
        staff.role = role

        if not password:
            pass
        else:
            staff.password = generate_password_hash(password)

        db.session.commit()
        flash("Profile Updated Successfully", 'success')
        return redirect(url_for('admin.staffs'))    

    return render_template('admin/register_staff.html', staff=staff, form=StaffRegisterForm(), title="Update Staff Info")


@bp.route('/delete_staff/<int:id>', methods=['POST', 'GET'])
def delete_staff(id):
    staff = Staffs.query.filter_by(id=id).first_or_404()

    if request.method == 'POST':
        db.session.delete(staff)
        db.session.commit()
        flash("Staff Successfully Deleted", 'success')

        return redirect(url_for('admin.staffs'))

    return render_template('admin/delete_user.html', user_home='admin.staffs')


@bp.route('/students')
@login_required
def students():
    all_students = Students.query.paginate(per_page=10)
    return render_template('admin/students_list.html', students=all_students)


@bp.route('/new_student', methods=['GET', 'POST'])
@login_required
def new_student():
    if request.method == 'POST':
        first_name = request.form.get('first_name', '')
        surname = request.form.get('surname', '')
        other_name = request.form.get('other_name', '')
        dob = request.form.get('dob', '')
        state = request.form.get('state', '')
        lga = request.form.get('lga', '')
        gender = request.form.get('gender', '')
        reg_no = request.form.get('reg_no', '')
        department = request.form.get('department', '')
        level = request.form.get('level', '')
        course_title = request.form.get('course_title', '')
        school = request.form.get('school', '')
        reason_for_leaving = request.form.get('reason_for_leaving', '')
        password = request.form.get('password', '')

        user = Students.query.filter_by(reg_no=reg_no).first()

        if user:
            error = "User Already Exists"
        else:
            new = Students(first_name=first_name, surname=surname, other_name=other_name,
                dob = date.fromisoformat(dob), state=state, lga=lga, gender=gender, reg_no=reg_no,
                password = generate_password_hash(password), department=department, level=level,
                reason_for_leaving=reason_for_leaving, school=school, course_title=course_title
            )

            for staff in Staffs.query.all():
            	if staff.role != 'HOD':
                	staff.new_requests = staff.new_requests+[new.reg_no]
            hod = Staffs.query.filter_by(role='HOD', department=new.department).first()
            hod.new_requests = hod.new_requests+[new.reg_no]
            
            print(hod.first_name, hod.surname)

                
            db.session.add(new)
            db.session.commit()
            flash("Student Added Successfully", 'success')

            return redirect(url_for('admin.students'))

        flash(error, 'danger')

    return render_template('admin/register_student.html', form=StudentRegisterForm(), title="Register New Student")


@bp.route('/update_student_info/<int:id>', methods=['GET', 'POST'])
@login_required
def update_student_info(id):
    student = Students.query.filter_by(id=id).first_or_404()
    form = StudentRegisterForm()
    if request.method == 'POST':
        first_name =form.first_name.data
        surname =form.surname.data
        other_name =form.other_name.data
        dob =form.dob.data
        state =form.state.data
        lga =form.lga.data
        gender =form.gender.data
        reg_no =form.reg_no.data
        level =form.level.data
        department =form.department.data
        course_title =form.course_title.data
        school =form.school.data
        reason_for_leaving =form.reason_for_leaving.data
        password =form.password.data

        student.first_name = first_name
        student.surname = surname
        student.other_name = other_name
        student.dob = date.fromisoformat(str(dob))
        student.state = state
        student.lga = lga
        student.gender = gender
        student.reg_no = reg_no
        student.department = department
        student.level = level
        student.course_title = course_title
        student.school = school
        student.reason_for_leaving = reason_for_leaving

        if not password:
            pass
        else:
            student.password = generate_password_hash(password)

        db.session.commit()
        flash("Profile Updated Successfully", 'success')
        return redirect(url_for('admin.students'))    

    return render_template('admin/register_student.html', student=student, form=form, title="Update Student Info")


@bp.route('/delete_student/<int:id>', methods=['POST', 'GET'])
def delete_student(id):
    student = Students.query.filter_by(id=id).first_or_404()

    if request.method == 'POST':
        db.session.delete(student)
        db.session.commit()
        flash("Student Successfully Deleted", 'success')

        return redirect(url_for('admin.students'))

    return render_template('admin/delete_user.html', user_home='admin.students')