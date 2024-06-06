import re, requests, json5

class ZtreamHub():
  
  PATTERN_TITLE = r'\<h1 class\=\"h5 playerbox-title\"\>\n([^\n]*)\n[^\<]*\<\/h1\>'
  PATTERN_DATA = r"setup\((\{[^\)]*)\)\;"
  PATTERN_PARAMS = r"eval\([^\n]*\}\(([^\n]*)\.split\(\'\|\'\)\)\)"

  def __base_n__(self, num, b, numerals="0123456789abcdefghijklmnopqrstuvwxyz"):
    return ((num == 0) and numerals[0]) or (self.__base_n__(num // b, b, numerals).lstrip(numerals[0]) + numerals[num % b])

  def __decode__(self, text, encoding_base, loop_counter, decode_map):

    while loop_counter > 0:
      loop_counter -= 1
      if len(decode_map[loop_counter]) > 0:
        encoded_value = self.__base_n__(loop_counter, encoding_base)
        text = re.sub(rf"\b{encoded_value}\b", decode_map[loop_counter], text, flags=re.MULTILINE)
      
    return text

  def __download_data__(self, url):
    text = requests.get(url).text
    return text

  def __get_parameters__(self, html_doc):
    parameters = re.findall(self.PATTERN_PARAMS, html_doc)[0].rsplit(",", 3)
    return (parameters[0].replace("\\\'", "'"), int(parameters[1]), int(parameters[2]), parameters[3].strip("'").split("|"))
  
  def __get_title__(self, html_doc):
    title = re.findall(self.PATTERN_TITLE, html_doc)[0]
    return title.strip()

  def __get_raw_data__(self, html_doc):
    parameters = self.__get_parameters__(html_doc)
    text = self.__decode__(parameters[0], parameters[1], parameters[2], parameters[3])
    data = re.findall(self.PATTERN_DATA, text)[0]
    return json5.loads(data)
  
  def __get_data__(self, url):
    html_doc = self.__download_data__(url)
    title = self.__get_title__(html_doc)
    raw_data = self.__get_raw_data__(html_doc)
    return {
      "title": title,
      "source": raw_data['sources'][0]['file'],
      "duration": raw_data['duration'],
      "thumbnail": raw_data['image'],
      "qualityLabels": raw_data['qualityLabels']
    }

  def getData(self, url):
    return self.__get_data__(url)