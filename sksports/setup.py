PACKAGE_NAME = 'sksports'


def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration

    config = Configuration(PACKAGE_NAME, parent_package, top_path)

    config.add_subpackage('__check_build')

    # pure python packages
    config.add_subpackage('datasets')
    config.add_subpackage('datasets/tests')
    config.add_subpackage('io')
    config.add_subpackage('io/tests')
    config.add_subpackage('metrics')
    config.add_subpackage('metrics/tests')
    config.add_subpackage('utils')
    config.add_subpackage('utils/tests')

    # packages that have their own setup.py -> cython files
    config.add_subpackage('extraction')

    return config


if __name__ == '__main__':
    from numpy.distutils.core import setup
    setup(**configuration(top_path='').todict())
