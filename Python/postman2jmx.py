import json
import re
import sys
import logging
import os
import argparse

logging.basicConfig(level=logging.INFO)

########### Global Declarations #########
variablefile = None
globalvariablefile = None
itr_jmx = ''
itr_final_jmx = ''

baseline_jmx = """
<?xml version="1.0" encoding="UTF-8"?>
<jmeterTestPlan version="1.2" properties="5.0" jmeter="5.2.1">
    <hashTree>
        <TestPlan guiclass="TestPlanGui" testclass="TestPlan" testname="JMeter Test Plan" enabled="true">
            <stringProp name="TestPlan.comments"></stringProp>
            <boolProp name="TestPlan.functional_mode">false</boolProp>
            <boolProp name="TestPlan.serialize_threadgroups">false</boolProp>
            <elementProp name="TestPlan.user_defined_variables" elementType="Arguments" guiclass="ArgumentsPanel" testclass="Arguments" testname="User Defined Variables" enabled="true">
                <collectionProp name="Arguments.arguments"/>
            </elementProp>
            <stringProp name="TestPlan.user_define_classpath"></stringProp>
        </TestPlan>
        <hashTree>
            <CacheManager guiclass="CacheManagerGui" testclass="CacheManager" testname="HTTP Cache Manager" enabled="true">
                <boolProp name="clearEachIteration">true</boolProp>
                <boolProp name="useExpires">true</boolProp>
                <boolProp name="CacheManager.controlledByThread">false</boolProp>
            </CacheManager>
            <hashTree/>
            <Arguments guiclass="ArgumentsPanel" testclass="Arguments" testname="User Defined Variables - EDIT ALL VARIABLES HERE!" enabled="true">
                <collectionProp name="Arguments.arguments">
                    <elementProp name="THREADS" elementType="Argument">
                        <stringProp name="Argument.name">THREADS</stringProp>
                        <stringProp name="Argument.value">10</stringProp>
                        <stringProp name="Argument.metadata">=</stringProp>
                        <stringProp name="Argument.desc">Change as per requirement</stringProp>
                    </elementProp>
                    <elementProp name="THREADS_RAMPUP_TIME" elementType="Argument">
                        <stringProp name="Argument.name">THREADS_RAMPUP_TIME</stringProp>
                        <stringProp name="Argument.value">10</stringProp>
                        <stringProp name="Argument.desc">Value in seconds - Change as per requirement</stringProp>
                        <stringProp name="Argument.metadata">=</stringProp>
                    </elementProp>
                    <elementProp name="START_TPS" elementType="Argument">
                        <stringProp name="Argument.name">START_TPS</stringProp>
                        <stringProp name="Argument.value">5</stringProp>
                        <stringProp name="Argument.metadata">=</stringProp>
                        <stringProp name="Argument.desc">Change as per requirement</stringProp>
                    </elementProp>
                    <elementProp name="END_TPS" elementType="Argument">
                        <stringProp name="Argument.name">END_TPS</stringProp>
                        <stringProp name="Argument.value">5</stringProp>
                        <stringProp name="Argument.metadata">=</stringProp>
                        <stringProp name="Argument.desc">Change as per requirement</stringProp>
                    </elementProp>
                    <elementProp name="TEST_DURATION" elementType="Argument">
                        <stringProp name="Argument.name">TEST_DURATION</stringProp>
                        <stringProp name="Argument.value">60</stringProp>
                        <stringProp name="Argument.metadata">=</stringProp>
                        <stringProp name="Argument.desc">Value in seconds - Change as per requirement</stringProp>
                    </elementProp>
                    MY-POSTMAN-VARIABLE
                </collectionProp>
                <stringProp name="TestPlan.comments">EDIT ALL VARIABLES HERE!</stringProp>
            </Arguments>
            <hashTree/>
            <ResponseAssertion guiclass="AssertionGui" testclass="ResponseAssertion" testname="Global Response Assertion" enabled="true">
                <collectionProp name="Asserion.test_strings">
                    <stringProp name="1538630">20\d</stringProp>
                </collectionProp>
                <stringProp name="Assertion.custom_message"></stringProp>
                <stringProp name="Assertion.test_field">Assertion.response_code</stringProp>
                <boolProp name="Assertion.assume_success">false</boolProp>
                <intProp name="Assertion.test_type">2</intProp>
            </ResponseAssertion>
            <hashTree/>
            <kg.apc.jmeter.timers.VariableThroughputTimer guiclass="kg.apc.jmeter.timers.VariableThroughputTimerGui" testclass="kg.apc.jmeter.timers.VariableThroughputTimer" testname="LOAD / SOAK TEST - Throughput Shaping Timer" enabled="true">
                <collectionProp name="load_profile">
                    <collectionProp name="731866749">
                        <stringProp name="1606799354">${START_TPS}</stringProp>
                        <stringProp name="779619553">${END_TPS}</stringProp>
                        <stringProp name="-1857560941">${TEST_DURATION}</stringProp>
                    </collectionProp>
                </collectionProp>
            </kg.apc.jmeter.timers.VariableThroughputTimer>
            <hashTree/>
            <kg.apc.jmeter.timers.VariableThroughputTimer guiclass="kg.apc.jmeter.timers.VariableThroughputTimerGui" testclass="kg.apc.jmeter.timers.VariableThroughputTimer" testname="CAPACITY TEST - Throughput Shaping Timer" enabled="false">
                <collectionProp name="load_profile">
                    <collectionProp name="1954571997">
                        <stringProp name="53">5</stringProp>
                        <stringProp name="53">5</stringProp>
                        <stringProp name="53430">600</stringProp>
                    </collectionProp>
                    <collectionProp name="1571222845">
                        <stringProp name="1567">10</stringProp>
                        <stringProp name="1567">10</stringProp>
                        <stringProp name="53430">600</stringProp>
                    </collectionProp>
                    <collectionProp name="1572182109">
                        <stringProp name="1572">15</stringProp>
                        <stringProp name="1572">15</stringProp>
                        <stringProp name="53430">600</stringProp>
                    </collectionProp>
                </collectionProp>
            </kg.apc.jmeter.timers.VariableThroughputTimer>
            <hashTree/>
            <BackendListener guiclass="BackendListenerGui" testclass="BackendListener" testname="Backend Listener">
        <elementProp name="arguments" elementType="Arguments" guiclass="ArgumentsPanel" testclass="Arguments">
          <collectionProp name="Arguments.arguments">
            <elementProp name="apiKey" elementType="Argument">
              <stringProp name="Argument.name">apiKey</stringProp>
              <stringProp name="Argument.value">DATADOG-API-KEY</stringProp>
              <stringProp name="Argument.metadata">=</stringProp>
            </elementProp>
            <elementProp name="datadogUrl" elementType="Argument">
              <stringProp name="Argument.name">datadogUrl</stringProp>
              <stringProp name="Argument.value">https://api.datadoghq.com/api/</stringProp>
              <stringProp name="Argument.metadata">=</stringProp>
            </elementProp>
            <elementProp name="logIntakeUrl" elementType="Argument">
              <stringProp name="Argument.name">logIntakeUrl</stringProp>
              <stringProp name="Argument.value">https://http-intake.logs.datadoghq.com/v1/input/</stringProp>
              <stringProp name="Argument.metadata">=</stringProp>
            </elementProp>
            <elementProp name="metricsMaxBatchSize" elementType="Argument">
              <stringProp name="Argument.name">metricsMaxBatchSize</stringProp>
              <stringProp name="Argument.value">200</stringProp>
              <stringProp name="Argument.metadata">=</stringProp>
            </elementProp>
            <elementProp name="logsBatchSize" elementType="Argument">
              <stringProp name="Argument.name">logsBatchSize</stringProp>
              <stringProp name="Argument.value">500</stringProp>
              <stringProp name="Argument.metadata">=</stringProp>
            </elementProp>
            <elementProp name="sendResultsAsLogs" elementType="Argument">
              <stringProp name="Argument.name">sendResultsAsLogs</stringProp>
              <stringProp name="Argument.value">true</stringProp>
              <stringProp name="Argument.metadata">=</stringProp>
            </elementProp>
            <elementProp name="includeSubresults" elementType="Argument">
              <stringProp name="Argument.name">includeSubresults</stringProp>
              <stringProp name="Argument.value">false</stringProp>
              <stringProp name="Argument.metadata">=</stringProp>
            </elementProp>
            <elementProp name="excludeLogsResponseCodeRegex" elementType="Argument">
              <stringProp name="Argument.name">excludeLogsResponseCodeRegex</stringProp>
              <stringProp name="Argument.value"></stringProp>
              <stringProp name="Argument.metadata">=</stringProp>
            </elementProp>
            <elementProp name="samplersRegex" elementType="Argument">
              <stringProp name="Argument.name">samplersRegex</stringProp>
              <stringProp name="Argument.value"></stringProp>
              <stringProp name="Argument.metadata">=</stringProp>
            </elementProp>
            <elementProp name="customTags" elementType="Argument">
              <stringProp name="Argument.name">customTags</stringProp>
              <stringProp name="Argument.value"></stringProp>
              <stringProp name="Argument.metadata">=</stringProp>
            </elementProp>
          </collectionProp>
        </elementProp>
        <stringProp name="classname">org.datadog.jmeter.plugins.DatadogBackendClient</stringProp>
      </BackendListener>
      <hashTree/>
            <ResultCollector guiclass="SummaryReport" testclass="ResultCollector" testname="Summary Report" enabled="true">
                <boolProp name="ResultCollector.error_logging">false</boolProp>
                <objProp>
                    <name>saveConfig</name>
                    <value class="SampleSaveConfiguration">
                        <time>true</time>
                        <latency>true</latency>
                        <timestamp>true</timestamp>
                        <success>true</success>
                        <label>true</label>
                        <code>true</code>
                        <message>true</message>
                        <threadName>true</threadName>
                        <dataType>true</dataType>
                        <encoding>false</encoding>
                        <assertions>true</assertions>
                        <subresults>true</subresults>
                        <responseData>false</responseData>
                        <samplerData>false</samplerData>
                        <xml>false</xml>
                        <fieldNames>true</fieldNames>
                        <responseHeaders>false</responseHeaders>
                        <requestHeaders>false</requestHeaders>
                        <responseDataOnError>false</responseDataOnError>
                        <saveAssertionResultsFailureMessage>true</saveAssertionResultsFailureMessage>
                        <assertionsResultsToSave>0</assertionsResultsToSave>
                        <bytes>true</bytes>
                        <sentBytes>true</sentBytes>
                        <threadCounts>true</threadCounts>
                        <idleTime>true</idleTime>
                        <connectTime>true</connectTime>
                    </value>
                </objProp>
                <stringProp name="filename"></stringProp>
            </ResultCollector>
            <hashTree/>
            <ResultCollector guiclass="ViewResultsFullVisualizer" testclass="ResultCollector" testname="View Results Tree" enabled="true">
                <boolProp name="ResultCollector.error_logging">false</boolProp>
                <objProp>
                    <name>saveConfig</name>
                    <value class="SampleSaveConfiguration">
                        <time>true</time>
                        <latency>true</latency>
                        <timestamp>true</timestamp>
                        <success>true</success>
                        <label>true</label>
                        <code>true</code>
                        <message>true</message>
                        <threadName>true</threadName>
                        <dataType>false</dataType>
                        <encoding>false</encoding>
                        <assertions>true</assertions>
                        <subresults>false</subresults>
                        <responseData>false</responseData>
                        <samplerData>false</samplerData>
                        <xml>false</xml>
                        <fieldNames>true</fieldNames>
                        <responseHeaders>false</responseHeaders>
                        <requestHeaders>false</requestHeaders>
                        <responseDataOnError>true</responseDataOnError>
                        <saveAssertionResultsFailureMessage>true</saveAssertionResultsFailureMessage>
                        <assertionsResultsToSave>0</assertionsResultsToSave>
                        <bytes>true</bytes>
                        <hostname>true</hostname>
                        <threadCounts>true</threadCounts>
                        <sampleCount>true</sampleCount>
                    </value>
                </objProp>
                <stringProp name="filename"></stringProp>
            </ResultCollector>
            <hashTree/>
            <ThreadGroup guiclass="ThreadGroupGui" testclass="ThreadGroup" testname="Thread Group" enabled="true">
                <stringProp name="ThreadGroup.on_sample_error">startnextloop</stringProp>
                <elementProp name="ThreadGroup.main_controller" elementType="LoopController" guiclass="LoopControlPanel" testclass="LoopController" testname="Loop Controller" enabled="true">
                    <boolProp name="LoopController.continue_forever">1</boolProp>
                    <intProp name="LoopController.loops">1</intProp>
                </elementProp>
                <stringProp name="ThreadGroup.num_threads">${THREADS}</stringProp>
                <stringProp name="ThreadGroup.ramp_time">${THREADS_RAMPUP_TIME}</stringProp>
                <boolProp name="ThreadGroup.scheduler">false</boolProp>
                <stringProp name="ThreadGroup.duration"></stringProp>
                <stringProp name="ThreadGroup.delay"></stringProp>
                <boolProp name="ThreadGroup.same_user_on_next_iteration">false</boolProp>
BASELINE_JMX_FIND
"""

