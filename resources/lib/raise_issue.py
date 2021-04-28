# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

import xbmcgui

import getpass
import os
import requests

from resources.lib import repository
from resources.lib import settings
from resources.lib import tools
from resources.lib.github_api import GithubAPI

API = GithubAPI()

_home = tools.translate_path('special://home')
_log_location = tools.translate_path('special://logpath')

_addon_name = settings.get_addon_info('name')
_addon_id = settings.get_addon_info('id')
_addon_version = settings.get_addon_info('version')

_color = settings.get_setting_string('general.color')
_compact = settings.get_setting_boolean('general.compact')

_paste_url = 'https://paste.kodi.tv/'
_github_token = settings.get_setting_string('github.token')


def raise_issue():
    user, repo = _get_repo_selection()
    if user and repo:
        dialog = xbmcgui.Dialog()
        title = dialog.input(settings.get_localized_string(32006))
        if title:
            description = dialog.input(settings.get_localized_string(32007))
            log_key = None
            response, log_key = _upload_log()

            if response:
                try:
                    resp = _post_issue(_format_issue(title, description, log_key), user, repo)
                    if 'message' not in resp:
                        dialog.notification(_addon_name,
                                            settings.get_localized_string(32009).format(_color, repo, _color, log_key))
                    else:
                        dialog.ok(_addon_name, resp['message'])
                except requests.exceptions.RequestException as e:
                    dialog.notification(_addon_name, settings.get_localized_string(32010))
                    tools.log('Error opening issue: {}'.format(e), 'error')
        else:
            dialog.ok(_addon_name, settings.get_localized_string(32011))
        del dialog


def _get_repo_selection():
    dialog = xbmcgui.Dialog()
    repos, files = repository.get_repos()
    names = [i for i in [i["name"] for i in repos.values()]]
    keys = [i for i in repos]
    
    repo_items = []
    for name in names:
        li = xbmcgui.ListItem("{}".format(name))
        
        if not _compact:
            repo_def = [repos[i] for i in repos if repos[i]['name'] == name][0]
            user = repo_def['user']
            repo = repo_def['repo_name']
            icon = repository.get_icon(user, repo)
            li.setArt({'thumb': icon})

        repo_items.append(li)

    selection = dialog.select(settings.get_localized_string(32012), repo_items, useDetails=not _compact)
    del dialog
    if not selection == -1:
        repo = repos[keys[selection]]
        return repo['user'], repo['repo_name']
    return '', ''


def _post_issue(post_data, user, repo):
    return API.raise_issue(user, repo, post_data)


def _get_log_contents():
    log_file = os.path.join(_log_location, 'kodi.log')
    if os.path.exists(log_file):
        return tools.read_all_text(log_file)
    else:
        tools.log("Error finding logs!", 'error')


def _censor_log_content(log_content):
    censor_string = '--- CENSORED ---'
    log_content = log_content.replace(getpass.getuser(), censor_string)
    log_content = log_content.replace(_github_token, censor_string)
    return log_content


def _upload_log():
    log_data = _censor_log_content(_get_log_contents())
    user_agent = '{}: {}'.format(_addon_id, _addon_version)

    try:
        response = requests.post(_paste_url + 'documents',
                                 data=log_data.encode('utf-8'),
                                 headers={'User-Agent': user_agent}).json()
        if 'key' in response:
            return True, response['key']
        elif 'message' in response:
            tools.log('Upload failed: {}'.format(response['message']), level='error')
            return False, response['message']
        else:
            tools.log('Invalid response: {}'.format(response), level='error')
            return False, 'Error posting the log file.'
    except requests.exceptions.RequestException as e:
        tools.log('Failed to retrieve the paste URL: {}'.format(e), level='error')
        return False, 'Failed to retrieve the paste URL.'


def _format_issue(title, description, log_key):
    log_desc = """{}
    
    {}
    
    Log File - {}""".format(settings.get_localized_string(32013).format(_addon_name), description, _paste_url + 'raw/' + log_key)

    return {
        "title": title,
        "body": log_desc
    }
