# -*- mode: python -*-

block_cipher = None


a = Analysis(['vix-prepare-dc-am-ex10_with_ui.py'],
             pathex=['D:\\Program Files\\Python36\\Lib\\site-packages\\PyQt5\\Qt\\bin', 'C:\\Users\\vhuang1\\PycharmProjects\\AAT'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='vix-prepare-dc-am-ex10_with_ui',
          debug=False,
          strip=False,
          upx=True,
          console=False , icon='C:\\Users\\vhuang1\\PycharmProjects\\AAT\\images\\icon.ico')
