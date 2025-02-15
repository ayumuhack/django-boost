import os
from setuptools import setup


def fullsplit(path, result=None):
    """
    Split a pathname into components (the opposite of os.path.join) in a
    platform-neutral way.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)


# Compile the list of packages available, because distutils doesn't have
# an easy way to do this.
packages, package_data = [], {}

root_dir = os.path.dirname(__file__)
if root_dir != '':
    os.chdir(root_dir)
extensions_dir = 'django_boost'

for dirpath, dirnames, filenames in os.walk(extensions_dir):
    # Ignore PEP 3147 cache dirs and those whose names start with '.'
    dirnames[:] = [d for d in dirnames if not d.startswith(
        '.') and d != '__pycache__']
    parts = fullsplit(dirpath)
    package_name = '.'.join(parts)
    if '__init__.py' in filenames:
        packages.append(package_name)
    elif filenames:
        relative_path = []
        while '.'.join(parts) not in packages:
            relative_path.append(parts.pop())
        relative_path.reverse()
        path = os.path.join(*relative_path)
        package_files = package_data.setdefault('.'.join(parts), [])
        package_files.extend([os.path.join(path, f) for f in filenames])


requires = ["Django>=2.0", "user-agents>=2.0"]


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


setup(
    name='django_boost',
    version='1.1',
    description='Django Extension library',
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    url='https://github.com/ChanTsune/Django-Boost',
    author='ChanTsune',
    author_email='yshegou@gmail.com',
    license='MIT',
    keywords='django extension',
    packages=packages,
    install_requires=requires,
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Framework :: Django',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'License :: OSI Approved :: MIT License',
    ],
)
