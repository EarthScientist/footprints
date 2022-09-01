from lxml import etree
from pathlib import Path

class MapCatalog:
    def __init__(self, utmzone, filename, desc=None, \
                    min_percent="10.000000", max_percent="0.000000"):
        self.utmzone = utmzone
        self.prj_name = f'UTM_ZONE{self.utmzone}_WGS84'
        self.filename = filename
        if not desc:
            self.desc = Path(self.filename).name
        self.min_percent = min_percent
        self.max_percent = max_percent
        self._templatefn = r'c:\repos\footprints\footprints\template.xml'
        self.tree = etree.parse(self._templatefn)
        self.root = self.tree.getroot()

    def updateroot(self):
        self.root.attrib.update({
                    'prj_name':self.prj_name,
                    'filename':self.filename,
                    'desc':self.desc,
                    'min_percent':self.min_percent,
                    'max_percent':self.max_percent,
                    })
    
    # def updateproj(self, proj=None):
    #     prj = self.root.find('.//projection', namespaces=self.root.nsmap)
    #     prj.attrib.update({'name':self.prj_name})
    #     prj.text = proj

    def addproj(self):
        prj = self.root.find('.//projection', namespaces=self.root.nsmap)
        UTM =\
            f'''Projection     UTM
            Datum          WGS84
            Zunits         NO
            Units          METERS
            Zone           {str(self.utmzone)}
            Xshift         0.000000
            Yshift         0.000000
            Parameters'''

        prj.attrib.update({'name':self.prj_name})
        prj.text = UTM

    def addmaps(self, maps=[]):
        projection = self.root.find('.//projection', namespaces=self.root.nsmap)
        for m in maps:
            projection.addnext(m)

    def deletemaps(self):
        print('NotYetImplemented')
        pass

    def write(self, outfn):
        self.tree.write(outfn, 
                encoding='utf-8', 
                xml_declaration=True, 
                pretty_print=False)
        return outfn