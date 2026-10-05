import zipfile
import os


def create_minimal_vfs(path):
    with zipfile.ZipFile(path, 'w') as zf:
        zf.writestr('hello.txt', 'Hello, VFS!')


def create_several_vfs(path):
    with zipfile.ZipFile(path, 'w') as zf:
        zf.writestr('file1.txt', 'Content of file 1')
        zf.writestr('file2.txt', 'Content of file 2')
        zf.writestr('folder/file3.txt', 'Content of file 3')
        zf.writestr('folder/file4.txt', 'Content of file 4')


def create_deep_vfs(path):
    with zipfile.ZipFile(path, 'w') as zf:
        zf.writestr('root.txt', 'Root file')
        zf.writestr('level1/l1.txt', 'Level 1 file')
        zf.writestr('level1/level2/l2.txt', 'Level 2 file')
        deep = 'level1/level2/level3/l3.txt'
        zf.writestr(deep, 'Level 3 file')


if __name__ == "__main__":
    os.makedirs('tests', exist_ok=True)
    create_minimal_vfs('tests/vfs_minimal.zip')
    create_several_vfs('tests/vfs_several.zip')
    create_deep_vfs('tests/vfs_deep.zip')
    print("Test VFS archives created!")