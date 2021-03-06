# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

##########################################################################
# OpenLP - Open Source Lyrics Projection                                 #
# ---------------------------------------------------------------------- #
# Copyright (c) 2008-2022 OpenLP Developers                              #
# ---------------------------------------------------------------------- #
# This program is free software: you can redistribute it and/or modify   #
# it under the terms of the GNU General Public License as published by   #
# the Free Software Foundation, either version 3 of the License, or      #
# (at your option) any later version.                                    #
#                                                                        #
# This program is distributed in the hope that it will be useful,        #
# but WITHOUT ANY WARRANTY; without even the implied warranty of         #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
# GNU General Public License for more details.                           #
#                                                                        #
# You should have received a copy of the GNU General Public License      #
# along with this program.  If not, see <https://www.gnu.org/licenses/>. #
##########################################################################
import logging

from flask import abort, request, Blueprint, jsonify

from openlp.core.api.lib import login_required
from openlp.core.lib.plugin import PluginStatus
from openlp.core.common.registry import Registry

log = logging.getLogger(__name__)


plugins = Blueprint('v2-plugins', __name__)


def search(plugin_name, text):
    plugin = Registry().get('plugin_manager').get_plugin_by_name(plugin_name)
    if plugin.status == PluginStatus.Active and plugin.media_item and plugin.media_item.has_search:
        results = plugin.media_item.search(text, False)
        return results
    return None


def live(plugin_name, id):
    plugin = Registry().get('plugin_manager').get_plugin_by_name(plugin_name)
    if plugin.status == PluginStatus.Active and plugin.media_item:
        getattr(plugin.media_item, '{action}_go_live'.format(action=plugin_name)).emit([id, True])


def add(plugin_name, id):
    plugin = Registry().get('plugin_manager').get_plugin_by_name(plugin_name)
    if plugin.status == PluginStatus.Active and plugin.media_item:
        item_id = plugin.media_item.create_item_from_id(id)
        getattr(plugin.media_item, '{action}_add_to_service'.format(action=plugin_name)).emit([item_id, True])


def get_options(plugin_name):
    plugin = Registry().get('plugin_manager').get_plugin_by_name(plugin_name)
    if plugin.status == PluginStatus.Active and plugin.media_item:
        options = plugin.media_item.search_options()
        return options
    return []


def set_option(plugin_name, search_option, value):
    plugin = Registry().get('plugin_manager').get_plugin_by_name(plugin_name)
    success = False
    if plugin.status == PluginStatus.Active and plugin.media_item:
        success = plugin.media_item.set_search_option(search_option, value)
    return success


@plugins.route('/<plugin>/search')
@login_required
def search_view(plugin):
    log.debug(f'{plugin}/search called')
    text = request.args.get('text', '')
    result = search(plugin, text)
    return jsonify(result)


@plugins.route('/<plugin>/add', methods=['POST'])
@login_required
def add_view(plugin):
    log.debug(f'{plugin}/add called')
    data = request.json
    if not data:
        abort(400)
    id = data.get('id', -1)
    add(plugin, id)
    return '', 204


@plugins.route('/<plugin>/live', methods=['POST'])
@login_required
def live_view(plugin):
    log.debug(f'{plugin}/live called')
    data = request.json
    if not data:
        abort(400)
    id = data.get('id', -1)
    live(plugin, id)
    return '', 204


@plugins.route('/<plugin>/search-options', methods=['GET'])
def search_options(plugin):
    """
    Get the plugin's search options
    """
    log.debug(f'{plugin}/search-options called')
    return jsonify(get_options(plugin))


@plugins.route('/<plugin>/search-options', methods=['POST'])
@login_required
def set_search_option(plugin):
    """
    Sets the plugin's search options
    """
    log.debug(f'{plugin}/search-options-set called')
    data = request.json
    if not data:
        log.error('Missing request data')
        abort(400)
    option = data.get('option', None)
    value = data.get('value', None)
    if value is None:
        log.error('Invalid data passed in value')
        abort(400)

    if set_option(plugin, option, value):
        return '', 204
    else:
        log.error('Invalid option or value')
        return '', 400