TG_TC_HTTPSampler_jmx = """
<HTTPSamplerProxy guiclass="HttpTestSampleGui" testclass="HTTPSamplerProxy" testname="MY-NAME" enabled="true">DYNAMIC-BODY-PART
    <stringProp name="HTTPSampler.domain">MY-DOMAIN</stringProp>
    <stringProp name="HTTPSampler.port">MY-PORT</stringProp>
    <stringProp name="HTTPSampler.protocol">MY-PROTOCOL</stringProp>
    <stringProp name="HTTPSampler.contentEncoding"></stringProp>
    <stringProp name="HTTPSampler.path">MY-PATH</stringProp>
    <stringProp name="HTTPSampler.method">MY-METHOD</stringProp>
    <boolProp name="HTTPSampler.follow_redirects">true</boolProp>
    <boolProp name="HTTPSampler.auto_redirects">false</boolProp>
    <boolProp name="HTTPSampler.use_keepalive">true</boolProp>
    <boolProp name="HTTPSampler.DO_MULTIPART_POST">false</boolProp>
    <stringProp name="HTTPSampler.embedded_url_re"></stringProp>
    <stringProp name="HTTPSampler.connect_timeout"></stringProp>
    <stringProp name="HTTPSampler.response_timeout"></stringProp>
    MY-URL-PARAM
</HTTPSamplerProxy>
"""

