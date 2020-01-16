from .baseapi import BaseAPI, GET, POST, DELETE , PUT

class Project(BaseAPI):
    def __init__(self,*args, **kwargs):
        self.name = None
        self.description = None
        self.purpose = None
        self.environment = None
        self.id = None
        self.is_default = None
        self.owner_uuid = None
        self.owner_id = None
        self.created_at = None
        self.updated_at = None
        self.resources = None

        super(Project,self).__init__(*args, **kwargs)

    @classmethod
    def get_object(cls, api_token, project_id):
        """Class method that will return a Project object by ID.
        Args:
            api_token (str): token
            kwargs (str): project id or project name
        """

        project = cls(token=api_token, id=project_id)
        project.load()
        return project

    def load(self):
        # URL https://api.digitalocean.com/v2/projects
        project = self.get_data("projects/%s" % self.id)
        project = project['project']
        for attr in project.keys():
            setattr(self, attr, project[attr])

    def set_as_default_project(self):

        data = {
            "name": self.name,
            "description": self.description,
            "purpose": self.purpose,
            "environment": self.environment,
            "is_default": True
        }

        project = self.get_data("projects/%s" % self.id, type=PUT, params=data)
        return project

    def create_project(self,**kwargs):

        """Creating Project with the following arguments
        Args:
            api_token (str): token
            "name": Name of the Project - Required
            "description": Description of the Project - Optional
            "purpose": Purpose of the project - Required
            "environment": Related Environment of  Project - Optional
                         - Development
                         - Stating
                         - Production
            kwargs (str): project id or project name
        """

        for attr in kwargs.keys():
            setattr(self, attr, kwargs[attr])
        data = {
            "name": self.name,
            "purpose": self.purpose
        }
        if self.description:
            data['description'] = self.description
        if self.environment:
            data['environment'] = self.environment
        data = self.get_data("projects", type=POST, params=data)
        if data:
            self.id = data['project']['id']
            self.owner_uuid  = data['project']['owner_uuid']
            self.owner_id = data['project']['id']
            self.name = data['project']['name']
            self.description = data['project']['description']
            self.purpose = data['project']['purpose']
            self.environment = data['project']['environment']
            self.is_default = data['project']['is_default']
            self.created_at = data['project']['created_at']
            self.updated_at = data['project']['updated_at']
        return self


    def delete_project(self):
        data = {}
        return self.get_data("projects/%s" % self.id, type=DELETE, params=data)

    def update_project(self, **kwargs):
        data = {
            "name": self.name,
            "description": self.description,
            "purpose": self.purpose,
            "environment": self.environment,
            "is_default": self.is_default
        }

        if kwargs.get("name", None):
            data['name'] = kwargs.get("name", self.name)

        if kwargs.get("description", None):
            data['description'] = kwargs.get("description", self.description)

        """
        Options for Purpose by Digital Ocean
         - Just Trying out DigitalOcean
         - Class Project / Educational Purposes
         - Website or blog
         - Web Application
         - Service or API
         - Mobile Application
         - Machine Learning / AI / Data Processing
         - IoT
         - Operational / Developer tooling
         - Other 
        """

        if kwargs.get("purpose", None):
            data['purpose'] = kwargs.get("purpose", self.purpose)
        """
        Options for Environment by Digital Ocean
         - Development
         - Stating
         - Production
        """
        if kwargs.get("environment", None):
            data['environment'] = kwargs.get("environment", self.environment)

        return self.get_data("projects/%s" % self.id, type=PUT, params=data)

    def get_all_resources(self):
        project_resources_response = self.get_data("projects/%s/resources" % self.id)
        project_resources = project_resources_response['resources']
        self.resources = []
        for i in project_resources:
            self.resources.append(i['urn'])
        return self.resources

    def load_resources(self):
        project_resources_response = self.get_data("projects/%s/resources" % self.id)
        project_resources = project_resources_response['resources']
        self.resources = []
        for i in project_resources:
            self.resources.append(i['urn'])

    def assign_resource(self, resources):
        data = {
            'resources': resources
        }
        return self.get_data("projects/%s/resources" % self.id, type=POST, params=data)

    def __str__(self):
        return "<Project: " + self.name + "> " + self.id