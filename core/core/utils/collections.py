def deep_update(base_dict, update_with):
    # Iterate over each item in the new dict
    for key, value in update_with.items():
        
        # If the value is a dict
        if isinstance(value, dict):
            base_dict_value = base_dict.get(key)

            # If the original value is also a dict then 
            # run it through this same function (recursive)
            if isinstance(base_dict_value, dict):
                deep_update(base_dict_value, value)
            # If the original value is NOT a dict then just set the new value
            else:
                base_dict[key] = value
                
        # If the new value is NOT a dict
        else:
            base_dict[key] = value
    
    return base_dict