headerStringStart_jmx = """
<hashTree>
    <HeaderManager guiclass="HeaderPanel" testclass="HeaderManager" testname="HTTP Header Manager" enabled="true">
        <collectionProp name="HeaderManager.headers">
"""
headerStringEnd_jmx = """
</collectionProp>
</HeaderManager>
<hashTree/></hashTree>
"""

raw_body_part = """
<boolProp name="HTTPSampler.postBodyRaw">true</boolProp>
<elementProp name="HTTPsampler.Arguments" elementType="Arguments">
    <collectionProp name="Arguments.arguments">
        <elementProp name="" elementType="HTTPArgument">
            <boolProp name="HTTPArgument.always_encode">false</boolProp>
            <stringProp name="Argument.value">MY-BODY</stringProp>
            <stringProp name="Argument.metadata">=</stringProp>
        </elementProp>
    </collectionProp>
</elementProp>
"""

without_body_part = """
<elementProp name="HTTPsampler.Arguments" elementType="Arguments" guiclass="HTTPArgumentsPanel" testclass="Arguments" testname="User Defined Variables" enabled="true">
    <collectionProp name="Arguments.arguments"/>
</elementProp>
"""

BASELINE_JMX_TEMPLATE = '</ThreadGroup>'+ '<hashTree>'+ itr_final_jmx + '</hashTree>'+ '</hashTree>   </hashTree> </jmeterTestPlan>'

