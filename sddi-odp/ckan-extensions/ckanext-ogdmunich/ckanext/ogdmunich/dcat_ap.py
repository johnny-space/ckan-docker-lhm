from flask import Blueprint, render_template
import ckan.plugins as p
import ckan.plugins.toolkit as toolkit
from ckan.views.user import _extra_template_variables
import ckan.model as model
import json
import os


dcat_ap = Blueprint(u'dcat_ap', __name__)

def dataset_dcat_ap_validator(id):
    context = {
            'model': model,
            'session': model.Session,
            'user': toolkit.g.user or toolkit.g.author,
            'for_view': True,
            'auth_user_obj': toolkit.g.userobj
    }
    data_dict = {'id': id}
        
    try:
        toolkit.check_access('package_update', context, data_dict)
    except toolkit.ObjectNotFound:
        return toolkit.abort(404, ('Datensatz nicht gefunden'))
    except toolkit.NotAuthorized:
        return toolkit.abort(401, ('Sie haben keine Berechtigung, diese Seite zu sehen'))
    
    try:
        toolkit.g.pkg_dict = toolkit.get_action('package_show')(context, data_dict)
    except toolkit.ObjectNotFound:
        return toolkit.abort(404, ('Datensatz nicht gefunden'))
    except toolkit.NotAuthorized:
        return toolkit.abort(401, ('Sie haben keine Berechtigung, diese Seite zu sehen'))
    
    if os.path.isfile("/srv/app/format_mapping.json"):
        with open('/srv/app/format_mapping.json') as json_file:
            format_mapping = json.load(json_file)
    else:
        format_mapping = "Kein Format Mapping gefunden. Bitte überprüfen Sie, ob dieses korrekt eingebaut ist."
    
    return toolkit.render("/package/dcat_ap.html",
                   extra_vars={'pkg_dict': toolkit.g.pkg_dict,
                                'format_mapping': format_mapping})

def dashboard_dcat_ap_validator():
    context = {u'for_view': True, u'user': toolkit.g.user, u'auth_user_obj': toolkit.g.userobj}
    data_dict = {u'user_obj': toolkit.g.userobj}
    try:
        toolkit.check_access('sysadmin', context, data_dict)
    except toolkit.NotAuthorized:
        return toolkit.abort(401, ('Sie haben keine Berechtigung, diese Seite zu sehen'))
    
    extra_vars = _extra_template_variables(context, data_dict)
    return toolkit.render(u'user/dcat_ap.html', extra_vars)

dcat_ap.add_url_rule('/dataset/dcat_ap/<id>',
              view_func=dataset_dcat_ap_validator,
              methods=[u'GET', u'POST'])

dcat_ap.add_url_rule('/dashboard/dcat_ap',
              view_func=dashboard_dcat_ap_validator)

def get_blueprints():
    return [dcat_ap]