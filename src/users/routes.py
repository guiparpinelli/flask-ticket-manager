from flask import (
    render_template,
    flash,
    request,
    current_app,
    redirect,
    url_for,
)
from sqlalchemy.exc import IntegrityError
from flask_login import login_user, logout_user, current_user, login_required

from src import db
from . import users_blueprint, schemas, crud, forms


@users_blueprint.route("/register", methods=["GET", "POST"])
def register():
    form = forms.RegistrationForm()

    if request.method == "POST":
        if form.validate_on_submit():
            try:
                new_user = schemas.UserCreate(
                    name=form.name.data,
                    email=form.email.data,
                    password=form.password.data,
                )
                db_user = crud.create_user(new_user)
                flash(f"Thanks for registering, {db_user.name}!")
                current_app.logger.info(
                    f"Registered new user: {form.email.data}!", "success"
                )
                return redirect(url_for("users.login"))
            except IntegrityError as exc:
                db.session.rollback()
                flash(f"ERROR! Email ({form.email.data}) already exists.", "error")
                raise exc

        flash("Error in form data!")
    return render_template("users/register.html", form=form)


@users_blueprint.route("/login", methods=["GET", "POST"])
def login():
    form = forms.LoginForm()

    if request.method == "POST":
        if form.validate_on_submit():
            user = crud.get_user_by_email(form.email.data)
            if user and user.is_password_correct(form.password.data):
                # User's credentials have been validated, so log them in
                login_user(user, remember=form.remember_me.data)
                flash(f"Thanks for logging in, {current_user.email}!")
                current_app.logger.info(f"Logged in user: {current_user.email}")
                # TODO redirect to home page on success
                return redirect(url_for("users.foo"))

        flash("ERROR! Incorrect login credentials.", "error")
    return render_template("users/login.html", form=form)


@users_blueprint.route("/foo")
def foo():
    return "Deu bom"


@users_blueprint.route("/logout")
@login_required
def logout():
    current_app.logger.info(f"Logged out user: {current_user.email}")
    logout_user()
    flash("Goodbye!")
    return redirect(url_for("users.login"))