# Global variables


########### Code  #########

def add_headers(headers):
    """
    Generates JMX header string for the given headers.
    """
    header_string_mid = ""
    try:
        for header in headers:
            if not header.get('disabled', False):  # Only process enabled headers
                header_to_add = (
                    '                <elementProp name="" elementType="Header">'
                    f'                   <stringProp name="Header.name">{header["key"]}</stringProp>'
                    f'                   <stringProp name="Header.value">{header["value"]}</stringProp>'
                    '                 </elementProp>'
                )
                header_string_mid += header_to_add
    except Exception as e:
        logging.error(f"Error while processing headers: {e}")
    return header_string_mid

def add_query_params(query_params):
    """
    Generates JMX query parameter string for the given query parameters.
    """
    param_string_mid = ""
    try:
        for param in query_params:
            if not param.get('disabled', False):  # Only process enabled parameters
                param_to_add = (
                    f'<elementProp name="{param["key"]}" elementType="HTTPArgument">'
                    ' <boolProp name="HTTPArgument.always_encode">true</boolProp>'
                    f' <stringProp name="Argument.value">{param["value"]}</stringProp>'
                    ' <stringProp name="Argument.metadata">=</stringProp>'
                    ' <boolProp name="HTTPArgument.use_equals">true</boolProp>'
                    f' <stringProp name="Argument.name">{param["key"]}</stringProp>'
                    ' </elementProp>'
                )
                param_string_mid += param_to_add
    except Exception as e:
        logging.error(f"Error while processing query parameters: {e}")
    return param_string_mid

