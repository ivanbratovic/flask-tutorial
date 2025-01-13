import sqlalchemy as sa
from flask_wtf import FlaskForm
from flask_babel import _, lazy_gettext as _l
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Length
from app import db
from app.models import User


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
                raise ValidationError(_("Please use a different username."))


class PostForm(FlaskForm):
    post = TextAreaField(
        _l("What's on your mind?"), validators=[DataRequired(), Length(min=1, max=140)]
    )
    submit = SubmitField(_l("Publish post"))


class EmptyForm(FlaskForm):
    submit = SubmitField("Empty Submit")
