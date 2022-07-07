# Overseer - The easy wifi auditor
<p align="center">
  <img src="https://user-images.githubusercontent.com/55766197/177827198-6da8a6ec-4798-498e-a60b-67dfe7b9de77.png" width=35% height=35%>
</p>

Overseer is a wifi auditing tool that is designed to help small businesses perform a security check of their wireless network. With a graphical interface, automated attacks and automatic report generation, this tool aims to reduce the complexity and knowledge required to perform a wifi audit so that anyone outside the world of cybersecurity can check the security state of their wireless network.

## Requirements

| Tool        | Version   |  100% required  |
| -------     | ---       | ---             |
| Python      | >=3.7     | Yes             |
| Aircrack-ng | >=1.6     | Yes             |
| Bully       | >=1.4     | No              |
| DNSChef     | >=0.4     | No              |
| tshark      | >=3.6.2   | No              |
| lighttpd    | >=1.4.64  | No              |
| john (jumbo)| >=1.9.0   | No              |
| macchanger  | >=1.7.0   | No              |

## Installation

Clone this repository

```
git clone https://github.com/Dukke0/Overseer
```
Install all previous requirements as well as the following python modules

- pandas: ```pip install pandas```
- sv_ttk: ```pip install sv-ttk``` Source: https://github.com/rdbende/Sun-Valley-ttk-theme

## Features

### Attacks

- Deauthentication (Active & Passive)
- Dictionary password crack
- WPS Pixie Dust
- WPS Brute Force
- Evil twin (Captive Portal)

### Tools

- Dictionary generator: Generate a dictionary for the dictionary password attack with keywords.
- MAC Changer: Change your mac address randomly or specify one to avoid white/black lists.
- Network scan.

## :warning:	Disclaimer :warning:	

Overseer should be used for authorized penetration testing and/or nonprofit educational purposes only. Any misuse of this software will not be the responsibility of the author or of any other collaborator.

:no_entry:	**Use it at your own networks and/or with the network owner's permission.** :no_entry:

## About

This project was created for my final degree project. If you intend to use this software for actual wifi audits, please note that this software lacks a lot of features needed to fully test your network and has not been tested with users other than myself.
