import sqlalchemy as sa
from flask_wtf import FlaskForm
from flask_babel import lazy_gettext as _l
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app import db
from app.models import User


class LoginForm(FlaskForm):
    username = StringField(_l("Username"), validators=[DataRequired()])
    password = PasswordField(_l("Password"), validators=[DataRequired()])
    remember_me = BooleanField(_l("Remember me"))
    submit = SubmitField(_l("Sign in"))


class RegisterForm(FlaskForm):
    username = StringField(_l("Username"), validators=[DataRequired()])
    email = StringField(_l("E-mail"), validators=[DataRequired(), Email()])
    password = PasswordField(_l("Password"), validators=[DataRequired(), Length(min=8)])
    password_repeat = PasswordField(
        _l("Repeat Password"), validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField(_l("Register"))

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(User.username == username.data))
        if user is not None:
            raise ValidationError(_l("Please use a different username."))

    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(User.email == email.data))
        if user is not None:
            raise ValidationError(_l("Please use a different e-mail address."))


class EditProfileForm(FlaskForm):
    username = StringField(_l("Username"), validators=[DataRequired()])
    about_me = TextAreaField(_l("About me"), validators=[Length(max=140)])
    submit = SubmitField(_l("Update profile"))

    def __init__(self, original_username, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = db.session.scalar(
                sa.select(User).where(User.username == username.data)
            )
            if user is not None:
                raise ValidationError(_l("Please use a different username."))


class PostForm(FlaskForm):
    post = TextAreaField(
        _l("What's on your mind?"), validators=[DataRequired(), Length(min=1, max=140)]
    )
    submit = SubmitField(_l("Publish post"))


class EmptyForm(FlaskForm):
    submit = SubmitField(_l("Submit"))


class ResetPasswordRequestForm(FlaskForm):
    email = StringField(_l("E-mail"), validators=[DataRequired(), Email()])
    submit = SubmitField(_l("Request password reset"))


class ResetPasswordForm(FlaskForm):
    password = PasswordField(_l("Password"), validators=[DataRequired(), Length(min=8)])
    password_repeat = PasswordField(
        _l("Repeat Password"), validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField(_l("Reset password"))
