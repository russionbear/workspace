# strategy_map_type = {
#     'type': 'background',
#     'lastUrl': r'E:\TMP\OIP-C.jpg',
#     'editSize': (800, 600)
# }
"""
type : pass, key, action


keyName

duration
merged
rows
cols
collideRect
"""

# order
# root key: usage

strategy_map_type = {
    'type': 'block',
    'winSize': (800, 600),
    'mapSize': (1000, 600),
    'blockSize': (40, 40),
    'font_path': '',

    # 'testStructureForSource': {
    #
    # },
    'sourceDir': {
        'geo': {
            '__guard': {"key": {"keyName": "name"}},
            "tree": {
                "__guard": {"key": {"keyName": 'action'}},
                "wave1": {
                    "__guard": {"action", {"duration": 1.2, "amount": 12, "beginColor": (255, 0, 0), "endColor": (255, 0, 50), 'fontColor': (255, 255, 255), 'fontSize': 20}},
               }
            }
        },
        "unit": {
            "__guard": {"key": {"keyName": "flag"}},
            "red": {
                '__guard': {"key": {"keyName": "name"}},
                "footman": {
                    "__guard": {"key": {"keyName": 'action'}},
                    "left": {
                        "__guard": {"action", {"duration": 1.2, "amount": 12, "beginColor": (255, 0, 0), "endColor": (255, 0, 50)}},
                    },
                    "right": {
                        "__guard": {"action", {"duration": 1.2, "amount": 12, "beginColor": (100, 0, 0), "endColor": (100, 0, 50)}},
                   }
                }
            }
        }
    },
    "musicDir": ""
    # 'layer': {
    #     "geo": {
    #         "level": 0,
    #         "limitation": {
    #
    #         },
    #         "attribute": [],
    #     },
    #     "resource": {
    #         "oil": {}
    #     }
    # }
}

