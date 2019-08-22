import git
import tempfile
import shutil

def get_branch(url, br):

    dirpath = tempfile.mkdtemp()
    repo = git.Repo.clone_from(url=url, to_path=dirpath,branch=br)

    origin = repo.remotes.origin
    git_command = git.cmd.Git()

    matching = []

    while(len(matching) == 0):
        # Checking the remote ref exists or not.
        print("Test the remote branch")
        list_ref = git_command.ls_remote(url).split("\n")
        matching = [s for s in list_ref if br in s]

    del matching
    del git_command

    print("Start to fetching")

    return dirpath

############
#user = "18z"
#br = "patch-1"
#print(get_branch("https://github.com/"+user+"/test-g", br))
############
