from enums import Heya, Shusshin, Kimarite, Wins, Sansho, Yusho, Division, Debut

BOUT_QUERY_URL_BASE = 'http://sumodb.sumogames.de/Query_bout.aspx?show_form=0&rowcount=5'

_MAEZUMO_STRINGS = ['mz', 'mae-zumo', 'maezumo']
_JONOKUCHI_STRINGS = ['jk', 'jonokuchi']
_JONDIAN_STRINGS = ['jd', 'jondian']
_SANDANME_STRINGS = ['sd', 'sandanme']
_MAKUSHITA_STRINGS = ['ms', 'makushita']
_JURYO_STRINGS = ['j', 'juryo']
_MAKUUCHI__STRINGS = ['m', 'makuuchi ', 'makunouchi']
_SHIKONA_CHANGES_STRINGS = ['changes', 'include changes', 'include-changes', 'shikona-changes', 'shikona changes']
_WINS_OPTION_STRINGS = ['wins-options', 'wins options', 'winsopt', 'wins option', 'wins-option']


def create_url(
        basho=None,
        day=None,
        division=None,  # str or list of str for all divisions
        east_side_only=False,
        rikishi1_wins_only=False,
        rikishi1_losses_only=False,
        kimarite=None,
        rikishi1=None,  # Dictionary with all the values of rikishi 1
        rikishi2=None  # Dictionary with all the values of rikishi 2
):
    """
    Create the url for querying with the parameters provided

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
    :return: url for querying
    :rtype: str
    """
    retstr = BOUT_QUERY_URL_BASE
    if basho is not None:
        retstr += _create_basho(basho)
    if day is not None:
        retstr += _create_day(day)
    if division is not None:
        retstr += _create_division(division)
    if kimarite is not None:
        retstr += _create_kimarite(kimarite)
    retstr += _check_bool_and_create('east1', east_side_only, 'east_side_only')
    retstr += _check_bool_and_create('onlyw1', rikishi1_wins_only, 'rikishi1_wins_only')
    retstr += _check_bool_and_create('onlyl1', rikishi1_losses_only, 'rikishi1_losses_only')
    if rikishi1 is not None:
        retstr += _create_rikishi_parameters(1, rikishi1)
    if rikishi2 is not None:
        retstr += _create_rikishi_parameters(2, rikishi2)
    return retstr


def _create_basho(basho):
    """
    :param basho: basho year, date or range of dates
    :rtype: int or str
    :return: the url parameter string
    :rtype: str
    """
    retstr = '&year='
    if type(basho) == int:
        retstr += str(basho)
    elif type(basho) == str:
        retstr += basho
    else:
        raise TypeError('Basho must be int or str')
    return retstr


def _create_day(day):
    """
    :param day: basho day or range of days, 16 for playoffs
    :type day: int or str
    :return: the url parameter string
    :rtype: str
    """
    retstr = '&day='
    if type(day) == int:
        retstr += str(day)
    elif type(day) == str:
        retstr += day
    else:
        raise TypeError('Day must be int or str')
    return retstr


def _create_division(division):
    """

    :param division:
    :type division: str or list[str]
    :return: the url parameter string
    :rtype: str
    """
    retstr = ''
    if type(division) == str:
        retstr += _division_str_to_parameter(division)
    elif _is_list_of_type(division, str):
        for _ in division:
            retstr += _division_str_to_parameter(_)
    else:
        raise TypeError('division must be an str or list[str]')
    return retstr


def _division_str_to_parameter(division):
    division = division.lower()
    if division in _MAEZUMO_STRINGS:
        return '&mz=on'
    elif division in _JONOKUCHI_STRINGS:
        return '&jk=on'
    elif division in _JONDIAN_STRINGS:
        return '&jd=on'
    elif division in _SANDANME_STRINGS:
        return '&sd=on'
    elif division in _MAKUSHITA_STRINGS:
        return '&ms=on'
    elif division in _JURYO_STRINGS:
        return '&j=on'
    elif division in _MAKUUCHI__STRINGS:
        return '&m=on'
    else:
        raise ValueError('\'' + division + '\' is not recognized as a division')


