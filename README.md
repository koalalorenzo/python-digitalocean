<h1 align="center">python-digitalocean</h1>
<p align="center">Easy access to Digital Ocean APIs to deploy droplets, images and more.</p>

<p align="center">
<a href="https://travis-ci.org/koalalorenzo/python-digitalocean"><img src="https://travis-ci.org/koalalorenzo/python-digitalocean.svg" alt="Build Status"></a>
<a href="https://travis-ci.org/koalalorenzo/python-digitalocean"><img src="https://img.shields.io/github/forks/badges/shields.svg?style=social&label=Fork"></a>
<a href="https://travis-ci.org/koalalorenzo/python-digitalocean"><img src="https://img.shields.io/github/stars/badges/shields.svg?style=social&label=Star"></a>
<a href="https://travis-ci.org/koalalorenzo/python-digitalocean"><img src="https://img.shields.io/github/watchers/badges/shields.svg?style=social&label=Watch"></a>
</p>

## Table of Contents

- [How to install](#how-to-install)
- [Features](#Features)
- [Examples](#Examples)
   - [Listing the droplets](#listing-the-droplets)
   - [Listing the droplets by tags](#listing-the-droplets-by-tags)
   - [Add a tag to a droplet](#add-a-tag-to-a-droplet)
   - [Shutdown all droplets](#shutdown-all-droplets)
   - [Creating a Droplet and checking its status](#creating-a-droplet-and-checking-its-status)
   - [Checking the status of the droplet](#checking-the-status-of-the-droplet)
   - [Add SSHKey into DigitalOcean Account](#add-sshkey-into-digitalocean-account)
   - [Creating a new droplet with all your SSH keys](#creating-a-new-droplet-with-all-your-ssh-keys)
   - [Creating a Firewall](#creating-a-firewall)
- [Getting account requests/hour limits status](#getting-account-requests-hour-limits-status)
- [Testing](#testing)
   - [Test using Docker](#test-using-docker)
   - [Testing using pytest manually](#testing-using-pytest-manually)
- [Links](#links)

## How to install

You can install python-digitalocean using **pip**

    pip install -U python-digitalocean

or via sources:

    python setup.py install

**[⬆ back to top](#table-of-contents)**

## Features
python-digitalocean support all the features provided via digitalocean.com APIs, such as:

* Get user's Droplets
* Get user's Images (Snapshot and Backups)
* Get public Images
* Get Droplet's event status
* Create and Remove a Droplet
* Create, Add and Remove Tags from Droplets
* Resize a Droplet
* Shutdown, restart and boot a Droplet
* Power off, power on and "power cycle" a Droplet
* Perform Snapshot
* Enable/Disable automatic Backups
* Restore root password of a Droplet

**[⬆ back to top](#table-of-contents)**

## Examples
### Listing the droplets

This example shows how to list all the active droplets:

```python
import digitalocean
manager = digitalocean.Manager(token="secretspecialuniquesnowflake")
my_droplets = manager.get_all_droplets()
print(my_droplets)
```

**[⬆ back to top](#table-of-contents)**

### Listing the droplets by tags

This example shows how to list all the active droplets:

```python
import digitalocean
manager = digitalocean.Manager(token="secretspecialuniquesnowflake")
my_droplets = manager.get_all_droplets(tag_name="awesome")
print(my_droplets)
```

**[⬆ back to top](#table-of-contents)**

### Add a tag to a droplet

This example shows how to list all the active droplets:

```python
import digitalocean
tag = digitalocean.Tag(token="secretspecialuniquesnowflake", name="tag_name")
tag.create() # create tag if not already created
tag.add_droplets(["DROPLET_ID"])
```

**[⬆ back to top](#table-of-contents)**

### Shutdown all droplets

This example shows how to shutdown all the active droplets:

```python
import digitalocean
manager = digitalocean.Manager(token="secretspecialuniquesnowflake")
my_droplets = manager.get_all_droplets()
for droplet in my_droplets:
    droplet.shutdown()
```

**[⬆ back to top](#table-of-contents)**

### Creating a Droplet and checking its status

This example shows how to create a droplet and how to check its status

```python
import digitalocean
droplet = digitalocean.Droplet(token="secretspecialuniquesnowflake",
                               name='Example',
                               region='nyc2', # New York 2
                               image='ubuntu-14-04-x64', # Ubuntu 14.04 x64
                               size_slug='512mb',  # 512MB
                               backups=True)
droplet.create()
```

**[⬆ back to top](#table-of-contents)**

### Checking the status of the droplet
```python
actions = droplet.get_actions()
for action in actions:
    action.load()
    # Once it shows complete, droplet is up and running
    print action.status
```

**[⬆ back to top](#table-of-contents)**

### Add SSHKey into DigitalOcean Account
```python
from digitalocean import SSHKey

user_ssh_key = open('/home/<$USER>/.ssh/id_rsa.pub').read()
key = SSHKey(token='secretspecialuniquesnowflake',
             name='uniquehostname',
             public_key=user_ssh_key)
key.create()
```

**[⬆ back to top](#table-of-contents)**

### Creating a new droplet with all your SSH keys
```python
manager = digitalocean.Manager(token="secretspecialuniquesnowflake")
keys = manager.get_all_sshkeys()

droplet = digitalocean.Droplet(token="secretspecialuniquesnowflake",
                               name='DropletWithSSHKeys',
                               region='ams3', # Amster
                               image='ubuntu-14-04-x64', # Ubuntu 14.04 x64
                               size_slug='512mb',  # 512MB
                               ssh_keys=keys, #Automatic conversion
                               backups=False)
droplet.create()
```

**[⬆ back to top](#table-of-contents)**

### Creating a Firewall

This example creates a firewall that only accepts inbound tcp traffic on port 80 from a specific load balancer and allows outbout tcp traffic on all ports to all addresses.

```python
from digitalocean import Firewall, InboundRule, OutboundRule, Destinations, Sources

inbound_rule = InboundRule(protocol="tcp", ports="80",
                           sources=Sources(
                               load_balancer_uids=[
                                   "4de7ac8b-495b-4884-9a69-1050c6793cd6"]
                               )
                           )

outbound_rule = OutboundRule(protocol="tcp", ports="all",
                             destinations=Destinations(
                               addresses=[
                                   "0.0.0.0/0",
                                   "::/0"]
                                 )
                             )

firewall = Firewall(token="secretspecialuniquesnowflake",
                    name="new-firewall",
                    inbound_rules=[inbound_rule],
                    outbound_rules=[outbound_rule],
                    droplet_ids=[8043964, 8043972])
firewall.create()
```

**[⬆ back to top](#table-of-contents)**

## Getting account requests/hour limits status
Each request will also include the rate limit information:

```python
import digitalocean
account = digitalocean.Account(token="secretspecialuniquesnowflake").load()
# or
manager = digitalocean.Manager(token="secretspecialuniquesnowflake")
account = manager.get_account()
```
Output:
```text
droplet_limit: 25
email: 'name@domain.me'
email_verified: True
end_point: 'https://api.digitalocean.com/v2/'
floating_ip_limit: 3
ratelimit_limit: '5000'
ratelimit_remaining: '4995'
ratelimit_reset: '1505378973'
status: 'active'
status_message: ''
token:'my_secret_token'
uuid: 'my_id'
```

When using the Manager().get_all.. functions, the rate limit will be stored on the manager object:
 ```python
import digitalocean
manager = digitalocean.Manager(token="secretspecialuniquesnowflake")
domains = manager.get_all_domains()

print(manager.ratelimit_limit) 
```

**[⬆ back to top](#table-of-contents)**

## Testing

### Test using Docker
To test this python-digitalocean you can use [docker](https://www.docker.com) to have a **clean environment automatically**. First you have to build the container by running in your shell on the repository directory:

    docker build -t "pdo-tests" .

Then you can run all the tests (for both python 2 and python 3)

    docker run pdo-tests

**Note**: This will use Ubuntu 14.04 as base and use your repository to run tests. So every time you edit some files, please run these commands to perform tests on your changes.

**[⬆ back to top](#table-of-contents)**

### Testing using pytest manually
Use [pytest](http://pytest.org/) to perform testing. It is recommended to use a dedicated virtualenv to perform tests, using these commands:

    $ virtualenv /tmp/digitalocean_env
    $ source /tmp/digitalocean_env/bin/activate
    $ pip install -r requirements.txt

To run all the tests manually use py.test command:

    $ python -m pytest

**[⬆ back to top](#table-of-contents)**

## Links

  * GitHub: [https://github.com/koalalorenzo/python-digitalocean](https://github.com/koalalorenzo/python-digitalocean)
  * PyPI page: [https://pypi.python.org/pypi/python-digitalocean/](https://pypi.python.org/pypi/python-digitalocean/)
  * Author Website: [http://who.is.lorenzo.setale.me/?](http://setale.me/)
  * Author Blog: [http://blog.setale.me/](http://blog.setale.me/)

**[⬆ back to top](#table-of-contents)**
