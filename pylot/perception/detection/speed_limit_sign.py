import pylot.utils
from pylot.perception.detection.utils import DetectedObstacle


class SpeedLimitSign(DetectedObstacle):
    """Class that stores info about a detected speed limit signs.

    Args:
        speed_limit (:obj:`int`): The speed limit (in km/h).
        confidence (:obj:`float`): The confidence of the detection.
        bounding_box (:py:class:`.BoundingBox2D`): The bounding box of the
            speed limit sign in camera view.
        id (:obj:`int`): Id associated with the sign.
        transform (:py:class:`~pylot.utils.transform`): Transform of the sign
            in the world.

    Attributes:
        speed_limit (:obj:`int`): The speed limit (in km/h).
        confidence (:obj:`float`): The confidence of the detection.
        bounding_box (:py:class:`.BoundingBox2D`): The bounding box of the
            speed limit sign in camera view.
        id (:obj:`int`): Id associated with the sign.
        transform (:py:class:`~pylot.utils.transform`): Transform of the sign
            in the world.
    """
    def __init__(self,
                 speed_limit,
                 confidence,
                 bounding_box=None,
                 id=-1,
                 transform=None):
        super(SpeedLimitSign, self).__init__(bounding_box, confidence,
                                             'speed limit', id, transform)
        self.speed_limit = speed_limit

    @classmethod
    def from_carla_actor(cls, actor):
        """Creates a detected speed limit sign from a CARLA actor.

        Args:
            actor (carla.TrafficSign): A carla speed limit sign actor.

        Returns:
            :py:class:`.SpeedLimitSign`: A detected speed limit sign.
        """
        import carla
        if not isinstance(actor, carla.TrafficSign):
            raise ValueError('actor should be of type carla.TrafficSign')
        transform = pylot.utils.Transform.from_carla_transform(
            actor.get_transform())
        speed_limit = int(actor.type_id.split('.')[-1])
        return cls(speed_limit, 1.0, id=actor.id, transform=transform)

    def get_in_log_format(self):
        return (self.label + ' ' + str(self.speed_limit),
                (self.bounding_box.get_min_point(),
                 self.bounding_box.get_max_point()))

    def draw_on_image(self, image_np, bbox_color_map, ego_transform=None):
        text = '{} {} {:.1f}'.format(self.speed_limit, self.label,
                                     self.confidence)
        super(SpeedLimitSign, self).draw_on_image(image_np, bbox_color_map,
                                                  ego_transform, text)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return 'SpeedLimitSign(label: {}, limit: {}, '\
            'confidence: {}, id: {}, transform: {}, bbox: {})'.format(
                self.label, self.speed_limit, self.confidence, self.id,
                self.transform, self.bounding_box)
