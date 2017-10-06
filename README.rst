*****
Git-clippy
*****

Git-clippy is a file change recommendation tool, which helps you identify relevant files that you 
may have to modify when you touch a particular file. Recommendation is based on all past commit 
histories and clustering and ranking of files.

git-clippy>git-clippy
Finding changed files: 0 files [00:00, ? files/s]
Analyzing commit history: 21 commits [00:00, 103.07 commits/s]
14 co-occurring files in commit history.

    XXXXX
   X     X
-----+  +----+      ------------------------------------------------------
| .  |  | .  |      | I see you've added some bugs!                      |
|    |  |    |      | Maybe you need to change these files as well?      |
-----+  +----+      |                                                    |
  X      X          |                                                    |
  X  X   X          | setup.py                                           |
  X  X   X   +------| get_recommendations.py                             |
  X  X   X          | .gitignore                                         |
  X  X   X          | create-commit-graph.py                             |
  X  X  X  X        | ui.py                                              |
  X   XX  X         ------------------------------------------------------
   X      X
    XXXXXX
