import httprequest

class HttpRequestProcessor:
    def __init__(self):
        self.continue_receiving = True
        self.string_buffer = ""
        self.parsing_headers = True
        self.header_dict = {}
        self.all_headers = []
        self.payload = ""
        self.verb = ""
        self.path = ""
        self.done_with_headers = False
        self.parameters = {}

    def keep_receiving(self):
        return self.continue_receiving

    def parse_http_stream(self, data):
        self.string_buffer = self.string_buffer + data.decode("utf-8")
        list_of_headers = self._construct_headers_list(self.string_buffer)
        self.string_buffer = self._trim_buffer(list_of_headers, self.string_buffer)
        self.all_headers = self.all_headers + list_of_headers

        if not self.parsing_headers:
            if not self.done_with_headers:
                self.done_with_headers = True
                self.all_headers = self.extract_pre_header(self.all_headers)
                self.header_dict = self.construct_header_dict(self.all_headers)
            if "Content-Length" not in self.header_dict:
                self.continue_receiving = False
            else:
                self.parse_payload(self.string_buffer)

    def parse_payload(self, data):
        if len(data) == int(self.header_dict["Content-Length"]):
            self.payload = data
            self.continue_receiving = False

    def _construct_headers_list(self, data):
        if "\r\n\r\n" not in data:
            return []
        header_portion = data.split('\r\n\r\n')[0]
        list_of_strings = header_portion.split('\r\n')
        headers_list = []
        if len(list_of_strings) > 1:
            for element in list_of_strings:
                headers_list.append(element)

        self.parsing_headers = False
        return headers_list

    def extract_pre_header(self, headers_list):
        line = headers_list.pop(0)
        self.verb, self.path, version = line.split(" ")
        path_parameters = self.path.split("?")
        if len(path_parameters) > 1:
            print("Params detected")
            self.parameters = self.extract_parameters(path_parameters[1])
            self.path = path_parameters[0]
        if version != "HTTP/1.1":
            raise Exception("Wrong Version" + version)
        return headers_list

    @staticmethod
    def extract_parameters(path_with_parameters):
        parameter_dictionary = {}
        list_of_parameter_pairs = path_with_parameters.split("&")
        for parameter_pair in list_of_parameter_pairs:
            key, value = parameter_pair.split("=")
            parameter_dictionary[key] = value

        return parameter_dictionary

    @staticmethod
    def construct_header_dict(header_strings):
        headers_dict = {}
        for header_pair in header_strings:
            header_key, header_value = header_pair.split(":", 1)
            headers_dict[header_key] = header_value
        return headers_dict

    @staticmethod
    def _check_headers_complete(headers_list):
        return not headers_list[-1] or not headers_list[0]

    @staticmethod
    def _trim_buffer(list_of_headers, string_buffer):

        if list_of_headers:
            header_strings_length = 0
            for header in list_of_headers:
                header_strings_length = len(header) + header_strings_length + 2
                # 2 bytes to account for the \r\n split character

            string_buffer = string_buffer[header_strings_length + 2:]
            # Add 2 to ensure we remove the last \r\n from the payload portion

        return string_buffer

    def process(self, folder_loc, handlers):
        if self.verb + self.path in handlers:
            function = handlers[self.verb + self.path]
            function(httprequest.HttpRequest(self.payload, self.path))
            return "HTTP/1.1 200 OK\r\n\r\n".encode()
        elif self.verb == "GET":
            if self.path == "/":
                self.path = "/index.html"
            try:
                with open(folder_loc + self.path, "r") as fd:
                    data = fd.read()
            except FileNotFoundError:
                return "HTTP/1.1 404" \
                       "\r\nMy-Header:My-Value" \
                       "\r\n\r\nthank you".encode()
            return "HTTP/1.1 200 OK" \
                   "\r\nContent-Type:text/html" \
                   "\r\nContent-Length:{}\r\n\r\n" \
                   "{}".format(len(data), data).encode()
        else:
            return "HTTP/1.1 500 brUH" \
                   "\r\nMy-Header:My-Value" \
                   "\r\n\r\nthank you".encode()