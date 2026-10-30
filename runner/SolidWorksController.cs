using System;
using System.IO;
using System.Collections.Generic;
using SolidWorks.Interop.sldworks;
using SolidWorks.Interop.swconst;

namespace SolidWorksQuizRunner;

internal sealed class SolidWorksController : IDisposable
{
    private readonly SldWorks _app;
    private SolidWorksController(SldWorks app) => _app = app;

    public static SolidWorksController Connect()
    {
        var app = new SldWorks
        {
            Visible = true
        };
        System.Threading.Thread.Sleep(1500);
        return new SolidWorksController(app);
    }

    public void BuildTheoryPart(QuizProfile p, string folder)
    {
        var model = NewPart();
        var eq = model.GetEquationMgr();
        Add(eq, "Z1", p.Z1.ToString()); Add(eq, "Z2", p.Z2.ToString());
        Add(eq, "M", $"{p.ModuleM}mm"); Add(eq, "Alfa", $"{p.AlphaDeg}deg");
        Add(eq, "A", $"{p.HelixDeg}deg"); Add(eq, "Dp1", "\"M\" * \"Z1\"");
        Add(eq, "Dp2", "\"M\" * \"Z2\""); Add(eq, "De1", "\"Dp1\" + 2 * \"M\"");
        Add(eq, "De2", "\"Dp2\" + 2 * \"M\""); Add(eq, "Di1", "\"Dp1\" - 2.5 * \"M\"");
        Add(eq, "Di2", "\"Dp2\" - 2.5 * \"M\""); Add(eq, "Ct", "pi * \"M\"");
        Add(eq, "P", "\"Ct\" / \"Z1\""); Add(eq, "Delta", "(\"Dp1\" + \"Dp2\") / 2");
        CreateBlank(model, p.Z1, p.ModuleM, 0.04);
        SaveChecked(model, Path.Combine(folder, "Quiz-Teorico.SLDPRT"));
    }

    public void BuildGearPair(QuizProfile p, string folder)
    {
        var gear1 = BuildGear(p, p.Z1, p.HelixDeg, folder);
        var gear2 = BuildGear(p, p.Z2, -p.HelixDeg, folder);
        BuildAssembly(p, gear1, gear2, folder);
    }

    public void BuildThreadedUnion(QuizProfile p, string folder)
    {
        var pitch = 25.4 / p.ThreadsPerInch;
        File.WriteAllText(Path.Combine(folder, "Union-Roscada.txt"),
            $"Student: {p.StudentName}\nThreads per inch: {p.ThreadsPerInch}\nPitch (mm): {pitch:0.000}\nParts: tornillo, tuerca, contratuerca, tuerca redonda, arandela\n");
    }

    public void BuildVerifiedHelicalGear(QuizProfile p, int teeth, string folder)
    {
        var model = NewPart();
        var eq = model.GetEquationMgr();
        Add(eq, "Z", teeth.ToString());
        Add(eq, "M", $"{p.ModuleM}mm");
        Add(eq, "Alfa", $"{p.AlphaDeg}deg");
        Add(eq, "Beta", $"{p.HelixDeg}deg");
        Add(eq, "Dp", "\"M\" * \"Z\"");
        Add(eq, "De", "\"Dp\" + 2 * \"M\"");
        Add(eq, "Di", "\"Dp\" - 2.5 * \"M\"");
        Add(eq, "Ct", "pi * \"M\"");

        CreateTwistedGearLoft(model, teeth, p.ModuleM, p.AlphaDeg, p.HelixDeg, 0.04);
        SaveChecked(model, Path.Combine(folder, $"N{teeth}_Q{p.AlphaDeg:0.#}_M{p.ModuleM:0.#}_A{p.HelixDeg:0.#}.SLDPRT"));
    }

