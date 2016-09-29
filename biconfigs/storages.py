import codecs

__memory_storage = {}

def file_read(path):
    with codecs.open(path, 'r', 'utf-8') as f:
        return f.read()

def file_write(path, text):
    with codecs.open(path, 'w', 'utf-8') as f:
        return f.write(text)

def memory_write(key, data):
    __memory_storage[key] = data

STORAGES = {
    'file': {
        'read': file_read,
        'write': file_write
    },
    'memory': {
        'read': lambda x: __memory_storage[x],
        'write': memory_write
    }
}
