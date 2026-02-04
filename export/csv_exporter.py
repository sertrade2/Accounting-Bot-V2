# export/csv_exporter.py

import pandas as pd
from pathlib import Path

from models.document_models import StructuredAccountingData


class CSVExporter:

    def export(self, data: StructuredAccountingData, output_dir: str):

        output = Path(output_dir)
        output.mkdir(parents=True, exist_ok=True)

        items_df = pd.DataFrame([i.model_dump() for i in data.items])
        items_file = output / "items.csv"

        summary_df = pd.DataFrame([{
            **data.metadata.model_dump(),
            **data.totals.model_dump()
        }])
        summary_file = output / "summary.csv"

        items_df.to_csv(items_file, index=False)
        summary_df.to_csv(summary_file, index=False)

        return [str(items_file), str(summary_file)]
