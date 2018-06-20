# CalebJ Cogs
#### General, fun and utility modules for [Red-DiscordBot](https://github.com/Cog-Creators/Red-DiscordBot/)
[![Patreon](https://img.shields.io/badge/Support-me!-orange.svg)](https://www.patreon.com/calebj) [![Donate](https://img.shields.io/badge/Paypal-donate-blue.svg)](https://paypal.me/calebrj) [![discord.py](https://img.shields.io/badge/discord-py-blue.svg)](https://github.com/Rapptz/discord.py) [![Red-DiscordBot](https://img.shields.io/badge/red-bot-red.svg)](https://github.com/Cog-Creators/Red-DiscordBot/) [![Support server invite](https://img.shields.io/discord/240154543684321280.svg)](https://discord.gg/2DacSZ7) [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

This repo contains cogs I've written, as well as those I've modified and republished when a PR was either unwanted or too drastic of a change from the original cog's scope.

## Table of Contents
* [Installation](#installation)
* [Support and Contact](#support-and-contact)
* [Cog Descriptions](#cog-descriptions)
* [Frequently Asked Questions](#frequently-asked-questions)
  * [What does activitylog do?](#what-does-activitylog-do)
  * [How do I use embedwiz?](#how-do-i-use-embedwiz)
  * [How do I use recensor?](#how-do-i-use-recensor)
  * [How do I use scheduler?](#how-do-i-use-scheduler)
  * [How do I use watchdog?](#how-do-i-use-watchdog)
  * [How do I use xorole?](#how-do-i-use-xorole)
* [Contributing](#contributing)
* [Analytics and Privacy Policy](#analytics-and-privacy-policy)
* [License and Copyright](#license-and-copyright)

## Installation
Type the following commands into any channel your bot can see, or in a direct message to it.

**1. Adding the repo** - replace `[p]` with your bot's prefix:
```
[p]cog repo add calebj-cogs https://github.com/calebj/calebj-cogs
```

**2. Installing a cog** - replace `[COG_NAME]` with the name of the cog you want:
```
[p]cog install calebj-cogs [COG_NAME]
```

## Support and Contact
If you have questions or need support for any of my cogs, please ask in my [Red Cog support server](https://discord.gg/2DacSZ7) channel (#support_calebj). I may ask you to open a GitHub issue in this repo if your fix or request isn't a quick one.

If you want to contact me directly, I am **@calebj#0001** on Discord, and my email is **me@calebj.io**.

If my cogs have made your life easier, consider supporting me through [PayPal](https://paypal.me/calebrj) or [becoming a patron](https://www.patreon.com/calebj). I also take cog commissions, which can either be public (added to this repo) or private (only for you).

## Cog Descriptions
* activitylog: Log messages, attachments, and server changes to disk. See [below](#what-does-activitylog-do).
* customgcom: Bot-wide custom commands. Only the bot owner can add/remove them.
* datadog: Publish various metrics and events to a local statsd instance.
* description: Change the header of Red's [p]help command.
* dice: Wraps the python-dice library. Command is `[p]dice <expression>`.
* duel: Procedurally generated duel with a flexible lexicon system.
* embedwiz: A simple tool to generate and post custom embeds.
* galias: Bot-wide command aliases. Only the bot owner can add/remove them.
* gallery: Automatically clean up comments in content-focused channels.
* punish: Timed text and voice mute with evasion protection.
* purgepins: Delete pin notification messages after a per-channel interval.
* recensor: Create inclusive or exclusive regex filters per channel or server.
* scheduler: Squid's [scheduler cog][squid_scheduler], with enhancements.
* serverquotes: Store and recall memorable quotes for your server.
* sinfo: Simple text dump of server and channel information.
* watchdog: Helps systemd know when your bot is functioning. See [below](#how-do-i-use-watchdog).
* xorole: Self-role functionality with single-membership role sets.
* zalgo: H͕̭͒̈́E̡̩͋͐ C̺̻̉O̟͋M̞̐Ę͒ͅS̬̣̍́.

[squid_scheduler]: https://github.com/tekulvw/Squid-Plugins/blob/master/scheduler/scheduler.py

## Frequently Asked Questions
### What does activitylog do?
This cog saves messages and DMs, attachments, and updates to server settings __to log files in your bot's data folder__. If you want a cog that posts events in a channel, use [Grenzpolizei](http://cogs.red/cogs/PaddoInWonderland/PaddoCogs/grenzpolizei/) by [PaddoInWonderland](https://github.com/PaddoInWonderland).

There is no support for uploading logfiles yet, though it is planned. Logging of embed contents and posting events in a channel are NOT planned features.

Activitylog can record the following events:
* Channel messages (per-channel): `logset channel {on|off} [#channel-name]`
  * Includes edits and deletions
* Server events (per-server): `logset events {on|off}`
  * Member changes: nickname, username, roles, join/leave, ban, kick
  * Server changes: name, region, owner, icon
  * Channel changes: create, delete, name, position, topic, permissions
  * Role changes: create, delete, permissions, name, color, hoist, mentionable, rank
* Server override (per-server): `logset server {on|off}`
  * If this is `on`, all channels and server events are logged.
* Direct messages: `logset dm {on|off}`
  * Also includes edits and deletions
* Message attachments: `logset attachments {on|off}`
* Default setting: `logset default {on|off}`
  * If you haven't set an option on or off, this default is used.
  * Server override, global override, and attachments don't use this.
* Global override: `logset everything {on|off}`
  * If this is `on`, the bot will log everything.
  * Attachment downloading is still its own setting.

Note: The version of discord.py that Red v2 is based on doesn't have a way to record audit logs, so there's no way to record which member made a particular change.

### How do I use embedwiz?
Embedwiz is a fairly simply cog.

To build an embed, specify the following parameters seperated by a semicolon (`;`):
* Title: to make a link, put `[Title text](title url)`
* Color: "none" (default), #ABC123, 0xABC123, "random", "black" or any member of [`discord.Colour`](https://discordpy.readthedocs.io/en/async/api.html#discord.Colour)
* Footer text
* Footer icon URL
* Embed image URL
* Thumbnail image URL
* Embed body text: or "prompt" to make the next message you post the embed body.

All fields can be left blank. If Discord doesn't like a title link or image URL, it may throw an error.

By default, author information is included in the embed's header so that it can be edited later using the `embedwiz edit` command. To omit this information, put `-noauthor` in front of the between the command and its parameters. Keep in mind that you won't be able to edit it later if you do this.

An example embed specification:
```
[p]embedwiz [Test Embed](https://github.com/calebj/calebj-cogs/);
#2196F3;
Created by embedwiz;
https://calebj.io/images/l3icon.png;
https://upload.wikimedia.org/wikipedia/commons/b/bf/Test_card.png;
https://www.python.org/static/community_logos/python-powered-h-140x182.png;
Example embed body text. Full **markdown** __is__ *supported*. ~~Nothing to see here.~~

Newlines also work.

And now for [something completely different](https://www.youtube.com/watch?v=ltmMJntSfQI).
```

Which looks like this:

![Test embed](embedwiz/test.png?raw=true)


Only mods and those with the manage_messages permission can use these subcommands:
* `embedwiz channel [channel] [embed_spec ...]` : posts the embed in the channel `channel` instead.
* `embedwiz delete [embed_spec ...]` : deletes the command message (and prompt message, if used).
* `embedwiz edit [channel] [message_id] [embed_spec ...]` : edits **any** existing embed.

### How do I use recensor?
The recensor cog uses Python's [`re.match()`](https://docs.python.org/3/library/re.html#re.match) to decide which messages to filter. An introduction to Python regex can be found [here](https://docs.python.org/3/howto/regex.html#regex-howto), and the full syntax is [here](https://docs.python.org/3/library/re.html#regular-expression-syntax). Unlike [`re.search()`](https://docs.python.org/3/library/re.html#re.search), the pattern matching is anchored to the beginning of the message text. If you want a pattern to match anywhere in the message, you must put `.*` at the beginning of the pattern.

The bot's owner, administrators and moderators are always immune from the filter.

**Inclusive** mode means that messages which match the pattern will be deleted, whereas **exclusive** mode means that messages which do __not__ match the pattern will be deleted. Naturally, only one exclusive mode filter can be set at a time. Also, you cannot set an exclusive filter for a channel if one is set for the server, and vice-versa.

### How do I use scheduler?
The scheduler cog supports a number of different functions. All users can schedule a command to run in the future ("one-shot"), but only moderators and members with the "manage messages" permission can add or manage repeating commands. Additionally, only one of the same command can be scheduled at a time for each member. To schedule it again, they must cancel the one they scheduled before.

Time interval can be any combination of numbers and units, e.g. 5m30s, or a long format such as "5 minutes and 30 seconds". Valid units are `s`, `m`, `h`, `d`, `w`. For all subcommands that don't have the time interval as the last argument, intervals containing spaces must be in double quotes.

Timestamp can be an ISO8601 timestamp (e.g. 2017-12-11T01:15:03.449371-0500), UNIX timestamp (e.g. 1512972903.449371) or "now".

Regular members can use these subcommands to `[p]scheduler`:
* `add [time_interval] [command ...]`: schedules the specified command to run in `time_interval`.
  * `time_interval` must be in double quotes if it contains spaces.
* `add_timelast [command] [time_interval ...]`: `add`, but `time_interval` is the last parameter.
  * `command` must be in double quotes if it contains spaces.
  * Useful for creating command aliases that take a variable time.
* `add_twostage [command_1] [time_interval] [command_2 ...]`: runs `command_1`, schedules `command_2`.
  * `command_1` and `time_interval` must be in double quotes if they contain spaces.
* `add_twostage_timelast [command_1] [command_2] [time_interval ...]`: `add_twostage`, but interval is last.
  * `command_1` and `command_2` must be in double quotes if they contain spaces.
  * Useful for creating command aliases that take a variable time.
* `cancel [command ...]`: cancels a scheduled command. You can only cancel your scheduled commands.

Moderators and members with the "manage messages" permission can run these subcommands:
* `repeat [name] [time_interval] [command ...]`: repeats the given command every `time_interval`.
* `repeat_from [name] [start] [interval] [command ...]`: `repeat`, starting at timestamp `start`.
* `repeat_in name start_in interval command ...`: `repeat`, starting in the interval `start_in`.
* `remove [name]`: removes the repeating command named `name` and cancels the next scheduled run.
* `list`: lists the names of all scheduled commands (TODO: show channel and command).
  * Also shows scheduled oneshots. Cancel them by using `remove` with the full `UID-name`.

An example application of twostage is to have a self-assigned role (using selfrole from the [Squid Admin cog](http://cogs.red/cogs/tekulvw/Squid-Plugins/admin/)) that is added and then removed after a custom delay, using a single alias.

### How do I use watchdog?
First of all, if you aren't running your bot on a Linux machine with systemd, or another service manager that listens for watchdog messages in the same way, **this cog won't do anything for you**. Sorry.

With that out of the way, some important information: **this cog doesn't actually restart your bot for you**. Systemd has to do that. All the cog does is periodically send systemd messages that everything is working.

The service has to be configured to expect these messages by adding:

```
# Discord hearbeat is about every 40 seconds. Using 90 to be safe from false restarts.
WatchdogSec=90
```

to your service unit. As long as the environment variables from systemd are
passed through to the bot (i.e. you aren't using the launcher), the cog will
know where to send the OK messages.

If you are new to systemd, you can use the provided [`red@.service`](watchdog/red@.service) unit template. It assumes that:
1. there exists a user and group named `red` for your bot to run under,
2. the bot files are located in `/srv/red/<some name>/`,
3. all files in 2 are owned by user `red` and group `red`, and
4. you enable and start the service as `red@<some name>`

Assuming your bot is set up (i.e. token set, etc) and is located in a folder named `Red-DiscordBot`; and that `red@.service` is in `/etc/systemd/system/`:
base
If your bot's nickname is Squid, you would do the following (as root):
```sh
# Create the base folder, if it doesn't exist
mkdir -p /srv/red/

# Create the red user if it doesn't exist
id -u red 2>/dev/null || useradd red -r -U -d /srv/red/

# Move the bot's files to a subdirectory of /srv/red/
mv Red-DiscordBot /srv/red/squid

# Change the ownership to the bot user
chown red:red /srv/red -R

# Enable and start the bot
systemctl enable --now red@squid
```

After which your bot should now be running (check with `systemctl status red@squid`).

### How do I use xorole?
Xorole was created out of the need for "role sets", which are groups of roles that a member should only have one of at a time. Thus the name, which is short for "exclusive-or roles". Examples use cases include self-assignable color roles, timezone or region roles, and teams (e.g. Ingress or Pokemon Go).

The following user commands are available as subcommands of `xorole`:
* `list`: lists available rolesets and the roles in them.
* `add [role]`: assigns a user a role, removing any others in the same set.
* `toggle [roleset]`: toggle a role on or off, or between a two-role set.
* `remove [role|roleset]`: removes the `role` or their role in `roleset` from the user.

For a roleset of size one, `xorole toggle` will add the role if they don't have it, or remove it if they do. For a roleset of size two, it will toggle between the two roles (one must already be assigned). For other sizes, the command will error.

Calling `[p]xorole [role]` without a valid subcommand is the same as calling `[p]xorole add [role]`.

The cog is configured using the following subcommands of `xoroleset`:
* `addroleset [name]`: creates a new roleset.
* `rmroleset [name]`: deletes a roleset.
* `renroleset [old_name] [new_name]`: renames a roleset.
* `addroles [roleset] [role,[role,...]`: Adds a comma-seperated list of roles (or IDs) to a roleset.
* `rmroles [roleset] [role,[role,...]`: Removes a comma-seperated list of roles (or IDs) from a roleset.
* `audit`: Lists members that have more than one role in a xorole roleset.

## Contributing
Please submit patches to code or documentation as GitHub pull requests!

Contributions must be licensed under the GNU GPLv3. The contributor retains the copyright. I won't accept new cogs unless I want to support them.

## Analytics and Privacy Policy
Most of the cogs in this repo use a custom [usage reporting tool](_analytics/analytics_core.py) which, upon being loaded, checks to see if you have opted in before sending anything. I use [Matomo](https://matomo.org/) on my webserver to record events, and do not share the data with anyone else. All user IDs are hashed before sending to make them unique without being able to identify the users in question. More information can be found in my [privacy policy](PRIVACY.md).

The gibberish seen at the top of most of the cogs is actually a compressed form of this analytics agent generated by [pyminifier](https://github.com/liftoff/pyminifier) and [this script](_analytics/build_analytics.sh), then updated by [this script](_analytics/substitute_analytics.sh). I included these scripts to allow others to easily verify that the output is identical.

## License and Copyright
Except for [scheduler](scheduler/), which is licensed under the [MIT license](scheduler/LICENSE), all code in this repository is licensed under the [GNU General Public License version 3](LICENSE).

Copyright (c) 2016-2018 Caleb Johnson, contributors and original authors.
