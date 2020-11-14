import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="geosy",
    version="0.0.1",
    author="Leonardo Antunes",
    author_email="antunesleo4@gmail.com",
    description="Geo processing doesn't have to be so hard",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/antunesleo/geosy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    python_requires='>=3.8',
)
