[xml]$rus = Get-Content 'ModData/Data/Core/Languages/Russian/Features.xml' -Raw -Encoding UTF8
[xml]$ukr = Get-Content 'ModData/Data/Core/Languages/Ukrainian/Features.xml' -Raw -Encoding UTF8

$rusNames = @($rus.language.entry.name)
$ukrNames = @($ukr.language.entry.name)
$missing = $rusNames | Where-Object { $ukrNames -notcontains $_ }

Write-Host "Russian entries: $($rusNames.Count)"
Write-Host "Ukrainian entries: $($ukrNames.Count)"
Write-Host "Missing: $($missing.Count)"
Write-Host ""

if ($missing.Count -gt 0) {
    Write-Host "Missing entries:"
    foreach ($name in $missing) {
        $entry = $rus.language.entry | Where-Object { $_.name -eq $name }
        Write-Host "  $name = $($entry.value)"
    }
}
