from bs4 import BeautifulSoup
from datetime import datetime
import urllib.request
import os
import time
import pgi
pgi.require_version('Notify', '0.7')
from pgi.repository import Notify

Notify.init('pdl')


def get_current_url():
    with urllib.request.urlopen('http://www.poorlydrawnlines.com/') as pdl_site:
        data = pdl_site.read()

    soup = BeautifulSoup(data, features='html.parser')
    image = soup.find('figure', attrs={'class': 'wp-block-image'}).find('img')
    image_url = (image.attrs['src'])
    title = image_url.split('/')[-1].replace('.png', '')
    new_url = 'http://www.poorlydrawnlines.com/comic/' + title

    return new_url


def notify_comic(url):
    notification = Notify.Notification.new('New comic!', url, 'emblem-OK')
    notification.show()


def check_comic():
    home_folder = os.path.expanduser('~')
    local_folder = home_folder + '/.local/share/pdl-notify'
    last_seen_path = home_folder + '/.local/share/pdl-notify/last_seen'

    if not os.path.exists(last_seen_path):
        if not os.path.exists(local_folder):
            os.makedirs(local_folder)

        os.mknod(last_seen_path)

    current_url = get_current_url()

    with open(last_seen_path, mode='r') as last_seen_file:
        last_seen_url = last_seen_file.read()

    if not last_seen_url or last_seen_url != current_url:
        with open(last_seen_path, mode='w') as last_seen_file:
            last_seen_file.write(current_url)
            notify_comic(current_url)


def check_date():
    day_of_week = datetime.today().weekday()

    return day_of_week in [0, 2, 4]


if __name__ == '__main__':
    check_comic()

    while check_date():
        time.sleep(5 * 60)
        check_comic()
