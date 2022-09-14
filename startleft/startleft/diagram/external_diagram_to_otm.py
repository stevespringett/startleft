import logging

from otm.otm.otm import OTM
from slp_base import DiagramType
from slp_base.slp_base.errors import DiagramFileNotValidError, OtmBuildingError, LoadingDiagramFileError
from startleft.startleft import messages
from startleft.startleft.diagram.mapping.diagram_to_otm import DiagramToOtm
from startleft.startleft.diagram.objects.visio.visio_diagram_factories import VisioComponentFactory, \
    VisioConnectorFactory
from startleft.startleft.diagram.parsing.visio.visio_diagram_parser import VisioDiagramParser
from startleft.startleft.mapping.mapping_file_loader import MappingFileLoader
from startleft.startleft.validators.generic_mapping_validator import GenericMappingValidator

logger = logging.getLogger(__name__)


def get_parser_for_diagram_type(provider):
    if provider == DiagramType.VISIO:
        return VisioDiagramParser(VisioComponentFactory(), VisioConnectorFactory())
    msg = messages.CANNOT_RECOGNIZE_GIVEN_DIAGRAM_TYPE
    raise DiagramFileNotValidError('UnknownDiagramType', msg, f'{msg} {provider}')


class ExternalDiagramToOtm:
    def __init__(self, diagram_type: DiagramType):
        self.diagram_type = diagram_type
        self.mapping_file_loader = MappingFileLoader()
        self.mapping_validator = GenericMappingValidator('diagram_mapping_schema.json')

    def run(self, diagram_source: str, mapping_data_list, project_name: str, project_id: str) -> OTM:
        diagram_mapping = self.mapping_file_loader.load(mapping_data_list)
        self.mapping_validator.validate(diagram_mapping)
        try:
            diagram = get_parser_for_diagram_type(self.diagram_type).parse(diagram_source)
        except Exception as e:
            logger.error(f'{e}')
            detail = e.__class__.__name__
            message = e.__str__()
            raise LoadingDiagramFileError('Diagram file is not valid', detail, message)

        try:
            return DiagramToOtm(
                project_id=project_id,
                project_name=project_name,
                diagram=diagram,
                mapping_file=diagram_mapping
            ).run()
        except Exception as e:
            logger.error(f'{e}')
            detail = e.__class__.__name__
            message = e.__str__()
            raise OtmBuildingError('Error building the threat model with the given files', detail, message)