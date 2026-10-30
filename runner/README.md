# runner

C# / .NET 8 console app that drives SolidWorks through its COM API.

- `Program.cs`: reads the JSON profile (or `QuizProfiles.json` by default) and runs the build; supports `--smoke-test`.
- `SolidWorksController.cs`: COM connection, Equation Manager table, gear geometry and the save step.
- `InspectApi.ps1`: PowerShell helper that lists assembly API members to check method names for the installed version.
- `profiles.example.json`: placeholder profiles; copy to `profiles.json` and edit.
- `SolidWorksQuizRunner.csproj`: project file; points at the default SolidWorks install.
