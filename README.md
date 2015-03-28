#python-digitalocean
##

This library provides easy access to Digital Ocean APIs to deploy droplets, images and more.

[![](https://travis-ci.org/koalalorenzo/python-digitalocean.svg)](https://travis-ci.org/koalalorenzo/python-digitalocean)

<div align="center">

<iframe src="http://ghbtns.com/github-btn.html?user=koalalorenzo&repo=python-digitalocean&type=follow&size=large&count=true"
  allowtransparency="true" frameborder="0" scrolling="0" width="220" height="30"></iframe>

<iframe src="http://ghbtns.com/github-btn.html?user=koalalorenzo&repo=python-digitalocean&type=watch&size=large&count=true"
  allowtransparency="true" frameborder="0" scrolling="0" width="150" height="30"></iframe>

</div>

## How to install

You can install python-digitalocean using **pip**

    pip install -U python-digitalocean

or via sources:

    python setup.py install

## Features
python-digitalocean support all the features provided via digitalocean.com APIs, such as:

* Get user's Droplets
* Get user's Images (Snapshot and Backups)
* Get public Images
* Get Droplet's event status
* Create and Remove a Droplet
* Resize a Droplet
* Shutdown, restart and boot a Droplet
* Power off, power on and "power cycle" a Droplet
* Perform Snapshot
* Enable/Disable automatic Backups
* Restore root password of a Droplet


## Examples
### Shutdown all droplets

This example shows how to shutdown all the active droplets:

```python
import digitalocean
manager = digitalocean.Manager(token="secretspecialuniquesnowflake")
my_droplets = manager.get_all_droplets()
for droplet in my_droplets:
    droplet.shutdown()
```

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

### Checking the status of the droplet
```python
actions = droplet.get_actions()
for action in actions:
    action.load()
    # Once it shows complete, droplet is up and running
    print action.status
```

## Testing

### Test using Docker
To test this python-digitalocean you can use [docker](https://www.docker.com) to have a **clean environment automatically**. First you have to build the container by running in your shell on the repository directory:

    docker build -t "pdo-tests" .

Then you can run all the tests (for both python 2 and python 3)

    docker run pdo-tests

**Note**: This will use Ubuntu 14.04 as base and use your repository to run tests. So every time you edit some files, please run these commands to perform tests on your changes.

### Testing using pytest manually
Use [pytest](http://pytest.org/) to perform testing. It is recommended to use a dedicated virtualenv to perform tests, using these commands:

    $ virtualenv /tmp/digitalocean_env
    $ source /tmp/digitalocean_env/bin/activate
    $ pip install -r requirements.txt

To run all the tests manually use py.test command:

    $ py.test


## Links

  * GitHub: [https://github.com/koalalorenzo/python-digitalocean](https://github.com/koalalorenzo/python-digitalocean)
  * PyPi page: [https://pypi.python.org/pypi/python-digitalocean/](https://pypi.python.org/pypi/python-digitalocean/)
  * Author Website: [http://who.is.lorenzo.setale.me/?](http://setale.me/)
  * Author Blog: [http://blog.setale.me/](http://blog.setale.me/)
