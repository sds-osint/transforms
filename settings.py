from maltego_trx.decorator_registry import TransformSetting

api_key_setting = TransformSetting(
    name="api_key", display_name="API Key", setting_type="string", global_setting=True
)

language_setting = TransformSetting(
    name="language",
    display_name="Language",
    setting_type="string",
    default_value="en",
    optional=True,
    popup=True,
)

deepl_auth_key = TransformSetting(name='deepl_auth_key',
                                    display_name="DeepL Auth Key",
                                    setting_type='string',
                                    default_value='',
                                    optional=False,
                                    popup=True)

ops_user = TransformSetting(name='ops_user',
                                    display_name="OpenPeopleSearch Username",
                                    setting_type='string',
                                    default_value='',
                                    optional=True,
                                    popup=True)

ops_pass = TransformSetting(name='ops_pass',
                                    display_name="OpenPeopleSearch Password",
                                    setting_type='string',
                                    default_value='',
                                    optional=True,
                                    popup=True)

ops_auth = TransformSetting(name='ops_auth',
                                    display_name="OpenPeopleSearch Auth Token",
                                    setting_type='string',
                                    default_value='',
                                    optional=False,
                                    popup=True)

language_input = TransformSetting(name='language_input',
                                    display_name="Language Input",
                                    setting_type='string',
                                    default_value='EN-US',
                                    optional=False,
                                    popup=True)

city_input = TransformSetting(name='city_input',
                                    display_name="City",
                                    setting_type='string',
                                    default_value='',
                                    optional=True,
                                    popup=True)

state_input = TransformSetting(name='state_input',
                                    display_name="State",
                                    setting_type='string',
                                    default_value='',
                                    optional=True,
                                    popup=True)

leakcheck_api = TransformSetting(name='leakcheck_api',
                                   display_name='Leakcheck API Key',
                                   setting_type='string',
                                   optional=False,
                                   popup=True)

pagination_count = TransformSetting(name='pagination_count',
                                    display_name="Number of Pages",
                                    setting_type='integer',
                                    default_value='10',
                                    optional=True,
                                    popup=True)