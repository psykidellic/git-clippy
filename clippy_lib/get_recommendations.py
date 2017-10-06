from collections import Counter
from textwrap import dedent
import os
import sys

from clize import run
from git import Repo
from tqdm import tqdm
import ui


def update_counter(repo, paths, counter):
    for c in repo.iter_commits(paths=paths):
        if len(c.parents) > 1:
            # print('Skipping merge commit with {} parents'
            #       .format(len(c.parents)))
            continue

        counter.update(f for f in c.stats.files.keys() if f not in paths and '=>' not in f)
        yield None  # so it's an iterable for tqdm


def count_files(repo, paths):
    counter = Counter()
    for _ in tqdm(update_counter(repo, paths, counter),
                  desc="Analyzing commit history", unit=" commits"):
        pass

    return counter


def get_changed_files(repo):
    for d in repo.index.diff(None):
        yield d.b_path

def find_git_root(pwd):
    try:
        _, dirs, _ = next(os.walk(pwd))
        if '.git' in dirs:
            return pwd
        else:
            return find_git_root(os.path.dirname(pwd))
    except StopIteration:
        return None


def recommend(path, num_recommendations):
    repo_path = find_git_root(os.path.abspath(path))
    if repo_path is None:
        sys.stderr.write("Couldn't find git repo\n")
        sys.exit(1)
    repo = Repo(repo_path)
    changed_files = list(tqdm(get_changed_files(repo),
                              desc="Finding changed files", unit=" files"))
    for file in changed_files:
        print("You changed {}".format(file))

    counter = count_files(repo, changed_files)
    total_num_file_commits = sum(counter.values())
    total_num_files = len(counter)
    print("{} co-occurring files in commit history.".format(total_num_files))
    print('')
    files = []
    for file, _ in counter.most_common(num_recommendations):
        files.append(file)
    ui.output(files)

