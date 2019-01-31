from setuptools import setup

__version__ = "v0.0.2"

setup(name="illusional.cwlgen",
        version=__version__,
        description='Fork of python-cwlgen | Generation of CWL programmatically. Avaible types: CommandLineTool, Workflow and Requirements',
        long_description=open("./README.md").read(),
        author='Michael Franklin | Kenzo-Hugo Hillion and Herve Menager',
        author_email='michael.franklin@petermac.org',
        license='MIT',
        keywords = ['cwl'],
        install_requires=['six', 'ruamel.yaml==0.13.13'],
        packages=["cwlgen"],
        classifiers=[
            'Development Status :: 4 - Beta',
            'Topic :: Scientific/Engineering',
            'Intended Audience :: Developers',
            'Intended Audience :: Science/Research',
            'Environment :: Console',
            ],
        )
