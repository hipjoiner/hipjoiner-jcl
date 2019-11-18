from datetime import datetime, date
from functools import lru_cache
import os

from hipjoiner.jcl.config import config


class Posts:
    def __init__(self):
        pass

    def add(self, post):
        d = datetime.now().strftime('%Y-%m-%d-at-%H-%M-%S')
        subdir = '/'.join([self.post_dir, d])
        os.makedirs(subdir)
        post_fpath = '/'.join([subdir, 'post.txt'])
        with open(post_fpath, 'w') as fp:
            fp.write(post)

    def all_posts(self):
        all = []
        for dt, pdir in self.all_post_dirs():
            posts = os.listdir(pdir)
            for post in posts:
                dpath = '/'.join([pdir, post])
                if os.path.isdir(dpath):
                    all.append(dpath)
        return all

    def all_post_dirs(self):
        qdirs = []
        for root, dirs, files in os.walk(config.log_dir()):
            r = root.replace('\\', '/')
            for d in dirs:
                if d == 'posts':
                    qdirs.append((root[-10:], '/'.join([r, d])))
        return qdirs

    @property
    @lru_cache()
    def post_dir(self):
        return '/'.join([config.log_dir(date.today()), 'posts'])


posts = Posts()


if __name__ == '__main__':
    """
    print('All queue dirs:')
    for dt, d in schedule.all_post_dirs():
        print('  %s' % d)
    print('All posts:')
    for p in schedule.all_posts():
        print('  %s' % p)
    """
    posts.add('bleh')
