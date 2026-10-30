using System;
using System.IO;
using System.Text.Json;

namespace SolidWorksQuizRunner;

internal static class Program
{
    public static int Main(string[] args)
    {
        var configPath = args.Length > 0 ? args[0] : "QuizProfiles.json";
        if (!File.Exists(configPath))
        {
            Console.Error.WriteLine($"Configuration not found: {configPath}");
            return 2;
        }

        var profiles = JsonSerializer.Deserialize<QuizProfile[]>(File.ReadAllText(configPath)) ?? [];
        if (profiles.Length == 0)
        {
            Console.Error.WriteLine("No quiz profiles found.");
            return 3;
        }

        using var sw = SolidWorksController.Connect();
        var smokeOnly = args.Length > 1 && args[1].Equals("--smoke-test", StringComparison.OrdinalIgnoreCase);
        var selectedProfiles = smokeOnly ? profiles.Take(1) : profiles;
        foreach (var profile in selectedProfiles)
        {
            Console.WriteLine($"Processing {profile.StudentName} ({profile.StudentId})...");
            var folder = Path.Combine(profile.OutputRoot, SafeName(profile.StudentName));
            Directory.CreateDirectory(folder);
            if (smokeOnly)
            {
                sw.BuildVerifiedHelicalGear(profile, profile.Z1, folder);
            }
            else
            {
                sw.BuildTheoryPart(profile, folder);
                sw.BuildGearPair(profile, folder);
                sw.BuildThreadedUnion(profile, folder);
            }
        }

        Console.WriteLine(smokeOnly ? "Smoke test completed." : "Finished. Review the generated files in each student folder.");
        return 0;
    }

    private static string SafeName(string value)
    {
        foreach (var c in Path.GetInvalidFileNameChars()) value = value.Replace(c, '-');
        return value.Replace(',', ' ').Trim().Replace(' ', '-');
    }
}

internal sealed record QuizProfile(
    string StudentName,
    string StudentId,
    int Z1,
    int Z2,
    double ModuleM,
    double AlphaDeg,
    double HelixDeg,
    double ThreadsPerInch,
    string OutputRoot);
