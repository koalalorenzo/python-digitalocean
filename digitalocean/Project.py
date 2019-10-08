from .baseapi import BaseAPI


class Project(BaseAPI):
    """Project management

    Attributes returned by API:
    * id (str): UUID of project
    * owner_uuid (str): UUID of project owner
    * owner_id (str): ID of project owner
    * name (str): Name of project
    * description (str): Project description
    * purpose (str): Purpose of project
    * environment (str): The environment of the project's resources
    * is_default (bool): True if the project is default
    * created_at (str): Project's creation date in format '2019-09-16T07:44:15Z'
    * updated_at (str): Project's update date in format '2019-09-16T07:44:24Z'

    """

    def __init__(self, *args, **kwargs):
        self.id = None
        self.owner_uuid = None
        self.owner_id = None
        self.name = None
        self.description = None
        self.purpose = None
        self.environment = None
        self.is_default = None
        self.created_at = None
        self.updated_at = None

        super(Project, self).__init__(*args, **kwargs)

    def __str__(self):
        return '<Project: %s>' % self.name
