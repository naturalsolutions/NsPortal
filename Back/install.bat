:: ecoReleve-Sensor installation script
:: Requires Python 3.4.1, conda and conda-build
:: Minimum version of Pandas should be 0.15.0

conda install pyodbc
conda install sqlalchemy
conda install zope.interface
pip install pyramid_jwtauth


python setup.py install
