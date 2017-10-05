from collections import Counter
from textwrap import dedent

from clize import run
from git import Repo
from tqdm import tqdm


def update_counter(repo, paths, counter):
    for c in repo.iter_commits(paths=paths):
        if len(c.parents) > 1:
            # print('Skipping merge commit with {} parents'
            #       .format(len(c.parents)))
            continue

        counter.update(f for f in c.stats.files.keys() if f not in paths)
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


def main(path='.', num_recommendations=10):
    repo = Repo(path)
    changed_files = list(tqdm(get_changed_files(repo),
                              desc="Finding changed files", unit=" files"))
    for file in changed_files:
        print("You changed {}".format(file))

    counter = count_files(repo, changed_files)
    print(dedent("""
        XXXXX           XXXXX
        
        XXXXX   XXXXX   XXXXX
        X X X  X     X  X X X
        X   X  X  X  X  X   X    I see you have added bugs to some files!
        XXXXX  X  X  X  XXXXX    Perhaps you should consider these ones also:
               X  X  X
               X  X  X
           XX  X  X  X
            XX XXXX XX
             X      X
             XXXXXXX
        """))
    total_num_file_commits = sum(counter.values())
    total_num_files = len(counter)
    print("{} co-occurring files in commit history.".format(total_num_files))
    for file, count in counter.most_common(num_recommendations):
        print("{} ({:.2%})".format(file, count/total_num_file_commits))


if __name__ == "__main__":
    run(main)

