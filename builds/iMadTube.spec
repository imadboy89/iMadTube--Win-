# -*- mode: python -*-
a = Analysis(['C:\\Users\\IMAD-ELKHOLTI\\Documents\\GitHub\\iMadTube--Win-\\iMadTube\\iMadTube.py'],
             pathex=['C:\\Users\\IMAD-ELKHOLTI\\Documents\\GitHub\\iMadTube--Win-'],
             hiddenimports=[],
             hookspath=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name=os.path.join('dist', 'iMadTube.exe'),
          debug=False,
          strip=None,
          upx=True,
          console=False , icon='C:\\Users\\IMAD-ELKHOLTI\\Documents\\GitHub\\iMadTube--Win-\\iMadTube\\yt.ico')
app = BUNDLE(exe,
             name=os.path.join('dist', 'iMadTube.exe.app'))
