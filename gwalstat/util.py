status_check = {
    "state": "success",
    "target_url": "https://example.com/build/status",
    "description": "The spcheck succeeded!",
    "context": "JunWei-Bot/spcheck",
}

pending = {
    "state": "pending",
    "target_url": "https://example.com/build/status",
    "description": "Waiting for the check!",
    "context": "JunWei-Bot/spcheck",
}



async def post_status(gh, event, status):
    """Post a status in reaction to an event."""
    await gh.post(event.data["pull_request"]["statuses_url"], data=status)
