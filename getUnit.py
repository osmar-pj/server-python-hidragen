from main import sdk

parametersUnit = {
    'spec': {
        'itemsType': 'avl_unit',
        'propName': 'sys_name',
        'propValueMask': '*',
        'sortType': 'sys_name',
    },
    'force': 0,
    'flags': 1,
    'from': 0,
    'to': 0
}
units = sdk.core_search_items(parametersUnit)
# sdk.logout()
