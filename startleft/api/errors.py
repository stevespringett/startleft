from enum import Enum


class ErrorCode(Enum):

    IAC_LOADING_ERROR = (1, 400)
    IAC_NOT_VALID = (2, 400)
    IAC_UNEXPECTED = (5, 500)

    DIAGRAM_LOADING_ERROR = (11, 400)
    DIAGRAM_NOT_VALID = (12, 400)
    DIAGRAM_UNEXPECTED = (15, 500)

    MAPPING_LOADING_ERROR = (21, 400)
    MAPPING_FILE_NOT_VALID = (22, 400)
    MAPPING_UNEXPECTED = (25, 500)

    OTM_BUILDING_ERROR = (41, 400)
    OTM_RESULT_ERROR = (42, 400)
    OTM_GENERATION_ERROR = (45, 500)

    def __init__(self, system_exit_status, http_status):
        self.http_status = http_status
        self.system_exit_status = system_exit_status

    def __str__(self):
        return f'{self.exit_value}'


class CommonError(Exception):
    error_code: ErrorCode

    def __init__(self, title, detail, message):
        self.title = title
        self.detail = detail
        self.message = message

    def __str__(self):
        self.__class__.__name__


class IacFileNotValidError(CommonError):
    """ IaC file is not valid """
    error_code = ErrorCode.IAC_NOT_VALID


class DiagramFileNotValidError(CommonError):
    """ Diagram file is not valid """
    error_code = ErrorCode.DIAGRAM_NOT_VALID


class MappingFileNotValidError(CommonError):
    """ Mapping file is not valid """
    error_code = ErrorCode.MAPPING_FILE_NOT_VALID


class LoadingIacFileError(CommonError):
    """ IaC file cannot be loaded """
    error_code = ErrorCode.IAC_LOADING_ERROR


class LoadingDiagramFileError(CommonError):
    """ Diagram file cannot be loaded """
    error_code = ErrorCode.DIAGRAM_LOADING_ERROR


class LoadingMappingFileError(CommonError):
    """ Mapping file cannot be loaded """
    error_code = ErrorCode.MAPPING_LOADING_ERROR


class OtmBuildingError(CommonError):
    """ Error during OTM transformation. Eg: bad jmespath expression. """
    error_code = ErrorCode.OTM_BUILDING_ERROR


class OtmResultError(CommonError):
    """ Parsing provided given IaC/diagram file with the mapping file provided result in an invalid OTM file. """
    error_code = ErrorCode.OTM_RESULT_ERROR


class OtmGenerationError(CommonError):
    """ Provided files were processed successfully but an error occurred while generating the OTM file. """
    error_code = ErrorCode.OTM_GENERATION_ERROR
