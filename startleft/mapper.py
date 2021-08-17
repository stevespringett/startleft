import uuid

class TrustzoneMapper:
    def __init__(self, mapping):
        self.mapping = mapping
        self.id_map = {} 

    def run(self, source_model):
        trustzones = []

        if "$source" in self.mapping:
            source_objs =  source_model.search(self.mapping["$source"])
            if not isinstance(source_objs, list):
                source_objs = [source_objs]
        else:
            source_objs = [self.mapping]

        for source_obj in source_objs:
            trustzone = {}
            trustzone["name"] = source_model.search(self.mapping["name"], source=source_obj)
            trustzone["type"] = source_model.search(self.mapping["type"], source=source_obj)
            trustzone["source"] = source_obj
            if "properties" in self.mapping:
                trustzone["properties"] = self.mapping["properties"]

            source_id = source_model.search(self.mapping["id"], source=trustzone)
            if not source_id in self.id_map:
                tz_id = str(uuid.uuid4())
                self.id_map[source_id] = tz_id
            else:
                tz_id = self.id_map[source_id]
            trustzone["id"] = tz_id

            trustzones.append(trustzone)

        return trustzones


class ComponentMapper:
    def __init__(self, mapping):
        self.mapping = mapping
        self.source = None
        self.id_map = {}

    def run(self, source_model):
        components = []

        source_objs = source_model.search(self.mapping["$source"], source=None)
        if not isinstance(source_objs, list):
            source_objs = [source_objs]

        for source_obj in source_objs:
            if "parent" in self.mapping:
                parent = source_model.search(self.mapping["parent"], source=source_obj)
            else:
                parent = [None]

            if "name" in self.mapping:
                c_name = source_model.search(self.mapping["name"], source=source_obj)
            else:
                c_name = None

            c_type = source_model.search(self.mapping["type"], source=source_obj)

            if isinstance(parent, str):
                parent = [parent]
            for parent_element in parent:
                component = {}

                component["name"] = c_name
                component["type"] = c_type

                if parent_element in self.id_map:
                    parent_id = self.id_map[parent_element]
                else:
                    parent_id = str(uuid.uuid4())
                    self.id_map[parent_element] = parent_id 

                component["parent"] = parent_id
                component["source"] = source_obj

                if "properties" in self.mapping:
                    component["properties"] = self.mapping["properties"] 

                if "id" in self.mapping:
                    source_id = source_model.search(self.mapping["id"], source=component)
                else:
                    source_id = str(uuid.uuid4())

                if source_id not in self.id_map:
                    c_id = str(uuid.uuid4())
                    self.id_map[source_id] = c_id
                else:
                    c_id = self.id_map[source_id]                    
                component["id"] = c_id

                components.append(component)
        return components


class DataflowNodeMapper:
    def __init__(self, mapping):
        self.mapping = mapping
        self.id_map = {}

    def run(self, source_model, source):
        source_objs = source_model.search(self.mapping, source=source)
        if isinstance(source_objs, str):
            source_objs = [source_objs]
        return source_objs


class DataflowMapper:
    def __init__(self, mapping):
        self.mapping = mapping
        self.id_map = {}

    def run(self, source_model):

        dataflows = []

        source_objs = source_model.search(self.mapping["$source"], source=None)
        if not isinstance(source_objs, list):
            source_objs = [source_objs]
        for source_obj in source_objs:
            df_name = source_model.search(self.mapping["name"], source=source_obj)
            df_type = source_model.search(self.mapping["type"], source=source_obj)

            from_mapper = DataflowNodeMapper(self.mapping["from"])
            to_mapper = DataflowNodeMapper(self.mapping["to"])
            for from_node in from_mapper.run(source_model, source_obj):
                for to_node in to_mapper.run(source_model, source_obj):
                    # skip self referencing dataflows
                    if from_node == to_node:
                        continue               
                    
                    dataflow = {}
                    dataflow["name"] = df_name
                    dataflow["type"] = df_type

                    if from_node in self.id_map:
                        from_node_id = self.id_map[from_node]
                    else:
                        from_node_id = str(uuid.uuid4())
                        self.id_map[from_node] = from_node_id

                    if to_node in self.id_map:
                        to_node_id = self.id_map[to_node]
                    else:
                        to_node_id = str(uuid.uuid4())
                        self.id_map[to_node] = to_node_id

                    dataflow["from_node"] = from_node_id
                    dataflow["to_node"] = to_node_id
                    dataflow["source"] = source_obj
                    if "properties" in self.mapping:
                        dataflow["properties"] = self.mapping["properties"]

                    source_id = source_model.search(self.mapping["id"], source=dataflow)
                    if not source_id in self.id_map:
                        df_id = str(uuid.uuid4())
                        self.id_map[source_id] = df_id
                    dataflow["id"] = df_id     

                    dataflows.append(dataflow)
        return dataflows
