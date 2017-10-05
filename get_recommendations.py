from collections import Counter

from clize import run
from git import Repo


def count_files(repo, paths):
    counter = Counter()
    for c in repo.iter_commits(paths=paths):
        print(c.message)
        if len(c.parents) > 1:
            print('Skipping merge commit with {} parents'
                  .format(len(c.parents)))
        else:
            counter.update(c.stats.files.keys())

    return counter


def main(path='.', num_recommendations=10):
    repo = Repo(path)
    changed_files = [d.b_path for d in repo.index.diff(None)]
    counter = count_files(repo, changed_files)
    for file, count in counter.most_common(num_recommendations):
        print("{} with co-occurrence {}".format(file, count))


if __name__ == "__main__":
    run(main)

