from directed_graph import DirectedGraph

sample_dict = {
    "entities": [{
        "entity_id": 3,
        "name": "EntityA"
    }, {
        "entity_id": 5,
        "name": "EntityB"
    }, {
        "entity_id": 7,
        "name": "EntityC",
        "description": "More details about entity C"
    }, {
        "entity_id": 11,
        "name": "EntityD"
    }],
    "links": [{
        "from": 3,
        "to": 5
    }, {
        "from": 3,
        "to": 7
    }, {
        "from": 5,
        "to": 7
    }, {
        "from": 7,
        "to": 11
    }]
}

initial_number_of_entities = len(sample_dict['entities'])
initial_number_of_links = len(sample_dict['links'])


def test_given_case():
    graph = DirectedGraph(sample_dict)
    graph.clone_entity_by_id(5)
    assert initial_number_of_entities < len(graph.representation['entities'])
    assert initial_number_of_links < len(graph.representation['links'])


def test_given_entity_doesnt_exist():
    graph = DirectedGraph(sample_dict)
    assert graph.get_entity_by_id(graph.get_new_entity_id()) is None


def test_graph_with_loops():
    graph = DirectedGraph(sample_dict)
    graph.clone_entity_by_id(5)
    length_of_links_without_loop = len(graph.representation['links'])

    sample_dict_modified = {
        "entities": [{
            "entity_id": 3,
            "name": "EntityA"
        }, {
            "entity_id": 5,
            "name": "EntityB"
        }, {
            "entity_id": 7,
            "name": "EntityC",
            "description": "More details about entity C"
        }, {
            "entity_id": 11,
            "name": "EntityD"
        }],
        "links": [{
            "from": 3,
            "to": 5
        }, {
            "from": 3,
            "to": 7
        }, {
            "from": 5,
            "to": 7
        }, {
            "from": 7,
            "to": 11
        },
            {
                "from": 5,
                "to": 3
            }
        ]
    }

    graph = DirectedGraph(sample_dict_modified)
    graph.clone_entity_by_id(5)
    length_of_links_with_loop = len(graph.representation['links'])
    assert length_of_links_without_loop == length_of_links_with_loop  # no extra links created because of loop


if __name__ == "__main__":
    test_given_case()
    test_given_entity_doesnt_exist()
    test_graph_with_loops()
