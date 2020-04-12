import re
import urllib.request

import pandas as pd
from bs4 import BeautifulSoup

from url_builder import create_url

BOUT_QUERY_URL = 'http://sumodb.sumogames.de/Query_bout.aspx'  # The sumodb bout query address
_WIN_IMG_STRINGS = ['shiro', 'fusensho', 'hikiwake']
_DF_COLUMNS = ['Date', 'Day', 'Rikishi 1 Rank', 'Rikishi 1 Name', 'Rikishi 1 ID', 'Rikishi 1 Score',
               'Rikishi 1 Basho score', 'Rikishi 1 Result', 'Kimarite', 'Rikishi 2 Result', 'Rikishi 2 Rank',
               'Rikishi 2 Name', 'Rikishi 2 ID', 'Rikishi 2 Score', 'Rikishi 2 Basho Score']


def query(
        basho=None,
        day=None,
        division=None,  # str or list of str for all divisions
        east_side_only=False,
        rikishi1_wins_only=False,
        rikishi1_losses_only=False,
        kimarite=None,
        rikishi1=None,  # Dictionary with all the values of rikishi 1
        rikishi2=None,  # Dictionary with all the values of rikishi 2
        verbose=False
):
    """
    Query sumodb bout query with the given parameters.

    :param basho: Basho dates
    :type basho: int or str
    :param day: The day/s
    :type day: int or str
    :param division: The divisions
    :type division: str or list of str
    :param east_side_only: east side wins only
    :type east_side_only: bool
    :param rikishi1_wins_only: rikishi 1 wins
    :type rikishi1_wins_only: bool
    :param rikishi1_losses_only: rikishi 1 loses
    :type rikishi1_losses_only: bool
    :param kimarite: The kimarite enum
    :type kimarite: int or str
    :param rikishi1: the dictionary with the info for the rikishi 1
    :type rikishi1: dict
    :param rikishi2: the dictionary with the info for the rikishi 2
    :type rikishi2: dict
    :param verbose: print progress or not
    :type verbose: bool
    :return: A dataframe with the data, None of 0 bouts found
    :rtype: pandas.core.frame.DataFrame
    """
    url = create_url(basho, day, division, east_side_only, rikishi1_wins_only, rikishi1_losses_only, kimarite,
                     rikishi1, rikishi2)
    _print_verbose('Created url: ' + url, verbose)
    _print_verbose('Scraping page with offset 0', verbose)
    soup = get_soup_from_url(url)
    results_found = _get_results_found_from_soup(soup)
    if results_found == -1 or results_found == 0:
        _print_verbose('No results found', verbose)
        return None
    _print_verbose(str(results_found) + ' results found', verbose)
    df = get_bouts_from_soup(soup)
    if results_found > 1000:
        _print_verbose('Needs to scrape ' + str((results_found - 1) // 1000) + ' more pages', verbose)
        all_res = [df]
        for i in range(1000, results_found, 1000):
            _print_verbose('Scraping page with offset ' + str(i), verbose)
            all_res.append(get_bouts_from_soup(get_soup_from_url(url + '&offset=' + str(i))))
        _print_verbose('Finished scraping', verbose)
        return pd.concat(all_res)
    else:
        _print_verbose('Finished scraping', verbose)
        return df


def _get_results_found_from_soup(soup):
    """

    :param soup: soup of th
    :type soup: bs4.BeautifulSoup
    :return: number of results found, -1 if query is not valid
    :rtype: int
    """
    results_found_strings = soup.findAll(text=re.compile('results found'))
    if results_found_strings:
        return int(str(results_found_strings[0]).split(' ')[0])
    else:
        return -1


def _print_verbose(msg, verbose):
    """
    :param msg: The message
    :type msg: str
    :param verbose: marks whether printing is wanted or not
    :type verbose: bool
    """
    if verbose:
        print(msg)


# ---------------------------------------Data Extraction---------------------------------------


def get_soup_from_file(path):
    """
    Turns the html file into a soup

    :param path: A file path which contains an html file of bout query from sumodb
    :type path: str
    :return: A soup of the file
    :rtype: bs4.BeautifulSoup
    """
    return BeautifulSoup(open(path), 'html.parser')


def get_soup_from_url(url):
    """
    Reads the url html page and turns it into a soup

    :param url: A url to the query result from http://sumodb.sumogames.de/Query_bout.aspx
    :type url: str
    :return: A soup of the page's html
    :rtype: bs4.BeautifulSoup
    """
    if not url.startswith(BOUT_QUERY_URL) or 'show_form=0' not in url:
        raise ValueError('Url must be from http://sumodb.sumogames.de/Query_bout.aspx with show_form=0')
    with urllib.request.urlopen(url) as fp:
        return BeautifulSoup(fp.read().decode('utf8'), 'html.parser')


def get_bouts_from_soup(soup):
    """
    Extracts bouts into a dataframe from html soup.


    Given a soup of an query result html from http://sumodb.sumogames.de/Query_bout.aspx this function will return a
    dataframe of all the bouts in it.
    get_soup_from_file(path) or get_soup_from_url(url) can help you get the soup

    :param soup: A soup from an html file of sumodb
    :type soup: bs4.BeautifulSoup
    :return: A dataframe containing all the bouts in the soup
    :rtype: pandas.core.frame.DataFrame
    """
    table = soup.find('table')
    if table is None:
        return None
    table_rows = table.findAll('tr')
    all_res = []
    for i in range(2, len(table_rows)):
        all_res.append(_get_bout_from_row(table_rows[i]))
    return pd.DataFrame(all_res, columns=_DF_COLUMNS)


def _get_bout_from_row(row):
    """
    Given a <tr> it will return a list containing the bout data

    :param row: A list of the tr
    :type row: bs4.element.Tag
    :return: A list with the bout data from the <tr>
    :rtype: list of str
    """
    result = []
    tds = row.find_all('td')
    result.append(tds[0].getText())  # Basho date
    result.append(tds[1].getText())  # Basho day
    result.extend(_get_rikishi_bout_data(tds[2:5]))  # Rikishi 1 data
    result.append(img_to_result(tds[5].find('img')['src']))  # Rikishi 1 result
    result.append(tds[6].getText().strip())  # Kimarite
    result.append(img_to_result(tds[7].find('img')['src']))  # Rikishi 2 result
    result.extend(_get_rikishi_bout_data(tds[8:11]))  # Rikishi 2 data
    return result


def _get_rikishi_bout_data(rikishi_data):
    """
    Given a list with the rikishi data, it will extract and sanitize the data

    :param rikishi_data: A sub section of the <tr> related to the rikishi
    :type rikishi_data: list of bs4.element.Tag
    :return: A list with the rikishi's data
    :rtype: list of str
    """
    result = [rikishi_data[0].getText()]  # Rikishi Rank
    rikishi_link = rikishi_data[1].find('a', href=True)
    result.append(rikishi_link.getText())  # Rikishi name
    result.append(rikishi_link['href'].split('=')[1])  # Rikishi sumodb ID
    rikishi_score = rikishi_data[2].getText().split()
    if len(rikishi_score) == 1:  # The score cell contains only basho score if it's the last day or playoffs
        result.append(rikishi_score[0])  # Rikishi score after fight
        result.append(rikishi_score[0])  # Rikishi basho score
    else:
        result.append(rikishi_score[0])  # Rikishi score after fight
        result.append(rikishi_score[1][1:-1])  # Rikishi basho score
    return result


def img_to_result(img_src):
    """
    Determines if the image marks a win or a loss

    :param img_src: The source of the win/loss picture
    :type img_src: str
    :return: whether the rikishi won or lost
    :rtype: str
    """
    if any(_ in img_src for _ in _WIN_IMG_STRINGS):
        return 'win'
    else:
        return 'loss'
