from flask import Blueprint, render_template
from flask import redirect, url_for
from flask import abort
from sqlalchemy import exc
import sqlalchemy
import markdown2

from common.login import login_required, current_user
from common.db import Project, ProjectImages, db
from common.forms import ConfirmForm
from common.images import save_image, update_image, delete_image
from common.helpers import render_form_page
from portfolio.forms import ProjectForm, ProjectImageForm
from datetime import datetime
import admin


portfolio = Blueprint('portfolio', __name__,
                      template_folder='templates')


def load_project(id_):
    try:
        return Project.query.filter_by(id=id_).one()
    except sqlalchemy.orm.exc.NoResultFound:
        return None


def load_project_images(project_id):
    return ProjectImages.query.filter_by(project_id=project_id).all()


def load_project_image(project_image_id):
    return ProjectImages.query.filter_by(id=project_image_id).one_or_none()


def admin_page():
    projects = Project.query.all()
    return render_template("portfolio/project_table.html",
                           projects=projects)


admin.managed.append(admin_page)


@portfolio.route('/projects')
def portfolio_home_page():
    projects = Project.query\
        .filter(Project.pub_date <= datetime.utcnow())\
        .order_by(Project.id.desc())\
        .limit(20)\
        .all()
    p = []
    for project in projects:
        project.description = markdown2.markdown(
            project.description, extras=['fenced-code-blocks'])
        p.append(project)
    return render_template("portfolio/feed.html",
                           projects=p)


@portfolio.route('/manage')
@login_required
def project_table():
    projects = Project.query.all()
    return render_form_page("portfolio/project_table.html",
                            projects=projects)


@portfolio.route('/project/new', methods=["GET", "POST"])
@login_required
def project_new():
    # GET = new project form, POST create project
    form = ProjectForm()
    if form.validate_on_submit():
        image = save_image(form.thumbnail.data, form.title.data)
        project = Project(
            form.title.data,
            form.excerpt.data,
            form.description.data,
            current_user.get_db(),
            image,
            datetime.combine(form.publish_date.data, datetime.min.time()))
        db.session.add(image)
        db.session.add(project)
        db.session.commit()
        return redirect(url_for("portfolio.project_view",
                        project_id=project.id))

    return render_template(
        'form.html',
        form=form,
        btn_label="Create Post",
        path=url_for('portfolio.project_new'),
        method="post",
        with_file=True)


@portfolio.route('/project/<project_id>')
def project_view(project_id):
    # GET = view project
    project = load_project(project_id)
    if project is None:
        abort(404, "Project not found")
    project.description = markdown2.markdown(
        project.description, extras=['fenced-code-blocks'])
    return render_template("portfolio/project_single.html", project=project)


@portfolio.route('/project/<project_id>/edit', methods=["GET", "POST"])
@login_required
def project_edit(project_id):
    # GET = view project, POST = edit project
    project = load_project(project_id)
    if project is None:
        abort(404, "Post not found")
    form = ProjectForm()
    if form.validate_on_submit():
        image = None
        image_old = None
        if form.thumbnail.data is not None:
            image_old, image = update_image(
                project.thumbnail_id, form.thumbnail.data, form.title.data)
            db.session.add(image)
            db.session.delete(image_old)
        project.update(
            form.title.data,
            form.excerpt.data,
            form.description.data,
            datetime.combine(form.publish_date.data, datetime.min.time()),
            thumbnail=image)
        db.session.add(project)
        db.session.commit()
        return redirect(url_for("portfolio.project_view",
                        project_id=project.id))

    form.title.data = project.title
    form.excerpt.data = project.excerpt
    form.description.data = project.description
    form.publish_date.data = project.pub_date
    return render_template(
        'form.html',
        form=form,
        btn_label="Edit Post",
        path=url_for("portfolio.project_edit", project_id=project.id),
        method="post",
        with_file=True)


@portfolio.route('/project/<project_id>/delete', methods=["GET", "POST"])
@login_required
def project_delete(project_id):
    # GET = DELETE CONFIRM FORM, POST = DO DELETE
    project = load_project(project_id)
    if project is None:
        abort(404, "Post not found")
    form = ConfirmForm()

    if form.validate_on_submit():
        try:
            if form.yes.data is True:
                delete_image(project.thumbnail)
                for image in project.images:
                    delete_image(image.image)
                    project.images.remove(image)
                db.session.delete(project.thumbnail)
                db.session.delete(project)
                db.session.commit()
            return redirect(url_for("portfolio.portfolio_home_page"))
        except exc.IntegrityError:
            pass
    return render_template(
        'form.html',
        form=form,
        btn_label="Cancel",
        path=url_for("portfolio.project_delete", project_id=project.id),
        method="post",
        caption="Are you sure you would like to delete this project?")


# Project image endpoints here
@portfolio.route('/image/<project_id>', methods=["GET", "POST"])
@login_required
def project_image_edit(project_id):
    # GET = view project, POST = edit project
    project = load_project(project_id)
    if project is None:
        abort(404, "Post not found")
    form = ProjectImageForm()
    if form.validate_on_submit():
        image = save_image(form.image.data, form.caption.data)
        db.session.add(image)
        pi = ProjectImages(project, image)
        db.session.add(pi)
        db.session.commit()
    return render_template(
        'portfolio/image_list.html',
        form=form,
        btn_label="Add image to project",
        path=url_for("portfolio.project_image_edit", project_id=project.id),
        method="post",
        with_file=True,
        images=project.images)


@portfolio.route('/image/<project_image_id>/delete', methods=["GET", "POST"])
@login_required
def project_image_delete(project_image_id):
    # GET = DELETE CONFIRM FORM, POST = DO DELETE
    project_image = load_project_image(project_image_id)
    project_id = project_image.project_id
    if project_image is None:
        abort(404, "Post not found")
    form = ConfirmForm()
    if form.validate_on_submit():
        try:
            if form.yes.data is True:
                delete_image(project_image.image)
                db.session.delete(project_image.image)
                db.session.delete(project_image)
                db.session.commit()
            return redirect(url_for("portfolio.project_image_edit",
                                    project_id=project_id))
        except exc.IntegrityError:
            pass
    return render_template(
        'form.html',
        form=form,
        btn_label="Cancel",
        path=url_for("portfolio.project_image_delete",
                     project_image_id=project_image.id),
        method="post",
        caption="Are you sure you would like to delete this image?")
