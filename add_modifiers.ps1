[xml]$rus = Get-Content 'ModData/Data/Core/Languages/Russian/Modifiers.xml' -Raw -Encoding UTF8
[xml]$ukr = Get-Content 'ModData/Data/Core/Languages/Ukrainian/Modifiers.xml' -Raw -Encoding UTF8

$rusEntries = @{}
foreach ($entry in $rus.language.entry) {
    $rusEntries[$entry.name] = $entry.value
}

$ukrNames = @($ukr.language.entry.name)
$missing = $rusEntries.Keys | Where-Object { $ukrNames -notcontains $_ } | Sort-Object

# Create new entries to add
$newEntries = @()
foreach ($name in $missing) {
    # Translate from Russian to Ukrainian
    $value = $rusEntries[$name]

    # Direct translations
    $translations = @{
        'AfterAttackingMechanicalUnit' = 'після атаки на механічного юніта'
        'AgainstFortifications' = 'проти укріплень'
        'ForCyberTechnologies' = 'кібертехнологій'
        'ForVoiceUnits' = 'для юнітів Голосу'
        'FromFireDamage' = 'від вогню'
        'InForestRuinSmokeScreen' = 'у лісах, руїнах або димовій завісі'
        'OfFlagshipProductOnDeath' = '<string name=''Actions/PlatinumScionAffinityUpgrade2''/><string name=''Modifiers/OnDeath''/>'
        'TacticalInsertion' = 'до початку битви у клітині, яку раніше займав її ворожий юніт або нейтральна застава'
        'ToAdjacentEnemyLargeMechanicalNonTitanNonHeroUnits' = 'суміжні ворожі великі механічні юніти без-титанів, без-героїв'
        'ToAnchorite' = 'Пустельниці'
        'ToBuildingsOnTargetAlliedCityTile' = 'будівлі на клітинці вашого союзного міста'
        'ToChieftess' = 'Дикарці'
        'ToChieftessAnchoriteZephon' = 'Дикарці, Пустельниці і ЗЕФОНу'
        'ToNonHeadquartersBuildingsOnTargetAlliedCityTile' = 'будівлі без-штабу на клітинці вашого союзного міста'
        'ToSpawnedUnit' = 'призваного юніта'
        'ToTargetAlliedCherubimTitan' = 'союзному титану <string name=''Units/CherubimTitan''/>'
        'ToTargetAlliedNonLargeUnit' = 'союзному невеликому юніту'
        'ToTargetAlliedNonTitanUnit' = 'союзному без-титану'
        'ToTargetAlliedOutpost' = 'союзній нейтральній заставі'
        'ToTargetEnemyNonLargeUnit' = 'ворожому невеликому юніту'
        'ToTargetEnemyUnitAndWithHalfAttacksToEnemiesLeftAndRightOfTargetTile' = 'ворожому юніту і половину атак ворогам на клітинах зліва і справа від цілі'
        'ToTargetOwnUnit' = 'підконтрольному юніту'
        'ToUnitAndAdjacentAlliedUnits' = 'юніту і суміжним союзним юнітам'
        'ToZephon' = 'ЗЕФОНу'
        'WhenAttackingFromForestsOrRuins' = 'при атаці зі лісів або руїн'
        'WhenUnitMoves' = 'при переміщенні юніта'
    }

    $newEntries += [PSCustomObject]@{
        Name = $name
        Value = $translations[$name]
    }
}

Write-Host "Missing entries to add:"
foreach ($entry in $newEntries) {
    Write-Host "  <entry name=`"$($entry.Name)`" value=`"$($entry.Value)`"/>"
}
