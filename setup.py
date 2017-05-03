from setuptools import setup
import cwlgen

setup(name="cwlgen",
        version=cwlgen.version,
        description='Generation of CWL programmatically. Avaible types: CommandLineTool and DockerRequirement',
        author='Kenzo-Hugo Hillion and Herve Menager',
        author_email='kehillio@pasteur.fr and hmenager@pasteur.fr',
        license='MIT',
        keywords = ['cwl'],
        install_requires=['six', 'ruamel.yaml==0.13.13'],
        packages=["cwlgen"],
        classifiers=[
            'Development Status :: 4 - Beta',
            'Topic :: Scientific/Engineering :: Bio-Informatics',
            'Intended Audience :: Developers',
            'Intended Audience :: Science/Research',
            'Environment :: Console',
            ],
        )
