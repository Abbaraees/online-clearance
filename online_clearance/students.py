import functools

from flask import (
    Blueprint, request, redirect, url_for,
    flash, render_template, session, g
)
from online_clearance import db
from online_clearance.models import Students


bp = Blueprint('students', __name__, url_prefix='/students')

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
    return render_template('students/index.html')


@bp.route('/status')
@login_required
def status():
    student = g.user
    if all([student.hod_sign, student.academics_sect_sign, student.students_affair_sign,
            student.accountant_sign, student.librarian_sign, student.sports_master_sign,
            student.hall_master_sign]):
        return render_template('students/clearance_complete.html', student=student)
    return render_template('students/clearance_pending.html', student=student)


@bp.route('/cancel', methods=['POST', 'GET'])
@login_required
def cancel():
    if request.method == 'POST':
        user = g.user
        db.session.delete(user)
        db.session.commit()
        
        return redirect(url_for('inde'))

    return render_template('students/confirm_cancel.html')
