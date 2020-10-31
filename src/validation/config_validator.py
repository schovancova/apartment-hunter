"""Config validator"""


def validate_config(config, definition):
    """Validate config file"""
    error_msgs = []
    for item, fields in definition.items():
        # do not check for correctness if disabled
        if not config.has_section(item) or config[item]["enable"] == "false":
            continue
        for (key, value) in fields.items():
            validator = definition[item][key]
            try:
                validator.validate(config.get(item, key, fallback=None))
            except ValueError as ex:
                error_msgs.append(f"Config {item}: key {key} : {str(ex)}")
    # check for unrecognized sections and keys in config
    for item in config.sections():
        for (key, value) in config.items(item):
            if not definition.get(item) or not definition[item].get(key):
                error_msgs.append(f"Config {item}: Unrecognized config key: {key}")
    if error_msgs:
        exit("\n".join(error_msgs))
