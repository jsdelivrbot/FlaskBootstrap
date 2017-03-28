from werkzeug.utils import secure_filename
import imghdr
import hashlib
import os
import time
from common.db import Image


def save_image(f, caption):
    # we don't care what the file name is just hash it
    ext = imghdr.what(f)
    md5 = hashlib.md5()
    md5.update(secure_filename(f.filename).encode("utf-8"))
    filename = str(time.time()) +\
        md5.hexdigest() + "." + ext
    path = os.path.join(
        "/data", 'static', 'user', filename
    )
    f.save(path)
    image = Image(caption, path)
    return image


def load_image(id_):
    return Image.query.filter_by(id=id_).one_or_none()


def update_image(id_, f, caption):
    image = load_image(id_)
    os.unlink(image.path)
    image_new = save_image(f, caption)
    return image, image_new


def delete_image(image):
    os.unlink(image.path)
