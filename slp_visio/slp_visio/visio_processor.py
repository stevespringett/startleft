from starlette.datastructures import UploadFile

from sl_util.sl_util.file_utils import copy_to_disk
from slp_base import OtmProcessor, ProviderValidator, ProviderLoader, MappingValidator, MappingLoader, ProviderParser
from slp_visio.slp_visio.load.visio_loader import VisioLoader
from slp_visio.slp_visio.load.visio_mapping_loader import VisioMappingFileLoader
from slp_visio.slp_visio.parse.visio_parser import VisioParser
from slp_visio.slp_visio.validate.visio_mapping_file_validator import VisioMappingFileValidator
from slp_visio.slp_visio.validate.visio_validator import VisioValidator


class VisioProcessor(OtmProcessor):
    """
    Visio implementation of OtmProcessor
    """

    def __init__(self, project_id: str, project_name: str, source, mappings: [bytes]):
        self.project_id = project_id
        self.project_name = project_name
        self.mappings = mappings
        if type(source) is UploadFile:
            self.source = copy_to_disk(source.file, '.vsdx')
        else:
            self.source = source
        self.loader = None
        self.mapping_loader = None

    def get_provider_validator(self) -> ProviderValidator:
        return VisioValidator(self.source)

    def get_provider_loader(self) -> ProviderLoader:
        self.loader = VisioLoader(self.source)
        return self.loader

    def get_mapping_validator(self) -> MappingValidator:
        return VisioMappingFileValidator(self.mappings)

    def get_mapping_loader(self) -> MappingLoader:
        self.mapping_loader = VisioMappingFileLoader(self.mappings)
        return self.mapping_loader

    def get_provider_parser(self) -> ProviderParser:
        visio = self.loader.get_visio()
        return VisioParser(self.project_id, self.project_name, visio, self.mapping_loader)