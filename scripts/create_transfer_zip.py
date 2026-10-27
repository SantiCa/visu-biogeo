"""Archive the complete project, including hidden files, with ZIP64 and CRC QA."""
from pathlib import Path
import os,json,zipfile,time,hashlib,sys

ROOT=Path(__file__).resolve().parents[1]
ARCHIVE=ROOT.parent/'App Visu - traslado 2026-10-27 v8.10.zip'
PARTIAL=ARCHIVE.with_suffix('.zip.parcial')
REPORT=ARCHIVE.with_suffix('.verificacion.json')
COMPRESSED={'.jpg','.jpeg','.png','.webp','.gif','.pdf','.exe','.zip','.gz','.pack','.ico','.mp4','.woff2'}

def emit(**data):print(json.dumps(data,ensure_ascii=False),flush=True)

def main():
 if ARCHIVE.exists() or PARTIAL.exists():raise RuntimeError('Refuse to overwrite an existing archive or partial: '+str(ARCHIVE))
 if ROOT in ARCHIVE.parents:raise RuntimeError('Archive must be outside the source project')
 files=[];directories=[];links=[]
 for directory,dirs,names in os.walk(ROOT,followlinks=False):
  base=Path(directory);dirs.sort();names.sort()
  for name in dirs:
   p=base/name
   if p.is_symlink():links.append(str(p))
   directories.append(p)
  for name in names:
   p=base/name
   if p.is_symlink():links.append(str(p))
   st=p.stat();files.append((p,st.st_size,st.st_mtime_ns))
 if links:raise RuntimeError('Review symlinks before transfer: '+str(links))
 total=sum(n for _,n,_ in files);emit(phase='archive',files=len(files),directories=len(directories),sourceBytes=total,output=str(ARCHIVE))
 started=time.time();done=0;changed=[]
 with zipfile.ZipFile(PARTIAL,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=1,allowZip64=True,strict_timestamps=False) as z:
  z.write(ROOT,ROOT.name+'/')
  for p in directories:z.write(p,p.relative_to(ROOT.parent).as_posix()+'/')
  for i,(p,size,mtime) in enumerate(files,1):
   method=zipfile.ZIP_STORED if p.suffix.lower() in COMPRESSED else zipfile.ZIP_DEFLATED
   z.write(p,p.relative_to(ROOT.parent).as_posix(),compress_type=method,compresslevel=1)
   st=p.stat()
   if st.st_size!=size or st.st_mtime_ns!=mtime:changed.append(str(p.relative_to(ROOT)))
   done+=size
   if i%500==0 or i==len(files):emit(phase='archive',filesDone=i,filesTotal=len(files),sourceBytesDone=done,sourceBytesTotal=total,seconds=round(time.time()-started))
 if changed:raise RuntimeError('Source changed during packaging: '+str(changed))
 # Confirm every original path and file size, including hidden Git objects.
 with zipfile.ZipFile(PARTIAL) as z:
  byname={i.filename:i for i in z.infolist()};missing=[]
  for p,size,mtime in files:
   name=p.relative_to(ROOT.parent).as_posix()
   if name not in byname or byname[name].file_size!=size:missing.append(name)
   st=p.stat()
   if st.st_size!=size or st.st_mtime_ns!=mtime:changed.append(name)
  if missing or changed:raise RuntimeError('Completeness failed: '+str({'missing':missing,'changed':changed}))
  emit(phase='verify_crc',files=len(files),bytes=total)
  # Chunked CRC validation with progress instead of a silent whole-archive wait.
  for i,info in enumerate((x for x in z.infolist() if not x.is_dir()),1):
   with z.open(info) as f:
    while f.read(4*1024*1024):pass
   if i%2000==0 or i==len(files):emit(phase='verify_crc',filesDone=i,filesTotal=len(files),seconds=round(time.time()-started))
 emit(phase='sha256')
 digest=hashlib.sha256()
 with PARTIAL.open('rb') as f:
  while block:=f.read(8*1024*1024):digest.update(block)
 PARTIAL.replace(ARCHIVE)
 report={'date':'2026-10-27','source':str(ROOT),'archive':str(ARCHIVE),'zip64':True,'sourceFiles':len(files),'directoriesIncludingRoot':len(directories)+1,'sourceBytes':total,'archiveBytes':ARCHIVE.stat().st_size,'sha256':digest.hexdigest(),'allSourceFilesIncluded':True,'hiddenGitDirectoriesIncluded':True,'excludedFiles':[],'missingFiles':[],'changedFiles':[],'crcVerified':True,'seconds':round(time.time()-started),'continuationFile':'App Visu/CONTINUAR.md'}
 REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8');emit(phase='complete',**report,report=str(REPORT))

if __name__=='__main__':main()
