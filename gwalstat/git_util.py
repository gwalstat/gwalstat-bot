import git
import tempfile
import shutil

FILE_EXTENSION_CHECK = ("md", "rst")


def get_branch(url, br):

    dirpath = tempfile.mkdtemp()
    git_command = git.cmd.Git()
    matching = []
    changed_files_name = []
    changed_files_path = []
    result = {}

    while len(matching) == 0:
        # Checking the remote ref exists or not.
        print("Testing the remote branch")
        list_ref = git_command.ls_remote(url).split("\n")
        matching = [s for s in list_ref if br in s]

    del matching
    del git_command

    print("Start to fetching")

    repo = git.Repo.clone_from(url=url, to_path=dirpath, branch=br)

    # Find changed files and path.
    for diff_item in repo.head.commit.diff("HEAD~1"):
        if diff_item.a_path.endswith(FILE_EXTENSION_CHECK):
            changed_files_path.append(dirpath + "/" + diff_item.a_path)
            changed_files_name.append(diff_item.a_path)

    # Return the dict of file path and file name which was changed.
    result["filename"] = changed_files_name
    result["filepath"] = changed_files_path
    return result


# user = "krnick"
# br = "krnick-patch-8"
# print(get_branch("https://github.com/" + user + "/Gwalstat-test", br))
