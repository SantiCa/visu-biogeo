param([string]$Destination = '')
$ErrorActionPreference = 'Stop'
$visuRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
if (-not $Destination) { $Destination = Join-Path $visuRoot 'Visu BioGeo.exe' }
$visuCompiler = Join-Path $env:WINDIR 'Microsoft.NET\Framework64\v4.0.30319\csc.exe'
if (-not (Test-Path -LiteralPath $visuCompiler)) { throw 'No se encuentra el compilador de .NET Framework.' }
$visuArguments = @('/nologo', '/target:winexe', '/platform:anycpu', '/optimize+',
    ('/out:' + $Destination), ('/win32icon:' + (Join-Path $visuRoot 'icons\icon.ico')),
    '/reference:System.Windows.Forms.dll', '/reference:System.Drawing.dll',
    (Join-Path $visuRoot 'desktop\VisuBioGeo.cs'))
& $visuCompiler @visuArguments
if ($LASTEXITCODE -ne 0) { throw 'No se ha podido compilar el ejecutable.' }
Get-Item -LiteralPath $Destination | Select-Object FullName,Length
