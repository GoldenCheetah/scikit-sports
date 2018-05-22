#! /usr/bin/env python
"""A set of python modules for cyclist using powermeters."""

import io
import re
import os
import sys
import subprocess
import codecs

from setuptools import find_packages

PACKAGE_NAME = 'sksports'
DISTNAME = 'scikit-sports'
DESCRIPTION = 'A set of python modules for cyclist using powermeters.'
with codecs.open('README.rst', encoding='utf-8-sig') as f:
    LONG_DESCRIPTION = f.read()
MAINTAINER = 'G. Lemaitre'
MAINTAINER_EMAIL = 'g.lemaitre58@gmail.com'
URL = 'https://github.com/scikit-sports/scikit-sports'
LICENSE = 'MIT'
DOWNLOAD_URL = 'https://github.com/scikit-sports/scikit-sports'
INSTALL_REQUIRES = ['numpy', 'scipy', 'pandas', 'scikit-learn', 'six',
                    'joblib', 'fitparse', 'cython']
CLASSIFIERS = ['Intended Audience :: Science/Research',
               'Intended Audience :: Developers',
               'License :: OSI Approved',
               'Programming Language :: Python',
               'Topic :: Software Development',
               'Topic :: Scientific/Engineering',
               'Operating System :: Microsoft :: Windows',
               'Operating System :: POSIX',
               'Operating System :: Unix',
               'Operating System :: MacOS',
               'Programming Language :: Python :: 2.7',
               'Programming Language :: Python :: 3.5',
               'Programming Language :: Python :: 3.6']
PACKAGE_DATA = {'sksports': ['datasets/data/*.fit',
                              'datasets/data/*.csv',
                              'datasets/corrupted_data/*.fit',
                              'metrics/tests/data/rider_power_profile.csv']}
EXTRAS_REQUIRE = {
    'tests': [
        'pytest',
        'pytest-cov'],
    'docs': [
        'sphinx',
        'sphinx-gallery',
        'sphinx_rtd_theme',
        'numpydoc',
        'matplotlib',
    ]
}


def version(package, encoding='utf-8'):
    """Obtain the packge version from a python file e.g. pkg/_version.py
    See <https://packaging.python.org/en/latest/single_source_version.html>.
    """
    path = os.path.join(os.path.dirname(__file__), package, '_version.py')
    with io.open(path, encoding=encoding) as fp:
        version_info = fp.read()
    version_match = re.search(r"""^__version__ = ['"]([^'"]*)['"]""",
                              version_info, re.M)
    if not version_match:
        raise RuntimeError("Unable to find version string.")
    return version_match.group(1)


def generate_cython(package):
    """Cythonize all sources in the package"""
    cwd = os.path.abspath(os.path.dirname(__file__))
    print("Cythonizing sources")
    p = subprocess.call([sys.executable,
                         os.path.join(cwd, 'tools', 'cythonize.py'),
                         package],
                        cwd=cwd)
    if p != 0:
        raise RuntimeError("Running cythonize failed!")


def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration
    config = Configuration(None, parent_package, top_path)
    config.set_options(ignore_setup_xxx_py=True,
                       assume_default_configuration=True,
                       delegate_options_to_subpackages=True,
                       quiet=True)

    config.add_subpackage(PACKAGE_NAME)

    return config


def setup_package():
    from numpy.distutils.core import setup

    old_path = os.getcwd()
    local_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    src_path = local_path

    os.chdir(local_path)
    sys.path.insert(0, local_path)

    # Run build
    old_path = os.getcwd()
    os.chdir(src_path)
    sys.path.insert(0, src_path)

    cwd = os.path.abspath(os.path.dirname(__file__))
    if not os.path.exists(os.path.join(cwd, 'PKG-INFO')):
        # Generate Cython sources, unless building from source release
        generate_cython(PACKAGE_NAME)

    try:
        setup(name=DISTNAME,
              author=MAINTAINER,
              author_email=MAINTAINER_EMAIL,
              maintainer=MAINTAINER,
              maintainer_email=MAINTAINER_EMAIL,
              description=DESCRIPTION,
              license=LICENSE,
              url=URL,
              version=version(PACKAGE_NAME),
              download_url=DOWNLOAD_URL,
              long_description=LONG_DESCRIPTION,
              zip_safe=False,  # the package can run out of an .egg file
              classifiers=CLASSIFIERS,
              packages=find_packages(),
              package_data=PACKAGE_DATA,
              install_requires=INSTALL_REQUIRES,
              extras_require=EXTRAS_REQUIRE,
              configuration=configuration)
    finally:
        del sys.path[0]
        os.chdir(old_path)

    return


if __name__ == '__main__':
    setup_package()
