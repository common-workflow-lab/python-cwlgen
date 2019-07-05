from setuptools import setup

exec(open("cwlgen/version.py").read())

setup(
    name="cwlgen",
    version=__version__,
    description="Generation of CWL programmatically. Available types: Workflow, CommandLineTool and Requirements",
    author="Kenzo-Hugo Hillion and Herve Menager",
    author_email="kehillio@pasteur.fr",
    long_description=open("./README.md").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    keywords=["cwl"],
    install_requires=["ruamel.yaml >= 0.12.4, <= 0.15.87"],
    packages=["cwlgen"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Environment :: Console",
    ],
)
