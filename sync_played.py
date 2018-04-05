#!/usr/bin/python
# -*- coding: utf-8 -*-
####
# 04/2018 Graham Benton <dp.gpbenton@xoxy.net>
#
# This script is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# gPodder is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#

# This script sends a played indication to the web service when the
# state goes from new to played.

import gpodder
import logging
logger = logging.getLogger(__name__)

_ = gpodder.gettext

__title__ = _('sync played status')
__description__ = _('sends played notice to web service')
__authors__ = 'Graham Benton <dp.gpbenton@xoxy.net>'
__category__ = 'post-download'

class gPodderExtension:
    def __init__(self, container):
        self.container = container
        self.config = container.config
        self.wasNew = set()

    def on_ui_object_available(self, name, ui_object):
        if name == 'gpodder-gtk':
            self.ui_object = ui_object

    def on_podcast_updated(self, podcast):
        new_episodes = [e for e in podcast.get_all_episodes() if e.is_new]
        for episode in new_episodes:
            logger.debug("Adding {}".format(episode.trimmed_title))
            self.wasNew.add(episode.guid)

    def on_episode_save(self, episode):
        if not episode.is_new:
            if episode.guid in self.wasNew:
                logger.info("Sending played for {}".format(episode.trimmed_title))
                if hasattr(self, "ui_object"):
                    self.ui_object.mygpo_client.on_playback([episode])
                self.wasNew.remove(episode.guid)

