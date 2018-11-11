from ftplib import FTP
#from string import maketrans
import gzip
import datetime
import unicodedata
import re
import http.client


def f_normalize(data):

    text = unicodedata.normalize('NFKD', data)
    text = text.encode('ascii', 'ignore')
    text = text.decode('utf_8')
    return str(text)



def f_ftp_download(host, directory, filename, filename_local):
    """FTP file download method

    Details are coming shortly.
    """
    ftp = FTP(host)
    ftp.login()
    ftp.cwd(directory)
    #ftp.dir()
    ftp.retrbinary('RETR ' + filename, open(filename_local, 'wb').write)
    ftp.quit()

def f_read_gzip_file(filename, encoding = 'utf_8'):
    """Reads gzip file content

    Returns an array; file content is split by EOL
    """
    with gzip.open(filename, 'rt', encoding) as f:
        file_content = f.read().splitlines()
        #file_content = f.readlines()
        #splitlines >>> removes EOL
        #readlines  >>> EOL stays
        return file_content

def f_print(message):
    date_time = datetime.datetime.now().isoformat(sep=' ')
    print(date_time + ': ' + message)


def f_is_float(num):
    try:
        float(num)
        return True
    except:
        return False


def f_is_int(num):
    try:
        int(num)
        return True
    except:
        return False


def f_get_country(id):

    cc = 'Country:'
    conn = http.client.HTTPSConnection('www.imdb.com')
    conn.request('GET', '/title/' + id + '/')
    resp = conn.getresponse()
    # print(resp.status, resp.reason)
    content = resp.read().decode('utf-8') # convert 'bytes' to 'string'

    if cc in content:
        start = content.find(cc) + len(cc)
        end = content.find('</div>', start)
        content = content[start:end]
        content = re.sub('\s*'        , ''   , content)
        content = re.sub('<a\S*?>'    , ''   , content)
        content = re.sub('<s\S*?n>'   , ', ' , content)
        content = re.sub('</h4>|</a>' , ''   , content)
    else:
        content = '...'

    return content



if __name__ == '__main__':
    """used for testing

    """
    pass


