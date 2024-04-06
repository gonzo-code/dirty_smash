from h2spacex import H2OnTlsConnection
from time import sleep
from h2spacex import h2_frames
from urllib.parse import urlparse

# User inputs
input_url = input("Enter the URL: ")
input_auth_token = input("Enter the Auth Token: ")
input_body = input("Enter the Body (JSON format): ")

# Parse the URL to extract the host and path
parsed_url = urlparse(input_url)
hostname = parsed_url.hostname
path = parsed_url.path

# Default port for HTTPS
port_number = 443

h2_conn = H2OnTlsConnection(
    hostname=hostname,
    port_number=port_number
)

h2_conn.setup_connection()

### STEP 1 -- Add Bearer token
headers = f"""accept: application/json, text/plain, */*
content-type: application/json
authorization: Bearer {input_auth_token}
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.85 Safari/537.36
sec-ch-ua-platform: "macOS"
sec-fetch-site: same-site
sec-fetch-mode: cors
sec-fetch-dest: empty
accept-encoding: gzip, deflate, br
accept-language: en-US,en;q=0.9
priority: u=1, i
connection: close
"""  # Updated headers

body = input_body  # Use the user-provided body

stream_ids_list = h2_conn.generate_stream_ids(number_of_streams=5)

all_headers_frames = []  # all headers frame + data frames which have not the last byte
all_data_frames = []  # all data frames which contain the last byte

for s_id in stream_ids_list:
    header_frames_without_last_byte, last_data_frame_with_last_byte = h2_conn.create_single_packet_http2_post_request_frames(
        method='POST',
        headers_string=headers,
        scheme='https',
        stream_id=s_id,
        authority=hostname,
        body=body,
        path=path
    )

    all_headers_frames.append(header_frames_without_last_byte)
    all_data_frames.append(last_data_frame_with_last_byte)


# concatenate all headers bytes
temp_headers_bytes = b''
for h in all_headers_frames:
    temp_headers_bytes += bytes(h)

# concatenate all data frames which have last byte
temp_data_bytes = b''
for d in all_data_frames:
    temp_data_bytes += bytes(d)

# send header frames
h2_conn.send_frames(temp_headers_bytes)

# wait some time
sleep(0.1)

# send ping frame to warm up connection
h2_conn.send_ping_frame()

# send remaining data frames
h2_conn.send_frames(temp_data_bytes)

# parse response frames
resp = h2_conn.read_response_from_socket(_timeout=3)
frame_parser = h2_frames.FrameParser(h2_connection=h2_conn)
frame_parser.add_frames(resp)
frame_parser.show_response_of_sent_requests()

# close the connection to stop response parsing and exit the script
h2_conn.close_connection()
