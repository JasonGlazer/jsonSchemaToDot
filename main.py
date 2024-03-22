import os
import json
import re
import random

nodes = set()

colors = ['black', 'blue', 'brown', 'cyan', 'darkred', 'firebrick', 'darkorange', 'darkviolet', 'green', 'turquoise', 'yellow']

def node_details(file, node):
    if node not in nodes:
        file.write('  ' + node + '[fontsize="32" shape="box" height="0.7"]\n')
        nodes.add(node)
    return


with open('ASHRAE229connection.gv', 'w') as gv_file:
# with open('ASHRAE229_RCT_project_connection.gv', 'w') as gv_file:
# with open('ASHRAE229_RCT_software_connection.gv', 'w') as gv_file:
# with open('Output2019ASHRAE901_connection.gv', 'w') as gv_file:
    gv_file.write('digraph G {\n')
    gv_file.write('    size="10, 10";\n')
    gv_file.write('    ranksep="1.4";\n')
    # gv_file.write('    rankdir=LR;\n')
    with open('ASHRAE229.schema.json') as json_file:
#    with open('RCT_project_output_test_report.schema.json') as json_file:
#    with open('RCT_software_output_test_report.schema.json') as json_file:
#    with open('Output2019ASHRAE901.schema.json') as json_file:
        schema = json.load(json_file)
        # print(json.dumps(schema, indent=4))
        definitions = schema['definitions']
        for data_group_name, data_group_contents in definitions.items():
            if data_group_contents['type'] == "object":
                # print('==========================================================')
                # print(data_group_name)
                data_elements = data_group_contents['properties']
                for data_element_name, fields in data_elements.items():
                    if "$ref" in fields:
                        if "Enumerations" not in fields["$ref"]:
                            ref = os.path.split(fields["$ref"])[-1]
                            if ref in definitions:
                                if "enum" not in definitions[ref]:
                                    # print(ref)
                                    gv_file.write('  {} -> {} [arrowhead=empty color="{}"]\n'.format(data_group_name, ref, random.choice(colors)))
                                    node_details(gv_file, data_group_name)
                                    node_details(gv_file, ref)
                            else:
                                print("Unconnected reference {} in {} of {}".format(ref, data_element_name, data_group_name))
                    if "items" in fields:
                        field_items = fields['items']
                        if "$ref" in field_items:
                            if "Enumerations" not in field_items["$ref"]:
                                ref = os.path.split(field_items["$ref"])[-1]
                                if ref in definitions:
                                    if "enum" not in definitions[ref]:
                                        # print(ref, '(list)')
                                        gv_file.write('  {} -> {} [color="{}"]\n'.format(data_group_name, ref, random.choice(colors)))
                                        # gv_file.write("  {} -> {}  [color=blue headlabel=\"head\" taillabel=\"tail\"  ]\n".format(data_group_name, ref))
                                        node_details(gv_file, data_group_name)
                                        node_details(gv_file, ref)
                                else:
                                    print("Unconnected reference {} in {} of {}".format(ref, data_element_name, data_group_name))
                    if "notes" in fields:
                        note = fields["notes"]
                        constraints = re.findall(r":[a-zA-Z]*:", note)
                        for constraint in constraints:
                            # print(data_element_name, constraint, constraint[1:-1])
                            constraint_strip = constraint[1:-1]
                            if constraint_strip in definitions:
#                                gv_file.write("  {} -> {} [color=red arrowhead=empty] \n".format(data_group_name, constraint_strip))
                                gv_file.write("  {} -> {} [style=dotted arrowhead=empty] \n".format(data_group_name, constraint_strip))
                                node_details(gv_file, data_group_name)
                                node_details(gv_file, constraint_strip)
                            else:
                                print("Unconnected constraint {} in {} of {}".format(constraint, data_element_name, data_group_name))
    gv_file.write('}\n')


            #print(json.dumps(data_group_contents, indent=4))


# at the command line running the following:
#    dot -Tpdf ASHRAE229connection.gv -o ASHRAE229connection.pdf
#    dot -Tpdf ASHRAE229_RCT_project_connection.gv -o ASHRAE229_RCT_project_connection.pdf
#    dot -Tpdf ASHRAE229_RCT_software_connection.gv -o ASHRAE229_RCT_software_connection.pdf
#    dot -Tpdf Output2019ASHRAE901_connection.gv -o Output2019ASHRAE901_connection.pdf