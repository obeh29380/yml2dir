import os
import yaml


def load_yaml(file_path):
    """
    yamlファイル読み込み
    """
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def __do_recursive(current, node, checkonly=False):
    """
    current: 現在の絶対パス
    以下のようなファイル・ディレクトリ情報が投入される
    - name: child1_file.txt
      type: file
      content: |
        This is child1_file.txt
    """
    current = os.path.join(current, node['name'])

    if node['type'] == 'file':

        if 'children' in node:
            raise ValueError('File cannot have children')
        if checkonly is False:
            with open(current, 'w') as f:
                f.write(node.get('content', ''))

    elif node['type'] in ['directory', 'dir']:

        if checkonly is False:
            os.makedirs(current, exist_ok=True)
        if 'children' in node:
            for child in node['children']:
                __do_recursive(current, child)

    if not checkonly:

        if 'owner' in node or 'group' in node:
            os.chown(current, node.get('owner', -1), node.get('group', -1))
        if 'permissions' in node:
            os.chmod(current, int(node['permissions'], 8))

def apply(yaml):
    """
    読み込んだyamlファイルをもとにディレクトリを作成する
    """
    y = load_yaml(yaml)
    if 'root' not in y:
        raise ValueError('YAML must contain a root node')

    current = y['root']
    if not os.path.isdir(current):
        raise ValueError('Root must be a directory')

    if 'children' in y:
        for child in y['children']:
            __do_recursive(current, child)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python y2d.py <yaml_file>")
        sys.exit(1)

    yaml_file = sys.argv[1]
    apply(yaml_file)