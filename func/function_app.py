import logging
import azure.functions as func
import tempfile
import time
from os import listdir
from azurefunctions.extensions.http.fastapi import Request, StreamingResponse

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

def generate_temp_file_data(file_path: str):
    """Generate real-time streaming data from a temporary file."""
    try:
        with open(file_path, 'rb') as temp_file:
            chunk_size = 1024 * 1024  # 1MB chunks
            while chunk := temp_file.read(chunk_size):
                yield chunk
    except Exception as e:
        yield f"data: Error occurred while reading file: {str(e)}\n\n"

@app.route(route="TmpFSCheck", auth_level=func.AuthLevel.ANONYMOUS)
async def TmpFSCheck(req: Request) -> StreamingResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        # Create a temporary file and write 1GB of data
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        data_chunk = b'a' * (1024 * 1024)  # 1MB chunk
        for _ in range(1024):  # Write 1024 chunks (1GB total)
            temp_file.write(data_chunk)
        temp_file.close()

        # Streaming file content to the client
        return StreamingResponse(generate_temp_file_data(temp_file.name), media_type="application/octet-stream")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return func.HttpResponse(f"An error occurred: {e}", status_code=500)
