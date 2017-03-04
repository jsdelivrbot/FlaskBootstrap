from flask import Blueprint, render_template
from flask import request, redirect, url_for
from flask import abort
from sqlalchemy import exc
import sqlalchemy
import markdown

from common.login import login_required, current_user
from common.db import Post, db
from common.forms import ConfirmForm
from blog.forms import PostForm
from datetime import datetime


blog = Blueprint('blog', __name__,
                 template_folder='templates')


def load_post(id_):
    try:
        return Post.query.filter_by(id=id_).one()
    except sqlalchemy.orm.exc.NoResultFound:
        return None


@blog.route('/')
def blog_home_page():
    pass


@blog.route('/post/manage')
def post_table():
    posts = Post.query.all()
    return render_template("blog/post_table.html", posts=posts)


@blog.route('/post/new', methods=["GET", "POST"])
@login_required
def new_post():
    # GET = new post form, POST create post
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            form.title.data,
            form.body.data,
            current_user.get_db(),
            datetime.combine(form.publish_date.data, datetime.min.time()))
        db.session.add(post)
        try:
            db.session.commit()
            return redirect(url_for("blog.post_view", post_id=post.id))
        except exc.IntegrityError:
            form.title.errors.append("Title already exists")
    return render_template(
        'form.html',
        form=form,
        btn_label="Create Post",
        path=request.url_rule,
        method="post")


@blog.route('/post/<post_id>')
def post_view(post_id):
    # GET = view post, POST = edit post
    post = load_post(post_id)
    if post is None:
        abort(404, "Post not found")
    post.blog = 
    return render_template("blog/post_single.html", post=post)


@blog.route('/post/<post_id>/edit', methods=["GET", "POST"])
@login_required
def post_edit(post_id):
    # GET = view post, POST = edit post
    post = load_post(post_id)
    if post is None:
        abort(404, "Post not found")
    form = PostForm()
    if form.validate_on_submit():
        post.update(
            form.title.data,
            form.body.data,
            datetime.combine(form.publish_date.data, datetime.min.time()))
        db.session.add(post)
        try:
            db.session.commit()
            return redirect(url_for("blog.post_view", post_id=post.id))
        except exc.IntegrityError:
            form.title.errors.append("Title already exists")
    form.title.data = post.title
    form.body.data = post.body
    form.publish_date.data = post.pub_date
    return render_template(
        'form.html',
        form=form,
        btn_label="Edit Post",
        path=url_for("blog.post_edit", post_id=post.id),
        method="post")


@blog.route('/post/<post_id>/delete', methods=["GET", "POST"])
@login_required
def post_delete(post_id):
    # GET = DELETE CONFIRM FORM, POST = DO DELETE
    post = load_post(post_id)
    if post is None:
        abort(404, "Post not found")
    form = ConfirmForm()

    if form.validate_on_submit():
        try:
            if form.yes.data is True:
                db.session.delete(post)
                db.session.commit()
            return redirect(url_for("blog.home_page"))
        except exc.IntegrityError:
            pass
    return render_template(
        'form.html',
        form=form,
        btn_label="Cancel",
        path=url_for("blog.post_delete", post_id=post.id),
        method="post",
        caption="Are you sure you would like to delete this post?")
