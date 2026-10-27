$ErrorActionPreference = 'Stop'
$visuExe = Join-Path $PSScriptRoot 'Visu BioGeo.exe'
if (-not (Test-Path -LiteralPath $visuExe)) { throw 'Mantén este archivo junto a Visu BioGeo.exe.' }
$visuShell = New-Object -ComObject WScript.Shell
$visuShortcut = $visuShell.CreateShortcut((Join-Path ([Environment]::GetFolderPath('Desktop')) 'Visu BioGeo.lnk'))
$visuShortcut.TargetPath = $visuExe
$visuShortcut.WorkingDirectory = $PSScriptRoot
$visuShortcut.Description = 'Entrenamiento visual de Biología y Geología'
$visuShortcut.IconLocation = $visuExe
$visuShortcut.Save()
Write-Output 'Acceso directo creado en el escritorio. Mantén la carpeta de Visu BioGeo en esta ubicación.'
