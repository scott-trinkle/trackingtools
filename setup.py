from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='trackingtools',
      version='0.1',
      description='Tools for tracking diffusion MRI and microCT data',
      long_description=readme(),
      author='Scott Trinkle',
      author_email='tscott.trinkle@gmail.com',
      license='MIT',
      packages=['trackingtools'],
      package_dir={'trackingtools': 'trackingtools'},
      package_data={'trackingtools': ['data/*']},
      zip_safe=False)
