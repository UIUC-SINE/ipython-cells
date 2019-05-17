from setuptools import setup
from ipython_cells import version

setup(
    name='ipython_cells',
    version=version.__version__,
    packages=['ipython_cells'],
    author="Evan Widloski, Ulaş Kamacι",
    author_email="evan@evanw.org, ukamaci2@illinois.edu",
    description="Jupyter-like cell running in ipython",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license="GPLv3",
    keywords="jupyter ipython cells magic extension",
    url="https://github.com/uiuc-sine/ipython-cells",
    install_requires=[
        "IPython"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
    ]
)
