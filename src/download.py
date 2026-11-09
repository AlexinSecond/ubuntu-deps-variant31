"""Download and decompress an Ubuntu Packages index using the stdlib."""

import gzip
import io
import lzma
from urllib.parse import urlsplit, urlunsplit
from urllib.request import Request, urlopen

TIMEOUT = 30
MAX_DOWNLOAD = 64 * 1024 * 1024
MAX_TEXT = 256 * 1024 * 1024


def index_url(url):
    """A repository directory means its Packages.xz index."""
    parts = urlsplit(url)
    path = parts.path
    if path.endswith("/"):
        path += "Packages.xz"
    return urlunsplit(parts._replace(path=path))


def decode_index(data, path):
    """Decode supported gzip, xz, or plain UTF-8 metadata."""
    if path.endswith(".gz"):
        with gzip.GzipFile(fileobj=io.BytesIO(data)) as stream:
            data = stream.read(MAX_TEXT + 1)
    elif path.endswith(".xz"):
        with lzma.LZMAFile(io.BytesIO(data)) as stream:
            data = stream.read(MAX_TEXT + 1)
    if len(data) > MAX_TEXT:
        raise ValueError("Packages index exceeds the text size limit")
    return data.decode("utf-8-sig")


def download_index(url):
    """Fetch data with a timeout, size limit and TLS verification."""
    url = index_url(url)
    request = Request(url, headers={"User-Agent": "Variant31-Study/1.0"})
    with urlopen(request, timeout=TIMEOUT) as response:
        data = response.read(MAX_DOWNLOAD + 1)
    if len(data) > MAX_DOWNLOAD:
        raise ValueError("Download exceeds the size limit")
    return decode_index(data, urlsplit(url).path)
