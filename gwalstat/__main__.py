import os
import aiohttp

from aiohttp import web
from gidgethub import routing, sansio
from gidgethub import aiohttp as gh_aiohttp

from . import util
from .git_util import get_branch


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
    # reaction_url = f"{url}/reactions"
    author = event.data["pull_request"]["user"]["login"]
    diff_url = event.data["pull_request"]["diff_url"]
    number = event.data["number"]
    full_url = "https://github.com/"+event.data["pull_request"]["head"]["repo"]["full_name"]
    dirname = get_branch(full_url, "refs/pull/"+str(number)+"/merge")
    f = open(dirname+"/README.md","r")


    message = (
        f"🤖 Thanks for the pull_request @{author}! <br>"
        f"Your commit is on {diff_url} <br>"
        f"full url: {full_url} <br>"
        f"Pull Request number is : {number}! <br>"
        f"Change content is: <br><br> {f.read()} <br><br>"
        "I will look into it ASAP! (I'm a bot, BTW 🤖)."
    )
    await gh.post(url, data={"body": message})
    await util.post_status(gh, event, util.status_check)


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


if __name__ == "__main__":
    app = web.Application()
    app.add_routes(routes)
    port = os.environ.get("PORT")
    if port is not None:
        port = int(port)

    web.run_app(app, port=port)
