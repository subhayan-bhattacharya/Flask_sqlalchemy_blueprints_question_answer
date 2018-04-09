from werkzeug.security import generate_password_hash, check_password_hash
from flask import session,render_template,url_for,redirect,Blueprint,flash
from project.users.forms import RegisterForm,LoginForm
from project.models.users_model import Users
from flask import current_app

users_blueprint = Blueprint(
    'users',
    __name__,
    template_folder='templates/users'
)

@users_blueprint.route('/users')
def users():
    current_app.logger.debug('Inside /users route of users views')
    user_details = Users.get_current_user()
    if user_details:
        if user_details.admin:
            users = Users.get_all_nonadmin_users()
            return render_template('users.html',user=user_details,users=users)
        else:
            current_app.logger.debug('Redirecting to index route of questions blueprint')
            return redirect(url_for('questions.index'))
    else:
        current_app.logger.debug('Redirecting to login route of users blueprint')
        return redirect(url_for('users.login'))

@users_blueprint.route('/promote/<user_id>')
def promote(user_id):
    current_app.logger.debug('Inside promote route of users blueprint')
    user_details = Users.get_current_user()
    if user_details:
        if user_details.admin:
            user_details = Users.get_by_id(user_id)
            if user_details.expert:
                user_details.expert = False
            else:
                user_details.expert = True
            user_details.save_to_db()
            current_app.logger.debug('Redirecting to users route of users blueprint')
            return redirect(url_for('users.users'))
        else:
            current_app.logger.debug('Redirecting to index route of questions blueprint')
            return redirect(url_for('questions.index'))
    else:
        return redirect(url_for('login'))

@users_blueprint.route('/register',methods=["GET","POST"])
def register():
    current_app.logger.debug('Inside register route of users blueprint')
    user_details = Users.get_current_user()
    error_message = None
    registerform = RegisterForm()
    if registerform.validate_on_submit():
        username = registerform.username.data
        password = registerform.password.data
        existing_user = Users.get_by_name(name=username)
        if not existing_user:
            hashed_password = generate_password_hash(password,method='sha256')
            new_user = Users(name=username,password=hashed_password,expert=False,admin=False)
            new_user.save_to_db()
            session['username'] = username
            if username == 'admin':
                admin_user = Users.get_by_name(name='admin')
                admin_user.admin = True
                admin_user.save_to_db()
            current_app.logger.debug('Redirecting to index route of questions blueprint')
            return redirect(url_for('questions.index'))
        else:
            current_app.logger.error('User already exists')
            error_message = "User already exists!"

    return render_template('register.html',user=user_details,error=error_message,form=registerform)

@users_blueprint.route('/login',methods=["GET","POST"])
def login():
    current_app.logger.debug('Inside login route of users blueprint')
    user_details = Users.get_current_user()
    user_error_message = None
    pass_error_message = None
    loginform = LoginForm()

    if loginform.validate_on_submit():
        username = loginform.username.data
        password = loginform.password.data
        hashed_password = generate_password_hash(password,method='sha256')
        user_result = Users.get_by_name(name=username)
        if user_result:
            returned_password = user_result.password
            if check_password_hash(returned_password,password):
                session['username'] = user_result.name
                return redirect(url_for('questions.index'))
            else:
                current_app.logger.error('passwords are not matching')
                pass_error_message = "Passwords don't match"
        else:
            current_app.logger.error('User does not exist')
            user_error_message = "User does not exist!"

    return render_template('login.html',user=user_details,user_error=user_error_message,pass_error=pass_error_message,form=loginform)

@users_blueprint.route('/logout')
def logout():
    current_app.logger.debug('Logging out')
    session.pop('username',None)
    return redirect(url_for('questions.index'))