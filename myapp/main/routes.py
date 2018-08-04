
from flask import render_template, request, current_app, url_for
from flask_login import login_required
from myapp.models import User, Application


from myapp.main import bp

@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html', title='Home')


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)

    apps = Application.query.filter_by(applicant=user).paginate(page, current_app.config['APPS_PER_PAGE'], False)
    next_url = url_for('main.applications', page=apps.next_num) \
        if apps.has_next else None
    prev_url = url_for('main.applications', page=apps.prev_num) \
        if apps.has_prev else None
    return render_template('user.html', user=user, entries=apps.items, next_url=next_url, prev_url=prev_url)

    return render_template('user.html', user=user)


@bp.route('/applications')
@login_required
def applications():
    page = request.args.get('page', 1, type=int)

    apps = Application.query.paginate(page, current_app.config['APPS_PER_PAGE'], False)
    next_url = url_for('main.applications', page=apps.next_num) \
        if apps.has_next else None
    prev_url = url_for('main.applications', page=apps.prev_num) \
        if apps.has_prev else None
    return render_template('applications.html', entries=apps.items, next_url=next_url, prev_url=prev_url)