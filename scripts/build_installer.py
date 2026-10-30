"""Build a self-contained Windows installer containing only public app assets."""
from pathlib import Path
import hashlib,zipfile,subprocess,os,json
from prepare_release import public_files,ROOT

def main():
    files=public_files();release=ROOT/'output/windows-installer';release.mkdir(parents=True,exist_ok=True)
    executable=ROOT/'Abrir Visu BioGeo.exe'
    version='8.12-'+hashlib.sha256(b''.join((ROOT/name).read_bytes() for name in files if not name.startswith('assets/'))+executable.read_bytes()).hexdigest()[:12]
    (release/'version.txt').write_text(version,encoding='ascii')
    payload=release/'payload.zip'
    with zipfile.ZipFile(payload,'w',zipfile.ZIP_DEFLATED,compresslevel=1) as archive:
        archive.write(executable,'Visu BioGeo.exe')
        for file in files:archive.write(ROOT/file,'app/'+file)
        archive.writestr('LEEME.txt','Visu BioGeo\n\nAbre Visu BioGeo.exe. No necesita Python.\nEn Ajustes, accede con el correo y la contraseña de tu cuenta de estudio.\nEl paquete contiene el catálogo y las imágenes aprobadas, sin cuentas ni sesiones.\nPara Mac, iPad y móvil instala la app desde:\nhttps://visu-biogeo-santica.nimblequail260.chatgpt.site/\n')
    output=ROOT/'output/Instalar Visu BioGeo Windows.exe'
    compiler=Path(os.environ['WINDIR'])/'Microsoft.NET/Framework64/v4.0.30319/csc.exe'
    args=[str(compiler),'/nologo','/target:winexe','/platform:x64','/optimize+',f'/out:{output}',f'/win32icon:{ROOT/"icons/icon.ico"}',f'/resource:{payload},VisuPayload',f'/resource:{release/"version.txt"},VisuVersion','/reference:System.Windows.Forms.dll','/reference:System.Drawing.dll','/reference:System.IO.Compression.dll','/reference:Microsoft.CSharp.dll',str(ROOT/'desktop/Installer.cs')]
    subprocess.run(args,check=True)
    report={'version':version,'files':len(files)+2,'payloadBytes':payload.stat().st_size,'installerBytes':output.stat().st_size,'output':str(output)}
    (release/'build.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(report,ensure_ascii=False),flush=True)

if __name__=='__main__':main()

