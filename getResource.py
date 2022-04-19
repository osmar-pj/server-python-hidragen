from main import sdk


parameterResource = {
    'spec': {
        'itemsType': 'avl_resource',
        'propName': 'sys_name',
        'propValueMask': '*',
        'sortType': 'sys_name',
    },
    'force': 0,
    'flags': 1,
    'from': 0,
    'to': 0
}
resources = sdk.core_search_items(parameterResource)
# sdk.logout()
