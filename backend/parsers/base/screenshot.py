import os
from dataclasses import dataclass
from pathlib import Path

import pdfkit
from django.conf import settings
from django.core.files.storage import default_storage
from django.utils import timezone


@dataclass
class Screenshot:
    path: str
    url: str
    name: str


def make_screenshot_from_html(html: str, page_url: str) -> Screenshot:
    html = html.replace("<head>", f"<head><base href=\"{page_url}\">")

    now = timezone.now()
    output_name = Path("screenshots") / now.strftime("%Y-%m-%d") / (now.strftime("%H%M%S%f") + '.pdf')
    output_path = settings.MEDIA_ROOT / output_name
    output_url = default_storage.url(output_name)

    os.makedirs(output_path.parent, mode=0o0770, exist_ok=True)

    pdfkit.from_string(html, output_path)

    return Screenshot(path=output_path, url=output_url, name=output_name)
