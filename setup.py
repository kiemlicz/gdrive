import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gdrive",
    version="0.0.1",
    author="kiemlicz",
    author_email="stanislaw.dev@gmail.com",
    description="Google Drive simple client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kiemlicz/gdrive",
    setup_requires=['pytest-runner', 'pytest-pylint'],
    tests_require=['pytest', 'pytest-mock', 'pylint'],
    install_requires=[
        "setuptools~=50.3.0",
        "google-api-python-client~=1.12.5",
        "google-auth-oauthlib~=0.4.1",
        "google-auth-httplib2~=0.0.4",
        "google-auth==1.22.1",
        "six==1.15.0",
        "pykeepass~=3.2.1"
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
