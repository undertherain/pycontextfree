"""Setup script for contextfree package."""

import setup_boilerplate


class Package(setup_boilerplate.Package):

    """Package metadata."""

    name = 'contextfree'
    description = 'cfdg-inspired cairo-based pythonic generative art framework'
    url = "https://github.com/undertherain/pycontextfree"
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only']
    keywords = ['generative', 'art', 'graphics']


if __name__ == '__main__':
    Package.setup()
