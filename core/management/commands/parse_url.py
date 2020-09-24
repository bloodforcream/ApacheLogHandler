import re
from datetime import datetime
import requests

from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand
from django.core.validators import URLValidator

from core.models import ApacheLog

ip_address_regex = '\A\d+\.\d+\.\d+\.\d+'
log_date_regex = '[0-9A-Za-z/:+\s]+'
http_method_regex = '[A-Z]{2,}'
uri_regex = '[A-Za-z0-9_/\|)(#\'"`%?!*;:@&,+$~=.-]{1,1023}'
status_code_regex = '[0-9]'
response_size_regex = '[0-9]+|-'

APACHE_LOG_PATTERN = re.compile(
    fr'({ip_address_regex})\s-\s-\s'
    fr'\[({log_date_regex})\]\s'
    fr'\"({http_method_regex})\s'
    fr'({uri_regex})\s[A-Z/0-9".]+\s'
    fr'({status_code_regex}{{3}})\s'
    fr'({response_size_regex})'
)


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_arguments(self, parser):
        parser.add_argument('url', type=str)

    def handle(self, *args, **options):
        url = options['url']
        url_validator = URLValidator()

        try:
            url_validator(url)
        except ValidationError:
            return 'Invalid url'

        file_name = download_logs_from_url(url)
        write_logs_from_file_to_db(file_name)

        return 'Done'


def download_logs_from_url(url, chunk_size=8192):
    # file is downloaded by chunks (chunk_size measured in bytes)

    response = requests.get(url, stream=True)

    kbs_in_chunk = chunk_size // 1024
    kb_downloaded = 0

    file_name = f'{url.split("/")[-1]}_apache_log.txt'
    with open(file_name, 'wb') as log_file:
        for chunk in response.iter_content(chunk_size=chunk_size):
            log_file.write(chunk)
            kb_downloaded += kbs_in_chunk
            print(f'{kb_downloaded} kb downloaded')
    return file_name


def write_logs_from_file_to_db(file_name, batch_size=999):
    counter = 0
    batch_of_data = []
    entries_inserted = 0
    with open(file_name) as log_file:
        for line in log_file:
            if counter <= batch_size:
                parsed_line = _parse_line(line)
                if parsed_line:
                    batch_of_data.append(_parse_line(line))
                    counter += 1
            else:
                ApacheLog.objects.bulk_create(
                    [ApacheLog(**{key: val for key, val in log.items()})
                     for log in batch_of_data])

                batch_of_data = []
                counter = 0

                entries_inserted += batch_size
                print(f'{entries_inserted} entries inserted to database')


def _parse_line(line):
    results = APACHE_LOG_PATTERN.findall(line)
    if results:
        ip_address, log_date, http_method, uri, status_code, response_size = results[0]
        log = {
            'ip_address': ip_address,
            'log_date': datetime.strptime(log_date, '%d/%b/%Y:%H:%M:%S %z'),
            'http_method': http_method,
            'uri': uri,
            'status_code': int(status_code),
            'response_size': None if response_size == '-' else int(response_size)
        }
        return log
    return {}
