# export/xml_exporter.py

import xml.etree.ElementTree as ET

from models.document_models import StructuredAccountingData


class XMLExporter:

    def export(self, data: StructuredAccountingData, output_path: str):

        root = ET.Element("AccountingDocument")

        metadata = ET.SubElement(root, "Metadata")
        for k, v in data.metadata.model_dump().items():
            ET.SubElement(metadata, k).text = str(v)

        supplier = ET.SubElement(root, "Supplier")
        for k, v in data.supplier.model_dump().items():
            ET.SubElement(supplier, k).text = str(v)

        buyer = ET.SubElement(root, "Buyer")
        for k, v in data.buyer.model_dump().items():
            ET.SubElement(buyer, k).text = str(v)

        items_node = ET.SubElement(root, "Items")
        for item in data.items:
            node = ET.SubElement(items_node, "Item")
            for k, v in item.model_dump().items():
                ET.SubElement(node, k).text = str(v)

        totals = ET.SubElement(root, "Totals")
        for k, v in data.totals.model_dump().items():
            ET.SubElement(totals, k).text = str(v)

        tree = ET.ElementTree(root)
        tree.write(output_path, encoding="utf-8", xml_declaration=True)

        return output_path
