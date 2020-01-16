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

        self.assertEqual(project.id, "4e1bfbc3-dc3e-41f2-a18f-1b4d7ba71679")
        self.assertEqual(project.owner_uuid, "99525febec065ca37b2ffe4f852fd2b2581895e7")
        self.assertEqual(project.owner_id, 2)
        self.assertEqual(project.name, "my-web-api")
        self.assertEqual(project.description, "My website API")
        self.assertEqual(project.purpose, "Service or API")
        self.assertEqual(project.environment, "Production")
        self.assertEqual(project.is_default, False)
        self.assertEqual(project.updated_at, "2018-09-27T20:10:35Z")
        self.assertEqual(project.created_at, "2018-09-27T20:10:35Z")


if __name__ == '__main__':
    unittest.main()