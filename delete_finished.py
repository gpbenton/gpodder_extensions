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

# This extension deletes downloaded file and marks played any episodes
# that are marked finished

import gpodder
import logging
logger = logging.getLogger(__name__)

_ = gpodder.gettext

__title__ = _('Delete finished episodes')
__description__ = _('Deletes downloaded files for finished episodes')
__authors__ = 'Graham Benton <dp.gpbenton@xoxy.net>'
__category__ = 'post-download'

class gPodderExtension:
    def __init__(self, container):
        self.container = container
        self.config = container.config

    def on_episode_save(self, episode):
        """ Called when an episode is saved to the database

        This extension will be called when a new episode is added to the
        database or when the state of an existing episode is changed.

        @param episode: A gpodder.model.PodcastEpisode instance
        """
        if episode.is_finished():
            if episode.state == gpodder.STATE_DOWNLOADED:
                logger.warning("delete_finished: deleting file {}".format(episode.trimmed_title))
                episode.delete_from_disk()
            if episode.check_is_new():
                episode.mark(is_played=True)

