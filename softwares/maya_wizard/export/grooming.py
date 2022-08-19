# coding: utf-8
# Author: Leo BRUNEL
# Contact: contact@leobrunel.com

# Python modules
import os
import traceback
import logging
logger = logging.getLogger(__name__)

# Wizard modules
import wizard_communicate
from maya_wizard import wizard_tools
from maya_wizard import wizard_export

# Maya modules
import pymel.core as pm

def main():
    scene = wizard_export.save_or_save_increment()
    try:
        export_name = 'main'
        if wizard_tools.check_obj_list_existence(['grooming_GRP']):
            grooming_GRP_node = pm.PyNode('grooming_GRP')
            asset_name = os.environ['wizard_asset_name']
            grooming_GRP_node.rename(asset_name)
            export_GRP_list = [asset_name]

            exported_string_asset = wizard_communicate.get_string_variant_from_work_env_id(os.environ['wizard_work_env_id'])

            additionnal_objects = wizard_export.trigger_before_export_hook('grooming', exported_string_asset)
            export_GRP_list += additionnal_objects

            wizard_export.export('grooming', export_name, exported_string_asset, export_GRP_list)
    except:
        logger.error(str(traceback.format_exc()))
    finally:
        wizard_export.reopen(scene)