def postman_param(value):
    return "${"+value.strip('}').strip('{')+"}"

def process_request(request, num, TG_TC_HTTPSampler_jmx, raw_body_part, without_body_part, headerStringStart_jmx, headerStringEnd_jmx):
    """
    Processes a single request dictionary to generate the corresponding JMX snippet.
    """
    try:
        temp_jmx = TG_TC_HTTPSampler_jmx
        my_name = request['name']
        
        #print(request['request']['url']['protocol'])

        my_name_updated = f"{num}_{my_name}"

        # Creatinf Request
        temp_jmx = temp_jmx.replace('MY-NAME', my_name_updated)

        if "{{" in request['request']['url']['protocol']:
            protocol = postman_param(request['request']['url']['protocol'])
            temp_jmx = temp_jmx.replace('MY-PROTOCOL',protocol)
        else:
            temp_jmx = temp_jmx.replace('MY-PROTOCOL',request['request']['url']['protocol'])

        if "{{" in request['request']['url']['host'][0]:
            host = postman_param(request['request']['url']['host'][0])
            temp_jmx = temp_jmx.replace('MY-DOMAIN',host)
        else:
            temp_jmx = temp_jmx.replace('MY-DOMAIN',{request['request']['url']['host'][0]})
        
        if "{{" in request['request']['url']['port']:
            port = postman_param(request['request']['url']['port'])
            temp_jmx = temp_jmx.replace('MY-PORT',port)
        else:
            temp_jmx = temp_jmx.replace('MY-PORT',request['request']['url']['port'])

        temp_jmx = temp_jmx.replace('MY-METHOD', request['request']['method'])

        try :
            if request['request']['url']['query']:
                url_param = ''
                for i in request['request']['url']['query']:
                    element = f"""
                                    <elementProp name="HTTPsampler.Arguments" elementType="Arguments" guiclass="HTTPArgumentsPanel" testclass="Arguments" testname="User Defined Variables">
                                        <collectionProp name="Arguments.arguments">
                                        <elementProp name="{i['key']}" elementType="HTTPArgument">
                                            <boolProp name="HTTPArgument.always_encode">false</boolProp>
                                            <stringProp name="Argument.value">{i['value']}</stringProp>
                                            <stringProp name="Argument.metadata">=</stringProp>
                                            <boolProp name="HTTPArgument.use_equals">true</boolProp>
                                            <stringProp name="Argument.name">n</stringProp>
                                        </elementProp>
                                        </collectionProp>
                                    </elementProp>
                                """
                    url_param += element
                temp_jmx = temp_jmx.replace('MY-URL-PARAM',url_param)
                    
        except KeyError:
            temp_jmx = temp_jmx.replace('MY-URL-PARAM','')


        # Replace URL
        path = request['request']['url']['path']
        #print('/'.join(path))
        my_url = re.sub('&', '&amp;', '/'.join(path))
        temp_jmx = temp_jmx.replace('MY-PATH', my_url)

        # Handle body
        my_request_body = ""
        try:
            body = request['request']['body']
            body_mode = body['mode']
            if body_mode == 'raw':
                my_request_body = re.sub(r'&', '&amp;', body['raw'].replace('\n', ''))
                my_request_body = re.sub('<', '&lt;', my_request_body)
                my_request_body = re.sub('>', '&gt;', my_request_body)
                body_part = raw_body_part.replace('MY-BODY', my_request_body)
                temp_jmx = temp_jmx.replace('DYNAMIC-BODY-PART', body_part)
            elif body_mode in ['urlencoded', 'formdata']:
                for param in body[body_mode]:
                    if not param.get('disabled', False):
                        param_to_add = (
                            f'<elementProp name="{param["key"]}" elementType="HTTPArgument">'
                            ' <boolProp name="HTTPArgument.always_encode">true</boolProp>'
                            f' <stringProp name="Argument.value">{param["value"]}</stringProp>'
                            ' <stringProp name="Argument.metadata">=</stringProp>'
                            ' <boolProp name="HTTPArgument.use_equals">true</boolProp>'
                            f' <stringProp name="Argument.name">{param["key"]}</stringProp>'
                            ' </elementProp>'
                        )
                        my_request_body += param_to_add
                param_string_all = f'<collectionProp name="Arguments.arguments">{my_request_body}</collectionProp>'
                temp_jmx = temp_jmx.replace('DYNAMIC-BODY-PART', without_body_part.replace('<collectionProp name="Arguments.arguments"/>           </elementProp>', param_string_all))
        except KeyError:
            # If body doesn't exist, handle query parameters
            if 'query' in request['request']['url']:
                query_params = request['request']['url']['query']
                param_string_mid = add_query_params(query_params)
                param_string_all = f'<collectionProp name="Arguments.arguments">{param_string_mid}</collectionProp>'
                temp_jmx = temp_jmx.replace('DYNAMIC-BODY-PART', without_body_part.replace('<collectionProp name="Arguments.arguments"/>           </elementProp>', param_string_all))
            else:
                temp_jmx = temp_jmx.replace('DYNAMIC-BODY-PART', without_body_part)

        # Add headers
        header_string_mid = add_headers(request['request'].get('header', []))
        header_jmx = headerStringStart_jmx + header_string_mid + headerStringEnd_jmx
        temp_jmx += header_jmx

        return temp_jmx
    except Exception as e:
        logging.error(f"Error while processing request: {e}")
        return ""

