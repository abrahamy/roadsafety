from setuptools import find_packages, setup

setup(
    name='roadsafety',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask==1.0.2',
        'flask-restplus==0.11.0',
        'Flask-SQLAlchemy==2.3.2',
        'googlemaps==2.5.1',
        'python-dotenv==0.8.2',
        'Authlib==0.7',
        'requests==2.18.4',
        'six==1.11.0',
        'WTForms==2.1',
    ],
)
