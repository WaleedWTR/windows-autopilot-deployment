Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$computer = Get-CimInstance Win32_ComputerSystem
$os = Get-CimInstance Win32_OperatingSystem
$disk = Get-CimInstance Win32_LogicalDisk -Filter "DeviceID='$($env:SystemDrive)'"

$tpmPresent = $false
if (Get-Command Get-Tpm -ErrorAction SilentlyContinue) {
    try {
        $tpmPresent = [bool](Get-Tpm -ErrorAction Stop).TpmPresent
    } catch {}
}

$secureBoot = $false
if (Get-Command Confirm-SecureBootUEFI -ErrorAction SilentlyContinue) {
    try {
        $secureBoot = [bool](Confirm-SecureBootUEFI -ErrorAction Stop)
    } catch {}
}

[pscustomobject]@{
    ComputerName = $env:COMPUTERNAME
    OS            = $os.Caption
    OSVersion     = $os.Version
    MemoryGB      = [math]::Round($computer.TotalPhysicalMemory / 1GB, 2)
    FreeDiskGB    = [math]::Round($disk.FreeSpace / 1GB, 2)
    TpmPresent    = $tpmPresent
    SecureBoot    = $secureBoot
    CheckedAtUtc  = [datetime]::UtcNow
}
