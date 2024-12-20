import logging
import azure.functions as func
import tempfile
from os import listdir

app = func.FunctionApp()

@app.route(route="TmpFSCheck", auth_level=func.AuthLevel.ANONYMOUS)
def TmpFSCheck(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        # Create a temporary file and write 1GB of data
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        data_chunk = b'a' * (1024 * 1024)  # 1MB chunk
        for _ in range(1024):  # Write 1024 chunks (1GB total)
            temp_file.write(data_chunk)
        temp_file.close()

        temp_dir = tempfile.gettempdir()
        files_in_temp = listdir(temp_dir)

        response_message = (
            f"Temporary file created: {temp_file.name}\n"
            f"Size: 1GB\n"
            f"Files in temp directory: {files_in_temp}"
        )

        return func.HttpResponse(response_message, status_code=200)

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return func.HttpResponse(f"An error occurred: {e}", status_code=500)
