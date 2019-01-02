:: ecoReleve-Sensor installation script
:: Requires Python 3.4.1, conda and conda-build
:: Minimum version of Pandas should be 0.15.0

call python -m pip install --user virtualenv
call python -m venv .\portalvenv
call portalvenv\Scripts\activate
call python -m pip install --upgrade pip setuptools
call python setup.py install
