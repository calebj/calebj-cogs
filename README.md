# CalebJ-Cogs
[![Patreon](https://img.shields.io/badge/Support-me!-orange.svg)](https://www.patreon.com/calebj) [![Donate](https://img.shields.io/badge/Paypal-donate-blue.svg)](https://paypal.me/calebrj)

This repo contains modules for [Twentysix's Red-DiscordBot](https://github.com/Twentysix26/Red-DiscordBot)

If you have questions or would like some support for these cogs, please head over to the **#coding** channel in Twentysix's [Red - Discord Bot](https://discordapp.com/invite/0k4npTwMvTpv9wrh) discord server.


## Description of cogs
* activitylog: Log DM messages, server changes, and even attachments. See below.
* ~~bartender~~: Removed because changes were merged into [Mash's repo](https://github.com/Canule/Mash-Cogs/).
* duel: Procedurally generated duel with a flexible lexicon system.
* galias: Bot-wide command aliases. Only owner can add/remove them.
* mute: Adds a Mute role and removes it after a prescribed time.
* punish: Zero-configuration timed mute with evasion protection.
* purgepins: Delete pin notification messages after a per-channel interval. 
* recensor: Create inclusive or exclusive regex filters per channel or server.
* serverquotes: Store and recall memorable quotes for your server.
* watchdog: Interfaces with systemd watchdog to restart bot if it goes offline.
* zalgo: HE COMES.


## What does activitylog record?\*
* Channel messages (per-channel): `logset channel {on|off} [#channel-name]`
  * Includes edits and deletions
* Server events (per-server): `logset events {on|off}`
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
  * If this is `on`, the bot will log everything, period.

\* note: Currently, changes in channel permission overrides (role-specific allow/deny) are not logged. Furthermore, discord currently does not have a way to tell *who* changed something, only that it changed.

If my cogs have made your life easier, consider donating through [paypal](https://paypal.me/calebrj) or [becoming a patron](https://www.patreon.com/calebj).
