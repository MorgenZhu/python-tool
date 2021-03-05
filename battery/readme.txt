

1. pyinstaller issue
PyInstaller packages the library to exe without importing the Winiobinary folder.
So we need to specify the packaging folder.

a. pyinstaller -F -w -uac-admin hello.py
b. It will create a file called hello.spec, open it
c. modify Analysis->datas as follows :
		a = Analysis(['batteryview.py'],
             pathex=['F:\\python-code\\python-tool\\battery'],
             binaries=[],
             datas=[('D:\python\Lib\site-packages\winiobinary','winiobinary')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

d. pyinstaller -F -w -uac-admin hello.spec