    private string BuildGear(QuizProfile p, int teeth, double signedHelixDeg, string folder)
    {
        var model = NewPart();
        var eq = model.GetEquationMgr();
        Add(eq, "Z", teeth.ToString()); Add(eq, "M", $"{p.ModuleM}mm");
        Add(eq, "Alfa", $"{p.AlphaDeg}deg"); Add(eq, "Beta", $"{signedHelixDeg}deg");
        Add(eq, "Dp", "\"M\" * \"Z\""); Add(eq, "De", "\"Dp\" + 2 * \"M\"");
        Add(eq, "Di", "\"Dp\" - 2.5 * \"M\""); Add(eq, "Ct", "pi * \"M\"");
        CreateTwistedGearLoft(model, teeth, p.ModuleM, p.AlphaDeg, signedHelixDeg, 0.04);
        var path = Path.Combine(folder, $"N{teeth}_Q{p.AlphaDeg:0.#}_M{p.ModuleM:0.#}_A{Math.Abs(signedHelixDeg):0.#}.SLDPRT");
        SaveChecked(model, path);
        return path;
    }

    private void BuildAssembly(QuizProfile p, string gear1Path, string gear2Path, string folder)
    {
        var model = NewAssembly();
        var assembly = (IAssemblyDoc)model;
        var centerDistance = p.ModuleM * (p.Z1 + p.Z2) / 2000.0;
        var c1 = assembly.AddComponent5(gear1Path,
            (int)swAddComponentConfigOptions_e.swAddComponentConfigOptions_CurrentSelectedConfig,
            "", false, "", 0, 0, 0);
        var c2 = assembly.AddComponent5(gear2Path,
            (int)swAddComponentConfigOptions_e.swAddComponentConfigOptions_CurrentSelectedConfig,
            "", false, "", centerDistance, 0, 0);
        if (c1 == null || c2 == null) throw new InvalidOperationException("No se pudieron insertar ambos engranajes en el ensamblaje.");
        model.EditRebuild3();
        SaveChecked(model, Path.Combine(folder, $"{p.StudentName.Replace(',', ' ').Replace(' ', '_')}_{p.StudentId}.SLDASM"));
    }

    private static void CreateTwistedGearLoft(ModelDoc2 model, int teeth, double moduleMm, double alphaDeg, double helixDeg, double widthM)
    {
        var basePlane = GetFirstReferencePlane(model) ?? throw new InvalidOperationException("No se encontró el plano base.");
        var pitchRadiusM = moduleMm * teeth / 2000.0;
        var totalTwist = widthM * Math.Tan(helixDeg * Math.PI / 180.0) / pitchRadiusM;
        var sketches = new List<IFeature>();
        const int sections = 4;

        for (var section = 0; section < sections; section++)
        {
            var fraction = section / (double)(sections - 1);
            IFeature plane = basePlane;
            if (section > 0)
            {
                model.ClearSelection2(true);
                if (!basePlane.Select2(false, 0)) throw new InvalidOperationException("No se pudo seleccionar el plano base para crear un plano desplazado.");
                model.FeatureManager.InsertRefPlane(
                    (int)swRefPlaneReferenceConstraints_e.swRefPlaneReferenceConstraint_Distance,
                    widthM * fraction, 0, 0, 0, 0);
                plane = GetLastFeatureByType(model, "RefPlane") ?? throw new InvalidOperationException("No se pudo crear el plano desplazado.");
            }
            sketches.Add(CreateGearProfileSketch(model, plane, teeth, moduleMm, alphaDeg, totalTwist * fraction));
        }

        model.ClearSelection2(true);
        for (var i = 0; i < sketches.Count; i++)
            if (!sketches[i].Select2(i > 0, 1)) throw new InvalidOperationException($"No se pudo seleccionar la sección {i + 1} del loft.");

        var loft = model.FeatureManager.InsertProtrusionBlend2(false, true, false, 1.0,
            0, 0, 1.0, 1.0, true, true, false, 0, 0, 0, true, true, true,
            (int)swGuideCurveInfluence_e.swGuideCurveInfluenceNextGlobal);
        if (loft == null) throw new InvalidOperationException("SolidWorks rechazó el loft helicoidal.");
        model.EditRebuild3();
        CreateBoreAndKeyway(model, basePlane, pitchRadiusM, moduleMm / 1000.0, widthM);
        HideReferencePlanes(model);
        AssertSolidBody(model);
    }

