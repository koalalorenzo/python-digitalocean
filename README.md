#python-digitalocean
## 

python-digitalocean is a python package that provide easy acces to digitalocean.com APIs to manage droplets, images and more.

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
* Get user's Images ( Snapshot and Backups )
* Get pubblic Images
* Get Droptlet's event status
* Create and Remove a Droplet
* Resize a Droplet
* shutdown, restart and boot a Droplet
* power off, power on and "power cycle" a Droplet
* Perform Snapshot
* Enable/Disable automatic Backups
* Restore root password of a Droplet


## Examples
### Shutdown all droplets

This example shows how to shutdown all the droplets active:

    import digitalocean
    manager = digitalocean.Manager(client_id="ABC", api_key="ABC")
    my_droplets = manager.get_all_droplets()
    for droplet in my_droplets:
        droplet.shutdown()

### Creating a Droplet and checking it's status

This example shows how to create a droplet and how to check it's status

	import digitalocean
	droplet = digitalocean.Droplet(client_id=client_id,
							       api_key=api_key,
							       name = 'Example',
							       region_id=1 #New York,
							       image_id=2676 #Ubuntu 12.04 x64 Server,
							       size_id=66 #512MB,
							       backup_active=False)
	droplet.create()

### Checking the status of the droplet
	events = droplet.get_events()[0]
### Refreshing the event status
    event.load()
    #Once it shows 100, droplet is up and running
    print event.percentage

## Liks

  * Project Site: [http://projects.setale.me/Steroids](http://projects.setale.me/python-digitalocean)
  * GitHub: [https://github.com/koalalorenzo/Steroids](https://github.com/koalalorenzo/python-digitalocean)
  * PyPi page: [https://pypi.python.org/pypi/steroids/](https://pypi.python.org/pypi/python-digitalocean/)
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