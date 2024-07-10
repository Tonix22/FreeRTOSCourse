# Doorstop Setup and Usage Guide

Doorstop is an effective tool for managing requirements directly within your version control system, 
especially useful when integrated with Git. Below are detailed steps for installation and basic usage.

## Installation

### Step 1: Install Python

Ensure Python is installed on your system. Doorstop requires Python 3.

### Step 2: Install Doorstop

Install Doorstop using pip, Python’s package installer:

```bash
pip install doorstop
doorstop create REQ ./reqs
doorstop add REQ
```
In the editor, write the requirement:

```bash
doorstop publish all
```
Generate an HTML report of your requirements:

```bash
doorstop publish all path/to/output.html
```