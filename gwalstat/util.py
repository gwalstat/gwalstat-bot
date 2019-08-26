success = {
    "state": "success",
    "target_url": "https://example.com/build/status",
    "description": "The spcheck succeeded!",
    "context": "Gwalstat/spcheck",
}

pending = {
    "state": "pending",
    "target_url": "https://example.com/build/status",
    "description": "Waiting for the check!",
    "context": "Gwalstat/spcheck",
}

failure = {
    "state": "failure",
    "target_url": "https://gwalstat.herokuapp.com/",
    "description": "TYPOS in your Pull Request found!",
    "context": "Gwalstat/spcheck",
}


async def post_status(gh, event, status):
    """Post a status in reaction to an event."""
    await gh.post(event.data["pull_request"]["statuses_url"], data=status)
