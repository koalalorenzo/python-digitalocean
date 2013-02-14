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

