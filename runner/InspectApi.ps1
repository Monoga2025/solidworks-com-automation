$assembly = [Reflection.Assembly]::LoadFrom('C:\Program Files\SOLIDWORKS Corp\SOLIDWORKS\SolidWorks.Interop.sldworks.dll')
$type = $assembly.GetType('SolidWorks.Interop.sldworks.IAssemblyDoc')
$type.GetMethods() | Where-Object { $_.Name -match '^AddComponent5$|^CreateMateData$|^CreateMate$' } | ForEach-Object { $_.ToString() }
