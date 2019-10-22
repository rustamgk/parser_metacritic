import typing
import os
import gzip

__all__ = (
    'load_test_asset',
)


def load_test_asset(filename):
    # type: (str) -> typing.Any
    asset = os.path.join(os.path.dirname(__file__), 'assets', filename)
    if asset.endswith('.gz'):
        with gzip.open(asset, 'rb') as fp:
            return fp.read().decode('utf-8')
    else:
        with open(asset, 'r') as fp:
            return fp.read()
