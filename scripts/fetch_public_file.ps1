param([Parameter(Mandatory=$true)][string]$Uri,[Parameter(Mandatory=$true)][string]$Destination)
$ErrorActionPreference = 'Stop'
# Use the normal Windows certificate store; never disable TLS verification.
Invoke-WebRequest -Uri $Uri -OutFile $Destination -TimeoutSec 35
