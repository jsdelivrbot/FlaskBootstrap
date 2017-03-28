from flask import render_template


def render_form_page(page, **args):
    """Render a form on a page with a header and footer"""
    return (render_template("theme/header.html") +
            render_template(page, **args) +
            render_template("theme/footer.html"))
