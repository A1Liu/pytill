import os, json, hashlib, logging

def md5(txt):
    m = hashlib.md5()
    m.update(txt.encode('utf8'))
    return m.hexdigest()

# Tracks files. Stores data permanently in a metadata file set by 'path' in __init__
# Checks whether files have been edited since the tracker was last instantiated.
class FileTracker():

    def __init__(self, path):
        data_path = os.path.abspath(path)
        self.logger = logging.getLogger('aliu.file_tracker.FileTracker(%s)' % data_path)
        self.logger.setLevel(logging.DEBUG)
        self.data = {}
        self.load_data(data_path)
        self.data_path = data_path
        self.changed = False

    def load_data(self,data_path):
        # Loads data from file
        self.logger.info('Loading Data...')
        if os.path.isdir(data_path):
            raise ValueError("data_path cannot be a directory!")
        if os.path.exists(data_path):
            with open(data_path) as f:
                self.data.update(json.load(f))
            self.logger.info('Data loaded!')
        else:
            self.logger.info('Data file not found. Checking path validity...')
            open(data_path,'x').close() # Check a few things
            os.remove(data_path)
            self.changed = True
            self.logger.info('Starting from scratch with no archived file hashes.')

    def save_data(self):
        # Saves data to self.data_path file, if there has been any changes to files
        if self.changed is False: return
        with open(self.data_path,'w') as f:
            json.dump(self.data,f)

    def was_edited(self, path, update = True):
        # Returns true if the file at path was edited since we last checked.
        # If update is false, the internal file tracker isn't updated.
        with open(path) as f:
            hash = md5(f.read())
        if path in self.data and self.data[path] == hash:
            return False
        else:
            if update == True:
                self.data[path] = hash
                self.changed = True
            return True
