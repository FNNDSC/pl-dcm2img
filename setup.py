from setuptools import setup

setup(
    name='dcm2img',
    version='1.0.2',
    description='A ChRIS plugin that converts medical images (typically DICOM) to more friendly JPG/PNG format.',
    author='FNNDSC',
    author_email='dev@babyMRI.org',
    url='https://github.com/rudolphpienaar/pl-dcm2img',
    py_modules=['dcm2img'],
    install_requires=['chris_plugin'],
    license='MIT',
    python_requires='>=3.8.2',
    entry_points={
        'console_scripts': [
            'dcm2img = dcm2img:main'
        ]
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Medical Science Apps.'
    ]
)
