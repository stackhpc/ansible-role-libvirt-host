class FilterModule(object):

    def filters(self):
        return {
            'xml2dict': self.xml2dict,
        }

    def xml2dict(self, value):
        from xml.etree import ElementTree
        # return json.dumps(xmltodict.parse(value))
        res = {}
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
