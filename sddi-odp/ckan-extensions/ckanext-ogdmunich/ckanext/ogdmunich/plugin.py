# -*- coding: utf-8 -*- 

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import logging
from ckan.lib.helpers import json
import json
from ckan.logic import NotFound, get_action
from ckan import model
from ckan.model import Session
from ckanext.ogdmunich import dcat_ap


log = logging.getLogger(__name__)

def package_tracking(package_id):
    mypackage = toolkit.get_action('package_show')(data_dict={'id': package_id, 'include_tracking': True})
    return mypackage['tracking_summary']['total']

def this_site_url():
    if toolkit.config.get('ckan.site_url'):
        this_site_url = toolkit.config.get('ckan.site_url')
    else:
        this_site_url=''

    return this_site_url

def most_popular_groups():
    '''Return a sorted list of the groups with the most datasets.'''

    # Get a list of all the site's groups from CKAN, sorted by number of
    # datasets.
    groups = toolkit.get_action('group_list')(
        data_dict={'sort': 'package_count desc', 'all_fields': True})

    # Truncate the list to the 11 most popular groups only.
    groups = groups[:11]
    groupsWithPackages = []
    for grp in groups:
        if grp['package_count'] and grp['package_count'] >0:
            groupsWithPackages.append(grp)

    return groupsWithPackages

class OGDMunichThemePlugin(plugins.SingletonPlugin):
    '''Theme plugin for OGD Munich.

    '''
    # Declare that this class implements IConfigurer.
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IBlueprint)

    def get_blueprint(self):
        return dcat_ap.get_blueprints()

    def update_config(self, config):

        # Add this plugin's templates dir to CKAN's extra_template_paths, so
        # that CKAN will use this plugin's custom templates.
        # 'templates' is the path to the templates dir, relative to this
        # plugin.py file.
        toolkit.add_template_directory(config, 'templates')
        toolkit.add_public_directory(config, 'public')
        toolkit.add_resource('assets', 'ogdmunich_assets')

    def get_helpers(self):
        '''Register the most_popular_groups() function above as a template
        helper function.

        '''
        # Template helper function names should begin with the name of the
        # extension they belong to, to avoid clashing with functions from
        # other extensions.
        return {'ogdmunich_most_popular_groups': most_popular_groups, 'this_site_url': this_site_url, 'ogdmunich_package_tracking':package_tracking}