def process_level(level, TG_TC_HTTPSampler_jmx, raw_body_part, without_body_part, headerStringStart_jmx, headerStringEnd_jmx):
    """
    Recursively processes a level (folder or requests) to handle nested structures.
    """
    itr_final_jmx = ""
    for num, item in enumerate(level, start=1):
        if 'item' in item:  # Folder structure
            logging.info(f"Processing folder: {item['name']}")
            itr_final_jmx += process_level(item['item'], TG_TC_HTTPSampler_jmx, raw_body_part, without_body_part, headerStringStart_jmx, headerStringEnd_jmx)
        else:  # Single request
            itr_final_jmx += process_request(item, num, TG_TC_HTTPSampler_jmx, raw_body_part, without_body_part, headerStringStart_jmx, headerStringEnd_jmx)
    return itr_final_jmx

def process_variables_file(filepath, description, output):
    """
    Process a variable file (environment or global) and replace placeholders in the output.
    """
    try:
        with open(filepath, 'r') as rf:
            file_content = rf.read()
            json_file = json.loads(file_content)
            variables = json_file.get('values', [])
            
            current_udv = re.search(r'<collectionProp name="Arguments.arguments">(.*?)</collectionProp>', output)
            if not current_udv:
                logging.warning(f"Could not find user-defined variables in the template.")
                return output

            imported_udv = ""
            for var in variables:
                key = var.get('key', '')
                value = var.get('value', '')
                if key:
                    # Add to user-defined variables
                    element = (
                        f'<elementProp name="{key}" elementType="Argument">'
                        f'<stringProp name="Argument.name">{key}</stringProp>'
                        f'<stringProp name="Argument.value">{value}</stringProp>'
                        f'<stringProp name="Argument.metadata">=</stringProp>'
                        f'<stringProp name="Argument.desc">{description}</stringProp>'
                        f'</elementProp>'
                    )
                    imported_udv += element

                    # Replace placeholders in the output
                    output = output.replace(f"{{{{{key}}}}}", f"${{{key}}}")

            final_udv = current_udv.group(1) + imported_udv
            output = output.replace(current_udv.group(1), final_udv)

    except Exception as e:
        logging.info(f'Error processing "{description}" file: {str(e)}')

    return output

