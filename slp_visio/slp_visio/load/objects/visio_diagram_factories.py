from typing import Optional

from vsdx import Shape

from slp_visio.slp_visio.load.objects.diagram_objects import DiagramComponent, DiagramConnector


def get_component_type_from_master(shape: Shape):
    return shape.master_shape.text.replace('\n', '') if shape.master_shape else ''


# if it has two shapes connected and is not pointing itself
def is_valid_connector(connected_shapes) -> bool:
    if len(connected_shapes) < 2:
        return False
    if connected_shapes[0].shape_id == connected_shapes[1].shape_id:
        return False
    return True


class VisioComponentFactory:

    def create_component(self, shape, origin, representer) -> DiagramComponent:
        return DiagramComponent(
            id=shape.ID,
            name=shape.text.replace('\n', ''),
            type=get_component_type_from_master(shape),
            origin=origin,
            representation=representer.build_representation(shape))


class VisioConnectorFactory:

    def create_connector(self, shape) -> Optional[DiagramConnector]:
        connected_shapes = shape.connects
        if not is_valid_connector(connected_shapes):
            return None
        if connected_shapes[0].from_rel == 'BeginX':
            return DiagramConnector(shape.ID, connected_shapes[0].shape_id, connected_shapes[1].shape_id)
        else:
            return DiagramConnector(shape.ID, connected_shapes[1].shape_id, connected_shapes[0].shape_id)