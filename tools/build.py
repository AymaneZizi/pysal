"""
Build requirements file for meta package from latest stable subpackages on pypi

The meta package will pin each subpackage to its most recent release on pypi at the time this script is run.
"""

import os
from yolk.pypi import CheeseShop

packages = """
libpysal
access
esda
giddy
inequality
pointpats
segregation
spaghetti
mgwr
spglm
spint
spreg
spvcm
tobler
mapclassify
splot
"""

other_reqs = """
urllib3>=1.26
python-dateutil<=2.8.0
pytest
pytest-cov
coverage
"""

PACKAGE_FILE = 'package_versions.txt'

# get most recent releases of subpackages on pypi
def _get_latest_version_number(package_name):
    pkg, all_versions = CheeseShop().query_versions_pypi(package_name)
    if len(all_versions):
        return all_versions[0]
    return None

def _get_pysal_sub_versions():
    lines = []
    print('Getting latest pypi versions of subpackages\n\n')
    for package in packages.split():
        version = _get_latest_version_number(package)
        fstring = f'{package} {version}'
        lines.append(fstring)
        print(fstring)
    with open(PACKAGE_FILE, 'w') as req:
        req.write("\n".join(lines))

def get_frozen():
    from os import path

    _get_pysal_sub_versions()
    with open(PACKAGE_FILE, 'r') as version_file:
        frozen = dict([line.strip().split()
                       for line in version_file.readlines()])
    return frozen


def build_frozen():
    base = os.path.join(os.pardir, 'pysal', 'frozen.py')
    content = f'"""\nFrozen subpackages for meta release.\n"""\n\n'

    print('Creating ../frozen.py')
    with open(base, 'w') as target_file:
        target_file.write(content)
        frozen = get_frozen()
        target_file.write('frozen_packages = {')
        lines = []
        for package, version in frozen.items():
            lines.append(f'    "{package}": "{version}"')
        lines = ",\n".join(lines)

        target_file.write(lines)
        target_file.write("\n}")



def build_requirements():
    """
    Write out requirements.txt file with pinning information

    """
    lines = []
    frozen = get_frozen()
    print('\n\n Writing requirements.txt:\n')
    for package in frozen.keys():
        version = frozen[package]
        print(package, version)
        if package != 'spvcm':
            lines.append(f'{package}>={version}')
        else:
            lines.append(f'{package}=={version}')

    for package in other_reqs.split():
        lines.append(package)

    with open('requirements.txt', 'w') as req:
        req.write("\n".join(lines))



def main():
    build_requirements()

if __name__ == '__main__':
    main()
