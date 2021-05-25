# coding: utf-8
# Author: Leo BRUNEL
# Contact: contact@leobrunel.com

# Python modules
import os

# Available softwares
_maya_ = 'maya'
_guerilla_render_ = 'guerilla_render'
_substance_painter_ = 'substance_painter'
_substance_designer_ = 'substance_designer'
_nuke_ = 'nuke'
_houdini_ = 'houdini'
_blender_ = 'blender'

_softwares_list_ = [_maya_,
					_guerilla_render_,
					_substance_painter_,
					_substance_designer_,
					_nuke_,
					_blender_,
					_houdini_]

# Extensions
_extensions_dic_ = dict()
_extensions_dic_[_maya_] = 'ma'
_extensions_dic_[_guerilla_render_] = 'gproject'
_extensions_dic_[_substance_painter_] = 'spp'
_extensions_dic_[_substance_designer_] = 'sbs'
_extensions_dic_[_nuke_] = 'nk'
_extensions_dic_[_houdini_] = 'hip'
_extensions_dic_[_blender_] = 'blend'

# Launch commands
_executable_key_ = '[executable]'
_file_key_ = '[file]'
_script_key_ = '[startup_script]'
_reference_key_ = '[reference]'

_file_command_ = dict()
_file_command_[_maya_] = '"{}" -file "{}" -script "{}"'.format(_executable_key_, _file_key_, _script_key_)
_file_command_[_guerilla_render_] = '''"{}" "{}" --pycmd "execfile('{}')"'''.format(_executable_key_, _file_key_, _script_key_)
_file_command_[_substance_painter_] = '"{}" --mesh "{}" --split-by-udim "{}"'.format(_executable_key_, _reference_key_, _file_key_)
_file_command_[_substance_designer_] = '"{}" "{}"'.format(_executable_key_, _file_key_)
_file_command_[_nuke_] = '"{}" --nukex "{}"'.format(_executable_key_, _file_key_)
_file_command_[_houdini_] = '"{}" "{}" waitforui "{}" '.format(_executable_key_, _file_key_, _script_key_)
_file_command_[_blender_] = '"{}" "{}" --python "{}"'.format(_executable_key_, _file_key_, _script_key_)

_no_file_command_ = dict()
_no_file_command_[_maya_] = '"{}" -script "{}"'.format(_executable_key_, _script_key_)
_no_file_command_[_guerilla_render_] = '''"{}" --pycmd "execfile('{}')"'''.format(_executable_key_, _script_key_)
_no_file_command_[_substance_painter_] = '"{}" --mesh "{}" --split-by-udim'.format(_executable_key_, _reference_key_)
_no_file_command_[_substance_designer_] = '"{}"'.format(_executable_key_)
_no_file_command_[_nuke_] = '"{}" --nukex'.format(_executable_key_)
_no_file_command_[_houdini_] = '"{}" waitforui "{}" '.format(_executable_key_, _script_key_)
_no_file_command_[_blender_] = '"{}" --python "{}"'.format(_executable_key_, _script_key_)

# Environments
_script_env_dic_=dict()
_script_env_dic_[_maya_]='PYTHONPATH'
_script_env_dic_[_guerilla_render_]='GUERILLA_CONF'
_script_env_dic_[_substance_painter_]='SUBSTANCE_PAINTER_PLUGINS_PATH'
_script_env_dic_[_substance_designer_]='SBS_DESIGNER_PYTHON_PATH'
_script_env_dic_[_nuke_]='NUKE_PATH'
_script_env_dic_[_houdini_]='PYTHONPATH'
_script_env_dic_[_blender_]='PYTHONPATH'

# Plugins path
_main_script_path_ = os.path.normpath(os.path.abspath('softwares'))
_plugins_path_ = dict()
_plugins_path_[_maya_] = os.path.normpath(os.path.abspath(os.path.join('softwares', 'maya_wizard')))
_plugins_path_[_guerilla_render_] = os.path.normpath(os.path.abspath(os.path.join('softwares', 'guerilla_render_wizard')))
_plugins_path_[_substance_painter_] = os.path.normpath(os.path.abspath(os.path.join('softwares', 'substance_painter_wizard')))
_plugins_path_[_substance_designer_] = os.path.normpath(os.path.abspath(os.path.join('softwares', 'substance_designer_wizard')))
_plugins_path_[_nuke_] = os.path.normpath(os.path.abspath(os.path.join('softwares', 'nuke_wizard')))
_plugins_path_[_houdini_] = os.path.normpath(os.path.abspath(os.path.join('softwares', 'houdini_wizard')))
_plugins_path_[_blender_]  = os.path.normpath(os.path.abspath(os.path.join('softwares', 'blender_wizard')))

# Scripts files
_scripts_dic_ = dict()
_scripts_dic_[_maya_] = os.path.normpath(os.path.abspath(os.path.join(_plugins_path_[_maya_], 'startup.mel')))
_scripts_dic_[_guerilla_render_] = os.path.normpath(os.path.abspath(os.path.join(_plugins_path_[_guerilla_render_], 'startup.py')))
_scripts_dic_[_blender_] = os.path.normpath(os.path.abspath(os.path.join(_plugins_path_[_blender_], 'startup.py')))
_scripts_dic_[_houdini_] = os.path.normpath(os.path.abspath(os.path.join(_plugins_path_[_houdini_], 'startup.py')))