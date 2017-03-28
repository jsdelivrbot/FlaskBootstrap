from flask import Blueprint, send_file, abort
from common.db import Image


images = Blueprint('images', __name__,
                   template_folder='templates')


def load_image(id_):
    return Image.query.filter_by(id=id_).one_or_none()


@images.route('/<image_id>')
def view(image_id):
    image = load_image(image_id)
    if image is None:
        abort(404, "image not found")
    return send_file(image.path)
