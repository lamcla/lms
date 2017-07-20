# -*- coding: utf-8 -*-

"""Configuration for the Pyramid application."""

from __future__ import unicode_literals

from pyramid.config import Configurator

from lti.config.settings import (
    SettingError,
    env_setting,
    optional_env_setting,
)


def configure():
    """Return a Configurator for the Pyramid application."""
    return Configurator(settings = {
        'lti_server_scheme': env_setting('LTI_SERVER_SCHEME'),
        'lti_server_host': env_setting('LTI_SERVER_HOST'),
        'lti_server_port': optional_env_setting('LTI_SERVER_PORT'),
        'lti_credentials_url': env_setting('LTI_CREDENTIALS_URL'),
    })