# Gwalstat

🤖 A bot for checking pull requests spelling.


## Deployment
### Running on Heroku

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/)

1. Create Heroku project
2. Set the `GH_AUTH` and the environment variable to the GitHub oauth
   token to be used by the bot
3. Set up the Heroku project to get the code for the bot

### Adding to a GitHub repository (Python-specific instructions)
1. Add the appropriate labels (`TYPO`, `TYPOS Found in your pull request`, `#d73a4a`)
2. Add the webhook
    1. Add the URL
    2. Send `application/json` (the default)
    3. Add the secret
    4. Specify events to be `pull request` only (default is `push` which is unnecessary)

# Demo

[Example](https://github.com/krnick/Gwalstat-test/pull/1)


* **Labeled from Bot**

![](https://i.imgur.com/pcnZ6Ah.png)

* **Reply from Bot**

![](https://i.imgur.com/SPFIJia.png)

* **Status check from Bot**

![](https://i.imgur.com/omhLmPy.png)

* **Web View**

![](https://i.imgur.com/vDklO8B.png)



## *Aside*: where does the name come from?
Gurhyr Gwalstat, to go upon this quest, for thou knowest all languages, and art familiar with those of the birds and the beasts.
