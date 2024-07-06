import json
import os
import time
import zipfile

from config_parser import ConfigParser


def main(output_json, version, service_info=None):
    build_time = int(time.time())
    if service_info:
        with open(service_info, 'r') as f:
            service_info = json.load(f)
        plugin_list = [service_info]
    else:
        plugin_list = [{'provide': "ColdWindScholar", "manufacturer": "Github", "desc": "Free Plugin Repo"}]
    for i in os.listdir(os.getcwd()):
        if i.endswith('.mpk') and zipfile.is_zipfile(i):
            config = ConfigParser()
            with zipfile.ZipFile(i) as zf:
                with zf.open('info') as mpk_info:
                    config.read_string(mpk_info.read().decode('utf-8'))
                    try:
                        depend = config.get('module', 'depend').split()
                    except:
                        depend = []
                    plugin_list.append(
                        {
                            'name': config.get('module', 'name'),
                            'desc': config.get('module', 'describe'),
                            'author': config.get('module', 'author'),
                            'version': config.get('module', 'version'),
                            'size': os.stat(i).st_size,
                            "id": config.get('module', 'identifier'),
                            "depend": depend,
                            'files': [i]
                        }
                    )
    with open(output_json, 'w') as f:
        json.dump(plugin_list, f, indent=4, allow_nan=False, ensure_ascii=False)
    with open(version, 'w') as f:
        f.write(str(build_time))


if __name__ == '__main__':
    main('plugin.json', 'version.txt')
