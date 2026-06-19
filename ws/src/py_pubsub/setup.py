from setuptools import find_packages, setup

package_name = 'py_pubsub'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='vscode',
    maintainer_email='vscode@todo.todo',
    description='TODO: Package description',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'nodo_a_img = py_pubsub.nodo_a_img:main',
            'nodo_a_finale = py_pubsub.nodo_a_finale:main',
            'nodo_b_img = py_pubsub.nodo_b_img:main',
            'nodo_b_finale = py_pubsub.nodo_b_finale:main',
        ],
    },
)