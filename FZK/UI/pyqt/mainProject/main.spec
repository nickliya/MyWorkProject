# -*- mode: python -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['D:\\YQworckspace\\MyWorkProject\\UI\\pyqt\\mainProject'],
             binaries=[],
             datas=[('D:\\YQworckspace\\MyWorkProject\\UI\\pyqt\\mainProject\\qss', 'qss'),
			 ('D:\\YQworckspace\\MyWorkProject\\UI\\pyqt\\mainProject\\Resource\Data', './Resource/Data'),
			 ('D:\\YQworckspace\\MyWorkProject\\UI\\pyqt\\mainProject\\Resource\Images', './Resource/Images')],
             hiddenimports=['PyQt5.sip'],
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
          name='main',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='main')
