# -*- mode: python -*-

block_cipher = None


a = Analysis(['vix-prepare-dc-am-ex10.py'],
             pathex=['D:\\Program Files\\Python36\\Lib\\site-packages\\PyQt5\\Qt\\bin', 'C:\\Users\\vhuang1\\PycharmProjects\\AM-Automation'],
             binaries=[],
             datas=[ ('src', '.') ],
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
          exclude_binaries=True,
          name='vix-prepare-dc-am-ex10',
          debug=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='vix-prepare-dc-am-ex10')
