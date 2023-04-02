import os


def get_directory_resolver(directory: str):
    def resolve(fname: str):
        return open(os.path.join(directory, fname)).read()

    return resolve