    private static void CreateBoreAndKeyway(ModelDoc2 model, IFeature plane, double pitchRadiusM, double moduleM, double widthM)
    {
        var boreRadius = Math.Max(2.0 * moduleM, pitchRadiusM * 0.22);
        model.ClearSelection2(true);
        if (!plane.Select2(false, 0)) throw new InvalidOperationException("No se pudo seleccionar el plano para el agujero.");
        model.SketchManager.InsertSketch(true);
        model.SketchManager.CreateCircleByRadius(0, 0, 0, boreRadius);
        model.SketchManager.InsertSketch(true);
        var bore = CutThroughAll(model, widthM);
        bore.Name = "Bore";

        var keyWidth = Math.Max(3.0 * moduleM, boreRadius * 0.35);
        var keyDepth = Math.Max(1.5 * moduleM, boreRadius * 0.18);
        var y0 = boreRadius - keyDepth * 0.5;
        var y1 = boreRadius + keyDepth;
        model.ClearSelection2(true);
        if (!plane.Select2(false, 0)) throw new InvalidOperationException("No se pudo seleccionar el plano para el chavetero.");
        model.SketchManager.InsertSketch(true);
        model.SketchManager.CreateLine(-keyWidth / 2, y0, 0, keyWidth / 2, y0, 0);
        model.SketchManager.CreateLine(keyWidth / 2, y0, 0, keyWidth / 2, y1, 0);
        model.SketchManager.CreateLine(keyWidth / 2, y1, 0, -keyWidth / 2, y1, 0);
        model.SketchManager.CreateLine(-keyWidth / 2, y1, 0, -keyWidth / 2, y0, 0);
        model.SketchManager.InsertSketch(true);
        var keyway = CutThroughAll(model, widthM);
        keyway.Name = "Keyway";
        model.EditRebuild3();
    }

    private static IFeature CutThroughAll(ModelDoc2 model, double widthM)
    {
        var feature = model.FeatureManager.FeatureCut4(false, false, false,
            (int)swEndConditions_e.swEndCondThroughAll, (int)swEndConditions_e.swEndCondThroughAll,
            widthM, widthM, false, false, false, false, 0, 0, false, false, false, false,
            false, true, true, true, true, false, 0, 0, false, false);
        return feature ?? throw new InvalidOperationException("SolidWorks rechazó un corte pasante.");
    }

    private static void HideReferencePlanes(ModelDoc2 model)
    {
        model.ClearSelection2(true);
        var features = (object[])model.FeatureManager.GetFeatures(false);
        var append = false;
        foreach (var item in features)
        {
            if (item is IFeature feature && feature.GetTypeName2() == "RefPlane")
            {
                feature.Select2(append, 0);
                append = true;
            }
        }
        if (append) model.BlankRefGeom();
        model.ClearSelection2(true);
    }

    private static IFeature CreateGearProfileSketch(ModelDoc2 model, IFeature plane, int teeth, double moduleMm, double alphaDeg, double rotation)
    {
        model.ClearSelection2(true);
        if (!plane.Select2(false, 0)) throw new InvalidOperationException("No se pudo seleccionar un plano de sección.");
        model.SketchManager.InsertSketch(true);
        model.SketchManager.AddToDB = true;
        var points = BuildGearOutline(teeth, moduleMm / 1000.0, alphaDeg * Math.PI / 180.0, rotation);
        for (var i = 0; i < points.Count; i++)
        {
            var a = points[i];
            var b = points[(i + 1) % points.Count];
            model.SketchManager.CreateLine(a.X, a.Y, 0, b.X, b.Y, 0);
        }
        model.SketchManager.AddToDB = false;
        model.SketchManager.InsertSketch(true);
        return GetLastFeatureByType(model, "ProfileFeature") ?? throw new InvalidOperationException("No se encontró el croquis recién creado.");
    }

