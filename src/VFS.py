import zipfile
import base64


class VFS:
    def __init__(self):
        self.tree = {}
        self.cwd = '/'

    def load_from_zip(self, zip_path):
        try:
            with zipfile.ZipFile(zip_path, 'r') as zf:
                self.tree = {}
                for name in zf.namelist():
                    self.add_entry(zf, name)
                self.cwd = '/'
        except FileNotFoundError:
            raise FileNotFoundError(
                f"VFS not found: {zip_path}"
            )
        except zipfile.BadZipFile:
            raise ValueError(
                f"Invalid ZIP format: {zip_path}"
            )

    def add_entry(self, zf, name):
        is_dir = name.endswith('/')
        name = name.strip('/')
        if not name:
            return

        parts = name.split('/')
        current = self.tree

        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]

        if is_dir:
            if parts[-1] not in current:
                current[parts[-1]] = {}
        else:
            self.add_file(zf, name, current, parts[-1])

    def add_file(self, zf, name, parent, filename):
        data = zf.read(name)
        try:
            parent[filename] = data.decode('utf-8')
        except UnicodeDecodeError:
            parent[filename] = data

    def parse_path(self, path):
        if path.startswith('/'):
            raw = path.strip('/')
        else:
            raw = self.cwd.strip('/')
            if raw:
                raw += '/' + path.strip('/')
            else:
                raw = path.strip('/')

        if not raw:
            return []

        parts = raw.split('/')
        result = []
        for part in parts:
            if part == '' or part == '.':
                continue
            if part == '..':
                if result:
                    result.pop()
            else:
                result.append(part)
        return result

    def get_node(self, parts):
        node = self.tree
        for part in parts:
            if not isinstance(node, dict):
                return None
            if part not in node:
                return None
            node = node[part]
        return node

    def list_dir(self, path=None):
        if path is None:
            parts = self.parse_path(self.cwd)
        else:
            parts = self.parse_path(path)

        node = self.get_node(parts) if parts else self.tree

        if node is None:
            raise ValueError(
                f"path not found: {path or self.cwd}"
            )
        if not isinstance(node, dict):
            raise ValueError(f"not a directory: {path}")

        return sorted(node.keys())

    def change_dir(self, path):
        if path == '/':
            self.cwd = '/'
            return

        parts = self.parse_path(path)
        node = self.get_node(parts) if parts else self.tree

        if node is None:
            raise ValueError(f"path not found: {path}")
        if not isinstance(node, dict):
            raise ValueError(f"not a directory: {path}")

        self.cwd = '/' + '/'.join(parts)