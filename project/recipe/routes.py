import binascii
import os
import subprocess
import filecmp
import secrets
from PIL import Image
import io
from flask import render_template, url_for, flash, redirect, request, send_file
from project import application, db, bcrypt, mail, admin
from project.form import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from project.models.user import UserModel,userView
from project.models.code_base import CodeBase,codeBaseView
from project.models.prob import Prob, probView
from project.models.test_cases import Testcases, testCaseView
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from flask_admin.contrib.fileadmin import FileAdmin

class custom_FileAdmin(FileAdmin):
    can_download = True

code_path = os.path.join(os.getcwd(), 'project/temp_codefolder')
admin.add_view(custom_FileAdmin(code_path, '/project/', name='Code Dir'))
# admin.add_view(FileAdmin(code_path, '/project/static/profile_pics', name='Profile Pics'))
admin.add_view(probView(Prob, db.session))
admin.add_view(codeBaseView(CodeBase, db.session))
admin.add_view(userView(UserModel, db.session))
admin.add_view(testCaseView(Testcases, db.session))


@application.before_first_request
def create_tables():
    db.create_all()


@application.route('/')
@application.route('/home')
def home():
    if current_user.is_authenticated:
        problem_list = Prob.query.all()
        return render_template('home.html', data=problem_list)
    return render_template('home.html')


@application.route('/problems/<problem_id>', methods=['GET', 'POST'])
def problems(problem_id):
    # if request.method=='GET':
    if current_user.is_authenticated:
        p = Prob.get_from_id(problem_id)
        # return p.title
        # test_cases = Testcases.get_from_project_id(problem_id)
        return render_template('problem.html', problem=p)  # , test_cases=test_cases)
    return render_template(url_for(login))


@application.route('/testing', methods=['GET', 'POST'])
def test():
    t = Testcases(1, 2, 1, 1)
    t.save_to_db()
    return 'save'


@application.route('/problems/<problem_id>/upload', methods=['POST'])
def problem_upload(problem_id):
    if current_user.is_authenticated:
        if 'code1' in request.files:
            data_file = request.files['code1']
            filename = str(current_user.id) + '.cpp'
            # filename = 'custom' + '.cpp'

            # print(os.getcwd())
            upload_code = CodeBase(data_file.read(), problem_id, current_user.id)
            upload_code.save_to_db()
            file1 = CodeBase.get_by_id(upload_code.id)
            dir_path = os.path.join(os.getcwd(), 'project/temp_codefolder/')
            with open(dir_path + filename, 'wb') as f:
                f.write(file1.code_file)
            # file1.code_file.save(os.path.join(dir_path, filename))
            p = Prob.get_from_id(problem_id)
            # test_cases = Testcases.get_from_project_id(problem_id)
            return redirect(url_for('upload', filename=filename, problemid=p.id), code=307)
            # return render_template('problem.html', problem=p, test_cases=test_cases)
        # p = Prob.get_from_id(problem_id)
        # return p.title
        # return render_template('problem.html', problem=p)
        #     return 'upload code for ' + problem_id
    # return render_template(url_for(home))


@application.route('/delete/testcase/<testcase_id>', methods=['GET'])
def deletetestcases(testcase_id):
    if current_user.is_authenticated and current_user.role == 2:
        Testcases.query.filter_by(id=testcase_id).delete()
        db.session.commit()
        flash(f'Test Case deleted successfully', 'success')
        return redirect(url_for('addingtestcases'))
    return redirect(url_for('home'))


@application.route('/showtestcases', methods=['POST'])
def showtestcases():
    if request.method == 'POST':
        try:
            prob_id = request.form['prob_id']
        except:
            flash(f'No Test Case detected', 'danger')
            return redirect(url_for('addingtestcases'))
        testcases = Testcases.query.filter_by(problem_id=prob_id)
        return render_template('showtestcases.html', testcases=testcases)


