from setuptools import setup
import sdist_upip


setup(
    name='micropython-homie',
    version='0.1.0',
    description='MicroPython implementation of the Homie v2 convention.',
    long_description='More documentation is available at https://github.com/microhomie/micropython-homie',
    url='https://github.com/microhomie/micropython-homie',
    author='MicroHomie Developers',
    author_email='contact@microhomie.com',
    maintainer='MicroHomie Developers',
    maintainer_email='contact@microhomie.com',
    license='MIT',
    cmdclass={'sdist': sdist_upip.sdist},
    packages=['homie', 'homie.node'],
    install_requires=['micropython-collections', 'micropython-umqtt.simple'],
)
