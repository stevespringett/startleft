from otm.otm.entity.threat import OtmThreatInstance


class OtmComponent:
    def __init__(self, component_id, name, component_type, parent, parent_type: str, source=None,
                 properties=None, tags=None, threats: [OtmThreatInstance] = None, representations=None):
        self.id = component_id
        self.name = name
        self.type = component_type
        self.parent = parent
        self.parent_type: str = parent_type
        self.source = source
        self.properties = properties
        self.tags = tags
        self.threats: [OtmThreatInstance] = threats or []
        self.representations = representations

    def add_threat(self, threat: OtmThreatInstance):
        self.threats.append(threat)

    def json(self):
        json = {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "parent": {
                self.parent_type: self.parent
            }
        }

        if self.properties:
            json["properties"] = self.properties
        if self.tags:
            json["tags"] = self.tags
        if self.representations:
            json["representations"] = [r.json() for r in self.representations]

        if len(self.threats) > 0:
            json["threats"] = []
            for threat in self.threats:
                json["threats"].append(threat.json())

        return json
