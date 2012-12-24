from distutils.core import setup

setup(
    name='dudebot',
    version='0.0.1',
    author='Sujay Mansingh',
    author_email='sujay.mansingh@gmail.com',
    packages=['dudebot'],
    scripts=[],
    url='https://github.com/sujaymansingh/dudebot',
    license='LICENSE.txt',
    description='Useful cricket-related stuff.',
    long_description=open('README.md').read(),
    install_requires=[
        'jabberbot==0.15',
        'xmpppy==0.5.0rc1',
        'feedparser==5.1.3',
    ],
)
