# Oraculo
This bot sends Priberam's word of the day to a designated Slack channel. 
It's meant to be added to a Slack server.

# Requirements
- Docker
- A Slack account and a server to add the bot to
- [_Optional_] A home server to self-host the bot

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

0. Rename the `.env.example` file to `.env`. You can run `cp .env.example .env`.
1. Open the `.env` file and paste the incoming webhook link you've copied from the previous steps into the `SLACK_INCOMING_WEBHOOK_URL` field.

# Execution

Run `docker compose up -d` in the root dir of the project.

If you want to program the bot to run everyday at a specific time, you can look into either:

**A.** Using an AWS lambda function (or similar) to run the bot on the cloud, which will cost _some_ money.

or

**B.** Using a cronjob in your host system, on-prem, which is free;

I opted for the latter. Inside the `scripts` folder, you'll find a `run.sh` file that allows you to self-host the bot, on a home server or similar.
I chose to set up a cronjob to run the container periodically, but you may do as you please.

If you too opt for this approach, consider the following steps:
1. From the root dir of this project, run `cp scripts/run.sh usr/local/bin/run-oraculo.sh`
2. Run `sudo crontab -e`, which will open an editor window for you to add your desired cron expression.
3. I appended `30 10 * * 1-5 /usr/local/bin/run-oraculo.sh` to the file
4. Save the contents of the file and exit. It'll now send the word of the day to the configured Slack channel every weekday at 10:30am.

# Troubleshooting
Check if the cronjob script is functioning properly by running:

`sh usr/local/bin/run-oraculo.sh`