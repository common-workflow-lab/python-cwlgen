

#  Constant(s)  ------------------------------

CWL_SHEBANG = "#!/usr/bin/env cwl-runner"
CWL_VERSIONS = ['draft-2', 'draft-3.dev1', 'draft-3.dev2', 'draft-3.dev3',
                'draft-3.dev4', 'draft-3.dev5', 'draft-3', 'draft-4.dev1',
                'draft-4.dev2', 'draft-4.dev3', 'v1.0.dev4', 'v1.0', None]
DEF_VERSION = 'v1.0'
CWL_TYPE = ['null', 'boolean', 'int', 'long', 'float', 'double', 'string', 'File',
            'Directory', None]



class Parameter(object):
    '''
    Based class for parameters (common field of Input and Output) for CommandLineTool and Workflow
    '''

    def __init__(self, param_id, label=None, secondary_files=None, param_format=None,
                 streamable=False, doc=None, param_type=None):
        '''
        :param param_id: unique identifier for this parameter
        :type param_id: STRING
        :param label: short, human-readable label
        :type label: STRING
        :param secondary_files: If type is a file, describes files that must be
                                included alongside the primary file(s)
        :type secondary_files: STRING
        :param param_format: If type is a file, uri to ontology of the format or exact format
        :type param_format: STRING
        :param streamable: If type is a file, true indicates that the file is read or written
                           sequentially without seeking
        :type streamable: BOOLEAN
        :param doc: documentation
        :type doc: STRING
        :param param_type: type of data assigned to the parameter
        :type param_type: STRING corresponding to CWLType
        '''
        if param_type not in CWL_TYPE:
            LOGGER.warning("The type is incorrect for the parameter.")
            param_type = None
        self.id = param_id
        self.label = label
        self.secondaryFiles = secondary_files
        self.format = param_format
        self.streamable = streamable
        self.doc = doc
        self.type = param_type

    def get_dict(self):
        '''
        Transform the object to a [DICT] to write CWL.

        :return: dictionnary of the object
        :rtype: DICT
        '''
        dict_param = {k: v for k, v in vars(self).items() if v is not None and v is not False}
        if dict_param['type'] != 'File':
            # Remove what is only for File
            for key in ['format', 'secondaryFiles', 'streamable']:
               try:
                   del(dict_param[key])
               except KeyError:
                   pass
        return dict_param
