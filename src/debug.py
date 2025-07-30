from dataloader0 import *
from vizualization import *
if __name__ == '__main__':
    file_paths = ["/path/to/the/file"]
    dataloader = Dataloader(file_paths)
    viz(dataloader.raw_df)
