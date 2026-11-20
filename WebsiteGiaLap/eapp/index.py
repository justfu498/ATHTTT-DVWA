import math
from os import abort

from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user

from eapp import app, dao, login


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/discuss')
def discuss_view():
    page = int(request.args.get('page', 1))
    posts = dao.load_posts(kw=request.args.get('search'), page=page)
    page_size = app.config['PAGE_SIZE']
    return render_template('discuss.html', posts=posts, page=page, pages=math.ceil(dao.count_post()/page_size))


@app.route('/login')
def login_view():
    return render_template('login.html')


@app.route('/login', methods=['post'])
def login_process():
    username = request.form.get('username')
    password = request.form.get('password')
    user = dao.authenticate(username, password)
    if user:
        login_user(user=user)
        return render_template('alert.html', msg='Đăng nhập tài khoản thành công!', href='/')
    return render_template('login.html', err_msg='Tên tài khoản hoặc mật khẩu sai')


@app.route('/logout')
def logout_process():
    logout_user()

    return redirect('/')


@app.route('/register')
def register_view():
    return render_template('register.html')


@app.route('/register', methods=['post'])
def register_process():
    name = request.form.get('name')
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm-password')
    if password != confirm_password:
        return render_template('register.html', name=name, username=username, err_msg='Mật khẩu xác nhận không khớp!')

    user = dao.register_user(name, username, password)
    logout_user()
    login_user(user=user)
    return render_template('alert.html', msg='Đăng ký tài khoản thành công!', href='/')


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


@app.route('/discuss/upload')
def upload_view():
    if not current_user.is_authenticated:
        return render_template('login.html')
    return render_template('upload.html')


@app.route('/discuss/upload', methods=['post'])
def upload_process():
    title = request.form.get('title')
    content = request.form.get('content')
    user_id = int(current_user.id)

    if dao.upload_post(title=title, content=content, user_id=user_id):
        return render_template('alert.html', msg='Đăng bài viết thành công!', href='/discuss')
    return render_template('alert.html', msg='Đã có lỗi xảy ra khi thực hiện đăng bài viết!', href='/discuss')


@app.route('/discuss/post')
def post_view():
    post = dao.get_post_by_id(request.args.get('id'))
    return render_template('post.html', post=post)


@app.route('/discuss/post/edit')
def edit_post_view():
    post = dao.get_post_by_id(request.args.get('id'))

    if post.user != current_user:
        return render_template('alert.html', msg='Không có quyền chỉnh sửa bài viết này!', href='/discuss')

    return render_template('edit.html', post=post)


@app.route('/discuss/post/edit', methods=['post'])
def edit_post_process():
    title = request.form.get('title')
    content = request.form.get('content')
    post_id = request.form.get('post_id')
    dao.update_post(title, content, post_id)

    return render_template('alert.html', msg='Cập nhật bài viết thành công!', href='/discuss/post?id=%s' % post_id)


@app.route('/discuss/post/delete')
def delete_post_view():
    post = dao.get_post_by_id(request.args.get('id'))

    if post.user != current_user:
        return render_template('alert.html', msg='Không có quyền xóa bài viết này!', href='/discuss')

    return render_template('delete.html', post=post)


@app.route('/discuss/post/delete', methods=['post'])
def delete_post_process():
    post_id = request.form.get('post_id')
    dao.delete_post(post_id)
    return render_template('alert.html', msg='Xóa bài viết thành công', href='/discuss')


if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)