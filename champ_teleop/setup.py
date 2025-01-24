from setuptools import setup

package_name = 'champ_teleop'

setup(
    name=package_name,
    version='0.6.2',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/teleop.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Juan Miguel Jimeno',
    maintainer_email='jimenojmm@gmail.com',
    description='Generic keyboard teleop for twist robots.',
    license='BSD',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'champ_teleop = champ_teleop.champ_teleop:main'
        ],
    },
)