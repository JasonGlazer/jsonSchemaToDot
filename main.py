import os
import json
import re


with open('ASHRAE229connection.gv', 'w') as gv_file:
    gv_file.write('digraph G {\n')
    gv_file.write('    size="7.5, 20";\n')
    gv_file.write('    rankdir=LR;\n')
    with open('ASHRAE229.schema.json') as json_file:
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
                                    gv_file.write("  {} -> {}\n".format(data_group_name, ref))
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
                                        gv_file.write("  {} -> {}\n".format(data_group_name, ref))
                                else:
                                    print("Unconnected reference {} in {} of {}".format(ref, data_element_name, data_group_name))
                    if "notes" in fields:
                        note = fields["notes"]
                        constraints = re.findall(r":[a-zA-Z]*:", note)
                        for constraint in constraints:
                            # print(data_element_name, constraint, constraint[1:-1])
                            constraint_strip = constraint[1:-1]
                            if constraint_strip in definitions:
                                gv_file.write("  {} -> {} [color=red] \n".format(data_group_name, constraint_strip))
                            else:
                                print("Unconnected constraint {} in {} of {}".format(constraint, data_element_name, data_group_name))
    gv_file.write('}\n')


            #print(json.dumps(data_group_contents, indent=4))


# at the command line running the following:
#    dot -Tpdf ASHRAE229connection.gv -o ASHRAE229connection.pdf