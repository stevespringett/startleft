import logging

from startleft.mapper import TrustzoneMapper, ComponentMapper, DataflowMapper

logger = logging.getLogger(__name__)


class Transformer:
    def __init__(self, source_model=None, threat_model=None):
        self.source_model = source_model
        self.threat_model = threat_model
        self.map = {}
        self.id_map = {}
        self.id_parents = dict()

    def build_lookup(self):
        if "lookup" in self.map:
            self.source_model.lookup = self.map["lookup"]

    def transform_trustzones(self):
        for mapping in self.map["trustzones"]:
            mapper = TrustzoneMapper(mapping)
            mapper.id_map = self.id_map
            source_trustzones = mapper.run(self.source_model)
            for trustzone_number, trustzone_element in enumerate(source_trustzones):
                if "$source" in mapping and isinstance(mapping["$source"], dict):
                    if "$singleton" in mapping["$source"] and trustzone_number > 0:
                        continue
                self.threat_model.add_trustzone(**trustzone_element)

    def transform_components(self):
        singleton = []
        components = []
        catchall = []
        skip = []
        for mapping in self.map["components"]:
            mapper = ComponentMapper(mapping)
            mapper.id_map = self.id_map
            for component in mapper.run(self.source_model, self.id_parents):
                if isinstance(mapping["$source"], dict):
                    if "$skip" in mapping["$source"]:
                        skip.append(component)
                        continue
                    elif "$catchall" in mapping["$source"]:
                        catchall.append(component)
                        continue
                    elif "$singleton" in mapping["$source"]:
                        singleton.append(component)
                        continue

                components.append(component)

        results = []
        for component in components:
            skip_this = False
            for skip_component in skip:
                if component["id"] == skip_component["id"]:
                    logger.debug("Skipping component '{}'".format(component["id"]))
                    skip_this = True
                    break
            if not skip_this:
                results.append(component)

        for component in catchall:
            skip_this = False
            for skip_component in skip:
                if component["id"] == skip_component["id"]:
                    logger.debug("Skipping catchall component '{}'".format(component["id"]))
                    skip_this = True
                    break
            for current_component in results:
                if component["id"] == current_component["id"]:
                    logger.debug("Catchall component already added '{}'".format(component["id"]))
                    skip_this = True
                    break
            if not skip_this:
                results.append(component)

        singleton_types_added = []
        for component in singleton:
            skip_this = False
            for skip_component in skip:
                if component["id"] == skip_component["id"]:
                    logger.debug("Skipping singleton component '{}'".format(component["id"]))
                    skip_this = True
                    break
            if not skip_this:
                if component["type"] not in singleton_types_added:
                    results.append(component)
                    singleton_types_added.append(component["type"])
                else:
                    # if the component is singleton and it already exists in otm (from a previous mapping)
                    # no new component is generated but the existing component is updated
                    # a)with the group name (even more if had a component name)
                    # b)with a new tag with data from this source component
                    for result in results:
                        if result["type"] == component["type"]:
                            if "singleton_multiple_name" in component:
                                result["name"] = component["singleton_multiple_name"]

                            #update "result" component with its multiple tags before adding tags from "component"
                            if "singleton_multiple_tags" in result:
                                if len(result["tags"]) <= len(result["singleton_multiple_tags"])\
                                        and result["tags"] is not result["singleton_multiple_tags"]:
                                    result["tags"] = result["singleton_multiple_tags"]

                            if "singleton_multiple_tags" in component:
                                for tag in component["singleton_multiple_tags"]:
                                    if tag not in result["tags"]:
                                        result["tags"].append(tag)
                            continue

        #removal of auxiliary data before adding components
        for component in results:
            if "singleton_multiple_name" in component:
                del component["singleton_multiple_name"]
            if "singleton_multiple_tags" in component:
                del component["singleton_multiple_tags"]

        for final_component in results:
            parent_component = next(filter(lambda x: x["id"] == final_component['parent'], results), None)
            if parent_component:
                final_component["parent_type"] = "component"
            else:
                final_component["parent_type"] = "trustZone"

            self.threat_model.add_component(**final_component)

    def transform_dataflows(self):
        for mapping in self.map["dataflows"]:
            mapper = DataflowMapper(mapping)
            mapper.id_map = self.id_map
            for dataflow in mapper.run(self.source_model, self.id_parents):
                self.threat_model.add_dataflow(**dataflow)

        self.__generate_dataflows_from_hubs()

    def run(self, iac_mapping):
        self.map = iac_mapping
        self.build_lookup()
        self.transform_trustzones()
        self.transform_components()
        self.transform_dataflows()

    def __generate_dataflows_from_hubs(self):
        for dataflow in self.threat_model.dataflows:
            if "-hub" in dataflow.source_node or "-hub" in dataflow.destination_node:
                print("SG DATAFLOW-> source: " + dataflow.source_node
                      + " destination: " + dataflow.destination_node)

