from setuptools import setup

setup(
    name="cryptodweet",
    version="0.1.2",
    description="A simple python package for the free dweet service with " + \
        "encryption.",
    long_description="https://github.com/jacklinquan/cryptodweet",
    long_description_content_type="text/markdown",
    url="https://github.com/jacklinquan/cryptodweet",
    author="Quan Lin",
    author_email="jacklinquan@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3"
    ],
    packages=["cryptodweet"],
    install_requires=["dweepy", "cryptomsg"]
)
