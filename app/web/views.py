import logging

from flask import Blueprint, redirect, request, url_for, render_template
from flask_login import current_user, login_user, logout_user, login_required

from ..database.models import User


logger = logging.getLogger(__name__)
web = Blueprint('web', __name__, url_prefix='/')


@web.route('')
@login_required
def index():
    return render_template('index.html')


@web.route('/login', methods=['GET', 'POST'])
def login():
    logger.debug(f'Handling Login View Request. Method: {request.method}')

    if User.query.count() == 0:
        if request.method == 'GET':
            logger.debug('No users exist. Returning first-run template.')
            return render_template('first-run.html')
        elif request.method == 'POST':
            if 'username' not in request.json \
                    or 'password' not in request.json:
                logger.debug('Invalid Request.')
                logger.debug(request.json)
                return '', 400
            logger.debug(f'Creating First User {request.json["username"]}...')
            first_user = User.create(request.json['username'],
                                     request.json['password'])
            logger.debug(f'{first_user.username} ({first_user.id}) created!')
            logger.debug('Returning user to login page.')
            return redirect(url_for('web.login'))

    if current_user.is_authenticated and current_user.is_active:
        logger.debug('Current user is already authenticated and active. Redirecting...')
        return redirect(url_for('web.index'))

    if request.method == 'GET':
        logger.debug('User is not logged in. Returning login template.')
        return render_template('login.html')

    if 'username' not in request.json \
            or 'password' not in request.json \
            or 'remember' not in request.json:
        logger.debug('Invalid Request.')
        logger.debug(request.json)
        return 'Invalid Request', 400

    if not User.authenticate(request.json['username'],
                             request.json['password']):
        logger.debug('User authentication failed!')
        return 'Invalid Credentials', 401

    user = User.query.filter(User.username == request.json['username']).first()
    if user is None:
        logger.critical('This should never execute. If so, something has gone severely wrong.')
        return 'Invalid Credentials', 401
    logger.debug(f'Authentication successful for {user.username}.')
    login_user(user, remember=request.json['remember'])
    return redirect(url_for('web.index'))


@web.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('web.login'))
