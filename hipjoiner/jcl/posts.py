from datetime import datetime, date
from functools import lru_cache
import json
import os

from hipjoiner.jcl.config import config


class Posts:
    def __init__(self):
        pass

    def add(self, post):
        d = datetime.now().strftime('%Y-%m-%d-at-%H-%M-%S')
        subdir = '/'.join([self.posts_dir, d])
        os.makedirs(subdir)
        post_fpath = '/'.join([subdir, self.post_fname])
        with open(post_fpath, 'w') as fp:
            json.dump({'command': post}, fp, indent=4)

    @property
    def close_fname(self):
        return 'close.json'

    @property
    def post_fname(self):
        return 'post.json'

    def post_dirs(self, filter='all'):
        result = []
        for dt, proot in self.post_roots():
            for pdir in os.listdir(proot):
                post_dir = '/'.join([proot, pdir])
                print(post_dir)
                for f in os.listdir(post_dir):
                    print('  Found %s' % f)
                result.append(post_dir)
        return result

    def post_roots(self):
        result = []
        for root, dirs, files in os.walk(config.log_dir()):
            r = root.replace('\\', '/')
            for d in dirs:
                if d == 'posts':
                    result.append((root[-10:], '/'.join([r, d])))
        return result

    @property
    @lru_cache()
    def posts_dir(self):
        return config.posts_dir(date.today())


posts = Posts()


if __name__ == '__main__':
    # posts.add('run bleh')
    pdirs = posts.post_dirs()
