$games = @(
    @{ Name = "Pokemon_X"; TitleID = "0004000000055D00" },
    @{ Name = "Pokemon_Y"; TitleID = "0004000000055E00" },
    @{ Name = "Pokemon_Omega_Ruby"; TitleID = "000400000011C400" },
    @{ Name = "Pokemon_Alpha_Sapphire"; TitleID = "000400000011C500" },
    @{ Name = "Pokemon_Sun"; TitleID = "0004000000164800" },
    @{ Name = "Pokemon_Moon"; TitleID = "0004000000175E00" },
    @{ Name = "Pokemon_Ultra_Sun"; TitleID = "00040000001B5000" },
    @{ Name = "Pokemon_Ultra_Moon"; TitleID = "00040000001B5100" }
)

foreach ($g in $games) {
    New-Item -ItemType Directory -Path "E:\Pokemon-XY-No-Trade-Mod\Mod-Package\3DS_Luma3DS\luma\titles\$($g.TitleID)\romfs" -Force | Out-Null
    New-Item -ItemType Directory -Path "E:\Pokemon-XY-No-Trade-Mod\Mod-Package\Citra_Lime3DS\$($g.Name)\romfs" -Force | Out-Null
}
