#python-digitalocean
## 

python-digitalocean is a python package that provide easy access to digitalocean.com APIs to manage droplets, images and more.

[![](https://tip4commit.com/projects/897.svg)](https://tip4commit.com/github/koalalorenzo/python-digitalocean)

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

## Links

  * Project Site: [http://projects.setale.me/python-digitalocean](http://projects.setale.me/python-digitalocean)
  * GitHub: [https://github.com/koalalorenzo/python-digitalocean](https://github.com/koalalorenzo/python-digitalocean)
  * PyPi page: [https://pypi.python.org/pypi/python-digitalocean/](https://pypi.python.org/pypi/python-digitalocean/)
  * Author Website: [http://who.is.lorenzo.setale.me/?](http://setale.me/)
  * Author Blog: [http://blog.setale.me/](http://blog.setale.me/)

<script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-10395528-24', 'setale.me');
  ga('send', 'pageview');

</script>
