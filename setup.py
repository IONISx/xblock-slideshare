"""Setup for slideshare XBlock."""

import os
from setuptools import setup


def package_data(pkg, roots):
    """Generic function to find package_data.

    All of the files under each of the `roots` will be declared as package
    data for package `pkg`.

    """
    data = []
    for root in roots:
        for dirname, _, files in os.walk(os.path.join(pkg, root)):
            for fname in files:
                data.append(os.path.relpath(os.path.join(dirname, fname), pkg))

    return {pkg: data}


setup(
    name='xblock-slideshare',
    version='1.0.0',
    description='Course component (Open edX XBlock) to embed a Slideshare presentation',
    packages=[
        'slideshare',
    ],
    install_requires=[
        'XBlock',
        'xblock-utils',
    ],
    entry_points={
        'xblock.v1': [
            'slideshare = slideshare.slideshare:SlideshareXBlock',
        ]
    },
    package_data=package_data("slideshare", ["static", "public"]),
)
