from otm.otm.entity.dataflow import OtmDataflow
from sl_util.sl_util.str_utils import deterministic_uuid
from slp_visio.slp_visio.load.objects.diagram_objects import DiagramConnector


def build_otm_dataflow(diagram_connector: DiagramConnector) -> OtmDataflow:
    return OtmDataflow(
        dataflow_id=diagram_connector.id,
        name=diagram_connector.name if diagram_connector.name else deterministic_uuid(diagram_connector.id),
        source_node=diagram_connector.from_id,
        destination_node=diagram_connector.to_id,
        bidirectional=diagram_connector.bidirectional if diagram_connector.bidirectional else None
    )


class DiagramConnectorMapper:
    def __init__(self, connectors: [DiagramConnector]):
        self.connectors = connectors

    def to_otm(self):
        return list(map(build_otm_dataflow, self.connectors))

