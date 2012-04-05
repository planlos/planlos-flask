# coding: utf-8
from flask import Blueprint, g, render_template, redirect, url_for, abort
from flask import current_app as app
from flask import flash, request, session
from flaskext.mail import Message
from planlos.forms import Login_Form, Signup_Form
from planlos.documents import Profile, User
from planlos.extensions import mail, db
from flaskext.login import current_user, login_user, logout_user, login_required
from planlos.account_tools import request_user_account


accounts = Blueprint('accounts', __name__)

@accounts.route('/')
def index():
    user = current_user
    return render_template('accounts/index.html', user=user)


@accounts.route('/profile/<username>', methods=['GET'])
@login_required
def profile(username):
    user = User.get_by_name(username)
    userprofile = user.profile
    return render_template('accounts/profile.html',
                           user=user,
                           profile=profile)


@accounts.route('/login', methods=['POST', 'GET'])
def login():
    form = Login_Form(username=request.args.get("username", None),
                     next=request.args.get("next", None))
    if form.validate_on_submit():
        user, authenticated = User.authenticate(form.username.data,
                                                form.password.data)
        if user and authenticated:
            login_user(user)
            flash("Logged in successfully.")
            return redirect( url_for('accounts.profile',
                                     username=user.username))
        flash("Sorry, wrong credentials")
    return render_template('accounts/login.html', form=form)


@accounts.route('/logout', methods=['GET'])
@login_required
def logout():
    logged_out_username = current_user.username
    logout_user()
    return render_template('accounts/logout.html', username=logged_out_username)


@accounts.route('/signup', methods = ['GET', 'POST'] )
def signup():
    if not current_user.is_anonymous():
        return abort(403)
    form = Signup_Form(username=request.args.get("username", None),
                       email=request.args.get("email", None),
                       next=request.args.get("next", None))
    if form.validate_on_submit():
        # add user (not activated)
        request_user_account(form.username.data,
                             form.password.data,
                             form.email.data)
        flash("Thanks for signing up! An Activation mail has been sent to you (%s) please come back..." % (form.email.data) )
        return redirect( url_for('base.index') )
    return render_template('accounts/signup.html', form=form)


@accounts.route('/<username>/activation/<code>/')
def activation(username, code):
    user = db.User.find_one_or_404({'username': username})
    if user:
        if user.activate_by_code(code):
            return render_template('accounts/activation.html', username=user.username)
    # raise 404
    return render_template('accounts/activation_fail.html')


@accounts.route('/<username>/pwreset', methods=['POST'])
@login_required
def pw_reset(username):
    if current_user.username == username or current_user.has_role('admin'):
        current_user.reset_password()
        flash("Passort was reset")
        next=request.args.get("next", None)
        return redirect(next)
    else:
        abort(403)
