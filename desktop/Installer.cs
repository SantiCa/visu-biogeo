using System;
using System.Diagnostics;
using System.IO;
using System.IO.Compression;
using System.Reflection;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Drawing;

internal static class Installer {
    static string Version(){using(StreamReader r=new StreamReader(Assembly.GetExecutingAssembly().GetManifestResourceStream("VisuVersion")))return r.ReadToEnd().Trim();}
    static void Extract(string destination,Action<int,string> progress){
        string root=Path.GetFullPath(destination).TrimEnd(Path.DirectorySeparatorChar)+Path.DirectorySeparatorChar;
        Directory.CreateDirectory(root);
        using(Stream payload=Assembly.GetExecutingAssembly().GetManifestResourceStream("VisuPayload"))
        using(ZipArchive zip=new ZipArchive(payload,ZipArchiveMode.Read)){
            int count=0;
            foreach(ZipArchiveEntry entry in zip.Entries){
                string target=Path.GetFullPath(Path.Combine(root,entry.FullName.Replace('/',Path.DirectorySeparatorChar)));
                if(!target.StartsWith(root,StringComparison.OrdinalIgnoreCase))throw new InvalidDataException("Ruta inválida en el paquete.");
                if(entry.FullName.EndsWith("/")){Directory.CreateDirectory(target);continue;}
                Directory.CreateDirectory(Path.GetDirectoryName(target));
                using(Stream input=entry.Open())using(FileStream output=new FileStream(target,FileMode.Create,FileAccess.Write))input.CopyTo(output);
                count++;progress(count*100/zip.Entries.Count,count+" / "+zip.Entries.Count+" archivos");
            }
        }
        File.WriteAllText(Path.Combine(root,"installed-version.txt"),Version());
    }
    static void Shortcut(string executable){
        dynamic shell=Activator.CreateInstance(Type.GetTypeFromProgID("WScript.Shell"));
        dynamic link=shell.CreateShortcut(Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.DesktopDirectory),"Visu BioGeo.lnk"));
        link.TargetPath=executable;link.WorkingDirectory=Path.GetDirectoryName(executable);link.IconLocation=executable;link.Description="Estudio visual de Biología y Geología";link.Save();
    }
    [STAThread] static int Main(string[] args){
        if(args.Length==2&&args[0]=="--extract-only"){
            try{Extract(args[1],delegate{});return 0;}catch{return 1;}
        }
        if(args.Length!=0)return 2;
        string version=Version();
        if(!System.Text.RegularExpressions.Regex.IsMatch(version,"^[0-9a-zA-Z.-]+$"))return 3;
        string destination=Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),"Programs","VisuBioGeo",version);
        string executable=Path.Combine(destination,"Visu BioGeo.exe");
        Application.EnableVisualStyles();
        using(Form window=new Form()){
            window.Text="Instalar Visu BioGeo";window.Size=new Size(560,240);window.StartPosition=FormStartPosition.CenterScreen;window.FormBorderStyle=FormBorderStyle.FixedDialog;window.MaximizeBox=false;window.MinimizeBox=false;
            Label title=new Label(){Text="Visu BioGeo",Font=new Font("Segoe UI",20,FontStyle.Bold),Location=new Point(28,22),AutoSize=true,ForeColor=Color.FromArgb(18,60,50)};
            Label detail=new Label(){Text="Preparando la aplicación y el banco de imágenes…",Location=new Point(30,80),Size=new Size(490,28)};
            ProgressBar bar=new ProgressBar(){Location=new Point(30,120),Size=new Size(480,24),Minimum=0,Maximum=100};
            window.Controls.Add(title);window.Controls.Add(detail);window.Controls.Add(bar);
            bool finished=false;
            window.FormClosing+=(s,e)=>{if(!finished)e.Cancel=true;};
            window.Shown+=async(s,e)=>{
                try{
                    await Task.Run(()=>Extract(destination,(percent,text)=>{window.BeginInvoke(new Action(()=>{bar.Value=percent;detail.Text="Instalando aplicación e imágenes · "+text;}));}));
                    Shortcut(executable);finished=true;window.Close();Process.Start(new ProcessStartInfo(executable){UseShellExecute=true});
                }catch(Exception error){finished=true;MessageBox.Show("No se ha completado la instalación. Puedes volver a ejecutarla.\n"+error.Message,"Visu BioGeo");window.Close();}
            };
            Application.Run(window);
        }
        return 0;
    }
}
