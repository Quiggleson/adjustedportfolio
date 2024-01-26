import json
import random
import numpy as np

# given a dict of field names and options
# and a number of properties
# return randomly genereated properties
def generate(attributes, count, value=[1000,2000]):

    # make list of properties
    properties = []

    # make a new property to match the count
    for i in range(count):

        # make property object
        property = {}

        # iterate keys
        for key in attributes:

            # index of the attribute value
            i = int(random.random()*len(attributes[key]))

            # add value to property
            property[key] = attributes[key][i]

        # add a random value in the given range
        val = int(random.random()*(value[1] - value[0]) + value[0])

        # add value to property
        property["value"] = val

        # add property to the list of properties
        properties.append(property)

    # return the randomly generated properties
    return properties
    
# given a dict of properties, return the dict with a new field for each property,
# con: which represents the dollar amount of that property's contribution to the total
# also given a dict of limits
def solve(properties: list[dict], limits):

    # return if empty
    if len(properties) == 0:
        return properties

    # check con field is not already defined
    if "con " in properties[0]:
        print(" warning: \"con\" field is already defined")

    # check if val field does not exist
    if "value" not in properties[0]:
        raise Exception("\"value\" field is undefined")

    # First, add con field
    # for i in range(len(properties)):
    for property in properties:
        property["con"] = property["value"]
        
    # flag to indicate change
    invalid = True

    # repeat until no changes
    while(invalid):

        # reset flag
        invalid = False

        # iterate attributes
        for attribute in [x for x in properties[0] if x != "value" and x != "con"]:

            # print(f'testing attr: {attribute}')

            # update properties for each attribute
            adj_properties = update_prop_attr(properties.copy(), attribute, limits[attribute])

        # get percs and check validity
        percs = get_percs(properties)

        # iterate attributes in percs
        for attr_key in percs:

            # get limit
            attr_limit = limits[attr_key]

            # iterate attr_vals
            for attr_val_key in percs[attr_key]:

                # if it's over the limit, reset the flag
                if percs[attr_key][attr_val_key] > attr_limit:

                    # print(f'{attr_key} {attr_val_key} is over limit {attr_limit}')

                    # reset the flag
                    invalid = True

    # return adjusted properties
    return properties

# helper func, optimize in terms of that attribute
# given properties and attribute, return the properties optimized to that attribute
def update_prop_attr(properties, attribute, limit):

    # get list of attribute values and their sums
    attr_vals = {}

    # iterate properties and add all values for the given attribute
    for property in properties:
        if property[attribute] not in attr_vals:
            attr_vals[property[attribute]] = property["con"]
        else:
            attr_vals[property[attribute]] += property["con"]

    # get adjusted attr_val
    adj_attr_val = adjust_attr(attr_vals.copy(), limit)

    # distribute change over properties
    for property in properties:

        # get the attribute value
        attr_val = property[attribute]

        # percentage change
        per = float(adj_attr_val[attr_val])/attr_vals[attr_val]

        # apply change to con
        property["con"] = int(property["con"] * per)

    # return updated properties
    return properties

# given a dict of attr_vals and their sums and limit
# return adjusted sums
def adjust_attr(attr_vals: dict, limit):
    # indicate change
    changed = True

    # loop until stable
    while (changed):

        # print(f'changing, current list: {attr_vals}')

        # set changed until proven otherwise
        changed = False

        # iterate sums
        for key in attr_vals:

            # get attr_sum from sums
            attr_sum = attr_vals[key]

            # get total
            total = sum(attr_vals.values())

            # if the attr_sum is greater than limit
            if attr_sum > limit * total:

                # get total not including current
                other_tot = total - attr_sum

                # readjust attr_sum according to formula
                attr_vals[key] = int(limit / (1-limit) * other_tot)

                # modify changed flag
                changed = True
        
    return attr_vals

# return a dict with given value and adjusted value
# requires "con" field
def get_total(properties):

    # keep track of sum
    sum = {
        "adj_sum": 0,
        "val_sum": 0
    }

    # iterate properties
    for property in properties:
        sum["adj_sum"] += property["con"]
        sum["val_sum"] += property["value"]

    # return sum
    return sum

# return the sums of each attribute value
# for the properties, counting the "con" field
def get_sums(properties):

    # attributes object
    attributes = {}

    # iterate properties - add raw sum to each 
    for property in properties:

        # iterate attributes keys
        for key in [x for x in property if x != "value" and x != "con"]:

            # if the key is not in attributes, add it
            if key not in attributes:

                attributes[key] = {}

            # if the attribute value is not there, add it
            if property[key] not in attributes[key]:

                # init with con sum
                attributes[key][property[key]] = property["con"]

            # otherwise increment it
            else:

                # add con sum
                attributes[key][property[key]] += property["con"]

    return attributes

# return the percentageso of each attribute value
def get_percs(properties):

    # get the total
    total = get_total(properties)["adj_sum"]

    # get sums object
    attributes = get_sums(properties)

    # iterate attributes
    for key in attributes:

        # iterate attr values
        for attr_val_key in attributes[key]:

            # update sum to percentage
            attributes[key][attr_val_key] /= total

            # round
            attributes[key][attr_val_key] = round(attributes[key][attr_val_key], 2)

    # return percentages
    return attributes

# example to generate random properties
attributes = {
    "tenant": [
        "A",
        "B",
        "C",
        "D"
    ],
    "geo": [
        "SW",
        "MW",
        "E",
        "W"
    ],
    "IG?": [
        "Y",
        "N"
    ]
}
value = [1000,5000]
count = 40
limits = {
    "tenant": .3,
    "geo": .3,
    "IG?": .6
}

# generate random properties
properties = generate(attributes, count, value)

# save properties to a json file
with open('./given.json', 'w+') as f:
    json.dump(properties, f)

# get adjusted properties
adj_properties = solve(properties, limits)

# save new properties
with open('./properties.json', 'w+') as f:
    json.dump(adj_properties, f)

print(f'portfolio values: {get_total(properties)}')

with open('./properties.json', 'r') as f:
    adj_properties = json.load(f)

sums = get_sums(adj_properties)

print(sums)

percs = get_percs(adj_properties)

print(percs)