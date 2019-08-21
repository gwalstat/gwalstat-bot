import git
import tempfile
import shutil

def get_branch(url, ref):

    dirpath = tempfile.mkdtemp()
    repo = git.Repo.clone_from(url=url, to_path=dirpath)

    origin = repo.remotes.origin
    git_command = git.cmd.Git()

    matching = []

    while(len(matching) == 0):
        # Checking the remote ref exists or not.
        print("Test the remote ref")
        list_ref = git_command.ls_remote(url).split("\n")
        matching = [s for s in list_ref if ref in s]

    del matching
    del git_command

    print("Start to fetching")
    origin.fetch(ref)

    repo.git.checkout("-qf", "FETCH_HEAD")

    return dirpath

# get_branch("https://github.com/krnick/test-g", "refs/pull/25/merge")

