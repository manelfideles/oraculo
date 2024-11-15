# Oraculo
This bot sends Priberam's word of the day to a designated Slack channel. 
It's meant to be added to a Slack server.

# Requirements
- Docker
- A Slack account and a server to add the bot to

# Setup
To set up a Slack app:

0. You should be logged in to Slack
1. Go to https://api.slack.com/apps
2. Click "_Create New App_" > "_From scratch_"
3. Fill out the form with the app name and a workspace
4. Go to "_Incoming Webhooks_", toggle them on, and hit "_Add New Webhook to Workspace_"
5. Select a channel to post the bot messages to
6. You'll be redirected back to the "_Incoming Webhooks_". Copy the incoming webhook link.

To set up the bot `.env` file:

0. Rename the `.env.example` file to `.env`
1. Paste the incoming webhook link you copied from the previous steps into the `SLACK_INCOMING_WEBHOOK_URL` field, and you're good to go

# Execution

Run `docker compose up -d` in the root dir of the project.

If you want to program the bot to run everyday at a specific time, you can look into either:

**A.** Using a cronjob in your host system, on-prem, which is free;

or

**B.** Using an AWS lambda function (or similar) to run the bot on the cloud, which will cost _some_ money.