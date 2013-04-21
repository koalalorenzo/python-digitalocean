# python-digitalocean

python-digitalocean is a python package that provide easy acces to digitalocean.com APIs to manage droplets, images and more.

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


## Example: Shutdown all droplets

This example shows how to shutdown all the droplets active:

    import digitalocean
    manager = digitalocean.Manager(client_id="ABC", api_key="ABC")
    my_droplets = manager.get_all_droplets()
    for droplet in my_droplets:
        droplet.shutdown()

## Example: Creating a Droplet and checking it's status

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

	#Checking the status of the droplet
	events = droplet.get_events()[0]
	#Refreshing the event status
    event.load()
    #Once it shows 100, droplet is up and running
    print event.percentage