    private static List<(double X, double Y)> BuildGearOutline(int teeth, double moduleM, double alpha, double rotation)
    {
        var result = new List<(double X, double Y)>();
        var rp = moduleM * teeth / 2.0;
        var rb = rp * Math.Cos(alpha);
        var ra = rp + moduleM;
        var rr = Math.Max(rp - 1.25 * moduleM, moduleM * 0.25);
        var pitch = 2.0 * Math.PI / teeth;
        var halfPitchThickness = Math.PI / (2.0 * teeth);
        var invAlpha = Math.Tan(alpha) - alpha;
        var halfRoot = Math.Min(halfPitchThickness + invAlpha, pitch * 0.42);
        var startRadius = Math.Max(rb, rr);
        const int flankSteps = 5;
        const int arcSteps = 3;

        for (var tooth = 0; tooth < teeth; tooth++)
        {
            var center = rotation + tooth * pitch;
            AddPolar(result, rr, center - pitch / 2.0);
            AddPolar(result, rr, center - halfRoot);
            if (startRadius > rr) AddPolar(result, startRadius, center - halfRoot);
            for (var i = 0; i <= flankSteps; i++)
            {
                var radius = startRadius + (ra - startRadius) * i / flankSteps;
                var t = Math.Sqrt(Math.Max(0, radius * radius / (rb * rb) - 1));
                var half = halfPitchThickness + invAlpha - (t - Math.Atan(t));
                AddPolar(result, radius, center - half);
            }
            var tipT = Math.Sqrt(Math.Max(0, ra * ra / (rb * rb) - 1));
            var halfTip = halfPitchThickness + invAlpha - (tipT - Math.Atan(tipT));
            for (var i = 1; i <= arcSteps; i++)
                AddPolar(result, ra, center - halfTip + 2.0 * halfTip * i / arcSteps);
            for (var i = flankSteps; i >= 0; i--)
            {
                var radius = startRadius + (ra - startRadius) * i / flankSteps;
                var t = Math.Sqrt(Math.Max(0, radius * radius / (rb * rb) - 1));
                var half = halfPitchThickness + invAlpha - (t - Math.Atan(t));
                AddPolar(result, radius, center + half);
            }
            if (startRadius > rr) AddPolar(result, rr, center + halfRoot);
            AddPolar(result, rr, center + pitch / 2.0);
        }
        return result;
    }

    private static void AddPolar(List<(double X, double Y)> points, double radius, double angle) =>
        points.Add((radius * Math.Cos(angle), radius * Math.Sin(angle)));

    private static void AssertSolidBody(ModelDoc2 model)
    {
        var bodies = (object[])((IPartDoc)model).GetBodies2((int)swBodyType_e.swSolidBody, false);
        if (bodies == null || bodies.Length == 0) throw new InvalidOperationException("La pieza no contiene un sólido.");
    }

    private static void CreateBlank(ModelDoc2 model, int teeth, double moduleMm, double widthM)
    {
        var planeSelected = SelectFirstReferencePlane(model);
        if (!planeSelected) throw new InvalidOperationException("No se encontró ningún plano de referencia en la plantilla Part.");
        model.SketchManager.InsertSketch(true);
        var circle = model.SketchManager.CreateCircle(0, 0, 0, moduleMm * teeth / 2000.0, 0, 0);
        if (circle == null) throw new InvalidOperationException("No se pudo crear el círculo base.");
        model.SketchManager.InsertSketch(true);
        var feature = model.FeatureManager.FeatureExtrusion3(true, false, false,
            (int)swEndConditions_e.swEndCondBlind, (int)swEndConditions_e.swEndCondBlind,
            widthM, widthM, false, false, false, false, 0, 0, false, false, false, false,
            true, true, true, 0, 0, false);
        if (feature == null) throw new InvalidOperationException("No se pudo crear la extrusión base.");
        model.EditRebuild3();
        AssertSolidBody(model);
    }

