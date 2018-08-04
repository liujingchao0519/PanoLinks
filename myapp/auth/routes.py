from flask import render_template, redirect, url_for, flash, request
from myapp import db
from myapp.auth import bp
from flask_login import current_user, login_user, login_required, logout_user
from myapp.models import User
from myapp.auth.forms import LoginForm, RegistrationForm
from werkzeug.urls import url_parse






@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)

    return render_template('auth/login.html', title = 'Sign In', form=form)


#fix the third party login sometime in the future

#
# @myapp.route('/FBlogin')
# def FBogin():
#     if current_user.is_authenticated:
#         return redirect(url_for('index'))
#     callback=url_for(
#         'facebook_authorized',
#         next = request.args.get('next') or request.referrer or None,
#         _external=True
#
#     )
#     return facebook.authorize(callback=callback)
#
#
# @myapp.route('/FBlogin/authorized')
# def facebook_authorized():
#     resp = facebook.authorized_respons()
#     if resp is None:
#         return 'Access denied: reason=%s error=%s' % (
#             request.args['error_reason'],
#             request.args['error_description']
#         )
#     if isinstance(resp, OAuthException):
#         return 'Access denied: %s' % resp.message
#
#     session['fb_token'] = (resp['access_token'], '')
#     me = facebook.get('/me')
#     return 'Logged in as id=%s name=%s redirect=%s' % \
#            (me.data['id'], me.data['name'], request.args.get('next'))
#
# @facebook.tokengetter
# def get_facebook_oauth_token():
#     return session.get('fb_token')




@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', title = 'Register', form=form)






@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))



