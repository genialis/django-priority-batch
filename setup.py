import os.path
import setuptools

# Get long description from README.
with open('README.rst', 'r') as fh:
    long_description = fh.read()

# Get package metadata from '__about__.py' file.
about = {}
base_dir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(base_dir, 'django_priority_batch', '__about__.py'), 'r') as fh:
    exec(fh.read(), about)

setuptools.setup(
    name=about['__title__'],
    use_scm_version=True,
    description=about['__summary__'],
    long_description=long_description,
    long_description_content_type='text/x-rst',
    author=about['__author__'],
    author_email=about['__email__'],
    url=about['__url__'],
    license=about['__license__'],
    packages=setuptools.find_packages(),
    python_requires='>=3.6, <3.8',
    install_requires=['Django~=1.11.6'],
    extras_require={
        'docs': ['Sphinx', 'sphinx_rtd_theme'],
        'package': ['twine', 'wheel'],
        'test': [
            'black',
            'pydocstyle',
            'check-manifest',
            'readme_renderer',
            'setuptools_scm',
            'pytest',
            'pytest-django',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='django transaction batching prioritization',
)
