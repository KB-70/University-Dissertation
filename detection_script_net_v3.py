import re
from bs4 import BeautifulSoup
import random
import string

qe = []
captured = []
sqli_captured_list = []
xss_keywords = []
xss_captured_list = []


class DetectionAlgorithm():
    # query_analysis function assesses whether input string is SQL or JS script
    def query_analysis(self, new_request):
        global query, script, injection
        # If statement categorises SQL or JS
        if "SELECT" in new_request or "INSERT" in new_request:
            query = new_request
            injection = query
        else:
            script = new_request
            injection = script

        return injection

    # sqli_capture function compares SQL against a dataset of keywords
    def sqli_capture(self, query_elements, sqli_found, flagged):
        # find common sqli symbols and keywords
        # assign a value between 1-5 to indicate threat level - dict = {keyword: score}
        global sqli_detection_dataset
        global regex_special
        global rs
        global sqli_threshold

        regex_special = re.compile("[_!#'%&()\"?,/|}{~:]")
        rs = {regex_special: 1}
        # data is assigned 5 if it can cause severe harm or can be used by itself
        sqli_detection_dataset = {"SELECT": 4, "FROM": 3, "WHERE": 3, "DROP": 5, "UPDATE": 3, "INSERT": 3, "INTO": 2,
                                  "ALTER": 5, 'DELETE': 5, "JOIN": 4, "DATABASE": 3, "TABLE": 3, 'UNION': 5,
                                  "ADD": 5, "MODIFY": 5, "COLUMN": 3, "OR": 1, "AND": 1, ';': 1}

        for elements in query_elements:
            for keyword in sqli_detection_dataset:
                keyword_lower = keyword.lower()
                if keyword == elements or keyword_lower == elements:
                    flagged.append(elements)
                    sqli_found.append(elements)
                else:
                    pass
            if regex_special.search(elements) is None:
                pass
            else:
                flagged.append(elements)
                sqli_found.append(elements)

    # xss_capture function assesses HTML elements
    def xss_capture(self, html_found, flagged):
        # find any html within string
        found_html = BeautifulSoup(script, "html.parser").find()
        if bool(found_html):
            flagged.append(found_html)
            html_found.append(found_html)
        else:
            pass

    # caught_injection_parts pre-processes the input string
    # compares XSS against a dataset of keywords
    def caught_injection_parts(self, new_request):   # edit to prevent error in xss_max_threshold
        global xss_detection_dataset
        global xss_threshold
        global random_injection

        da = DetectionAlgorithm()
        random_injection = da.query_analysis(new_request)

        xss_detection_dataset = {'src': 5, 'on': 4, 'alert': 4, 'href': 2, 'var': 5, 'javascript': 5,
                                 'vbscript': 5, '<script>': 5, '<body>': 3, '<a>': 3, '<img': 2, '<frame>': 3,
                                 'prompt': 4, 'String.fromCharCode': 4, 'function': 1}

        if 'SELECT' in random_injection or 'INSERT' in random_injection:
            split_query = re.split(r'(?<!^)\s', random_injection)
            for word in split_query:
                qe.append(word)

            da.sqli_capture(qe, sqli_captured_list, captured)
        elif '<' in random_injection:
            regex = re.compile('[%s]' % re.escape(string.punctuation))
            html_no_punct = regex.sub(' ', random_injection)
            split_html = re.split(r'(?<!^)\s', html_no_punct)
            for word in split_html:
                qe.append(word)
                if word in xss_detection_dataset:
                    xss_keywords.append(word)
                    if 'on' in word:
                        xss_keywords.append(word)
                    else:
                        pass
                else:
                    pass

            da.xss_capture(xss_captured_list, captured)
        else:
            pass

        #print()
        return random_injection

    # injection_scoring calculates the score of the input string
    def injection_scoring(self):
        query_score_total = 0
        xss_score_total = 0

        for sqli_word in list(set(sqli_captured_list)):
            for s_key, s_value in sqli_detection_dataset.items():
                if sqli_word == s_key or sqli_word in s_key:
                    query_score_total = s_value + query_score_total
                else:
                    continue
            for s_key, s_value in rs.items():
                if s_key.match(sqli_word):
                    query_score_total = s_value + query_score_total
                else:
                    continue

        for xss_word in list(set(xss_keywords)):
            for x_key, x_value in xss_detection_dataset.items():
                if xss_word == x_key:
                    xss_score_total = x_value + xss_score_total
                elif xss_word in x_key:
                    xss_score_total = x_value + xss_score_total
                elif x_key.startswith('on'):
                    xss_score_total = x_value + xss_score_total
                else:
                    continue

        # Uncomment to see associated keywords below score
        # sqli_flagged_words = sqli_captured_list
        # print(sqli_flagged_words)
        # xss_flagged_words = xss_keywords
        # print(xss_flagged_words)

        return query_score_total, xss_score_total

    # static maximum score for benign sql
    def sqli_max_threshold(self):
        global sqli_detection_dataset
        DetectionAlgorithm().sqli_capture(qe, sqli_captured_list, captured)
        sqli_select = 16  # max(sqli_detection_dataset.values())
        sqli_insert = 8

        return sqli_select, sqli_insert

    # static maximum score for benign xss
    def xss_max_threshold(self, new_request):
        global xss_detection_dataset
        DetectionAlgorithm.caught_injection_parts(self, new_request)
        xss_th = 7  # max(xss_detection_dataset.values())

        return xss_th

    # signal_to_server compares scores and generates signal
    def signal_to_server(self, new_request):
        query_score, _ = DetectionAlgorithm().injection_scoring()
        _, xss_score = DetectionAlgorithm().injection_scoring()
        select_query_thresh, _ = DetectionAlgorithm().sqli_max_threshold()
        _, insert_query_thresh = DetectionAlgorithm().sqli_max_threshold()
        xss_thresh = DetectionAlgorithm().xss_max_threshold(new_request)
        signal = ''

        if "SELECT" in new_request:
            if query_score <= select_query_thresh:
                signal = "OK"  # Benign Query
                print("OK SQLi")
            elif query_score > select_query_thresh:
                signal = "NOT OK"  # Malicious Query
                print("NOT OK SQLi")
        elif 'INSERT' in new_request:
            if query_score <= insert_query_thresh:
                signal = "OK"  # Benign Query
                print("OK SQLi")
            elif query_score > insert_query_thresh:
                signal = "NOT OK"  # Malicious Query
                print("NOT OK SQLi")
        else:
            if xss_score <= xss_thresh:
                signal = "OK"  # Benign XSS
                print("OK XSS")
            elif xss_score > xss_thresh:
                signal = "NOT OK"  # Malicipus XSS
                print("NOT OK XSS")

        print("Total score of SQL query =", query_score)  # Uncomment to view score
        print("Total score of XSS script =", xss_score)  # Uncomment to view score

        qe.clear()
        captured.clear()
        sqli_captured_list.clear()
        xss_keywords.clear()

        return signal


# running main function executes a simulated version of the real system
if __name__ == '__main__':
    da = DetectionAlgorithm()
    test_request_SQL = "SELECT * FROM Topics JOIN Requests ON Topics.topic_id = Requests.topicID JOIN data_points ON " \
                   "Requests.request_id = data_points.requestID WHERE topic_string = 'car3/speed' AND publisherID = 9;"
    test_request_SQLi = "SELECT * FROM Topics JOIN Requests ON Topics.topic_id = Requests.topicID JOIN data_points ON " \
                       "Requests.request_id = data_points.requestID WHERE topic_string = 'car3/speed' AND publisherID = 9;" \
                        "DROP TABLE Topics;"
    test_request_JS = "<script>function Safe(){ echo 'Safe Script'; }</script>"
    test_request_XSS = "<div onerror=prompt(document.cookie)></div>"

    rand_request_SQL = random.choice([test_request_SQL, test_request_SQLi])
    rand_request_XSS = random.choice([test_request_JS, test_request_XSS])

    new_test_request = random.choice([rand_request_SQL, rand_request_XSS])

    print(new_test_request)

    da.query_analysis(new_test_request)
    da.caught_injection_parts(new_test_request)
    da.signal_to_server(new_test_request)
