import logging
import xml.etree.ElementTree as ET
from typing import Dict

from models.document import Document

logger = logging.getLogger(__name__)


class OneCXMLExporter:
    """
    Exports document into simplified 1C-compatible XML structure.
    """

    def export(self, document: Document) -> str:
        logger.info("Exporting document to 1C XML")

        root = ET.Element("Document")
        ET.SubElement(root, "DocumentID").text = document.document_id
        ET.SubElement(root, "Version").text = str(document.version)

        items_el = ET.SubElement(root, "Items")

        for item in document.table_items:
            item_el = ET.SubElement(items_el, "Item")
            ET.SubElement(item_el, "Description").text = item.description
            ET.SubElement(item_el, "Quantity").text = (
                str(item.quantity) if item.quantity is not None else ""
            )
            ET.SubElement(item_el, "UnitPrice").text = (
                str(item.unit_price) if item.unit_price is not None else ""
            )
            ET.SubElement(item_el, "LineTotal").text = (
                str(item.line_total) if item.line_total is not None else ""
            )

        validation_el = ET.SubElement(root, "Validation")
        if document.validation_report:
            for key, value in document.validation_report.items():
                ET.SubElement(validation_el, key).text = str(value)

        confidence_el = ET.SubElement(root, "Confidence")
        if document.confidence_breakdown:
            for k, v in document.confidence_breakdown.items():
                ET.SubElement(confidence_el, k).text = str(v)

        xml_str = ET.tostring(
            root,
            encoding="utf-8",
            xml_declaration=True,
        ).decode("utf-8")

        logger.info("1C XML export completed")
        return xml_str
