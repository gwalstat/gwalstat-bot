import os
import aiohttp

from aiohttp import web
from gidgethub import routing, sansio
from gidgethub import aiohttp as gh_aiohttp

from . import util
from .git_util import get_branch
from .spcheck import spelling_check
from .file_ext import filepath

routes = web.RouteTableDef()

router = routing.Router()


@router.register("issues", action="opened")
async def issue_opened_event(event, gh, *args, **kwargs):
    """
    Whenever an issue is opened, greet the author and say thanks.
    """
    url = event.data["issue"]["comments_url"]
    author = event.data["issue"]["user"]["login"]

    message = f"Thanks for the report @{author}! I will look into it ASAP! (I'm a bot)."
    await gh.post(url, data={"body": message})


@router.register("pull_request", action="opened")
async def pull_request_opened_event(event, gh, *args, **kwargs):
    """ Whenever a pull_request is opened, greet the author."""

    await util.post_status(gh, event, util.pending)

    url = event.data["pull_request"]["comments_url"]
    author = event.data["pull_request"]["user"]["login"]
    diff_url = event.data["pull_request"]["diff_url"]
    pr_number = event.data["number"]
    repository_name = event.data["pull_request"]["head"]["repo"]["name"]
    full_url = "https://github.com/" + author + "/" + repository_name
    branch = event.data["pull_request"]["head"]["ref"]
    dirname = get_branch(full_url, branch)
    file_path = filepath(dirname)
    print(file_path)
    f = open(dirname + "/README.md", "r")
    html_report = open("/tmp/" + str(pr_number) + ".txt", "w")

    result = spelling_check(f.read())
    if result is not None:

        html_report.write(result["report"])

        wrong_word = "\n".join(result["error_list"])
        message = (
            f"🤖 Thanks for the pull_request @{author}! <br>"
            f"Your commit is on {diff_url} <br>"
            f"Full Url: {full_url +'/tree/'+ branch} <br>"
            f"Pull Request number is : {pr_number} <br>"
            f"TYPOS Found Below: <br><br>"
            f"{wrong_word} <br><br>"
            "I will look into it ASAP! (I'm a bot, BTW 🤖)."
        )
        await gh.post(url, data={"body": message})
        await gh.patch(
            event.data["pull_request"]["issue_url"], data={"labels": ["TYPO"]}
        )
        util.failure["target_url"] += str(pr_number)
        await util.post_status(gh, event, util.failure)
    else:

        message = (
            f"🤖 Thanks for the pull_request @{author}! <br>"
            f"Your commit is on {diff_url} <br>"
            f"Full Url: {full_url} <br>"
            f"Pull Request number is : {pr_number} <br>"
            f"There is no TYPO found <br><br>"
            "I will look into it ASAP! (I'm a bot, BTW 🤖)."
        )

        await gh.post(url, data={"body": message})
        await util.post_status(gh, event, util.success)


@routes.post("/")
async def main(request):
    body = await request.read()

    secret = os.environ.get("GH_SECRET")
    oauth_token = os.environ.get("GH_AUTH")

    event = sansio.Event.from_http(request.headers, body, secret=secret)
    async with aiohttp.ClientSession() as session:
        gh = gh_aiohttp.GitHubAPI(session, "krnick", oauth_token=oauth_token)
        await router.dispatch(event, gh)
    return web.Response(status=200)


@routes.get("/{name}")
async def report(request):
    name = request.match_info.get("name", "Anonymous")
    f = open("/tmp/" + name + ".txt", "r")
    text = f.read()
    return web.Response(text=text, content_type="text/html")


if __name__ == "__main__":
    app = web.Application()
    app.add_routes(routes)
    port = os.environ.get("PORT")
    if port is not None:
        port = int(port)

    web.run_app(app, port=port)
