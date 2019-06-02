from django.shortcuts import render, redirect
from . import models
from . import forms
import hashlib
import pymssql


def hash_code(s, salt='mysite'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


def index(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    conn = pymssql.connect('localhost\sa', 'sa', '123456', 'django')
    cursor = conn.cursor(as_dict=True)
    # sql = 'SELECT*FROM GY_FYJY'
    # df = pd.read_sql(sql, conn)
    # conn.close()

    cursor.execute('SELECT*FROM GY_FYJY')
    rows = cursor.fetchone()
    # df = DataFrame(rows)

    # l = list()
    # for j in rows:
    #     for k in j:
    #         i = str(k.quantize(Decimal('0.0')))
    #         l.append(i)
    return render(request, 'login/index.html', {'rows': rows})


def login(request):
    if request.session.get('is_login', None):
        return redirect('/index/')
    if request.method == "POST":
        login_form = forms.UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            try:
                user = models.User.objects.get(name=username)
            except:
                message = '用户不存在！'
                return render(request, 'login/login.html', locals())

            if user.password == hash_code(password):
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                return redirect('/index/')
            else:
                message = '密码不正确！'
                return render(request, 'login/login.html', locals())
        else:
            return render(request, 'login/login.html', locals())
    login_form = forms.UserForm()
    return render(request, 'login/login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        return redirect('/index/')

    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        message = "请检查填写的内容!"
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')
            sex = register_form.cleaned_data.get('sex')

            if password1 != password2:
                message = '请检查填写内容！'
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:
                    message = '用户已经存在！'
                    return render(request, 'login/register.html', locals())
                same_mail_user = models.User.objects.filter(email=email)
                if same_mail_user:
                    message = '该邮箱已经被注册！'
                    return render(request, 'login/register.html', locals())

                new_user = models.User()
                new_user.name = username
                new_user.password = hash_code(password1)
                new_user.email = email
                new_user.sex = sex
                new_user.save()

                return redirect('/login/')
        else:
            return render(request, 'login/register.html', locals())
    register_form = forms.RegisterForm()
    return render(request, 'login/register.html')


def logout(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    request.session.flush()
    return redirect('/login/')



