import settings

from homie.node.simple import SimpleHomieNode
from homie.device import HomieDevice


def main():
    homie = HomieDevice(settings)

    node = SimpleHomieNode("nodetype", "node_property")

    homie.add_node(node)

    # run forever
    homie.start()


main()
