from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def handle(self, *args, **options):
        print('\n' + 'Unique IPs: ' + str(count_amount_of_unique_ips()[0][0]))

        print('\n' + 'Top IPs:')
        for ip in count_top_ips():
            print(ip[1] + ' - ' + str(ip[0]))

        print('\n' + 'Methods:')
        for method in count_http_methods():
            print(method[1] + ' - ' + str(method[0]))

        print('\n' + 'Sum response size: ' + str(sum_response_size()[0][0]))


def execute_query(query):
    cursor = connection.cursor()

    cursor.execute(query)
    return cursor.fetchall()


def count_amount_of_unique_ips():
    query = '''
        select count(distinct ip_address)
        from core_apachelog 
    '''
    return execute_query(query)


def count_top_ips(limit=10):
    query = f'''
        SELECT count(ip_address) as c, ip_address
        from core_apachelog 
        group by ip_address
        order by c desc
        limit {limit}
    '''
    return execute_query(query)


def count_http_methods():
    query = '''
        SELECT count(http_method) as c, http_method
        from core_apachelog 
        group by http_method
        order by c desc
    '''
    return execute_query(query)


def sum_response_size():
    query = '''
        SELECT sum(response_size)
        from core_apachelog 
    '''
    return execute_query(query)
