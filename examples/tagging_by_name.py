import digitalocean
from digitalocean.baseapi import BaseAPI
from digitalocean.Tag import Tag

TOKEN = "some-token"
TAG = "test"
APPLY_TAG_REQUIRED = lambda droplet_name: TAG in droplet_name.lowar()

tag = Tag(token=TOKEN, name=TAG)
tag.load_or_create()

ids = []
for droplet in manager.get_all_droplets():
    if APPLY_TAG_REQUIRED(droplet.name):
        ids.append(droplet.id)

tag.tagging_droplets(ids)
tag.load()
print(tag.resources['droplets']['count'])