def _is_list_of_type(value, test_type):
    if type(value) != list:
        return False
    for _ in value:
        if type(_) != test_type:
            return False
    return True


def _create_kimarite(kimarite):
    retstr = '&kimarite='
    if isinstance(kimarite, type(Kimarite.AMIUCHI)):
        retstr += str(kimarite.value)
    else:
        raise TypeError('Kimarite must be a Kimarite enum')
    return retstr


def _check_bool_and_create(param_str, value, errmsg_start):
    if type(value) == bool:
        if value:
            return '&' + param_str + '=on'
        else:
            return ''
    else:
        raise TypeError(errmsg_start + ' must be a bool')


def _create_rikishi_parameters(num, rikishi):
    retstr = ''
    for attr in rikishi:
        if type(attr) == str:
            attrl = attr.lower()
            if attrl == 'shikona':
                retstr += _create_rikishi_shikona(num, rikishi[attr])
            elif attrl in _SHIKONA_CHANGES_STRINGS:
                retstr += _create_rikishi_shikona_changes(num, rikishi[attr])
            elif attrl == 'heya':
                retstr += _create_rikishi_heya(num, rikishi[attr])
            elif attrl == 'shusshin':
                retstr += _create_rikishi_shusshin(num, rikishi[attr])
            elif attrl == 'rank':
                retstr += _create_rikishi_rank(num, rikishi[attr])
            elif attrl == 'wins':
                retstr += _create_rikishi_rank(num, rikishi[attr])
            elif attrl in _WINS_OPTION_STRINGS:
                retstr += _create_rikishi_winsopt(num, rikishi[attr])
            elif attrl == 'yusho':
                retstr += _create_rikishi_yusho(num, rikishi[attr])
            elif attrl == 'sansho':
                retstr += _create_rikishi_sansho(num, rikishi[attr])
            elif attrl == 'division':
                retstr += _create_rikishi_division(num, rikishi[attr])
            elif attrl == 'debut':
                retstr += _create_rikishi_debut(num, rikishi[attr])
            else:
                raise ValueError('\'' + attr + '\' is no a recognizable attribute')
        else:
            raise TypeError('All attributes in rikishi' + str(num) + 'must be str')
    return retstr


def _create_rikishi_shikona(num, attr_value):
    num = str(num)
    retstr = ''
    if type(attr_value) != str:
        retstr += '&shikona' + num + '=' + attr_value
    else:
        raise TypeError(' Shikona in rikishi' + num + ' must be an str')
    return retstr


def _create_rikishi_shikona_changes(num, attr_value):
    num = str(num)
    retstr = ''
    if type(attr_value) == bool:
        if attr_value:
            retstr += '&shikona_changes' + num + '=on'
    else:
        raise TypeError('Shikona-changes in rikishi' + num + ' must be a bool')
    return retstr


def _create_rikishi_heya(num, attr_value):
    num = str(num)
    retstr = ''
    if isinstance(attr_value, type(Heya.AJIGAWA)):
        retstr += '&heya' + num + '=' + str(attr_value.value)
    else:
        raise TypeError('Heya in rikishi' + num + ' must be a Heya enum')
    return retstr


def _create_rikishi_shusshin(num, attr_value):
    num = str(num)
    retstr = ''
    if isinstance(attr_value, type(Shusshin.AICHI)):
        retstr += '&shusshin' + num + '=' + str(attr_value.value)
    else:
        raise TypeError('Shusshin in rikishi' + num + ' must be a Shusshin enum')
    return retstr


def _create_rikishi_rank(num, attr_value):
    num = str(num)
    retstr = ''
    if type(attr_value) == str:
        retstr += '&rank' + num + '=' + attr_value
    elif _is_list_of_type(attr_value, str):
        retstr += '&rank' + num + '='
        for i in range(len(attr_value) - 1):
            retstr += attr_value[i] + ','
        retstr += attr_value[-1]
    else:
        raise TypeError('Rank in rikishi' + num + ' must be an str or list[str]')
    return retstr


