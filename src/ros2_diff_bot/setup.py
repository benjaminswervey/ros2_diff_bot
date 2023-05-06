from setuptools import setup

package_name = 'ros2_diff_bot'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='benjamin',
    maintainer_email='youremail@example.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'my_node = ros2_diff_bot.my_node:main',
            'encoder_reader = ros2_diff_bot.encoder_reader:main',
            'encoder_counter = ros2_diff_bot.encoder_counter:main',
            'encoder_calculator = ros2_diff_bot.encoder_calculator:main'
        ],
    },
)
