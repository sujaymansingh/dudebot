import setuptools

REQUIREMENTS = [
    "docopt==0.6.1",
    "feedparser==5.1.3",
    "jabberbot==0.15",
    "xmpppy==0.5.0rc1",
]

if __name__ == "__main__":
    setuptools.setup(
        name="dudebot",
        version="0.0.7",
        author="Sujay Mansingh",
        author_email="sujay.mansingh@gmail.com",
        packages=setuptools.find_packages(),
        scripts=[],
        url="https://github.com/sujaymansingh/dudebot",
        license="LICENSE.txt",
        description="A really simple framework for chatroom bots",
        long_description="View the github page (https://github.com/sujaymansingh/dudebot) for more details.",
        install_requires=REQUIREMENTS
    )