def _create_rikishi_wins(num, attr_value):
    num = str(num)
    retstr = ''
    if type(attr_value) == str:
        retstr += '&wins' + num + '=' + attr_value
    elif type(attr_value) == int:
        retstr += '&wins' + num + '=' + str(attr_value)
    else:
        raise TypeError('wins in rikishi' + num + ' must be an int or str')
    return retstr


def _create_rikishi_winsopt(num, attr_value):
    num = str(num)
    retstr = ''
    if isinstance(attr_value, type(Wins.AFTER_BOUT)):
        if attr_value != Wins.AFTER_BOUT:
            retstr += '&winsopt' + num + '=' + str(attr_value.value)
    else:
        raise TypeError('Wins option in rikishi' + num + ' must be a Wins enum')
    return retstr


def _create_rikishi_yusho(num, attr_value):
    num = str(num)
    retstr = ''
    if isinstance(attr_value, type(Yusho.OTHER)):
        retstr += _create_rikishi_yusho_helper(num, attr_value)
    elif _is_list_of_type(attr_value, type(Yusho.OTHER)):
        for _ in attr_value:
            retstr += _create_rikishi_yusho_helper(num, _)
    else:
        raise TypeError('Yusho option in rikishi' + num + ' must be a Yusho enum or list[Yusho]')
    return retstr


def _create_rikishi_yusho_helper(numstr, value):
    if value == Yusho.OTHER:
        return '&oy' + numstr + '=on'
    elif value == Yusho.YUSHO:
        return '&y' + numstr + '=on'
    elif value == Yusho.YUSHO_PLAYOFF:
        return '&yd' + numstr + '=on'
    elif value == Yusho.JUN_YUSHO:
        return '&jy' + numstr + '=on'
    else:
        return ''


def _create_rikishi_sansho(num, attr_value):
    num = str(num)
    retstr = ''
    if isinstance(attr_value, type(Sansho.GINO_SHO)):
        retstr += _create_rikishi_sansho_helper(num, attr_value)
    elif _is_list_of_type(attr_value, type(Sansho.GINO_SHO)):
        for _ in attr_value:
            retstr += _create_rikishi_sansho_helper(num, _)
    else:
        raise TypeError('Sansho option in rikishi' + num + ' must be a Sansho enum or list[Sansho]')
    return retstr


def _create_rikishi_sansho_helper(numstr, value):
    if value == Sansho.NO_SANSHO:
        return '&ns' + numstr + '=on'
    elif value == Sansho.SHUKUN_SHO:
        return '&ss' + numstr + '=on'
    elif value == Sansho.KANTO_SHO:
        return '&ks' + numstr + '=on'
    elif value == Sansho.GINO_SHO:
        return '&gs' + numstr + '=on'
    else:
        return ''


def _create_rikishi_division(num, attr_value):
    num = str(num)
    retstr = ''
    if isinstance(attr_value, type(Division.FROM_LOWER)):
        pass
    elif _is_list_of_type(attr_value, type(Division.FROM_LOWER)):
        pass
    else:
        raise TypeError('Sansho option in rikishi' + num + ' must be a Sansho enum or list[Sansho]')
    return retstr


def _create_rikishi_division_helper(numstr, value):
    if value == Division.FROM_LOWER:
        return '&lowerd' + numstr + '=on'
    elif value == Division.SAME_AS_BOUT:
        return '&samed' + numstr + '=on'
    else:
        return ''


def _create_rikishi_debut(num, attr_value):
    num = str(num)
    retstr = ''
    if isinstance(attr_value, type(Debut.RANK)):
        retstr += _create_rikishi_debut_helper(num, attr_value)
    elif _is_list_of_type(attr_value, type(Debut.RANK)):
        for _ in attr_value:
            retstr += _create_rikishi_debut_helper(num, _)
    else:
        raise TypeError('Debut option in rikishi' + num + ' must be a Debut enum or list[Debut]')
    return retstr


def _create_rikishi_debut_helper(numstr, value):
    if value == Debut.DIVISION:
        return '&debutd' + numstr + '=on'
    elif value == Debut.RANK:
        return '&debutr' + numstr + '=on'
    else:
        return ''
