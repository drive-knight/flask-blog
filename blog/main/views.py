from blog.models import db, User, Post

from flask import render_template, flash, redirect, request, session, g,  url_for, abort, Blueprint
from flask_login import current_user, login_required

from .forms import PostForm

main = Blueprint('main', __name__)


@main.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)


@main.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Ваш пост успешно создан', 'success')
        return redirect(url_for('main.home'))
    return render_template('create.html', title='Новый пост',
                           form=form)


@main.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@main.route('/<int:post_id>/update', methods=('GET', 'POST'))
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.body.data
        db.session.commit()
        flash('Ваш пост успешно обновлен!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.body.data = post.content
    return render_template('create.html', title='Обновление поста',
                           form=form)


@main.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Ваш пост успешно удален!', 'success')
    return redirect(url_for('main.home'))


@main.route("/user/<string:email>")
def get_posts(email):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(email=email).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .paginate(page=page, per_page=5)
    return render_template('get_posts.html', posts=posts, user=user)