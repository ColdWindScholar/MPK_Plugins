import json
import os
import time
import zipfile

from config_parser import ConfigParser


# {"name": "app1", "version": "1.0", "size": 102400, "desc": "app1", "id": "", "merge": "y", "files": ['f1.mpk.1', 'f1.mpk.2']}{"name": "app1", "version": "1.0", "size": 102400, "desc": "app1", "id": "", "merge": "y", "files": ['f1.mpk.1', 'f1.mpk.2']}
def main(output_json, version):
    build_time = int(time.time())
    plugin_list = []
    for i in os.listdir(os.getcwd()):
        if i.endswith('.mpk') and zipfile.is_zipfile(i):
            config = ConfigParser()
            with zipfile.ZipFile(i) as zf:
                with zf.open('info') as mpk_info:
                    config.read_string(mpk_info.read().decode('utf-8'))
                    plugin_list.append(
                        {
                            'name': config.get('module', 'name'),
                            'desc': config.get('module', 'describe'),
                            'author': config.get('module', 'author'),
                            'version': config.get('module', 'version'),
                            'size': os.stat(i).st_size,
                            "id": config.get('module', 'identifier'),
                            'files': [i]
                        }
                    )
    with open(output_json, 'w') as f:
        json.dump(plugin_list, f, indent=4, allow_nan=False, ensure_ascii=False)
    with open(version, 'w') as f:
        f.write(str(build_time))



if __name__ == '__main__':
    main('plugin.json', 'version.txt')
