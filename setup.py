from setuptools import setup
import sdist_upip


setup(
    name='microhomie',
    version='0.2.0',
    description='MicroPython implementation of the Homie v2 convention.',
    long_description='More documentation is available at https://github.com/microhomie/micropython-homie',
    url='https://github.com/microhomie/micropython-homie',
    author='Microhomie Developers',
    author_email='contact@microhomie.com',
    maintainer='Microhomie Developers',
    maintainer_email='contact@microhomie.com',
    license='MIT',
    cmdclass={'sdist': sdist_upip.sdist},
    packages=['homie', 'homie.node'],
    install_requires=['micropython-umqtt.simple'],
)
