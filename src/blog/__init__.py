from flask import Blueprint, render_template, abort
from flask import redirect, request
from common.login import login_required 
from blog.forms import PostForm


blog = Blueprint('blog', __name__,
                 template_folder='templates')


@blog.route('/')
def blog_home_page():
    pass


@blog.route('/post')
def list_posts():
    pass


@blog.route('/post/new', methods=["GET", "POST"])
@login_required
def new_post():
    # GET = new post form, POST create post
    form = PostForm()
    if form.validate_on_submit():
        pass
    return render_template(
        'form.html',
        form=form,
        btn_label="Login",
        path=request.url_rule,
        method="post")


@blog.route('/post/<post_id>')
def post_view():
    # GET = view post, POST = edit post
    pass


@blog.route('/post/<post_id>/edit', methods=["GET", "POST"])
@login_required
def post_edit():
    # GET = view post, POST = edit post
    pass


@blog.route('/post/<post_id>/delete', methods=["GET", "POST"])
@login_required
def post_delete():
    # GET = DELETE CONFIRM FORM, POST = DO DELETE
    pass