    private ModelDoc2 NewPart() => NewDocument(
        (int)swUserPreferenceStringValue_e.swDefaultTemplatePart,
        "Part.prtdot", swDocumentTypes_e.swDocPART);

    private ModelDoc2 NewAssembly() => NewDocument(
        (int)swUserPreferenceStringValue_e.swDefaultTemplateAssembly,
        "Assembly.asmdot", swDocumentTypes_e.swDocASSEMBLY);

    private ModelDoc2 NewDocument(int preference, string templateName, swDocumentTypes_e documentType)
    {
        var template = _app.GetUserPreferenceStringValue(preference) as string;
        if (string.IsNullOrWhiteSpace(template) || !File.Exists(template))
        {
            var roots = new[] { @"C:\ProgramData\SOLIDWORKS", @"C:\Program Files\SOLIDWORKS Corp" };
            foreach (var root in roots)
            {
                if (!Directory.Exists(root)) continue;
                var matches = Directory.GetFiles(root, templateName, SearchOption.AllDirectories);
                if (matches.Length > 0) { template = matches[0]; break; }
            }
        }
        if (string.IsNullOrWhiteSpace(template) || !File.Exists(template))
            throw new InvalidOperationException($"No encontré la plantilla {templateName}.");
        var model = (ModelDoc2)_app.NewDocument(template, (int)documentType, 0, 0);
        return model ?? throw new InvalidOperationException($"SolidWorks no pudo crear un documento usando: {template}");
    }

    private static IFeature? GetFirstReferencePlane(ModelDoc2 model)
    {
        var features = (object[])model.FeatureManager.GetFeatures(false);
        if (features == null) return null;
        foreach (var item in features)
            if (item is IFeature feature && feature.GetTypeName2() == "RefPlane") return feature;
        return null;
    }

    private static bool SelectFirstReferencePlane(ModelDoc2 model)
    {
        var plane = GetFirstReferencePlane(model);
        return plane != null && plane.Select2(false, 0);
    }

    private static IFeature? GetLastFeatureByType(ModelDoc2 model, string typeName)
    {
        IFeature? last = null;
        var features = (object[])model.FeatureManager.GetFeatures(false);
        if (features == null) return null;
        foreach (var item in features)
            if (item is IFeature feature && feature.GetTypeName2() == typeName) last = feature;
        return last;
    }

    private static void Add(EquationMgr eq, string name, string expression) =>
        eq.Add2(-1, $"\"{name}\" = {expression}", true);

    private static void SaveChecked(ModelDoc2 model, string path)
    {
        var result = model.SaveAs3(path, (int)swSaveAsVersion_e.swSaveAsCurrentVersion, (int)swSaveAsOptions_e.swSaveAsOptions_Silent);
        if (result != 0) throw new InvalidOperationException($"No se pudo guardar {path}. result={result}");
        if (!File.Exists(path) || new FileInfo(path).Length == 0) throw new InvalidOperationException($"El archivo guardado está vacío: {path}");
        model.ShowNamedView2("", (int)swStandardViews_e.swIsometricView);
        model.ViewZoomtofit2();
        var preview = Path.ChangeExtension(path, ".bmp");
        if (!model.SaveBMP(preview, 1200, 900)) throw new InvalidOperationException($"No se pudo exportar la vista previa: {preview}");
    }

    public void Dispose()
    {
        try { _app.ExitApp(); } catch { }
        try { System.Runtime.InteropServices.Marshal.FinalReleaseComObject(_app); } catch { }
    }
}
