import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='AnaPyzer',
    version='0.0.1',
    author='Daniel Estes, Michael Langley, Nathan O\'Brien, Noah Greer',
    author_email='noah.greer@gmail.com',
    description='Common and W3C log analyzer written in Python with Tkinter and Matplotlib',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url='https://github.com/NoahGreer/AnaPyzer',
    license='GNU GPLv3',
    packages = setuptools.find_packages(),
    classifiers = (
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Intended Audience :: System Administrators"
    )
)