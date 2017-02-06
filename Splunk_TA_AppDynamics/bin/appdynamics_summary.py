import splunk_ta_appdynamics_declare

import os
import sys
import time
import datetime

import modinput_wrapper.base_modinput
from solnlib.packages.splunklib import modularinput as smi



import input_module_appdynamics_summary as input_module


'''
    Do not edit this file!!!
    This file is generated by Add-on builder automatically.
    Add your modular input logic to file input_module_appdynamics_summary.py
'''
class ModInputappdynamics_summary(modinput_wrapper.base_modinput.BaseModInput):

    def __init__(self):
        if 'use_single_instance_mode' in dir(input_module):
            use_single_instance = input_module.use_single_instance_mode()
        else:
            use_single_instance = False
        super(ModInputappdynamics_summary, self).__init__("splunk_ta_appdynamics", "appdynamics_summary", use_single_instance)
        self.global_checkbox_fields = None

    def get_scheme(self):
        """overloaded splunklib modularinput method"""
        scheme = super(ModInputappdynamics_summary, self).get_scheme()
        scheme.title = ("AppDynamics Summary")
        scheme.description = ("Collect Overall Application, Business Transaction, Infrastructure Performance metrics and Application Events as well as Health Rule Violations from AppDynamics.")
        scheme.use_external_validation = True
        scheme.streaming_mode_xml = True

        scheme.add_argument(smi.Argument("name", title="Name",
                                         description="",
                                         required_on_create=True))

        """
        For customized inputs, hard code the arguments here to hide argument detail from users.
        For other input types, arguments should be get from input_module. Defining new input types could be easier.
        """
        scheme.add_argument(smi.Argument("host_port", title="AppD Collector URL",
                                         description="Enter the URL and Port for your AppDynamics Collector",
                                         required_on_create=True,
                                         required_on_edit=False))
        scheme.add_argument(smi.Argument("auth_token", title="Authorization Token",
                                         description="For a single tenant controller use the output of.: echo -n \'<user>@customer1:<password>\' | base64\'for multi-tenant controller use the output of:echo -n \'<user>@<accountname>:<password>\' | base64\'",
                                         required_on_create=True,
                                         required_on_edit=False))
        scheme.add_argument(smi.Argument("duration", title="Time Duration (in minutes)",
                                         description="The time period (in minutes) that you wish to retrieve data for.  e.g.:  5 = retrieve data for the past 5 minutes.",
                                         required_on_create=True,
                                         required_on_edit=False))
        scheme.add_argument(smi.Argument("app_name", title="Application Name (optional)",
                                         description="Leave this blank to retrieve data for ALL applications in AppDynamics.  If you only want a single application, enter that application\'s name here.",
                                         required_on_create=False,
                                         required_on_edit=False))
        return scheme

    def get_app_name(self):
        return "Splunk_TA_AppDynamics"

    def validate_input(self, definition):
        """validate the input stanza"""
        input_module.validate_input(self, definition)

    def collect_events(self, ew):
        """write out the events"""
        input_module.collect_events(self, ew)

    def get_account_fields(self):
        account_fields = []
        return account_fields

    def get_checkbox_fields(self):
        checkbox_fields = []
        return checkbox_fields

    def get_global_checkbox_fields(self):
        if self.global_checkbox_fields is None:
            checkbox_fields = []
            customized_settings = {u'parameters': [{u'required': True, u'type': u'text', u'label': u'AppD Collector URL', u'default_value': u'', u'format_type': u'text', u'help_string': u'Enter the URL and Port for your AppDynamics Collector', u'placeholder': u'http://demo.appdynamics.com:8090', u'name': u'host_port'}, {u'required': True, u'type': u'text', u'label': u'Authorization Token', u'default_value': u'', u'format_type': u'text', u'help_string': u"For a single tenant controller use the output of.: \necho -n '<user>@customer1:<password>' | base64'\n\nfor multi-tenant controller use the output of:\necho -n '<user>@<accountname>:<password>' | base64'\n", u'placeholder': u"echo -n '<user>@customer1:<password>' | base64'", u'name': u'auth_token'}, {u'required': True, u'type': u'text', u'label': u'Time Duration (in minutes)', u'default_value': u'5', u'format_type': u'text', u'help_string': u'The time period (in minutes) that you wish to retrieve data for.  e.g.:  5 = retrieve data for the past 5 minutes.', u'placeholder': u'', u'name': u'duration'}, {u'required': False, u'type': u'text', u'label': u'Application Name (optional)', u'default_value': u'', u'format_type': u'text', u'help_string': u"Leave this blank to retrieve data for ALL applications in AppDynamics.  If you only want a single application, enter that application's name here.", u'placeholder': u'', u'name': u'app_name'}], u'code': u'\n# encoding = utf-8\n\nimport os\nimport sys\nimport time\nimport datetime\n\n\'\'\'\n    IMPORTANT\n    Edit only the validate_input and collect_events functions.\n    Do not edit any other part in this file.\n    This file is generated only once when creating the modular input.\n\'\'\'\n\'\'\'\n# For advanced users, if you want to create single instance mod input, uncomment this method.\ndef use_single_instance_mode():\n    return True\n\'\'\'\n\ndef validate_input(helper, definition):\n    """Implement your own validation logic to validate the input stanza configurations"""\n    # This example accesses the modular input variable\n    # host_port = definition.parameters.get(\'host_port\', None)\n    # auth_token = definition.parameters.get(\'auth_token\', None)\n    # duration = definition.parameters.get(\'duration\', None)\n    # app_name = definition.parameters.get(\'app_name\', None)\n    pass\n\ndef collect_events(helper, ew):\n    #Implement your data collection logic here\n\n\n    import HTMLParser\n    import json\n    import urllib\n    import requests\n\n\n    \'\'\'\n    Variable declarations and initializations\n    \'\'\'\n\n    #  Process each account input in inputs.conf separately\n    #  Get the properties for each input (stanzas in inputs.conf)\n    stanzas = helper.input_stanzas\n    for stanza_name in stanzas:\n        opt_host_port   = helper.get_arg(\'host_port\')\n        opt_auth_token  = helper.get_arg(\'auth_token\')\n        opt_duration    = helper.get_arg(\'duration\')\n        opt_app_name    = helper.get_arg(\'app_name\')\n        #helper.log_info(\' = \'.join([\'opt_app_name\', str(opt_app_name)]))\n        idx = helper.get_output_index()\n        st = helper.get_sourcetype()\n\n        # If there are more than 1 input of this type, the arguments will be in a dictionary so grab them out\n        if type(opt_auth_token) == dict:\n            opt_host_port   = opt_host_port[stanza_name]\n        if type(opt_auth_token) == dict:\n            opt_auth_token  = opt_auth_token[stanza_name]\n        if type(opt_duration) == dict:\n            opt_duration    = opt_duration[stanza_name]\n        if type(idx) == dict:\n            idx = idx[stanza_name]\n        if type(st) == dict:\n            st = st[stanza_name]\n\n        #  app_name is optional so we need to account for the fact that it may not exist\n        if type(opt_app_name) == dict:\n            opt_app_name = opt_app_name[stanza_name]\n\n        #headers = {\'Authorization\':\'Basic YmFzaWNAY3VzdG9tZXIxOnczbGNvbWU=\'}\n        headers =  {\'Authorization\': \'Basic {}\'.format(opt_auth_token)}\n        parameters = "output=JSON&time-range-type=BEFORE_NOW&duration-in-mins=" + opt_duration\n        api_url = opt_host_port + "/controller/rest/applications"\n\n    \'\'\'\n    End of Variable declarations and initializations\n    \'\'\'\n\n    \n    # Remove any metric elements that have a metricName of \'METRIC DATA NOT FOUND\'\n    def del_empty_items(d):\n        for key, val in d.items():\n            if isinstance(val, list):\n                for i in reversed(range(len(val))):\n                    if val[i].get(\'metricName\') == "METRIC DATA NOT FOUND":\n                        val.pop(i)\n        return\n\n\n    def parse_piped_naming(d):\n        for key, val in d.items():  \n            #  let\'s parse out the metricPath from into component parts.  This will make our lives a little easier in Splunk ;-).\n            if isinstance(val, list):\n                for metrics in val:\n                    for key2, val2 in metrics.items():\n                        if key2 == "metricPath":\n                            parts = val2.split("|")\n                            for i in range(len(parts)):\n                                partName = "path-part-" + str(i+1)\n                                metrics[partName] = "{}".format(parts[i])\n        return\n\n\n\n    \n    #  get the list of all applications so that we can add app_id and app_name to the event.\n    #  This enables us to build a url back into AppDynamics.\n    def get_application_list():\n        response = helper.send_http_request(api_url, "GET", headers=headers,  parameters=parameters, payload=None, cookies=None, verify=None, cert=None, timeout=None, use_proxy=True)\n\n        # check the response status, if the status is not sucessful, raise requests.HTTPError\n        r_status = response.status_code\n        response.raise_for_status()\n        application_list = response.json()\n        return application_list;\n\n\n    # Given an application name, let\'s find it\'s ID\n    def get_app_id(app_name):\n        for app in application_list:\n            if app["name"] == app_name:\n                return app[\'id\'];\n        return -1;\n\n\n    # Execute a REST API Call to get data for a single application\n    # Example url = "https://host:port/controller/rest/applications/<app_name>/metric-data?metric-path=Business Transaction Performance|*|*|*|*"\n    def get_api_data(app_id, app_name, url, params, key_name):\n        response = helper.send_http_request(url, "GET", headers=headers,  parameters=params, payload=None, cookies=None, verify=None, cert=None, timeout=None, use_proxy=True)\n\n        # check the response status, if the status is not sucessful, raise requests.HTTPError\n        r_status = response.status_code\n        response.raise_for_status()\n\n        # get the response data\n        r_json = response.json()\n        \n        # if there\'s no data, let\'s just stop right here and move to the next one.\n        if not r_json:\n            return;\n\n\n        #  add the application ID & Name to the event so we can link back to AppDynamics in the UI\n        app_dict =  {\'application_name\': \'{}\'.format(app_name), \'application_id\' : app_id }\n        app_dict[key_name] = r_json\n        data = json.loads(json.dumps(app_dict))\n \n        #  if there are empty elements, let\'s get rid of those.\n        del_empty_items(data)\n        #parse_piped_naming(data)\n\n        \n        #   Now write the event to Splunk\n        event = helper.new_event(source=key_name, index=idx, sourcetype=st, data=json.dumps(data,sort_keys=True))\n        try:\n            ew.write_event(event)\n        except Exception as e:\n            raise e\n        return;\n\n\n    # This is where we define what data we would like ot pull back from Appdynamics\n    def get_app_metrics(app_id, app_name):\n        helper.log_info("processing app_id:" + app_id + "    app_name:" + app_name)\n\n        # Application Infrastructure Performance Metrics\n        api_url = opt_host_port + "/controller/rest/applications/" + app_name + "/metric-data"\n        params  = parameters + "&metric-path=Application Infrastructure Performance|*|*|*|*"\n        get_api_data( app_id, app_name, api_url, params, "infrastructure_performance" )\n\n        # Overall Application Performance Metrics\n        api_url = opt_host_port + "/controller/rest/applications/" + app_name + "/metric-data"\n        params  = parameters + "&metric-path=Overall Application Performance|*"\n        get_api_data( app_id, app_name, api_url, params, "application_performance" )\n\n        # Busienss Transaction Metrics\n        api_url = opt_host_port + "/controller/rest/applications/" + app_name + "/metric-data"\n        params  = parameters + "&metric-path=Business Transaction Performance|*|*|*|*"\n        get_api_data( app_id, app_name, api_url, params, "business_transactions" )\n\n        # Healthrule Violations\n        api_url = opt_host_port + "/controller/rest/applications/" + app_name + "/problems/healthrule-violations"\n        params  = parameters\n        get_api_data( app_id, app_name, api_url, params, "healthrule_violations" )\n\n        # Application Event \n        api_url = opt_host_port + "/controller/rest/applications/" + app_name + "/events"\n        params  = parameters + "&event-types=APPLICATION_ERROR,DIAGNOSTIC_SESSION&severities=INFO,WARN,ERROR"\n        get_api_data( app_id, app_name, api_url, params, "application_events" )\n\n        return;\n\n\n    \'\'\'\n    Begin processing logic\n    \'\'\'\n    # Get a list of all applications in AppDynamics\n    application_list = get_application_list()\n\n    # Are we getting data for ALL applications or one specific app?      (does the input specify an app name?)\n    if (opt_app_name is None ):\n        # We want to grab all data for all applications in AppDynamics\n        for app in application_list:\n            get_app_metrics(str(app[\'id\']),str(app[\'name\']))\n    else:\n        #  We want 1 specific application from AppDynamics\n        app_id = str(get_app_id(opt_app_name))\n        get_app_metrics(app_id, opt_app_name)\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n    """\n    # The following examples get the arguments of this input.\n    # Note, for single instance mod input, args will be returned as a dict.\n    # For multi instance mod input, args will be returned as a single value.\n    opt_host_port = helper.get_arg(\'host_port\')\n    opt_auth_token = helper.get_arg(\'auth_token\')\n    opt_duration = helper.get_arg(\'duration\')\n    opt_app_name = helper.get_arg(\'app_name\')\n    # In single instance mode, to get arguments of a particular input, use\n    opt_host_port = helper.get_arg(\'host_port\', stanza_name)\n    opt_auth_token = helper.get_arg(\'auth_token\', stanza_name)\n    opt_duration = helper.get_arg(\'duration\', stanza_name)\n    opt_app_name = helper.get_arg(\'app_name\', stanza_name)\n\n    # get input type\n    helper.get_input_type()\n\n    # The following examples get input stanzas.\n    # get all detailed input stanzas\n    helper.get_input_stanza()\n    # get specific input stanza with stanza name\n    helper.get_input_stanza(stanza_name)\n    # get all stanza names\n    helper.get_input_stanza_names()\n\n    # The following examples get options from setup page configuration.\n    # get the loglevel from the setup page\n    loglevel = helper.get_log_level()\n    # get proxy setting configuration\n    proxy_settings = helper.get_proxy()\n    # get user credentials\n    account = helper.get_user_credential_by_username("username")\n    account = helper.get_user_credential_by_id("account id")\n    # get global variable configuration\n    global_userdefined_global_var = helper.get_global_setting("userdefined_global_var")\n\n    # The following examples show usage of logging related helper functions.\n    # write to the log for this modular input using configured global log level or INFO as default\n    helper.log("log message")\n    # write to the log using specified log level\n    helper.log_debug("log message")\n    helper.log_info("log message")\n    helper.log_warning("log message")\n    helper.log_error("log message")\n    helper.log_critical("log message")\n    # set the log level for this modular input\n    # (log_level can be "debug", "info", "warning", "error" or "critical", case insensitive)\n    helper.set_log_level(log_level)\n\n    # The following examples send rest requests to some endpoint.\n    response = helper.send_http_request(url, method, parameters=None, payload=None,\n                                        headers=None, cookies=None, verify=True, cert=None,\n                                        timeout=None, use_proxy=True)\n    # get the response headers\n    r_headers = response.headers\n    # get the response body as text\n    r_text = response.text\n    # get response body as json. If the body text is not a json string, raise a ValueError\n    r_json = response.json()\n    # get response cookies\n    r_cookies = response.cookies\n    # get redirect history\n    historical_responses = response.history\n    # get response status code\n    r_status = response.status_code\n    # check the response status, if the status is not sucessful, raise requests.HTTPError\n    response.raise_for_status()\n\n    # The following examples show usage of check pointing related helper functions.\n    # save checkpoint\n    helper.save_check_point(key, state)\n    # delete checkpoint\n    helper.delete_check_point(key)\n    # get checkpoint\n    state = helper.get_check_point(key)\n\n    # To create a splunk event\n    helper.new_event(data, time=None, host=None, index=None, source=None, sourcetype=None, done=True, unbroken=True)\n    """\n\n    \'\'\'\n    # The following example writes a random number as an event. (Multi Instance Mode)\n    # Use this code template by default.\n    import random\n    data = str(random.randint(0,100))\n    event = helper.new_event(source=helper.get_input_type(), index=helper.get_output_index(), sourcetype=helper.get_sourcetype(), data=data)\n    ew.write_event(event)\n    \'\'\'\n\n    \'\'\'\n    # The following example writes a random number as an event for each input config. (Single Instance Mode)\n    # For advanced users, if you want to create single instance mod input, please use this code template.\n    # Also, you need to uncomment use_single_instance_mode() above.\n    import random\n    input_type = helper.get_input_type()\n    for stanza_name in helper.get_input_stanza_names():\n        data = str(random.randint(0,100))\n        event = helper.new_event(source=input_type, index=helper.get_output_index(stanza_name), sourcetype=helper.get_sourcetype(stanza_name), data=data)\n        ew.write_event(event)\n    \'\'\'\n', 'sourcetype': u'appdynamics_summary', u'data_inputs_options': [{u'description': u'Enter the URL and Port for your AppDynamics Collector', u'type': u'customized_var', u'default_value': u'', u'format_type': u'text', u'required_on_create': True, u'title': u'AppD Collector URL', u'placeholder': u'http://demo.appdynamics.com:8090', u'required_on_edit': False, u'name': u'host_port'}, {u'description': u"For a single tenant controller use the output of.: \necho -n '<user>@customer1:<password>' | base64'\n\nfor multi-tenant controller use the output of:\necho -n '<user>@<accountname>:<password>' | base64'\n", u'type': u'customized_var', u'default_value': u'', u'format_type': u'text', u'required_on_create': True, u'title': u'Authorization Token', u'placeholder': u"echo -n '<user>@customer1:<password>' | base64'", u'required_on_edit': False, u'name': u'auth_token'}, {u'description': u'The time period (in minutes) that you wish to retrieve data for.  e.g.:  5 = retrieve data for the past 5 minutes.', u'type': u'customized_var', u'default_value': u'5', u'format_type': u'text', u'required_on_create': True, u'title': u'Time Duration (in minutes)', u'placeholder': u'', u'required_on_edit': False, u'name': u'duration'}, {u'description': u"Leave this blank to retrieve data for ALL applications in AppDynamics.  If you only want a single application, enter that application's name here.", u'type': u'customized_var', u'default_value': u'', u'format_type': u'text', u'required_on_create': False, u'title': u'Application Name (optional)', u'placeholder': u'', u'required_on_edit': False, u'name': u'app_name'}], u'name': u'appdynamics_summary', 'streaming_mode_xml': True, 'interval': u'300', u'type': u'customized', u'title': u'AppDynamics Summary', u'description': u'Collect Overall Application, Business Transaction, Infrastructure Performance metrics and Application Events as well as Health Rule Violations from AppDynamics.', 'use_external_validation': True, u'is_loaded': True, u'customized_options': [{u'value': u'http://se-demo-east.demo.appdynamics.com:8090', u'name': u'host_port'}, {u'value': u'YmFzaWNAY3VzdG9tZXIxOnczbGNvbWU=', u'name': u'auth_token'}, {u'value': u'5', u'name': u'duration'}, {u'value': u'Order-Execution', u'name': u'app_name'}], u'sample_count': u'15', u'uuid': u'67933a0f1f714c068face951dee70ac6', 'index': u'default'}.get('global_settings', {}).get('customized_settings', [])
            for global_var in customized_settings:
                if global_var.get('type', '') == 'checkbox':
                    checkbox_fields.append(global_var['name'])
            self.global_checkbox_fields = checkbox_fields
        return self.global_checkbox_fields

if __name__ == "__main__":
    exitcode = ModInputappdynamics_summary().run(sys.argv)
    sys.exit(exitcode)
