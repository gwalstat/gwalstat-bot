import git
import tempfile
import shutil

FILE_EXTENSION_CHECK = ("md", "rst")


class GitUtil:
    def get_branch(self, url, br):

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
                changed_files_name.append(diff_item.a_path)

        # Return the dict of file path and file name which was changed.
        result["filename"] = changed_files_name
        result["filepath"] = dirpath
        return result


# user = "krnick"
# br = "krnick-patch-3"
# git_util = GitUtil()
# print(git_util.get_branch("https://github.com/" + user + "/Gwalstat-test", br))