@application.route('/addingtestcases', methods=['GET', 'POST'])
def addingtestcases():
    if request.method == 'GET':
        problems = Prob.query.all()
        return render_template('addingtestcases.html', problems=problems)
    if request.method == 'POST':
        prob_id = request.form['prob_id']
        input_file = request.form['Input']
        input_file = str(input_file).replace('\r', '')
        output_file = request.form['Output']
        output_file = str(output_file).replace('\r', '')
        timeout = request.form['Timeout']

        testcase = Testcases(input1=input_file, output=output_file, problem_id=prob_id, timeout=timeout)
        testcase.save_to_db()
        input_filename = 'problem' + str(prob_id) + 'test' + str(testcase.id) + '.txt'
        output_filename = 'refoutput' + input_filename
        dir_path = os.path.join(os.getcwd(), 'project/test_io/')

        with open(dir_path + input_filename, 'wb') as f:
            f.write(bytes(input_file.encode('utf-8')))
        with open(dir_path + output_filename, 'wt') as f:
            f.write(output_file)
        prob = Prob.get_from_id(prob_id)
        prob.test_case_number += 1
        db.session.commit()
        flash(f'New Test Case added with Id:  {testcase.id} for Problem: {prob.title}', 'success')
        return redirect(url_for('addingtestcases'))


@application.route('/deleting', methods=['POST'])
def deleting():
    if current_user.is_authenticated and current_user.role == 2:
        try:
            prob_id = request.form['problem_delete']
        except:
            flash(f'No more Problem detected', 'danger')
            return redirect(url_for('adding'))
        problem = Prob.query.filter_by(id=prob_id).delete()
        testcase = Testcases.query.filter_by(problem_id=prob_id).delete()
        # db.session.delete(testcase)
        # db.session.delete(problem)
        db.session.commit()
        flash(f'Problem deleted successfully', 'success')
        return redirect(url_for('adding'))
    return redirect(url_for('home'))


@application.route('/adding', methods=['GET', 'POST'])
def adding():
    if current_user.is_authenticated and current_user.role == 2:
        if request.method == 'GET':
            list_of_problems = Prob.query.all()
            return render_template('adding.html', problems=list_of_problems)
        else:
            title = request.form['title']
            difficulty = request.form['difficulty']
            content = request.form['Content']
            Input = request.form['Input']
            Output = request.form['Output']
            Constraint = request.form['Constraint']
            Explanation = request.form['Explanation']
            # test_case1 = request.form['Test_case1']
            p = Prob(title=title, difficulty=difficulty, content=content, input1=Input,
                     output1=Output, constraint=Constraint, explanation=Explanation)
            p.save_to_db()
            flash(f'New Problem added with Title:  {title}', 'success')
            # return str(title + difficulty + content)
            return redirect(url_for('adding'))
    else:
        return redirect(url_for('login'))


