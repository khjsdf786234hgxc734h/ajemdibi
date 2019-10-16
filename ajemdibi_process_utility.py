from ftplib import FTP
import gzip
import datetime
import unicodedata
import re
import urllib.request

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


def f_get_html_page(id):
    req = urllib.request.Request('https://www.imdb.com/title/' + id + '/')
    # !!! do not use 'gzip' in the header as encoding
    # !!! you will get an error, when you want to convert to 'utf-8'
    # !!! req.add_header('Accept-Encoding','gzip, deflate, br')
    req.add_header('Accept-Language','en-US,en;q=0.5')
    req.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    req.add_header('Cache-Control','max-age=0')
    req.add_header('Connection','keep-alive')
    req.add_header('DNT','1')
    req.add_header('Host','www.imdb.com')
    req.add_header('Referer','https://www.imdb.com/?ref_=nv_home')
    req.add_header('Upgrade-Insecure-Requests','1')
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0')
    #print('-------')
    #print(req.header_items())
    #print('-------')
    with urllib.request.urlopen(req) as resp:
        content = resp.read().decode('utf-8') # convert 'bytes' to 'string'
        #print('-------')
        #print(resp.geturl())
        #print('-------')
        #print(resp.info())
        #print('-------')
        #print(resp.status)
        #print('-------')
        #print(resp.reason)
        #print('-------')

    return content


def f_get_country(content):

    cc = 'Country:'
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


def f_get_movie_type(content):

    cc = 'title="See more release dates" >'
    if cc in content:
        start = content.find(cc) + len(cc)
        end = content.find('</a>', start)
        content = content[start:end]
        content = re.sub('([0-9]|\().*', ''   , content)
        content = re.sub('\s*$'        , ''   , content)
        if content == '':
            content = 'Film'
    else:
        content = '...'

    return content


if __name__ == '__main__':
    """used for testing

    """
    pass


