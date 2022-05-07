'''
Copyright (c) 2022 yu9824
'''

import re
import os

def replace_meta(fpath_meta, fpath_out=None):
    if os.path.isfile(fpath_meta):
        with open(fpath_meta, mode='r') as f:
            metadata = f.read()
    else:
        raise FileNotFoundError(f'{fpath_meta} not found')

    package_name = None
    # package_version = None

    result_name = re.search(r'{% set name = "(.+)" %}', metadata)
    if result_name:
        package_name = result_name.group(1)
    dirname = package_name.replace('-', '_')

    # result_version = re.search(r'{% set version = "(.+)" %}', metadata)
    # if result_version:
    #     package_version = result_version.group(1)
    
    # package_json_url = f'https://pypi.org/pypi/{package_name}/json'
    # response = requests.get(package_json_url)
    # if response:
    #     package_info = response.json()

    # for _d in package_info['releases'][package_version]:
    #     # endwith tar.gz
    #     if _d['url'].endswith('.tar.gz'):
    #         download_url = _d['url']
    #         break

    # Modify some metadata
    metadata_replaced = metadata
    # print(re.search(r'({% set name = ".+" %})', metadata_replaced))
    metadata_replaced = re.sub(r'({% set name = ".+" %})', '\\1\n{% set dirname = "' + dirname + '" %}', metadata_replaced)

    # metadata_replaced = re.sub(r'(source:\n\s+url:\s*")(http.+)"', f'\\1{download_url}"', metadata_replaced) # in conda-build 3.21.8, source link is not working
    metadata_replaced = re.sub('/{{ name }}', '/{{ dirname }}', metadata_replaced)
    metadata_replaced = re.sub(r'(recipe-maintainers:\n\s*-\s*)(your-github-id-here)', '\\1yu9824', metadata_replaced)
    metadata_replaced = re.sub(r'(build:\n)(\s*)', '\\1\\2noarch: python\n\\2', metadata_replaced)  # noarch but pure python package
    metadata_replaced = re.sub(r'(license_file:)', '\\1 LICENSE', metadata_replaced)    # to upload conda-forge
    metadata_replaced = re.sub(r'(host:\n)(\s*)(.|\n)*(\n\s*run:)', '\\1\\2- pip\n\\2- python\\4', metadata_replaced)   # to upload conda-forge
    metadata_replaced = re.sub(r'(- python)', '\\1 >=3.6', metadata_replaced)            # to upload conda-forge
    metadata_replaced = re.sub(r'\s*doc_url:\s*?\n', '\n', metadata_replaced)  # to upload conda-forge
    metadata_replaced = re.sub(r'(\s*dev_url:\s*?)\n', '\\1https://github.com/yu9824/{{ dirname }}\n', metadata_replaced)  # to upload conda-forge

    
    if fpath_out is None:
        fpath_out = fpath_meta
    with open(fpath_out, mode='w') as f:
        f.write(metadata_replaced)
        
if __name__ == '__main__':
    # debug
    # replace_meta('examples/meta.yaml', 'meta.yaml')
    
    # release
    import sys
    replace_meta(sys.argv[1])
