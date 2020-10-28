from setuptools import setup, find_packages

with open('README.md', encoding='utf8') as f:
    long_description = f.read()

with open('requirements.txt', encoding='utf8') as requirements_txt:
    install_requirements = requirements_txt.read().split(",")

setup(
    name='maleo',
    packages=find_packages(),
    version='0.0.1',
    license='MIT',
    description='Wrapper library for data cleansing, preprocessing in text',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Ruben Stefanus',
    author_email='researchjair@gmail.com',
    url='https://github.com/jakartaresearch/maleo',
    download_url='https://github.com/jakartaresearch/maleo/archive/v0.0.1.tar.gz',
    keywords=['nlp', 'text-processing', 'machine-learning'],
    install_requires=install_requirements,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Text Processing',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
