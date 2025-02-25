from llama_parse import LlamaParse
from django.conf import settings

class FileParser():
    def __init__(self):
        self.parser = LlamaParse(
            api_key=settings.LLAMA_CLOUD_API_KEY,
            result_type="markdown",
            premium_mode=False,     
            # auto_mode=True,               
            # auto_mode_trigger_on_table_in_page=True, 
            # auto_mode_trigger_on_image_in_page=True,
        )

    def parse(self, file_bytes: bytes, file_name: str) -> str:
        content = ''
        page_splitter = '\n\n Page Break \n\n'

        extra_info = {
            "file_name": file_name
        }
        documents = self.parser.load_data(file_bytes, extra_info=extra_info)

        for doc in documents:
            content += doc.text_resource.text
            content += page_splitter

        return content
        