"""
module containing functions to parse and order ipvX to a country
"""
import os
import random
import ipaddress
import lzma
import zipfile
import tarfile
import GeoIP as gi


def extract_file(args):
    """
    decompresses a file
    :param args: file obj
    :return: None
    """
    input_file = args['filename']
    tup = os.path.splitext(input_file)
    ext = tup[1]
    output_file = tup[0]
    if ext == '.xz':
        with lzma.open(input_file, 'rb') as i:
            with open(output_file, 'wb') as o:
                o.write(i.read())
    elif ext == '.zip':
        name = os.path.splitext(input_file)[0]
        with zipfile.ZipFile(input_file, 'r') as z:
            with open(output_file, 'wb') as i:
                i.write(z.read(name))
    elif ext == '.tar':
        with tarfile.open(input_file, mode='r|*') as i:
            i.extractall(path='uploads')
    elif ext == '.gz':
        with tarfile.open(input_file, mode='r|*') as i:
            i.extractall(path='uploads')


def make_readable(file):
    """
    Convert file into readable
    :param file: file object
    :return: proper path to a radable file
    """
    input_file = file
    output_file = os.path.splitext(input_file)[0] + '.txt'
    with open(input_file, 'rb') as i:
        with open(output_file, 'wb') as j:
            j.write(i.read())
    os.remove(input_file)
    return str(output_file)


def file_info(file):
    """
    General information about the file without reading
    :param file: file object
    :return: overall size, number of lines and their size
    """
    f = open(file)
    lines = 0
    size = os.stat(file).st_size
    for line in f:
        lines += 1
    line_size = size / lines
    f.close()
    return size, lines, line_size


def reservoir_algo(input_file, sample_size):
    """
    Random subsampling: https://en.wikipedia.org/wiki/Reservoir_sampling
    S(n) - input file with n lines (we assume n is unknown)
    R(k) - output file called "test_filename.ext" with k lines (k is given in the parameters)

    :param input_file:
    :param sample_size:
    :return:
    """
    f = open(input_file)
    outF = 'test_' + input_file
    o = open(outF, 'w')
    # get a single random line:
    total_size_b = os.stat(input_file).st_size
    for i in range(0, sample_size):
        rand_line = random.randint(0, total_size_b)
        f.seek(rand_line)
        f.readline()
        r = f.readline()
        o.write(str(r))
    return outF


def parse(s):
    """
    Helper function
    :param s:
    :return:
    """
    new_line = []
    r = s.split(' ')
    address = r[0]
    new_line.append(address)
    return new_line


def get_statistics(file_name, mapping_dict):
    """
    Parses the file to find out geographic distribution of the ips
    :param file_name: string file name
    :param mapping_dict: mapping country_code:int
    :return:
    """
    with open(file_name, 'r') as f:
        ip4 = gi.open('tmp/GeoIP.dat', gi.GEOIP_STANDARD)
        ip6 = gi.open("tmp/GeoIPv6.dat", gi.GEOIP_STANDARD)
        false_addresses = 0
        ip_by_country = {'undefined': 0}
        for country in mapping_dict.keys():
            ip_by_country[country.lower()] = 0
        ipv4_total = 0
        ipv6_total = 0

        for line in f:
            res = parse(line)
            try:
                if ipaddress.ip_address(res[0]):
                    if type(ipaddress.ip_address(res[0])) == ipaddress.IPv4Address:
                        ipv4_total += 1
                    else:
                        ipv6_total += 1
                    if ip4.country_name_by_addr(res[0]):
                        origin = ip4.country_name_by_addr(res[0]).lower()
                        ip_by_country[origin] += 1
                    elif ip6.country_name_by_addr_v6(res[0]):
                        origin = ip6.country_name_by_addr_v6(res[0]).lower()
                        ip_by_country[origin] += 1
                    else:
                        ip_by_country['undefined'] += 1
            except ValueError:
                false_addresses += 1

    res = {}
    for key, value in ip_by_country.items():
        res[mapping_dict[key]] = value
    return res

