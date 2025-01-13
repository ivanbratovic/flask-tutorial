from urllib.parse import urlsplit
import sqlalchemy as sa
from flask import redirect, render_template, flash, url_for, request
from flask_login import logout_user, current_user, login_user
from flask_babel import _
from app.auth.forms import LoginForm, RegisterForm, ResetPasswordForm, ResetPasswordRequestForm
from app.auth.email import send_password_reset_email
from app.auth import bp
from app.models import User
from app import db


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data)
        )
        if user is None or not user.check_password(form.password.data):
            flash(_("Invalid username or password"))
            return redirect(url_for("auth.login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or urlsplit(next_page).netloc != "":
            next_page = url_for("main.index")
        return redirect(next_page)
    return render_template("login.html", title=_("Sign in"), form=form)


@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.index"))


@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(_("Thank you for registering! You can now login."))
        return redirect(url_for("auth.login"))
    return render_template("register.html", title=_("Register"), form=form)


@bp.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.email == form.email.data))
        if user:
            send_password_reset_email(user)
            flash(
                _("Check your e-mail for instructions on how to reset your password.")
            )
            return redirect(url_for("auth.login"))
    return render_template("forgot_password.html", title=_("Reset password"), form=form)


@bp.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    user = User.verify_password_reset_token(token)
    if not user:
        return redirect(url_for("main.index"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(_("Your password has been reset. You can log in with your new password."))
        return redirect(url_for("auth.login"))
    return render_template("reset_password.html", form=form)
