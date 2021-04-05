from flask import Flask, render_template, redirect, request
from flask import make_response, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import abort

from website import create_app, create_session
from website.models.jobs import Job, Category
from website.models.users import User
from website.models.departments import Department
from website.forms.add_job import AddJobForm
from website.forms.add_depart import AddDepartForm
from website.forms.login import LoginForm
from website.forms.register import RegisterForm

app = create_app()


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = create_session()
        user = db_sess.query(User).filter(
            User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Wrong login or password", form=form)
    return render_template('login.html', title='Authorization', form=form)


@app.route("/")
@app.route("/index")
def index():
    db_sess = create_session()
    jobs = db_sess.query(Job).all()
    users = db_sess.query(User).all()
    names = {name.id: (name.surname, name.name) for name in users}
    return render_template("index.html", jobs=jobs, names=names, title='Work log')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Register', form=form,
                                   message="Passwords don't match")
        db_sess = create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Register', form=form,
                                   message="This user already exists")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            age=form.age.data,
            position=form.position.data,
            email=form.email.data,
            speciality=form.speciality.data,
            address=form.address.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/add-job', methods=['GET', 'POST'])
def add_job():
    add_form = AddJobForm()
    if add_form.validate_on_submit():
        db_sess = create_session()
        jobs = Job(
            job=add_form.job.data,
            team_leader=add_form.team_leader.data,
            work_size=add_form.work_size.data,
            collaborators=add_form.collaborators.data,
            is_finished=add_form.is_finished.data
        )
        db_sess.add(jobs)
        db_sess.commit()
        return redirect('/')
    return render_template('add_job.html', form=add_form)


@app.route('/jobs/<int:id>', methods=['GET', 'POST'])
@login_required
def job_edit(id):
    form = AddJobForm()
    if request.method == "GET":
        db_sess = create_session()
        jobs = db_sess.query(Job).filter(Job.id == id,
                                          (Job.team_leader == current_user.id) | (current_user.id == 1)).first()
        if jobs:
            form.job.data = jobs.job
            form.team_leader.data = jobs.team_leader
            form.work_size.data = jobs.work_size
            form.collaborators.data = jobs.collaborators
            form.is_finished.data = jobs.is_finished
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = create_session()
        jobs = db_sess.query(Job).filter(Job.id == id,
                                          (Job.team_leader == current_user.id) | (current_user.id == 1)).first()
        if jobs:
            jobs.job = form.job.data
            jobs.team_leader = form.team_leader.data
            jobs.work_size = form.work_size.data
            jobs.collaborators = form.collaborators.data
            jobs.is_finished = form.is_finished.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('add_job.html', title='Job Edit', form=form)


@app.route('/job_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def job_delete(id):
    db_sess = create_session()
    jobs = db_sess.query(Job).filter(Job.id == id,
                                      (Job.team_leader == current_user.id) | (current_user.id == 1)).first()
    if jobs:
        db_sess.delete(jobs)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/add_depart', methods=['GET', 'POST'])
def add_depart():
    add_form = AddDepartForm()
    if add_form.validate_on_submit():
        db_sess = create_session()
        depart = Department(
            title=add_form.title.data,
            chief=add_form.chief.data,
            members=add_form.members.data,
            email=add_form.email.data
        )
        db_sess.add(depart)
        db_sess.commit()
        return redirect('/')
    return render_template('add_depart.html', title='Adding a Department', form=add_form)


@app.route("/departments")
def depart():
    db_sess = create_session()
    departments = db_sess.query(Department).all()
    users = db_sess.query(User).all()
    names = {name.id: (name.surname, name.name) for name in users}
    return render_template("departments.html", departments=departments, names=names, title='List of Departments')


@app.route('/departments/<int:id>', methods=['GET', 'POST'])
@login_required
def depart_edit(id):
    form = AddDepartForm()
    if request.method == "GET":
        db_sess = create_session()
        depart = db_sess.query(Department).filter(Department.id == id,
                                                  (Department.chief == current_user.id) | (
                                                      current_user.id == 1)).first()
        if depart:
            form.title.data = depart.title
            form.chief.data = depart.chief
            form.members.data = depart.members
            form.email.data = depart.email
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = create_session()
        depart = db_sess.query(Department).filter(Department.id == id,
                                                  (Department.chief == current_user.id) | (
                                                      current_user.id == 1)).first()
        if depart:
            depart.title = form.title.data
            depart.chief = form.chief.data
            depart.members = form.members.data
            depart.email = form.email.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('add_depart.html', title='Department Edit', form=form)


@app.route('/depart_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def depart_delete(id):
    db_sess = create_session()
    depart = db_sess.query(Department).filter(Department.id == id,
                                              (Department.chief == current_user.id) | (
                                                  current_user.id == 1)).first()
    if depart:
        db_sess.delete(depart)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


if __name__ == '__main__':
    # session = create_session()
    app.run(debug=True)

