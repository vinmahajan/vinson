from setuptools import setup, find_packages

setup(
    name='vinson',
    version='0.1',
    author='Vinayak Mahajan',
    description="Vinson Database is a lightweight, file-based Python database.",
    long_description="Vinson Database is a lightweight, file-based Python database designed to manage structured data simply and efficiently. Optimized for handling CRUD operations with flexible querying and filtering capabilities, Vinson Database is ideal for small to medium datasets that require robust data manipulation without the overhead of traditional databases. The system also provides support for managing duplicates and indexing with primary keys.",
    author_email='vinayakmahajan06@gmail.com',
    packages=find_packages(),
    keywords=['python', 'json', 'nosql', 'database', 'nosql database', 'json database', 'python database'],
    classifiers=[
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: MIT License',
    'Operating System :: Unix',
    'Operating System :: Microsoft :: Windows',
    ],
    
)