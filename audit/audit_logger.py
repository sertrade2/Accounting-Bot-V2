import logging
from models.document import Document

logger = logging.getLogger(__name__)


class AuditLogger:
    """
    Writes immutable audit records.
    """

    def log(self, document: Document) -> None:
        for entry in document.audit_log:
            logger.info(
                "AUDIT | doc=%s | version=%d | reason=%s",
                document.document_id,
                entry["version"],
                entry["reason"],
            )
