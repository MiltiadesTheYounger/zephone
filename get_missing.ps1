param([string]$fileName)

$rusPath = "ModData/Data/Core/Languages/Russian/$fileName"
$ukrPath = "ModData/Data/Core/Languages/Ukrainian/$fileName"

[xml]$rus = Get-Content $rusPath -Raw -Encoding UTF8
[xml]$ukr = Get-Content $ukrPath -Raw -Encoding UTF8

$rusEntries = @{}
foreach ($entry in $rus.language.entry) {
    $rusEntries[$entry.name] = $entry.value
}

$ukrNames = @($ukr.language.entry.name)
$missing = $rusEntries.Keys | Where-Object { $ukrNames -notcontains $_ } | Sort-Object

Write-Host "File: $fileName"
Write-Host "Russian: $($rusEntries.Count)"
Write-Host "Ukrainian: $($ukrNames.Count)"
Write-Host "Missing: $($missing.Count)"
Write-Host ""

foreach ($name in $missing) {
    Write-Host "$name|$($rusEntries[$name])"
}
