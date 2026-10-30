' HelicalGearMacro.bas
' SolidWorks VBA macro for the helical-gear assignment.
' Tested conceptually against the SolidWorks API (2019+). Run from Tools > Macro > Run.
Option Explicit

Const swDocPART As Long = 1
Const swEndCondBlind As Long = 0
Const swEndCondMidPlane As Long = 6
Const swEndCondThroughAll As Long = 1

Dim swApp As Object
Dim swModel As Object
Dim swSketch As Object

' Assignment defaults from the accompanying PDFs.
Const MODULE_MM As Double = 5#
Const TEETH As Long = 25          ' Change to 33 for the second exercise.
Const HELIX_DEG As Double = 30#
Const FACE_WIDTH_MM As Double = 40#
Const BORE_MM As Double = 25#
Const KEY_WIDTH_MM As Double = 25.4
Const KEY_DEPTH_MM As Double = 12.7
Const PRESSURE_ANGLE_DEG As Double = 20#

Sub main()
    Set swApp = Application.SldWorks
    Set swModel = swApp.NewDocument("", swDocPART, 0, 0)
    If swModel Is Nothing Then Err.Raise vbObjectError + 1, , "Could not create a new part."

    AddGlobalEquations
    CreateBaseCylinder
    CutBore
    CutKeyway
    AddReferenceCircles
    AddHelixReference

    swModel.ViewZoomtofit2
    swModel.EditRebuild3
    MsgBox "Base of the helical gear created." & vbCrLf & _
           "Teeth: " & TEETH & " | Module: " & MODULE_MM & " mm | Helix: " & HELIX_DEG & " deg" & vbCrLf & _
           "Complete the tooth profile and swept cut using the reference planes from the PDF.", _
           vbInformation, "Helical gear macro"
End Sub

Private Sub AddGlobalEquations()
    Dim eq As Object
    Set eq = swModel.GetEquationMgr
    eq.Add2 -1, """M"" = " & CStr(MODULE_MM) & "mm", True
    eq.Add2 -1, """N"" = " & CStr(TEETH), True
    eq.Add2 -1, """beta"" = " & CStr(HELIX_DEG) & "deg", True
    eq.Add2 -1, """DP"" = ""M"" * ""N""", True
    eq.Add2 -1, """DE"" = ""DP"" + 2 * ""M""", True
    eq.Add2 -1, """DI"" = ""DP"" - 2.5 * ""M""", True
    eq.Add2 -1, """CT"" = pi * ""M""", True
    eq.Add2 -1, """A"" = " & CStr(FACE_WIDTH_MM) & "mm", True
    eq.Add2 -1, """Ch"" = 0.5 * ""M""", True
    eq.Add2 -1, """r"" = 0.3 * ""M""", True
    eq.Add2 -1, """d"" = " & CStr(BORE_MM) & "mm", True
End Sub

Private Sub CreateBaseCylinder()
    Dim sk As Object, feat As Object
    Set sk = StartSketchOnFront
    sk.CreateCircle 0#, 0#, 0#, (MODULE_MM * TEETH / 2#) / 1000#, 0#, 0#
    swModel.SketchManager.InsertSketch True
    swModel.ClearSelection2 True

    Set sk = swModel.FeatureManager.FeatureExtrusion2(True, False, False, _
        swEndCondMidPlane, swEndCondMidPlane, FACE_WIDTH_MM / 1000#, FACE_WIDTH_MM / 1000#, _
        False, False, False, False, 0#, 0#, False, False, False, False, _
        True, True, True, 0, 0#, False)
    If sk Is Nothing Then Err.Raise vbObjectError + 2, , "Base extrusion failed."
    sk.Name = "Gear blank (DP)"
End Sub

Private Sub CutBore()
    Dim sk As Object, feat As Object
    Set sk = StartSketchOnFront
    sk.CreateCircle 0#, 0#, 0#, BORE_MM / 2000#, 0#, 0#
    swModel.SketchManager.InsertSketch True
    swModel.ClearSelection2 True
    Set feat = swModel.FeatureManager.FeatureCut4(True, False, False, _
        swEndCondThroughAll, swEndCondThroughAll, 0#, 0#, False, False, False, False, _
        0#, 0#, False, False, False, False, False, False, True, True, True, True, False, 0, 0#, False)
    If feat Is Nothing Then Err.Raise vbObjectError + 3, , "Bore cut failed."
    feat.Name = "Bore"
End Sub

Private Sub CutKeyway()
    Dim sk As Object, feat As Object
    Set sk = StartSketchOnFront
    Dim x As Double, y As Double, w As Double, h As Double
    w = KEY_WIDTH_MM / 1000#
    h = KEY_DEPTH_MM / 1000#
    x = -w / 2#
    y = BORE_MM / 2000# - h
    sk.CreateLine x, y, 0#, x + w, y, 0#
    sk.CreateLine x + w, y, 0#, x + w, y + h, 0#
    sk.CreateLine x + w, y + h, 0#, x, y + h, 0#
    sk.CreateLine x, y + h, 0#, x, y, 0#
    swModel.SketchManager.InsertSketch True
    swModel.ClearSelection2 True
    Set feat = swModel.FeatureManager.FeatureCut4(True, False, False, _
        swEndCondThroughAll, swEndCondThroughAll, 0#, 0#, False, False, False, False, _
        0#, 0#, False, False, False, False, False, False, True, True, True, True, False, 0, 0#, False)
    If feat Is Nothing Then Err.Raise vbObjectError + 4, , "Keyway cut failed."
    feat.Name = "Keyway"
End Sub

Private Sub AddReferenceCircles()
    Dim sk As Object
    Set sk = StartSketchOnFront
    sk.CreateCircle 0#, 0#, 0#, (MODULE_MM * TEETH / 2#) / 1000#, 0#, 0#
    sk.CreateCircle 0#, 0#, 0#, (MODULE_MM * TEETH / 2# + MODULE_MM) / 1000#, 0#, 0#
    sk.CreateCircle 0#, 0#, 0#, (MODULE_MM * TEETH / 2# - 1.25 * MODULE_MM) / 1000#, 0#, 0#
    swModel.SketchManager.InsertSketch True
    swModel.ClearSelection2 True
End Sub

Private Sub AddHelixReference()
    ' The PDF's final tooth is created with a 30-degree helix and a swept/lofted cut.
    ' Creating that feature depends on selecting the generated tooth profile and two
    ' reference sections; leaving a named reference sketch is safer than silently
    ' generating an incorrect tooth geometry.
    Dim sk As Object
    Set sk = StartSketchOnFront
    sk.CreateLine 0#, 0#, 0#, (MODULE_MM * TEETH / 2#) / 1000#, 0#, 0#
    swModel.SketchManager.InsertSketch True
    swModel.ClearSelection2 True
End Sub

Private Function StartSketchOnFront() As Object
    swModel.ClearSelection2 True
    swModel.Extension.SelectByID2 "Front Plane", "PLANE", 0#, 0#, 0#, False, 0, Nothing, 0
    Set StartSketchOnFront = swModel.SketchManager.CreateSketch
End Function