def process_variable(value, output):
    postman_userdefined_values =''
    for i in value:
        element = (
            f'<elementProp name="{i['key']}" elementType="Argument">'
            f'<stringProp name="Argument.name">{i['key']}</stringProp>'
            f'<stringProp name="Argument.value">{i['value']}</stringProp>'
            f'<stringProp name="Argument.metadata">=</stringProp>'
            f'<stringProp name="Argument.desc">POSTMAN Variable</stringProp>'
            f'</elementProp>'
        )
        postman_userdefined_values += element
    return output.replace('MY-POSTMAN-VARIABLE',postman_userdefined_values)

def main(inputpath):
    #inputpath = input("Enter full directory path where Postman collection is parked along with environment and/or global variables: ")
    #inputpath = 'Postman Collection'
    global variablefile, globalvariablefile

    try:
        # Identify input files
        inputfile = None
        for filename in os.listdir(inputpath):
            filepath = os.path.join(inputpath, filename)
            if "collection" in filename:
                inputfile = filepath
            elif "environment" in filename:
                variablefile = filepath
            elif "globals" in filename:
                globalvariablefile = filepath

        if not inputfile:
            raise FileNotFoundError("Postman collection file not found in the specified directory.")

        # Load Postman collection
        with open(inputfile, 'r') as rf:
            file_content = rf.read()
            collection = json.loads(file_content)
            level_1 = collection.get('item', [])
            variable = collection.get('variable')
    except Exception as e:
        logging.error(f"Error opening input files: {e}")
        sys.exit(1)

    # Main processing starts here
    try:
        itr_final_jmx = process_level(level_1, TG_TC_HTTPSampler_jmx, raw_body_part, without_body_part, headerStringStart_jmx, headerStringEnd_jmx)
        #print(itr_final_jmx)
    except Exception as e:
        logging.error(f"Critical error during processing: {e}")
        sys.exit(1)

    # Update the baseline JMX
    try:
        #baseline_jmx_replace = BASELINE_JMX_TEMPLATE.format(hashTree='<hashTree>', itr_final_jmx=itr_final_jmx, baseline_suffix='</hashTree>   </hashTree> </jmeterTestPlan>')
        output = baseline_jmx.replace("BASELINE_JMX_FIND", '</ThreadGroup>'+ '<hashTree>'+ itr_final_jmx + '</hashTree>'+ '</hashTree>   </hashTree> </jmeterTestPlan>')
        #print(output)
    except Exception as e:
        logging.error(f"Error updating baseline JMX: {e}")
        sys.exit(1)
   
    # Process environment variables
    if variablefile:
        output = process_variables_file(variablefile, "Imported from environment variables", output)

    # Process global variables
    if globalvariablefile:
        output = process_variables_file(globalvariablefile, "Imported from global variables", output)
    
    if variable:
        output = process_variable(variable, output)
        print('output')
    else:
        output = output.replace('MY-POSTMAN-VARIABLE','')

    # Write final JMX to output file
    try:
        outfile_name = os.path.basename(inputfile).split('.')[0] + '.jmx'
        outfile = os.path.join(inputpath, outfile_name)
        with open(outfile, 'w') as wf:
            wf.write(output)
            logging.info(f"Successfully created JMeter JMX file at: {outfile}")
    except Exception as e:
        logging.error(f"Error writing output file: {e}")
        sys.exit(1)

if __name__ == '__main__':
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Convert Postman into Jmeter Script.")
    parser.add_argument("folder_path", help="Path to the postman folder")
    args = parser.parse_args()
    main(args.folder_path)
