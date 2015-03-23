# python-digitalocean backup

### Features
* **DROPLET BACKUP!!! (rsync and snapshot a droplet)**

--

### Example cronjob:

```sh
# DigitalOcean backup script
0 * * * * /usr/bin/python /Users/username/bin/backup.py
```

--

### Example backup script:

```python

import digitalocean
"""
Options:
    • ssh_user       - the user account that connects to the droplet via ssh. DEFAULT: "root" 
    • ssh_key        - the local ssh key file (~/.ssh/rsakey). MUST USE KEY BASED AUTH FOR SSH
    • backup_dir     - the local droplet backup directory. DEFAULT: $HOME/Droplets
    • remote_dirs    - droplet directories to rsync. DEFAULT: None
    • excludes       - exclude keywords from rsync. DEFAULT: None
    • snapshot_hour  - the hour of day to shutdown and snapshot the droplet. DEFAULT: 25
    • snapshot_count - number of snapshots to keep. DEFAULT: 1000
    • use_ip         - use droplet ip to connect instead of droplet.name. DEFAULT: False
"""

    options = {
      "dev.example.com": {
        "ssh_user"        : "root",
        "ssh_key"         : "rsakey",
        "remote_dirs"     : [
                              "/root", "/home", "/etc", "/src",
                              "/usr/local", "/usr/share", "/usr/bin",
                              "/usr/sbin", "/var/backups", "/var/mail",
                              "/var/log", "/var/www",
                            ],
        "excludes"        : [ "man3", ],
        "snapshot_hour"   : 5,
        "snapshot_count"  : 5,
        "use_ip"          : True,
      },
      "production.example.com": {
        "ssh_user"        : "root",
        "ssh_key"         : "ssh_key",
        "backup_dir"      : "/Users/username/Droplets",
        "remote_dirs"     : [ "/var/www", "/etc/nginx" ],
        "excludes"        : [ "wpcf7_captcha", "cache" ],
        "use_ip"          : False,
        "snapshot_hour"   : 3,
        "snapshot_count"  : 7,
      }
    }

    manager = digitalocean.Manager( token="YOUR_TOKEN" )
    for droplet in manager.droplets:
      digitalocean.Backup( options, droplet )



```