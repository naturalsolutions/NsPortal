import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'marshmallow==3.3.0',
    'marshmallow-sqlalchemy==0.21.0',
    'pyjwt==1.7.1',
    'pyodbc==4.0.27',
    'pyramid==1.10.4',
    'sqlalchemy==1.3.12',
    'transaction==3.0.0',
    'waitress==1.4.3',
    'webargs==6.0.0b3'
    ]

setup(
    name='ns_portal',
    version='0.4',
    description='ns_portal',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author='',
    author_email='',
    url='',
    keywords='web wsgi bfg pylons pyramid',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    test_suite='ns_portal',
    install_requires=requires,
    entry_points="""\
    [paste.app_factory]
    main = ns_portal:main
    [console_scripts]
    initialize_ns_portal_db = ns_portal.scripts.initializedb:main
    """
    )
