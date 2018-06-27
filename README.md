# CalebJ Cogs
#### General, fun and utility modules for [Red-DiscordBot](https://github.com/Cog-Creators/Red-DiscordBot/) v3

[![Patreon](https://img.shields.io/badge/Support-me!-f96854.svg)](https://www.patreon.com/calebj)
[![Donate](https://img.shields.io/badge/Paypal-donate-0070ba.svg)](https://paypal.me/calebrj)
[![discord.py](https://img.shields.io/badge/discord.py-rewrite-blue.svg)](https://github.com/Rapptz/discord.py/tree/rewrite)
[![Red-DiscordBot](https://img.shields.io/badge/Red--DiscordBot-v3-red.svg)](https://github.com/Cog-Creators/Red-DiscordBot/)
[![Support server invite](https://img.shields.io/discord/240154543684321280.svg?colorB=7289DA)](https://discord.gg/2DacSZ7)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-6f42c1.svg)](http://makeapullrequest.com)

This repo contains cogs I've written, as well as those I've modified and republished when a PR was either unwanted or too drastic of a change from the original cog's scope.

## Table of Contents
* [Installation](#installation)
* [Support and Contact](#support-and-contact)
* [Cog Descriptions](#cog-descriptions)
* [Frequently Asked Questions](#frequently-asked-questions)
* [Contributing](#contributing)
* [Automatic Error Reporting](#automatic-error-reporting)
* [Usage Statistics and Privacy Policy](#usage-statistics-and-privacy-policy)
* [License and Copyright](#license-and-copyright)

## Installation
Type the following commands into any channel your bot can see, or in a direct message to it.

**1. Adding the repo** - replace `[p]` with your bot's prefix:
```
[p]repo add calebj-cogs https://github.com/calebj/calebj-cogs v3/master
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
No cogs have been added yet.

## Frequently Asked Questions
### Is this section empty?
No.

## Contributing
Please submit patches to code or documentation as GitHub pull requests!

Contributions must be licensed under the GNU GPLv3 or compatible license. The contributor retains the copyright. I won't accept new cogs unless I want to support them.

## Automatic Error Reporting
In order to become aware of bugs and unanticipated edge cases quickly and without having to rely on user reports, I wrote a module which can listen for exceptions in any of my cogs and report them to my [Sentry](https://sentry.io/) account. This module can be enabled, disabled, and un/loaded like any other cog. Loading it is considered explicitly opting in to automatically sending exception reports.

I've done my best to configure Sentry to ignore any personal data but, depending on the nature of the error, reports can contain information about (for example) cog file paths, where a command was run, and with what parameters. I'm the only one with access to the account, and the reports are used strictly for fixing bugs in my code.

## Usage Statistics and Privacy Policy
To help get a better idea of how my cogs are used, I wrote a module to collect and send me data about which cogs are loaded, which commands are run, and some other cog-specific parameters. This module can be enabled, disabled, and un/loaded like any other cog. Loading it is considered explicitly opting in to automatically sending this information.

I use [Matomo](https://matomo.org/) on my webserver to record events, and don't share any users' data with anyone else. All user IDs are hashed before sending to make them unique without being able to identify the users (or bots) in question, and IP addresses are stripped. Only "Pseudonymous Data" is collected or stored, and since none of it is for commercial use, I am not obligated to respond to GDPR requests. More information can be found in my [privacy policy](PRIVACY.md).

## License and Copyright
All code in this repository is licensed under the [GNU General Public License version 3](LICENSE).

Copyright (c) 2016-2018 Caleb Johnson, contributors and original authors.
