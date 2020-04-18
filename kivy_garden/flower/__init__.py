"""
Demo flower
============

Defines the Kivy garden :class:`FlowerLabel` class which is the widget provided
by the demo flower.
"""

from kivy.uix.label import Label

__all__ = ('FlowerLabel', )

from ._version import __version__


class FlowerLabel(Label):
    """A :class:`~kivy.uix.label.Label` based class that shows
    The text `"Demo flower"`.
    """

    def __init__(self, **kwargs):
        super(FlowerLabel, self).__init__(**kwargs, text='Demo flower')
