from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    first_name = db.Column(db.String(20), nullable=False)
    surname = db.Column(db.String(20), nullable=False)
    other_name = db.Column(db.String(20), nullable=True)
    reg_no = db.Column(db.String(20), nullable=False, unique=True)
    course_title = db.Column(db.String(20), nullable=False)
    state = db.Column(db.String(20), nullable=False)
    lga = db.Column(db.String(30), nullable=False)
    gender = db.Column(db.String(), nullable=False)
    level = db.Column(db.Integer, nullable=False)
    dob = db.Column(db.Date, nullable=False)
    department = db.Column(db.String(20), nullable=False)
    school = db.Column(db.String(20), nullable=False)
    reason_for_leaving = db.Column(db.String(20), nullable=False)
    password = db.Column(db.Text, nullable=False)
    hod_sign = db.Column(db.Integer, default=False)
    students_affair_sign = db.Column(db.Boolean, default=False)
    academics_sect_sign = db.Column(db.Boolean, default=False)
    accountant_sign = db.Column(db.Boolean, default=False)
    librarian_sign = db.Column(db.Boolean, default=False)
    sports_master_sign = db.Column(db.Boolean, default=False)
    hall_master_sign = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return "Student %r" % (self.first_name+" "+self.surname)


class Staffs(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    first_name = db.Column(db.String(20), nullable=False)
    surname = db.Column(db.String(20), nullable=False)
    other_name = db.Column(db.String(20), nullable=True)
    dob = db.Column(db.Date, nullable=False)
    state = db.Column(db.String(20), nullable=False)
    lga = db.Column(db.String(30), nullable=False)
    gender = db.Column(db.String(), nullable=False)
    staff_no = db.Column(db.String(20), nullable=False, unique=True)
    role = db.Column(db.String(20), nullable=False)
    department = db.Column(db.String(20), nullable=True)
    password = db.Column(db.Text, nullable=False)
    new_requests = db.Column(db.PickleType, default=[])
    accepted_requests = db.Column(db.PickleType, default=[])
    rejected_requests = db.Column(db.PickleType, default=[])

    def __repr__(self):
        return "Staff %r" % (self.first_name+" "+self.surname)


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.Text, nullable=False)
