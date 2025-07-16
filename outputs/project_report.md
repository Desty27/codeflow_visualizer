# Project Report: Holehe

## Overview
Holehe is a Python-based tool designed to check if an email is used on various websites such as Twitter, Instagram, and Snapchat. It retrieves information from sites with a forgotten password function. The project is structured into multiple modules, each targeting different categories of websites.

## Structure
The project is organized into several directories and modules:
- **Core Module**: Contains the main functionality and entry point of the application.
- **Instruments Module**: Provides utility classes for asynchronous operations.
- **Local User Agent Module**: Manages user agent strings for HTTP requests.
- **Modules Directory**: Contains submodules for different categories like CMS, CRM, crowdfunding, forums, jobs, learning, mails, media, medical, music, OSINT, payment, porn, productivity, products, programming, real estate, shopping, social media, software, sport, and transport.

## Dependencies
Holehe relies on several Python packages:
- `termcolor`
- `bs4`
- `httpx`
- `trio`
- `tqdm`
- `colorama`

## Installation
The project can be installed using the `setup.py` script, which utilizes `setuptools` to manage package dependencies and installation.

## Usage
Holehe can be executed from the command line using the entry point defined in `setup.py`. It provides a console script `holehe` that invokes the main function in the core module.

## License
Holehe is licensed under the GNU General Public License v3 (GPLv3).

## Architecture Diagrams
### High-Level Flow
![](outputs\high_level_flowchart.svg)

### Code-Level Flow
![](outputs\code_level_flowchart.svg)