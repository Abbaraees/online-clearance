import functools

from flask import Blueprint, render_template, session, g, url_for, redirect, request

from online_clearance import db
from online_clearance.models import Staffs, Students


bp = Blueprint('staffs', __name__, url_prefix='/staffs')


def login_required(view):
        @functools.wraps(view)
        def wrapped_view(**kwargs):
            if g.user is None:
                return redirect(url_for('login'))

            return view(**kwargs)
            
        return wrapped_view


@bp.route('/')
@login_required
def index():
    return render_template('staffs/index.html')


@bp.route('/new_requests')
@login_required
def new_requests():
    user = g.user
    new_r = [x for x in Students.query.all() if x.reg_no in user.new_requests]

    return render_template('staffs/new_requets.html', new_requests=new_r)

@bp.route('/accepted_requests')
@login_required
def accepted_requests():
    user = g.user
    new_r = [x for x in Students.query.all() if x.id in user.accepted_requests]

    return render_template('staffs/accepted_requests.html', accepted_requests=new_r)


@bp.route('/rejected_requests')
@login_required
def rejected_requests():
    user = g.user
    new_r = [x for x in Students.query.all() if x.id in user.rejected_requests]

    return render_template('staffs/rejected_requests.html', rejected_requests=new_r)


@bp.route('/student_info/<int:id>')
def student_info(id):
    action = request.args.get("action")
    student = Students.query.filter_by(id=id).first_or_404()

    return render_template('staffs/student_info.html', student=student, action=action)


@bp.route('accept/<int:id>')
def accept(id):
    student = Students.query.filter_by(id=id).first_or_404()
    user = g.user
    if user.role == 'HOD':
        student.hod_sign = 1
    elif user.role == 'Academic Sect':
        student.academics_sect_sign = 1
    elif user.role == 'Students Affairs':
        student.students_affair_sign = 1
    elif user.role == 'Hall Master':
        student.hall_master_sign = 1
    elif user.role == 'Library':
        student.librarian_sign = 1
    elif user.role == 'Accounter':
        student.accountant_sign = 1
    elif user.role == 'Sports Master':
        student.sports_master_sign = 1

    user.new_requests = [x for x in user.new_requests if student.reg_no != student.reg_no]
    user.accepted_requests = user.accepted_requests+[student.id]
    db.session.commit()

    return redirect(url_for('staffs.new_requests'))


@bp.route('ignore/<int:id>')
def ignore(id):
    student = Students.query.filter_by(id=id).first_or_404()

    g.user.new_requests = [x for x in g.user.new_requests if student.reg_no != student.reg_no]
    g.user.rejected_requests = g.user.rejected_requests+[student.id]
    db.session.commit()

    return redirect(url_for('staffs.new_requests'))
