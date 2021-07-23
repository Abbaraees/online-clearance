from flask_wtf import FlaskForm
from wtforms import (
    StringField, SelectField, IntegerField, DateField, RadioField,
    SubmitField, PasswordField, SelectField
)
from wtforms.validators import Length, DataRequired, EqualTo


class StudentRegisterForm(FlaskForm):
    first_name = StringField('First Name',  validators=[Length(min=3, max=20)])
    surname = StringField('Surname',  validators=[Length(min=3, max=20)])
    other_name = StringField('Other Name',  validators=[Length(min=3, max=20)])
    reg_no = StringField('Registration Number',  validators=[Length(min=3, max=20)])
    course_title = StringField('Course Title',  validators=[Length(min=3, max=20)])
    state = StringField('State',  validators=[Length(min=3, max=20)])
    lga = StringField('LGA',  validators=[Length(min=3, max=20)])
    gender = SelectField('Gender', choices=[('male', 'Male'), ('female', 'Female')], default='male')
    level = IntegerField('Level')
    dob = DateField('Date Of Birth')
    department = StringField('Department',  validators=[Length(min=3, max=20)])
    school = StringField('School',  validators=[Length(min=3, max=20)])
    reason_for_leaving = StringField('Reason For Leaving',  validators=[Length(min=20, max=50)])
    password = PasswordField('Password',  validators=[Length(min=8, max=20)])
    register = SubmitField('Register')


class StaffRegisterForm(FlaskForm):
    first_name = StringField('First Name',  validators=[Length(min=3, max=20)])
    surname = StringField('Surname',  validators=[Length(min=3, max=20)])
    other_name = StringField('Other Name',  validators=[Length(min=3, max=20)])
    staff_no = StringField('Staff Number',  validators=[Length(min=3, max=20)])
    state = StringField('State',  validators=[Length(min=3, max=20)])
    lga = StringField('LGA',  validators=[Length(min=3, max=20)])
    gender = SelectField('Gender', choices=[('male', 'Male'), ('female', 'female')])
    dob = DateField('Date Of Birth')
    role = SelectField('Role',  choices=[
                        ('HOD', 'H.O.D'), ('Academic Sect', 'Academic Sect'), ('Students Affairs', 'Students Affairs'),
                        ('Accounter', 'Accounter'), ('Sports Master', 'Sports Master'), ('Library', 'Library'),
                        ('Hall Master', 'Hall Master')
                        ]
                    )
    department = StringField('Department',  validators=[Length(min=3, max=20)])
    password = PasswordField('Password',  validators=[Length(min=8, max=20)])
    register = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[Length(min=3, max=20), DataRequired()])
    password = PasswordField('Password', validators=[Length(min=8, max=20), DataRequired()])
    action = RadioField(label="Role", choices=[('staff', 'staff'), ('student', 'student')], default='student')
    login = SubmitField('Login')

class AdminRegistrationForm(FlaskForm):
    username = StringField("Username", validators=[Length(min=3, max=20), DataRequired()])
    password = PasswordField('Password', validators=[Length(min=8, max=20), DataRequired()])
    repeat_password = PasswordField('Repeat Password', validators=[Length(min=8, max=20), DataRequired(), EqualTo(password)])
    register = SubmitField('Register')   
