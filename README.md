# CalebJ-Cogs
[![Patreon](https://img.shields.io/badge/Support-me!-orange.svg)](https://www.patreon.com/calebj) [![Donate](https://img.shields.io/badge/Paypal-donate-blue.svg)](https://paypal.me/calebrj)

This repo contains modules for [Twentysix's Red-DiscordBot](https://github.com/Twentysix26/Red-DiscordBot)

If you have questions or would like some support for these cogs, please head over to the **#coding** channel in Twentysix's [Red - Discord Bot](https://discordapp.com/invite/0k4npTwMvTpv9wrh) discord server.


## Description of cogs
* activitylog: Log messages, attachments, and server changes to disk. See below.
* customgcom: Custom global commands.
* datadog: Publish various metrics and events to a local statsd instance.
* description: Change the header of Red's [p]help command.
* dice: Wraps the python-dice library. Command is `[p]rd <expression>`.
* duel: Procedurally generated duel with a flexible lexicon system.
* galias: Bot-wide command aliases. Only owner can add/remove them.
* gallery: clean up comments from channels focused on embedded content.
* punish: Zero-configuration timed mute with evasion protection.
* purgepins: Delete pin notification messages after a per-channel interval. 
* recensor: Create inclusive or exclusive regex filters per channel or server.
* serverquotes: Store and recall memorable quotes for your server.
* sinfo: Simple text dump of server and channel information.
* watchdog: Helps systemd restart your bot if it goes offline. See below.
* xorole: Self-role functionality with single-membership role sets.
* zalgo: H͕̭͒̈́E̡̩͋͐ C̺̻̉O̟͋M̞̐Ę͒ͅS̬̣̍́.


## What does activitylog do?
This cog saves messages and DMs, attachments, and updates to server settings
to logfiles in your bot's data folder. There is no support for uploading
logfiles yet, though it is planned. Logging of embed contents and posting
events in a channel are not planned features.

* Channel messages (per-channel): `logset channel {on|off} [#channel-name]`
  * Includes edits and deletions
* Server events\* (per-server): `logset events {on|off}`
  * Member changes: nickname, username, roles, join/leave, ban, kick
  * Server changes: name, region, owner, icon
  * Channel changes: create, delete, name, position, topic
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

\* note: Currently, changes in channel permission overrides (role-specific
allow/deny) are not logged. Furthermore, discord currently does not have a
way to tell *who* changed something, only that it changed.


## How do I use watchdog?  
First of all, if you aren't running your bot on a Linux machine with systemd,
you can't use this cog.  
It just won't do anything for you. No exceptions.  

With that out of the way, some important information:  
This cog doesn't actually restart your bot for you. Systemd has to do that.
All the cog does is periodically send systemd messages that everything is working.
The service has to be configured to use these messages by adding:

```
# Discord hearbeat is about every 40 seconds. Using 90 to be safe from false restarts.
WatchdogSec=90
```

to your service unit. As long as the environment variables from systemd are
passed through to the bot (i.e. you aren't using a launcher), the cog will
know where to send the OK messages.

If you are new to systemd, you can use the provided 
[`red@.service`](watchdog/red@.service) unit template.
It assumes that:
1. there exists a user and group named `red` for your bot to run under
2. the bot files are located in `/srv/red/<some name>/`
3. all files in 2 are owned by user `red` and group `red`
4. you enable and start the service as `red@<some name>`

Assuming your bot is set up (i.e. token set, etc) and is located in a folder
named `Red-DiscordBot`; and that `red@.service` is in `/etc/systemd/system/`:  
If your bot's nickname is Squid, you would do the following (as root):
```sh
# mkdir -p /srv/red/
# id -u red 2>/dev/null || useradd red -r -U -d /srv/red/
# mv Red-DiscordBot /srv/red/squid
# chown red:red /srv/red -R
# systemctl enable --now red@squid
```

After which your bot should now be running (check with `systemctl status red@squid`).


If my cogs have made your life easier, consider donating through [paypal](https://paypal.me/calebrj) or [becoming a patron](https://www.patreon.com/calebj).
