import json
import re

def convert_to_bind(json_file_path, bind_file_path):
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
        
    resource_records = data['ResourceRecordSets']
    
    def format_rname(rname):
        """Formats the responsible party email for SOA record."""
        return rname.replace("@", ".") + "."
    
    with open(bind_file_path, 'w') as bind_file:
        for record in resource_records:
            name = record['Name']
            rtype = record['Type']
            if 'TTL' in record:
                ttl = record['TTL']
            else:
                ttl = None

            if rtype == 'A':
                if 'AliasTarget' in record:
                    value = record['AliasTarget']['DNSName']
                    bind_file.write(f"{name} IN CNAME {value}\n")
                else:
                    values = [r['Value'] for r in record['ResourceRecords']]
                    for value in values:
                        bind_file.write(f"{name} {ttl} IN A {value}\n")

            elif rtype == 'NS':
                values = [r['Value'] for r in record['ResourceRecords']]
                for value in values:
                    bind_file.write(f"{name} {ttl} IN NS {value}\n")

            elif rtype == 'SOA':
                values = record['ResourceRecords'][0]['Value'].split()
                mname, rname, serial, refresh, retry, expire, minimum = values
                rname = format_rname(rname)
                bind_file.write(f"{name} {ttl} IN SOA {mname} {rname} {serial} {refresh} {retry} {expire} {minimum}\n")

            elif rtype == 'CNAME':
                values = [r['Value'] for r in record['ResourceRecords']]
                for value in values:
                    bind_file.write(f"{name} {ttl} IN CNAME {value}\n")

            elif rtype == 'TXT':
                values = [r['Value'] for r in record['ResourceRecords']]
                for value in values:
                    bind_file.write(f"{name} {ttl} IN TXT {value}\n")

            elif rtype == 'MX':
                values = [r['Value'] for r in record['ResourceRecords']]
                for value in values:
                    preference, exchange = value.split()
                    bind_file.write(f"{name} {ttl} IN MX {preference} {exchange}\n")

# Paths to the JSON input and BIND output files
json_file_path = '/path/to/route53.json'
bind_file_path = '/path/to/bind/export.zone.txt'

convert_to_bind(json_file_path, bind_file_path)