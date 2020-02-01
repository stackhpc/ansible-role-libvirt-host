class FilterModule(object):

    def filters(self):
        return {
            'xml2dict': self.xml2dict,
        }

    def xml2dict(self, value):
        from xml.etree import ElementTree
        # return json.dumps(xmltodict.parse(value))
        res = {}

        if isinstance(value, list):
            for item in value:
                e = self.xml2dict(item['get_xml'])
                res[e['name']] = e
            return res

        e = ElementTree.fromstring(value)

        def rp(root, result):
            for element in root:
                result[element.tag] = rp(element, {})
                result[element.tag].update(element.attrib)
                if not result[element.tag]:
                    result[element.tag] = element.text
            return result

        rp(e, res)
        return res
