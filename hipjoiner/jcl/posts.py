import os

from hipjoiner.jcl.config import config


class Posts:
    def __init__(self):
        pass

    def add(self):
        pass

    def all_posts(self):
        all = []
        for dt, pdir in self.all_queue_dirs():
            posts = os.listdir(pdir)
            for post in posts:
                dpath = '/'.join([pdir, post])
                if os.path.isdir(dpath):
                    all.append(dpath)
        return all

    def all_queue_dirs(self):
        qdirs = []
        for root, dirs, files in os.walk(config.log_dir()):
            r = root.replace('\\', '/')
            for d in dirs:
                if d == 'queue':
                    qdirs.append((root[-10:], '/'.join([r, d])))
        return qdirs


posts = Posts()


if __name__ == '__main__':
    print('All queue dirs:')
    for dt, d in posts.all_queue_dirs():
        print('  %s' % d)
    print('All posts:')
    for p in posts.all_posts():
        print('  %s' % p)
