from setuptools import setup, find_packages

setup(name='footprints',
      version='0.3',
      description='generate coverage shapefile from raster extents and raster data extents',
      url='http://github.com/earthscientist/footprints',
      author='Michael Lindgren',
      author_email='lindgren.mike@gmail.com',
      license='CLOSED',
	  packages = find_packages(),
	  entry_points={
	   'console_scripts': [
	      'footprints = footprints.footprints:main',
	        ], 
      },
      zip_safe=False)