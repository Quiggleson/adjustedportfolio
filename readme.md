# Algorithm to adjust portfolio value based on given attribute limits

To generate random properties, define attributes, a range for value, and a count:

```py
# define attributes
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

# define a range for property value
value = [1000,5000]

# define how many properties needed
count = 40

# generate the properties
properties = generate(attributes, count, value)
```

To get the adjusted property value, first define attribute limits then call the appropriate function:

```py

# set attribute limits - no single value for each attribute will contribute more than the limit to the total portfolio value
limits = {
    "tenant": .3,
    "geo": .3,
    "IG?": .6
}

# get adjusted properties object - same as old object with new "con" field to indicate raw value contribution to new total
adj_properties = solve(properties, limits)

```

Some additional functions are defined:

```py

# after running solve(), get the total portfolio value
get_total(adj_properties)

# after running solve(), get the dollar contribution by each value for each attribute
sums = get_sums(adj_properties)

# after running solve(), get the percentage contribution by each value for each attribute
percs = get_percs(adj_properties)
```