# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['installer.py'],
             pathex=['D:\\script\\wizard_2\\Installer'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

a.datas += [ ('__wizard__.zip', '.\\__wizard__.zip', 'DATA')]
a.datas += [ ('version.yaml', '.\\version.yaml', 'DATA')]
a.datas += [ ('ressources\\icons\\wizard_setup.svg', '.\\ressources\\icons\\wizard_setup.svg', 'DATA')]

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='__installer_temp__',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          icon='D:\\script\\wizard_2\\ressources\\icons\\wizard_setup.ico')