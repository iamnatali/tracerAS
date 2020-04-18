import subprocess
import itertools
import requests
import re
import json


def first_digit(line):
    mo = re.match(r'\s*[0-9]', line)
    return mo


def get_last_part(line):
    parts = line.split()
    return parts[len(parts)-1]


def filter_list(out):
    without_stars = itertools.takewhile(lambda x: "*" not in x, out)
    only_useful = filter(first_digit, without_stars)
    ip_list = list(map(get_last_part, only_useful))
    return ip_list


def get_ip_list(user_input):
    res = subprocess.run(["tracert", "-d", "-h", "10", user_input], capture_output=True)
    out = str(res.stdout, encoding="cp866").split("\r\n")
    print(out)
    return filter_list(out)


def get_asn(ip):
    asn_query = r"https://stat.ripe.net/data/network-info/data.json?resource="
    asn_resp = requests.get(asn_query + ip)
    json_dict = json.loads(asn_resp.text)
    asn_arr = json_dict["data"]
    if len(asn_arr) != 0:
        asn = asn_arr["asns"][0]
        return asn


def get_country_provider(ip, is_grey):
    country_provider_query = "https://stat.ripe.net/data/address-space-hierarchy/data.json?resource="
    country_provider_resp = requests.get(country_provider_query + ip)
    json_dict = json.loads(country_provider_resp.text)
    cp_arr = json_dict["data"]["exact"]
    country = cp_arr[0]["country"]
    if is_grey:
        provider = "grey address is not managed by the RIPE NCC"
    else:
        provider = cp_arr[0]["descr"]
    return country, provider


def main(user_input):
    print("please wait")
    ip_list = get_ip_list(user_input)
    i = 0
    heading = '{:3}{:16}{:8}{:8}{}'\
        .format("№","IP", "ASN", "country", "provider")
    print(heading)
    for ip in ip_list:
        i += 1
        asn = get_asn(ip)
        is_grey = not asn
        (country, provider) = get_country_provider(ip,is_grey)
        format_str = '{:3}{:16}{:8}{:3}{}'\
            .format(str(i), str(ip),str(asn), str(country), str(provider))
        print(format_str)


if __name__ == '__main__':
    ui = input("please enter ip or domain name\n")
    main(ui)
