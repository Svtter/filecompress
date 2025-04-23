import zipfile
from collections.abc import Generator
from datetime import datetime
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.file.file import File


class FilecompressTool(Tool):
  def _create_zip(self, files: list[File], zip_filename: str):
    zip_file = zipfile.ZipFile(zip_filename, "w")

    for file in files:
      zip_file.writestr(file.filename, file.blob)
    zip_file.close()

    with open(zip_filename, "rb") as f:
      return f.read()

  def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
    files = tool_parameters["compressFile"]
    filename = tool_parameters.get(
      "filename", f"{datetime.now().strftime('%Y%m%d%H%M%S')}.zip"
    )

    zip_file = self._create_zip(files, filename)

    yield self.create_blob_message(
      blob=zip_file,
      meta={
        "file_name": filename,
        "mime_type": "application/zip",
      },
    )
