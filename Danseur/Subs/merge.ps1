$org_dir = Convert-Path .
$yml = Join-Path -Path $org_dir -ChildPath "danseur_op.yml"
$opt_dir = "tmp"
New-Item -Path $opt_dir -ItemType Directory

$epn = Read-Host "ep. number"

Ikkoku merge -c $yml -o $opt_dir -var $epn SC
Ikkoku merge -c $yml -o $opt_dir -var $epn TC
