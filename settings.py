from pathlib import Path

settings = {
    'host': '127.0.0.1',
    'port': 9876,
    'chunck_size': 1024,
    'data_file_name': 'key_loggs.txt',
    'data_dir_name': Path(__file__).parent / 'received_loggs',
    'send_timeout': 5
}