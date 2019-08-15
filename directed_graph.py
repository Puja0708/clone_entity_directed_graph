import sys
import random
import simplejson as json


class DirectedGraph(object):

    def __init__(self, json_representation):
        self.representation = json_representation

    def get_entity_by_id(self, entity_id):  # make it global or a property
        """
        :param entity_id:
        :return: the entity dict for the matched entity id or None (if not found)
        """
        for i in self.get_entity_dict():
            if i['entity_id'] == entity_id:
                return i
        return None  # the given entity id does not exist

    def get_entity_dict(self):
        """
        :return: entities dict for the given graph
        """

        return self.representation.get("entities", {})

    def get_links_dict(self):
        """
        :return: links dict of the given graph
        """

        return self.representation.get("links", {})

    def get_new_entity_id(self):
        """
        :return: a random new/ unique entity id for the graph, i.e., an entity id not already present in the graph
        (currently, can only work for graphs < 100 nodes)
        """
        existing_entity_ids = self.get_all_entity_ids()
        new_entity_id = None
        while new_entity_id in existing_entity_ids or new_entity_id is None:
            new_entity_id = random.randrange(1, 100)  # keeping it 100 for now, ideally,
            # for really big graphs this should be a bigger number,
            # basically bigger than the total number of nodes in the graph
        return new_entity_id

    def get_from_nodes_for_entity(self, entity_id):
        """
        :param entity_id:
        :return: get all the nodes of the graph which have a path to a given node
        """
        edges = self.get_links_dict()
        return [i['from'] for i in edges if i['to'] == entity_id]

    def get_to_nodes_for_entity(self, entity_id):
        """
        :param entity_id:
        :return: get all the nodes of the graph which have a path from a given node
        """
        edges = self.get_links_dict()
        return [i['to'] for i in edges if i['from'] == entity_id]

    def get_all_entity_ids(self):
        return set([i['entity_id'] for i in self.get_entity_dict()])

    def clone_entity_by_id(self, entity_id):
        from_entities = self.get_from_nodes_for_entity(entity_id)
        to_entities = self.get_to_nodes_for_entity(entity_id)

        given_entity = self.get_entity_by_id(entity_id)
        new_entity = dict(entity_id=self.get_new_entity_id(),
                          name=given_entity['name'],
                          description=given_entity.get('description'))  # links will be modified
        self.representation['entities'].append(new_entity)

        # clone all the to and from nodes
        for entity_id in from_entities:
            # modify graph
            entity = self.get_entity_by_id(entity_id)
            new_from_entity = dict(entity_id=self.get_new_entity_id(),
                                   name=entity['name'],
                                   description=entity.get('description'))
            self.representation['entities'].append(new_from_entity)
            self.representation["links"].append({"from": new_from_entity['entity_id'],
                                                 "to": new_entity['entity_id']})

        for entity_id in to_entities:
            entity = self.get_entity_by_id(entity_id)
            new_to_entity = dict(entity_id=self.get_new_entity_id(),
                                 name=entity['name'],
                                 description=entity.get('description'))
            self.representation['entities'].append(new_to_entity)
            self.representation["links"].append({"from": new_entity['entity_id'],
                                                 "to": new_to_entity['entity_id']})

        return new_entity


def get_json_content_from_file(file_location):
    """
    :param file_location:
    :return:  utility function to extract json from a given json file
    """
    if not file_location.endswith('.json'):
        raise ValueError('Please enter a valid json file only')
    with open(file_location) as json_file:
        data = json.load(json_file)
        return data


if __name__ == "__main__":
    json_file_location = sys.argv[0]
    initial_entity_id = sys.argv[1]

    json_data = get_json_content_from_file(json_file_location)
    graph = DirectedGraph(json_data)
    initial_entity = graph.get_entity_by_id(int(initial_entity_id))
    if not initial_entity:
        raise ValueError('invalid entity id passed, please try again with a valid entity id')
    graph.clone_entity_by_id(initial_entity_id)
