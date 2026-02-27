"""BmzUtils module."""
import os
import sys


if not ("pytest" in sys.modules or "PYTEST_CURRENT_TEST" in os.environ):
    from .image.load_image import BmzLoadImage
    from .utils.bmz_video_settings import BmzVideoSettings
    from .utils.bmz_transfer_colors import BmzTransferColors
    from .utils.bmz_templated_string import BmzJinja2String

    NODE_CLASS_MAPPINGS = {
        "PersistLoadImage": BmzLoadImage,
        "PersistTransferColors": BmzTransferColors,
        "PersistVideoSettings": BmzVideoSettings,
        "BmzJinja2String": BmzJinja2String,
    }

    NODE_DISPLAY_NAME_MAPPINGS = {
        "PersistLoadImage": "[BMZ] LoadImage",
        "PersistTransferColors": "[BMZ] TransferColors",
        "PersistVideoSettings": "[BMZ] VideoSettings",
        "BmzJinja2String": "[BMZ] Jinja2String",
    }

WEB_DIRECTORY = os.path.join(os.path.dirname(__file__), "web")


def web_directory():
    """Indicate the location of web resources."""
    return WEB_DIRECTORY
