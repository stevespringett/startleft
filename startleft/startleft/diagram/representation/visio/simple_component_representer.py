from shapely.geometry import Polygon
from vsdx import Shape

from startleft.startleft.diagram.representation.visio.visio_shape_representer import VisioShapeRepresenter
from startleft.startleft.diagram.util.visio import get_limits


class SimpleComponentRepresenter(VisioShapeRepresenter):

    def build_representation(self, shape: Shape) -> Polygon:
        limits = get_limits(shape)

        points = [(limits[0][0], limits[0][1]),
                  (limits[0][0], limits[1][1]),
                  (limits[1][0], limits[1][1]),
                  (limits[1][0], limits[0][1])]

        return Polygon(points)