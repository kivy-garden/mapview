import pytest


def test_flower():
    from kivy_garden.flower import FlowerLabel
    label = FlowerLabel()
    assert label.text == 'Demo flower'