@application.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = UserModel.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful, Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@application.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = UserModel(username=form.username.data, password=hashed_password, email=form.email.data)
        user.save_to_db()
        flash(f'account created for {form.username.data}', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@application.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(application.root_path, 'static/profile_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


@application.route('/account', methods=['POST', 'GET'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('your account has been updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static',
                         filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


@application.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = UserModel.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@application.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = UserModel.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)


def compile_code(name: str, tc: str):
    # display_str = "Compiled Successfully "
    cmd1 = ['g++', 'project/temp_codefolder/' + name, '-o', 'project/temp_codefolder/' + name + '.out']
    compiler_out = subprocess.Popen(cmd1, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    o, e = compiler_out.communicate()
    if compiler_out.returncode == 0:
        # b,e = run_code(name,tc)
        # try:
        #     # print()
        #
        #     cmd2 = 'timeout 5s ' + './project/temp_codefolder/' + name + '.out' + ' <project/test_io/input' + tc + '.txt >project/test_io/output' + tc + '.txt'
        #     # print(cmd2)
        #     status_code = subprocess.Popen(cmd2, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        #
        #     o1, e1 = status_code.communicate()
        #     if status_code.returncode == 124:
        #         display_str = "Time Limit exceeds"
        #         return False, "Compiled Successfully ", display_str
        #     return True, "Compiled Successfully ", ''
        # except Exception as e:
        # return b, "Compiled Successfully ", str(e)
        return True, "Compiled Successfully ", ''
    else:
        compiler_error = e.decode('utf-8')
        return False, "Compiled Unsuccessfull ", compiler_error


def run_code(name: str, tc: str):
    try:
        cmd2 = 'timeout 5s ' + './project/temp_codefolder/' + name + '.out' + ' <project/test_io/' + tc + '.txt >project/test_io/' + str(
            current_user.id) + 'output' + tc + '.txt'
        print(cmd2)
        status_code = subprocess.Popen(cmd2, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

        o1, e1 = status_code.communicate()
        if status_code.returncode == 124:
            display_str = "Time Limit exceeds"
            return False, display_str
        return True, ''
    except Exception as e:
        return False, str(e)


@application.route('/successful_upload', methods=['POST', 'GET'])
def successful_upload():
    code_filename = 'temp' + str(current_user.id) + '.cpp'
    input_filename = 'inputtemp' + str(current_user.id)
    output_filename = str(current_user.id) + 'output' + input_filename
    r, compiler_output, compiler_message = compile_code(code_filename, input_filename)
    prog_output = ""
    if r is True:
        out, compiler_message = run_code(code_filename, input_filename)
        if out is True:
            dir_path = os.path.join(os.getcwd(), 'project/test_io/')
            with open(dir_path + output_filename + '.txt', 'rt') as f:
                prog_output = f.read()
            # try:
            #     a = filecmp.cmp('test_output/ref_out1.txt', 'code_output/output1.txt')
            # except Exception as e:
            #     print("error: ", e)
    return render_template('result.html', compiler_output=compiler_output, prog_output=prog_output,
                           compiler_message=compiler_message)


@application.route('/codingide', methods=['POST', 'GET'])
@login_required
def codingIde():
    if request.method == 'POST':
        code_file = request.form['code_editor']
        input_file = request.form['input']
        dir_path = os.path.join(os.getcwd(), 'project/temp_codefolder/')
        dir_path_io = os.path.join(os.getcwd(), 'project/test_io/')
        code_filename = 'temp' + str(current_user.id) + '.cpp'
        input_filename = 'inputtemp' + str(current_user.id) + '.txt'
        # print(binascii.hexlify(bytes(input_file.encode())))
        input_file = str(input_file).replace('\r','')
        # print(binascii.hexlify(bytes(input_file.encode())))

        with open(dir_path + code_filename, 'wt') as f:
            f.write(code_file)
        with open(dir_path_io + input_filename, 'wt') as f2:
            f2.write(input_file)
            # f2.write(bytes(input_file.encode()))
        # with open(dir_path_io + input_filename, 'rb') as f3:
        #     temp = f3.read()
            # print(binascii.hexlify(temp))
        return redirect(url_for('successful_upload'), code=307)
    else:
        return render_template('codingide.html')


@application.route('/upload/<filename>/<problemid>', methods=['POST', 'GET'])
def upload(filename: str, problemid):
    if request.method == 'POST':
        test_cases = Testcases.get_from_project_id(problemid)
        t = []

        bool_result, compiler_output, compiler_message = compile_code(filename, '')
        # compiler_output = 'not compiled'
        print(bool_result)
        if bool_result:
            for test in test_cases:
                print(test.id)
                testcase = 'problem' + str(problemid) + 'test' + str(test.id)
                a = False
                run_bool, compiler_message = run_code(filename, testcase)
                # t.append((test.id, bool_result, compiler_message))
                if run_bool is True:
                    try:
                        dir_path = "project/test_io/"
                        ref_out = ''
                        user_out = ''
                        ref_in = ''

                        input_filename = 'problem' + str(problemid) + 'test' + str(test.id) + '.txt'
                        output_filename = 'output' + 'problem' + str(problemid) + 'test' + str(test.id) + '.txt'
                        with open(dir_path + "ref" + output_filename, 'rt') as f:
                            ref_out = f.read()
                        with open(dir_path + str(current_user.id) + output_filename, 'rb') as f2:
                            user_out = f2.read()
                        with open(dir_path + input_filename, 'rt') as f3:
                            ref_in = f3.read()
                        a = filecmp.cmp('project/test_io/ref' + output_filename,
                                        'project/test_io/' + str(current_user.id) + output_filename)
                    except Exception as e:
                        # print("error: ", e)
                        compiler_message += str(e)
                t.append((test.id, a, compiler_message,ref_in,ref_out,user_out))
            return render_template('result.html', compiler_message=compiler_message,compiler_output=compiler_output, a=a, test_cases=t)
        else:
            flash(f'Compiled Unsuccessful:', 'danger')
            return render_template('result.html', compiler_message=compiler_message)
    else:
        return render_template('codingide.html')
