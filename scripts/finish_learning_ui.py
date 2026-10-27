from pathlib import Path
p=Path(__file__).with_name('integrate_learning_ui.py')
s=p.read_text(encoding='utf8').replace("'Practicar familia'","'Practicar también la familia'")
p.write_text(s,encoding='utf8')
exec('\n'.join(s.splitlines()[:5])+'\n'+s[s.index("replace('index.html','Practicar"):])
