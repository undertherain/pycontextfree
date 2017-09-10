import os
from fabric.api import local, lcd


def clean():
    with lcd(os.path.dirname(__file__)):
        local("python3.6 setup.py clean --all")
        local("find . | grep -E \"(__pycache__|\.pyc$)\" | xargs rm -rf")


def make():
    local("python3.6 setup.py bdist_wheel")


def deploy():
    test()
    make()
    local("twine upload dist/*")


def test():
    local("python3.6 -m unittest")
