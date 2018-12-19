from abc import ABC, abstractmethod


class Requirement(ABC):
    '''
    Requirement that must be met in order to execute the process.
    '''

    def __init__(self, req_class):
        '''
        :param req_class: requirement class
        :type req_class: STRING
        '''
        # class is protected keyword
        self.req_class = req_class

    @abstractmethod
    def get_dict(self):
        return {"class": self.req_class}


class InlineJavascriptReq(Requirement):
    """
    Indicates that the workflow platform must support inline Javascript expressions.
    If this requirement is not present, the workflow platform must not perform expression interpolatation.

    Documentation: https://www.commonwl.org/v1.0/Workflow.html#InlineJavascriptRequirement
    """

    def __init__(self, expression_lib=None):
        '''
        :param expression_lib: List of Strings
        :type expression_lib: STRING | list[STRING]
        '''
        Requirement.__init__(self, 'InlineJavascriptRequirement')
        self.expressionLib = expression_lib

    def get_dict(self):
        base = Requirement.get_dict(self)
        if self.expressionLib:
            base["expressionLib"] = self.expressionLib
        return base




class DockerRequirement(Requirement):
    '''
    Workflow component should be run in a Docker container.
    This class specifies how to fetch or build the image.
    '''

    def __init__(self, docker_pull=None, docker_load=None, docker_file=None,
                 docker_import=None, docker_image_id=None, docker_output_dir=None):
        '''
        :param docker_pull: image to retrive with docker pull
        :type docker_pull: STRING
        :param docker_load: HTTP URL from which to download Docker image
        :type docker_load: STRING
        :param docker_file: supply the contents of a Dockerfile
        :type docker_file: STRING
        :param docker_import: HTTP URL to download and gunzip a Docker images
        :type docker_import: STRING
        :param docker_image_id: Image id for docker run
        :type docker_image_id: STRING
        :param docker_output_dir: designated output dir inside the Docker container
        :type docker_output_dir: STRING
        '''
        Requirement.__init__(self, 'DockerRequirement')
        self.dockerPull = docker_pull
        self.dockerLoad = docker_load
        self.dockerFile = docker_file
        self.dockerImport = docker_import
        self.dockerImageId = docker_image_id
        self.dockerOutputDir = docker_output_dir

    def _to_dict(self):
        """
        Add this requirement to a dictionary description of a
        tool generated in an export method.

        """
        return {p: v for p, v in vars(self).items() if p.startswith('docker') and v is not None}


class SubworkflowFeatureRequirement(Requirement):

    def __init__(self):
        Requirement.__init__(self, 'SubworkflowFeatureRequirement')

    def _to_dict(self):
        return dict()