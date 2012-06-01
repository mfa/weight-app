from models import Scale, Weight, User
from main import db
from lxml import etree
import datetime

def import_weight_from_xml(filename):
    """ Import Scales and Weight from my own old xml-Data
    """

    def add_scales(doc):
        for elem in doc.xpath("//scales/item"):
            sc1 = Scale(name=unicode(elem.attrib["id"]))
            for i in elem:
                if i.tag=='owner':
                    sc1.owner = unicode(i.text)
                if i.tag=='model' and i.text:
                    sc1.model = unicode(i.text)
            db.session.add(sc1)
        db.session.commit()

    def add_weight(doc):
        for elem in doc.xpath('//days/day'):
            we1 = Weight()
            we1.wdate = datetime.datetime.strptime(elem.attrib['date'],
                                                   '%Y-%m-%d')
            w = False
            for i in elem:
                if i.tag=='weight' and i.text:
                    sc1 = Scale.query.get(unicode(i.attrib['scale']))
                    if sc1:
                        we1.scale_name = sc1.name
                    we1.weight = unicode(i.text)
                    w = True
                if i.tag=='comment' and i.text:
                    we1.comment = unicode(i.text)
            if w:
                db.session.add(we1)
        db.session.commit()
                
    doc = etree.parse(filename)
    add_scales(doc)
    add_weight(doc)
