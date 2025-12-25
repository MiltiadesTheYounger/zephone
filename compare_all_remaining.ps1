$files = @(
    'Colors.xml', 'GUI.xml', 'Items.xml', 'Modifiers.xml',
    'Notifications.xml', 'Objectives.xml', 'Quests.xml',
    'Regions.xml', 'Settings.xml', 'Tips.xml', 'Titles.xml',
    'Traits.xml', 'Units.xml', 'Upgrades.xml', 'Weapons.xml',
    'WorldParameters.xml'
)

$results = @()

foreach ($file in $files) {
    $rusPath = "ModData/Data/Core/Languages/Russian/$file"
    $ukrPath = "ModData/Data/Core/Languages/Ukrainian/$file"

    if ((Test-Path $rusPath) -and (Test-Path $ukrPath)) {
        [xml]$rus = Get-Content $rusPath -Raw -Encoding UTF8
        [xml]$ukr = Get-Content $ukrPath -Raw -Encoding UTF8

        $rusNames = @($rus.language.entry.name)
        $ukrNames = @($ukr.language.entry.name)
        $missing = $rusNames | Where-Object { $ukrNames -notcontains $_ }

        $results += [PSCustomObject]@{
            File = $file
            Russian = $rusNames.Count
            Ukrainian = $ukrNames.Count
            Missing = $missing.Count
        }
    }
}

$results | Format-Table -AutoSize
Write-Host ""
Write-Host "Files with missing entries:"
$results | Where-Object { $_.Missing -gt 0 } | ForEach-Object {
    Write-Host "  $($_.File): $($_.Missing) missing"
}
