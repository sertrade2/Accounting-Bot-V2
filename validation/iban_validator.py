# validation/iban_validator.py

import re


class IBANValidator:

    IBAN_RE = re.compile(r"^[A-Z]{2}\d{2}[A-Z0-9]{11,30}$")

    @staticmethod
    def validate(iban: str):
        if not iban:
            return [], ["IBAN missing."]

        iban = iban.replace(" ", "").upper()

        if not IBANValidator.IBAN_RE.match(iban):
            return ["Invalid IBAN format."], []

        # Checksum
        rearranged = iban[4:] + iban[:4]
        numeric = "".join(str(int(ch, 36)) for ch in rearranged)

        if int(numeric) % 97 != 1:
            return ["IBAN checksum failed."], []

        return [], []
