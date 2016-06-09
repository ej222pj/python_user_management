# -*- coding: utf-8 -*-
import json
import smtplib
import bcrypt
from datetime import datetime, timedelta
from optparse import OptionParser
import config as cfg
from flaskr_init import app, db, jsonify, render_template, flash, redirect, Response, session
from db_models.user import User
from db_models.tenant import Tenant
from forms.user import User
# from forms.new_user import NewUser
from forms.search_user import SearchUser
from forms.login import Login
from forms.edit_general_information import EditGeneralInformation
from forms.edit_tenant import EditTenant
from forms.register import Register

app.config.from_pyfile('config.py')
app_name = 'user_management'
version = 'v1.0'


def redirect_not_logged_in():
    """
    Redirect the page if the tenant is not logged in and is trying to reach a page without permission

    :return: redirect to front page
    """
    flash('You need to login before entering the application')
    return redirect('/')


def check_session():
    """
    Checks if the tenant is logged in by checking the session for username param and loggedin param
    This function is called by all other functions that handle tenant templates

    :return: True or false
    """
    if session.get('loggedIn') is not None:
        if session['loggedIn'] and session.get('username') is not None:
            return True
        else:
            return False
    return False


@app.route('/')
@app.route('/index')
def index():
    """
    Render index template if the user is logged in, if not the user is redirected to the login page

    :return: render template or redirect
    """
    if check_session():
        return render_template('index.html')
    else:
        return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    GET - Renders a login template for the tenant
    POST - Validates the login form and check if the values are right. If they pass the tenant is logged in and redirected
    to the front page again, if not the login template is rendered with an message.

    :return: Redirect or renders template
    """
    #try:
    if not check_session():
        form = Login()
        if form.validate_on_submit():
            current_tenant = Tenant.query.filter_by(username=form.username.data.title()).first()
            if current_tenant.password is not None:
                # Uses stored_hash to check if password is correct.
                if bcrypt.hashpw(form.password.data, current_tenant.password) == current_tenant.password:
                    session['loggedIn'] = True
                    session['username'] = form.username.data.title()
                    flash('Welcome %s' % form.username.data.title())
                    return redirect('/')
                else:
                    flash('Wrong username or password')
            else:
                flash('Wrong username')

        return render_template('login.html', title='Login', form=form)
    else:
        return redirect('/')
    #except:
        #flash('Error Trying to login, please try again.')
        #return redirect('/')


@app.route('/logout', methods=['GET'])
def logout():
    """
    Log outs the tenant. Destroys the session and redirects to the front page again.

    :return: redirect
    """
    session.pop('loggedIn', None)
    session.pop('username', None)
    return redirect('/')


@app.route('/register', methods=['GET', 'POST'])
def registration():
    """
    GET - Renders a registration form.
    POST - Validates the login form and check if the values are right. If they pass the informations is stored in
    the database and the tenant is registered and is redirected to the front page.
    If they fail the registration form is rendered with error messages.

    :return: Redirect or renders template
    """
    try:
        if not check_session():
            form = Register()
            if form.validate_on_submit():
                # Checks if the all ready exists
                current_tenant = Tenant.query.filter_by(username=form.username.data.title()).first()

                if current_tenant is None:
                    # 1 Get password from form
                    password = form.password.data.encode('utf-8')
                    # 2 Hash the password
                    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
                    # 3 Save the Tenant in the db
                    tmp_tenant = Tenant(form.username.data.title(), hashed_password, None,  None, form.company_name.data,
                                        form.address.data, form.phone.data, form.zip_code.data, form.city.data,
                                        form.email.data)

                    db.session.add(tmp_tenant)
                    db.session.commit()

                    flash('Registration done, you can now log in')
                    return redirect('/')
                else:
                    flash('Username already exists')

            return render_template('register.html', title='Register new Tenant', form=form, errors=form.errors)
        else:
            return redirect('/')
    except:
        flash('Error when trying to register, please try again.')
        return redirect('/')


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    """
    GET - Renders a settings form with tenant information
    POST - Validates the settings form and check if the values are right. If they pass the informations is stored in
    the database and the tenant is redirected to the front page.
    If they fail the settings form is rendered with error messages.

    :return: Redirect or renders template
    """
    try:
        if check_session():
            current_tenant = Tenant.query.filter_by(username=session['username']).first()

            if current_tenant is None:
                return "No user have this ID"

            form = EditTenant(obj=current_tenant)
            if form.validate_on_submit():

                hashed_pass = bcrypt.hashpw(form.password.data, current_tenant.password)
                # If old pass match
                if hashed_pass == current_tenant.password:
                    # Saves new pass from form
                    new_pass = form.new_password.data
                    # if the new pass is empty, use the old password
                    if form.new_password.data is '':
                        hashed_new_pass = current_tenant.password
                    else:
                        hashed_new_pass = bcrypt.hashpw(new_pass, bcrypt.gensalt())

                    current_tenant.password = hashed_new_pass
                    current_tenant.image = form.image.data
                    db.session.commit()
                    flash('Gym information changed')
                    return redirect('/')
                else:
                    flash('Wrong password, could not save changes')

            return render_template('settings.html', title='Settings Tab',
                                   form=form,
                                   data=current_tenant.dict(),
                                   error=form.errors)
        else:
            return redirect('/')
    except:
        flash('Error Updating information, please try again.')
        return redirect('/')


@app.route('/general_information', methods=['GET', 'POST'])
def general_information():
    """
    GET - Renders a settings form with general information.
    POST - Validates the settings form and check if the values are right. If they pass the informations is stored in
    the database and the tenant is redirected to the front page.
    If they fail the settings form is rendered with error messages.

    :return: Redirect or renders template
    """
    try:
        if check_session():
            current_tenant = Tenant.query.filter_by(username=session['username']).first()

            if current_tenant is None:
                return "No user have this ID"

            form = EditGeneralInformation(obj=current_tenant)

            if form.validate_on_submit():

                hashed_pass = bcrypt.hashpw(form.password.data, current_tenant.password)
                if hashed_pass == current_tenant.password:
                    current_tenant.company_name = form.company_name.data
                    current_tenant.address = form.address.data
                    current_tenant.phone = form.phone.data
                    current_tenant.zip_code = form.zip_code.data
                    current_tenant.city = form.city.data
                    current_tenant.email = form.email.data
                    db.session.commit()
                    flash('Gym information changed')
                    return redirect('/')
                else:
                    flash('Wrong password, could not save changes')

            return render_template('general_information.html', title='General Information Tab',
                                   form=form,
                                   data=current_tenant.dict(),
                                   error=form.errors)
        else:
            return redirect('/')
    except:
        flash('Error Updating general information, please try again.')
        return redirect('/')


# Renders a HTML page with status_filter on membership
@app.route('/all_users/<status_filter>', methods=['GET', 'POST'])
def all_users(status_filter=None):
    """
    Lists all members based on the status_filter.

    :param status_filter:
    :type status_filter: string
    :return: Redirect or renders template
    """
    try:
        if check_session():
            ret, users = [], []

            # Lists all users
            if status_filter == "all":
                users = User.query.order_by("expiry_date desc").all()
            # List users depending on the membership
            elif status_filter:
                users = User.query.status_filter(User.status == status_filter.title())
            for hit in users:
                js = hit.dict()
                ret.append(js)
            return render_template('all_users.html',
                                   title='All Users',
                                   hits=ret,
                                   filter=status_filter,
                                   count=len(users))
        else:
            return redirect_not_logged_in()
    except:
        flash('Error Showing all users, please try again.')
        return redirect('/')


# Deletes an user from the local DB based on their index
@app.route('/%s/%s/remove_user/<user_id>' % (app_name, version), methods=['POST'])
def remove_user(user_id):
    """
    Deletes a user from the database.

    :param user_id:
    :type user_id: integer
    :return: Redirect
    """
    try:
        if check_session():
            user = User.query.filter_by(id=user_id).first()
            db.session.delete(user)
            db.session.commit()
            return redirect("/all_users/all")
        else:
            return redirect_not_logged_in()
    except:
        flash('Error Removing a user, please try again.')
        return redirect('/')


# Adds an user to the local DB. Gets all the values from a form in the HTML page.
@app.route('/new_user', methods=['GET', 'POST'])
def add_new_user():
    """
    GET - Renders a new user form.
    POST - Validates the user form and check if the values are right. If they pass the informations is stored in
    the database and the user is registrated. The tenant is redirected to the user page.
    If they fail the user form is rendered with error messages.

    :return: Redirect or renders template
    """
    try:
        if check_session():
            form = User()
            if form.validate_on_submit():
                tmp_usr = User(0, form.firstname.data, form.lastname.data, form.email.data, form.phone.data,
                               form.address.data, form.address2.data, form.city.data, form.zip_code.data,
                               form.gender.data, form.ssn.data, form.expiry_date.data, None, form.status.data)
                db.session.add(tmp_usr)
                db.session.commit()
                flash('Created new user: %s %s with id: %s' % (form.firstname.data, form.lastname.data, tmp_usr.id))

                msg = tmp_usr.id

                form = User()
                return render_template('new_user.html',
                                       title='New User',
                                       form=form,
                                       message=msg)
            return render_template('new_user.html',
                                   title='New User',
                                   form=form)
        else:
            return redirect_not_logged_in()
    except:
        flash('Error Creating a new user, please try again.')
        return redirect('/')


# Renders a HTML page with a form to search for a specific user or many users.
@app.route('/search_user', methods=['GET', 'POST'])
def search_user():
    """
    GET - Renders a search user form.
    POST - Takes the value from the form and pass it to the database. Retrieves a list of user/users based on
    the information that was passed.

    :return: Renders template with the search result
    """
    try:
        if check_session():
            form = SearchUser()
            hits = []
            if form.validate_on_submit():
                if form.firstname.data:
                    users = User.query.filter(User.firstname.ilike('%' + form.firstname.data + '%'))
                    hits.extend(users)
                if form.lastname.data:
                    users = User.query.filter(User.firstname.ilike('%' + form.lastname.data + '%'))
                    hits.extend(users)
                if form.email.data:
                    users = User.query.filter(User.email.ilike('%' + form.email.data + '%'))
                    hits.extend(users)
                if form.city.data:
                    users = User.query.filter(User.phone.ilike('%' + form.city.data + '%'))
                    hits.extend(users)
                ret = []
                for hit in hits:
                    js = hit.dict()
                    ret.append(js)
                return render_template('search_user.html',
                                       title='Search User',
                                       form=form,
                                       hits=ret)
            return render_template('search_user.html',
                                   title='Search User',
                                   form=form)
        else:
            return redirect_not_logged_in()
    except:
        flash('Error Searching for a user, please try again.')
        return redirect('/')


# Renders a HTML page with a user and it debts
@app.route('/user_page/<user_index>', methods=['GET', 'POST'])
def user_page(user_index=None):
    """
    Renders a template with user information on a specified user.

    :param user_index:
    :type user_index: integer
    :return: Renders a template
    """
    try:
        if check_session():
            user = User.query.filter_by(id=user_index).first()
            if user is None:
                return "No user Found"
            else:
                return render_template('user_page.html',
                                       title='User Page',
                                       data=user.dict())
        else:
            return redirect_not_logged_in()
    except:
        flash('Error Showing a user page, please try again.')
        return redirect('/')


# Renders a HTML page to edit an user
@app.route('/edit_user/<user_index>', methods=['GET', 'POST'])
def edit_user(user_index=None):
    """
    GET - Renders a edit user form.
    POST - Validates the user form and check if the values are right. If they pass the information is stored in
    the database and the user is updated. The tenant is redirected to the user page.
    If they fail the edit user form is rendered with error messages.

    :param user_index:
    :type user_index: integer
    :return: Renders a template

    :param firstname: Firstname of the user.
    :param lastname: Lastname of the user.
    :param email: Email address of the user.
    :param phone: Phone number of the user.
    :param address: Address 1 of the user.
    :param address2: Address 2 of the user.
    :param city: City of the user.
    :param zip_code: Zip code of the city.
    :param gender: Gender of the user.
    :param ssn: Social Security Number.
    :param expiry_date: Expire date of the users membership.
    :param status: Status of the users membership.
    """
    try:
        if check_session():
            user = User.query.filter_by(id=user_index).first()
            if user is None:
                return "No user have this ID"
            form = User(obj=user)
            if form.validate_on_submit():
                user.firstname = form.firstname.data
                user.lastname = form.lastname.data
                user.email = form.email.data
                user.phone = form.phone.data
                user.address = form.address.data
                user.address2 = form.address2.data
                user.city = form.city.data
                user.zip_code = form.zip_code.data
                user.gender = form.gender.data
                user.ssn = form.ssn.data
                user.expiry_date = form.expiry_date.data
                user.status = form.status.data
                db.session.commit()

                return redirect("/user_page/" + str(user.id))
            if user:
                return render_template('edit_user.html',
                                       title='Edit User',
                                       form=form,
                                       data=user.dict(),
                                       error=form.errors)
            else:
                return "she wrote upon it; no such number, no such zone"

        else:
            return redirect_not_logged_in()
    except:
        flash('Error Editing a user, please try again.')
        return redirect('/')


if __name__ == '__main__':
    parser = OptionParser(usage="usage: %prog [options] arg\n Try this: " + "python flaskr.py", version="%prog 1.0")
    parser.add_option('--debug', dest='debug', default=False, action='store_true',
                      help="Do you want to run this thing with debug output?")
    (options, args) = parser.parse_args()
    # config['database_file'] = options.database
    # config['secret_key'] = options.secret
    db.create_all()
    # if options.debug:
    app.logger.propagate = False
    app.run(host='0.0.0.0', port=app.config["PORT"], debug=True)
