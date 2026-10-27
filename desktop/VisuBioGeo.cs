// Portable launcher: only the public application files are served on loopback.
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Windows.Forms;

internal static class VisuBioGeo {
    static TcpListener listener;
    static string root, origin;
    static int port=8081;
    static readonly HashSet<string> appFiles=new HashSet<string>(StringComparer.OrdinalIgnoreCase) {
        "index.html","app.js","styles.css","engine.mjs","classification-learning.mjs","taxonomy-guide.mjs","taxon-reference.mjs","exam-photos.mjs","catalogue.mjs","offline.mjs",
        "storage.mjs","cloud.mjs","install.mjs","notes.mjs","tooltips.mjs","community.mjs","config.js","sw.js","manifest.webmanifest"
    };
    static readonly HashSet<string> dataFiles=new HashSet<string>(StringComparer.OrdinalIgnoreCase) {
        "species.json","images.json","curated-images.json","andalucia-priority.json",
        "inaturalist-images.json","geological-images.json","geodil-images.json",
        "commons-extra-images.json","priority-additions.json","cloud-images.json",
        "asturnatura-images.json","taxonomy.json","teaching-images.json",
        "petrography-images.json","study-notes.json","family-notes.json","classification.json","learning-taxonomy.json","learning-geology.json","exams.json"
    };
    [STAThread] static int Main(string[] args) {
        bool serveOnly=false;int serveSeconds=0;
        root=AppDomain.CurrentDomain.BaseDirectory;
        foreach(string candidate in new string[]{Path.Combine(root,"app"),Path.Combine(root,"Visu BioGeo.app","Contents","Resources","app"),root})
            if(File.Exists(Path.Combine(candidate,"index.html"))){root=candidate;break;}
        for(int i=0;i<args.Length;i++){
            if(args[i]=="--serve-only")serveOnly=true;
            else if(args[i]=="--serve-for"&&i+1<args.Length){if(!int.TryParse(args[++i],out serveSeconds)||serveSeconds<1||serveSeconds>300)return 2;serveOnly=true;}
            else if(args[i]=="--port"&&i+1<args.Length){if(!int.TryParse(args[++i],out port)||port<1024||port>65535)return 2;}
            else if(args[i]=="--root"&&i+1<args.Length)root=args[++i];
            else return 2;
        }
        root=Path.GetFullPath(root).TrimEnd(Path.DirectorySeparatorChar)+Path.DirectorySeparatorChar;
        if(!File.Exists(Path.Combine(root,"index.html"))||!File.Exists(Path.Combine(root,"manifest.webmanifest"))){
            if(!serveOnly)MessageBox.Show("Mantén Visu BioGeo.exe junto a la carpeta de la aplicación. No se encuentra index.html.","Visu BioGeo");return 3;
        }
        origin="http://127.0.0.1:"+port;
        try{
            listener=new TcpListener(IPAddress.Loopback,port);listener.Start();
        }catch(SocketException){
            if(serveOnly)return 4;
            if(IsExistingVisu()){OpenApp();return 0;}
            MessageBox.Show("El puerto "+port+" está ocupado por otra aplicación. No se ha detenido ni modificado ese programa.","Visu BioGeo");return 4;
        }
        if(serveOnly){using(System.Threading.Timer timer=serveSeconds>0?new System.Threading.Timer(delegate{listener.Stop();},null,serveSeconds*1000,Timeout.Infinite):null){AcceptLoop();}return 0;}
        Thread server=new Thread(AcceptLoop);server.IsBackground=true;server.Start();
        Application.EnableVisualStyles();
        using(NotifyIcon tray=new NotifyIcon()){
            string ico=Path.Combine(root,"icons","icon.ico");tray.Icon=File.Exists(ico)?new System.Drawing.Icon(ico):System.Drawing.SystemIcons.Application;
            tray.Text="Visu BioGeo · servidor local";
            ContextMenuStrip menu=new ContextMenuStrip();
            menu.Items.Add("Abrir Visu BioGeo",null,delegate{OpenApp();});
            menu.Items.Add("Cerrar servidor local",null,delegate{listener.Stop();Application.Exit();});
            tray.ContextMenuStrip=menu;tray.DoubleClick+=delegate{OpenApp();};tray.Visible=true;
            OpenApp();Application.Run();tray.Visible=false;
        }
        return 0;
    }
    static bool IsExistingVisu(){
        try{HttpWebRequest req=(HttpWebRequest)WebRequest.Create(origin+"/manifest.webmanifest");req.Timeout=1500;req.Proxy=null;
            using(WebResponse response=req.GetResponse())using(StreamReader reader=new StreamReader(response.GetResponseStream()))return reader.ReadToEnd().Contains("Visu BioGeo");
        }catch{return false;}
    }
    static void OpenApp(){
        try{
            string edge=Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ProgramFilesX86),"Microsoft","Edge","Application","msedge.exe");
            if(File.Exists(edge))Process.Start(new ProcessStartInfo(edge,"--app="+origin+"/"){UseShellExecute=true});
            else Process.Start(new ProcessStartInfo(origin+"/"){UseShellExecute=true});
        }catch{MessageBox.Show("Abre "+origin+"/ en tu navegador.","Visu BioGeo");}
    }
    static void AcceptLoop(){
        while(true){try{TcpClient client=listener.AcceptTcpClient();ThreadPool.QueueUserWorkItem(delegate{Serve(client);});}catch(SocketException){break;}catch(ObjectDisposedException){break;}}
    }
    static string ReadLine(Stream stream){
        MemoryStream bytes=new MemoryStream();
        for(int i=0;i<8192;i++){int b=stream.ReadByte();if(b==-1)return null;if(b==10)return Encoding.ASCII.GetString(bytes.ToArray()).TrimEnd('\r');bytes.WriteByte((byte)b);}
        throw new IOException("Header too long");
    }
    static string AllowedPath(string url){
        string relative=Uri.UnescapeDataString(url.Split('?')[0]).TrimStart('/');
        if(relative=="")relative="index.html";
        if(relative.Contains("\\")||relative.Contains("\0"))return null;
        foreach(string segment in relative.Split('/'))if(segment==".."||segment=="."||segment=="")return null;
        bool allowed=appFiles.Contains(relative);
        if(relative.StartsWith("data/",StringComparison.Ordinal)&&dataFiles.Contains(relative.Substring(5)))allowed=true;
        if(relative.StartsWith("assets/reviewed/",StringComparison.Ordinal)){
            string file=relative.Substring(16);allowed=System.Text.RegularExpressions.Regex.IsMatch(file,"^[a-zA-Z0-9][a-zA-Z0-9_-]{0,119}\\.(?:jpg|jpeg|png|webp)$");
        }
        if(relative.StartsWith("icons/",StringComparison.Ordinal))allowed=System.Text.RegularExpressions.Regex.IsMatch(relative,"^icons/icon(?:-[0-9]+)?\\.(?:png|svg|ico)$");
        if(relative.StartsWith("vendor/",StringComparison.Ordinal))allowed=System.Text.RegularExpressions.Regex.IsMatch(relative,"^vendor/(?:supabase|[a-f0-9]{16})\\.mjs$");
        string path=Path.GetFullPath(Path.Combine(root,relative.Replace('/',Path.DirectorySeparatorChar)));
        return allowed&&path.StartsWith(root,StringComparison.OrdinalIgnoreCase)?path:null;
    }
    static void Serve(TcpClient client){
        using(client){client.ReceiveTimeout=5000;client.SendTimeout=15000;
            try{using(NetworkStream stream=client.GetStream()){
                string first=ReadLine(stream);if(first==null)return;string[] parts=first.Split(' ');if(parts.Length!=3){Error(stream,400,"Bad request");return;}
                Dictionary<string,string> headers=new Dictionary<string,string>(StringComparer.OrdinalIgnoreCase);
                for(int i=0;i<100;i++){string line=ReadLine(stream);if(line=="")break;if(line==null)return;int colon=line.IndexOf(':');if(colon>0)headers[line.Substring(0,colon)]=line.Substring(colon+1).Trim();if(i==99){Error(stream,431,"Too many headers");return;}}
                string host,requestOrigin;
                if(!headers.TryGetValue("Host",out host)||host!="127.0.0.1:"+port){Error(stream,403,"Forbidden host");return;}
                if(headers.TryGetValue("Origin",out requestOrigin)&&requestOrigin!=origin){Error(stream,403,"Forbidden origin");return;}
                if(parts[0]!="GET"&&parts[0]!="HEAD"){Error(stream,405,"Method not allowed");return;}
                if(!parts[1].StartsWith("/",StringComparison.Ordinal)){Error(stream,400,"Bad request");return;}
                if(parts[1].Split('?')[0]=="/desktop-runtime.json"){
                    string body="{\"bundledPhotos\":"+(Directory.Exists(Path.Combine(root,"assets","reviewed"))?"true":"false")+"}";
                    Write(stream,"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nCache-Control: no-store\r\nContent-Length: "+Encoding.UTF8.GetByteCount(body)+"\r\nConnection: close\r\n\r\n");if(parts[0]=="GET")Write(stream,body);return;
                }
                string path=AllowedPath(parts[1]);if(path==null||!File.Exists(path)){Error(stream,404,"Not found");return;}
                FileInfo file=new FileInfo(path);string ext=file.Extension.ToLowerInvariant();
                string mime=ext==".html"?"text/html; charset=utf-8":ext==".js"||ext==".mjs"?"text/javascript; charset=utf-8":ext==".css"?"text/css; charset=utf-8":ext==".json"||ext==".webmanifest"?"application/json; charset=utf-8":ext==".jpg"||ext==".jpeg"?"image/jpeg":ext==".png"?"image/png":ext==".webp"?"image/webp":ext==".svg"?"image/svg+xml":"image/x-icon";
                string cache=ext==".jpg"||ext==".jpeg"||ext==".png"||ext==".webp"?"public, max-age=31536000, immutable":"no-cache";
                Write(stream,"HTTP/1.1 200 OK\r\nContent-Type: "+mime+"\r\nContent-Length: "+file.Length+"\r\nCache-Control: "+cache+"\r\nX-Content-Type-Options: nosniff\r\nReferrer-Policy: no-referrer\r\nConnection: close\r\n\r\n");
                if(parts[0]=="GET")using(FileStream content=File.OpenRead(path))content.CopyTo(stream);
            }}catch(IOException){}catch(SocketException){}catch(Exception){}
        }
    }
    static void Write(Stream stream,string text){byte[] bytes=Encoding.UTF8.GetBytes(text);stream.Write(bytes,0,bytes.Length);}
    static void Error(Stream stream,int code,string message){byte[] bytes=Encoding.UTF8.GetBytes(message);Write(stream,"HTTP/1.1 "+code+" "+message+"\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: "+bytes.Length+"\r\nConnection: close\r\n\r\n");stream.Write(bytes,0,bytes.Length);}
}
