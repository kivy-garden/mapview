"""
Creates a distribution alias that just installs kivy_garden.mapview.
"""
from setuptools import setup

from setup import setup_params

setup_params.update({
    'install_requires': ['kivy_garden.mapview'],
    'name': 'mapview',
})


setup(**setup_params)
