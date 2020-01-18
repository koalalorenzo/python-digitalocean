import unittest
import responses
import digitalocean
from .BaseTest import BaseTest


class TestProject(BaseTest):

    def setUp(self):
        super(TestProject, self).setUp()

    @responses.activate
    def test_load(self):
        self.project = digitalocean.Project(
            id='4e1bfbc3-dc3e-41f2-a18f-1b4d7ba71679',
            token=self.token)
        data = self.load_from_file('projects/retrieve.json')
        project_path = "projects/4e1bfbc3-dc3e-41f2-a18f-1b4d7ba71679"

        url = self.base_url + project_path
        responses.add(responses.GET,
                      url,
                      body=data,
                      status=200,
                      content_type='application/json')
        self.project.load()
        self.assert_get_url_equal(responses.calls[0].request.url, url)
        self.assertEqual(self.project.id, '4e1bfbc3-dc3e-41f2-a18f-1b4d7ba71679')
        self.assertEqual(self.project.owner_uuid, "99525febec065ca37b2ffe4f852fd2b2581895e7")
        self.assertEqual(self.project.owner_id, 2)
        self.assertEqual(self.project.name, "my-web-api")
        self.assertEqual(self.project.description, "My website API")
        self.assertEqual(self.project.purpose, "Service or API")
        self.assertEqual(self.project.environment, "Production")
        self.assertEqual(self.project.is_default, False)
        self.assertEqual(self.project.updated_at, "2018-09-27T20:10:35Z")
        self.assertEqual(self.project.created_at, "2018-09-27T20:10:35Z")

    @responses.activate
    def test_create_new_project(self):
        data = self.load_from_file('projects/create.json')
        project_path = "projects"

        url = self.base_url + project_path
        responses.add(responses.POST,
                      url,
                      body=data,
                      status=201,
                      content_type='application/json')
        project = digitalocean.Project(token=self.token, name="my-web-api",
                                       purpose="Service or API",
                                       description="My website API",
                                       environment="Production")
        project.create_project()
        self.assertEqual(responses.calls[0].request.url, url)
        self.assertEqual(project.id, '4e1bfbc3-dc3e-41f2-a18f-1b4d7ba71679')
        self.assertEqual(project.owner_uuid, '99525febec065ca37b2ffe4f852fd2b2581895e7')
        self.assertEqual(project.is_default, False)
        self.assertEqual(project.name, "my-web-api")
        self.assertEqual(project.description, "My website API")
        self.assertEqual(project.purpose, "Service or API")
        self.assertEqual(project.environment, "Production")
        self.assertEqual(project.updated_at, "2018-09-27T15:52:48Z")
        self.assertEqual(project.created_at, "2018-09-27T15:52:48Z")

    @responses.activate
    def test_update_project(self):
        data = self.load_from_file('projects/update.json')
        project = digitalocean.Project(token=self.token,
                                       id="4e1bfbc3-dc3e-41f2-a18f-1b4d7ba71679")

        project_path = "projects/" + project.id
        url = self.base_url + project_path
        responses.add(responses.PUT,
                      url,
                      body=data,
                      status=200,
                      content_type='application/json')

        project.update_project(name="my-web-api",
                               description="My website API",
                               purpose="Service or API",
                               environment="Staging",
                               is_default=False)

        self.assertEqual(responses.calls[0].request.url, url)
        self.assertEqual(project.is_default, False)
        self.assertEqual(project.name, "my-web-api")
        self.assertEqual(project.description, "My website API")
        self.assertEqual(project.purpose, "Service or API")
        self.assertEqual(project.environment, "Staging")

    @responses.activate
    def test_get_all_resources(self):
        data = self.load_from_file('projects/project_resources.json')
        resource_project = digitalocean.Project(token=self.token,
                                                id="4e1bfbc3-dc3e-41f2-a18f-1b4d7ba71679")
        url = self.base_url + 'projects/' + resource_project.id + "/resources"
        responses.add(responses.GET, url,
                      body=data,
                      status=200,
                      content_type='application/json')

        all_resources = resource_project.get_all_resources()
        self.assertEqual(len(all_resources), 1)
        self.assertEqual(all_resources[0], "do:droplet:1")

    @responses.activate
    def test_delete(self):
        url = self.base_url + "projects/4e1bfbc3-dc3e-41f2-a18f-1b4d7ba71679"
        responses.add(responses.DELETE,
                      url,
                      status=204,
                      content_type='application/json')

        project_to_be_deleted = digitalocean.Project(token=self.token,
                                                     id="4e1bfbc3-dc3e-41f2-a18f-1b4d7ba71679")
        project_to_be_deleted.delete_project()
        self.assertEqual(responses.calls[0].request.url, url)

    @responses.activate
    def test_update_default_project(self):
        data = self.load_from_file('projects/update.json')
        project = digitalocean.Project(token=self.token,
                                       id="default")

        project_path = "projects/" + project.id
        url = self.base_url + project_path
        responses.add(responses.PUT,
                      url,
                      body=data,
                      status=200,
                      content_type='application/json')

        project.update_project(name="my-web-api",
                               description="My website API",
                               purpose="Service or API",
                               environment="Staging",
                               is_default=False)

        self.assertEqual(responses.calls[0].request.url, url)
        self.assertEqual(project.is_default, False)
        self.assertEqual(project.name, "my-web-api")
        self.assertEqual(project.description, "My website API")
        self.assertEqual(project.purpose, "Service or API")
        self.assertEqual(project.environment, "Staging")

    @responses.activate
    def test_assign_resource(self):
        data = self.load_from_file('projects/assign_resources.json')
        resource_project = digitalocean.Project(token=self.token,
                                                id="4e1bfbc3-dc3e-41f2-a18f-1b4d7ba71679")
        url = self.base_url + 'projects/' + resource_project.id + "/resources"

        responses.add(responses.POST, url,
                      body=data,
                      status=200,
                      content_type='application/json')
        add_resources = {
            "resources": ["do:droplet:1", "do:floatingip:192.168.99.100"]
        }

        result_resources = resource_project.assign_resource(add_resources)
        self.assertEqual(len(result_resources['resources']), 2)
        self.assertEqual(result_resources['resources'][0]['urn'], "do:droplet:1")
        self.assertEqual(result_resources['resources'][1]['urn'],
                         "do:floatingip:192.168.99.100")

    @responses.activate
    def test_list_default_project_resources(self):
        data = self.load_from_file('projects/project_resources.json')
        resource_project = digitalocean.Project(token=self.token,
                                                id="default")
        url = self.base_url + 'projects/' + resource_project.id + "/resources"
        responses.add(responses.GET, url,
                      body=data,
                      status=200,
                      content_type='application/json')

        all_resources = resource_project.get_all_resources()
        self.assertEqual(len(all_resources), 1)
        self.assertEqual(all_resources[0], "do:droplet:1")

    @responses.activate
    def test_assign_resource_to_default_project(self):
        data = self.load_from_file('projects/assign_resources.json')
        resource_project = digitalocean.Project(token=self.token,
                                                id="default")
        url = self.base_url + 'projects/' + resource_project.id + "/resources"

        responses.add(responses.POST, url,
                      body=data,
                      status=200,
                      content_type='application/json')
        add_resources = {
            "resources": ["do:droplet:1", "do:floatingip:192.168.99.100"]
        }

        result_resources = resource_project.assign_resource(add_resources)
        self.assertEqual(len(result_resources['resources']), 2)
        self.assertEqual(result_resources['resources'][0]['urn'], "do:droplet:1")
        self.assertEqual(result_resources['resources'][1]['urn'],
                         "do:floatingip:192.168.99.100")


if __name__ == '__main__':
    unittest.main()
