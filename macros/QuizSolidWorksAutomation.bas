' QuizSolidWorksAutomation.bas
' SolidWorks VBA automation for the three assigned quizzes.
' Assignment row used for testing: STUDENT C.
Option Explicit

Const swDocPART As Long = 1
Const swDocASSEMBLY As Long = 2
Const swEndCondMidPlane As Long = 6
Const swEndCondThroughAll As Long = 1

Dim swApp As Object

' ===== Test profiles: replace names/values to test three students =====
Private Type QuizProfile
    StudentName As String
    StudentId As String
    Z1 As Long
    Z2 As Long
    ModuleM As Double
    AlphaDeg As Double
    HelixDeg As Double
End Type

Sub main()
    Set swApp = Application.SldWorks
    If swApp Is Nothing Then
        MsgBox "Ejecuta la macro desde SolidWorks, no desde Excel/VBA independiente.", vbCritical
        Exit Sub
    End If
    Dim choice As String
    choice = InputBox("1 = Quiz teorico" & vbCrLf & "2 = Engranajes" & vbCrLf & "3 = Union roscada", _
                      "Quiz SolidWorks", "1")
    Select Case choice
        Case "1": RunTheoryQuiz
        Case "2": RunGearQuiz
        Case "3": RunThreadedUnionQuiz
        Case Else: MsgBox "Opcion no valida.", vbExclamation
    End Select
End Sub

Private Function GetProfile() As QuizProfile
    Dim p As QuizProfile
    p.StudentName = InputBox("Nombre del estudiante", "Perfil", "STUDENT C")
    p.StudentId = InputBox("ID del estudiante", "Perfil", "ID")
    p.Z1 = CLng(InputBox("Z1 - dientes del engranaje 1", "Parametros", "38"))
    p.Z2 = CLng(InputBox("Z2 - dientes del engranaje 2", "Parametros", "19"))
    p.ModuleM = CDbl(InputBox("M - modulo (mm)", "Parametros", "2"))
    p.AlphaDeg = CDbl(InputBox("Alfa - angulo de ataque (grados)", "Parametros", "20"))
    p.HelixDeg = CDbl(InputBox("Angulo helicoidal (grados)", "Parametros", "25"))
    GetProfile = p
End Function

Private Sub RunTheoryQuiz()
    Dim p As QuizProfile, eq As Object, model As Object
    p = GetProfile
    Set model = NewPart
    Set eq = model.GetEquationMgr

    ' Names follow the variable table in the supplied PDF.
    AddEq eq, "Z1", CStr(p.Z1)
    AddEq eq, "Z2", CStr(p.Z2)
    AddEq eq, "M", CStr(p.ModuleM) & "mm"
    AddEq eq, "Alfa", CStr(p.AlphaDeg) & "deg"
    AddEq eq, "A", CStr(p.HelixDeg) & "deg"
    AddEq eq, "Dp1", """M"" * ""Z1"""
    AddEq eq, "Dp2", """M"" * ""Z2"""
    AddEq eq, "De1", """Dp1"" + 2 * ""M"""
    AddEq eq, "De2", """Dp2"" + 2 * ""M"""
    AddEq eq, "Di1", """Dp1"" - 2.5 * ""M"""
    AddEq eq, "Di2", """Dp2"" - 2.5 * ""M"""
    AddEq eq, "Ct", "pi * ""M"""
    AddEq eq, "P", """Ct"" / ""Z1"""
    AddEq eq, "Delta", "(""Dp1"" + ""Dp2"") / 2"
    AddEq eq, "r", "0.3 * ""M"""

    MsgBox "Tabla teorica creada para " & p.StudentName & "." & vbCrLf & _
           "Revisa Equation Manager y completa R1/R2/R3 con la tabla del profesor.", _
           vbInformation, "Quiz teorico"
End Sub

Private Sub RunGearQuiz()
    Dim p As QuizProfile, answer As String
    p = GetProfile
    answer = InputBox("Escribe la carpeta de salida (ruta absoluta).", "Entrega", "C:\\Quiz_" & CleanName(p.StudentName))
    If Len(answer) = 0 Then Exit Sub

    ' The PDF requires two separate gear parts and a functional assembly.
    ' This macro creates the parametric base and equation table for each gear;
    ' the audited tooth-profile/swept-cut steps remain topology-sensitive.
    CreateGearPart p, p.Z1, answer & "\\N" & CStr(p.Z1) & "_Q" & CStr(p.AlphaDeg) & "_M" & CStr(p.ModuleM) & "_A" & CStr(p.HelixDeg)
    CreateGearPart p, p.Z2, answer & "\\N" & CStr(p.Z2) & "_Q" & CStr(p.AlphaDeg) & "_M" & CStr(p.ModuleM) & "_A" & CStr(p.HelixDeg)
    MsgBox "Se generaron los dos documentos base y sus ecuaciones." & vbCrLf & _
           "Completa el perfil helicoidal y el ensamblaje según el PDF antes de comprimir.", vbInformation
End Sub

Private Sub RunThreadedUnionQuiz()
    Dim p As QuizProfile, tpi As Double, pitch As Double
    p = GetProfile
    tpi = CDbl(InputBox("Hilos por pulgada", "Union roscada", "5"))
    pitch = (1# / tpi) * 25.4
    MsgBox "Paso de rosca calculado: " & Format(pitch, "0.000") & " mm" & vbCrLf & _
           "Se deben crear: tornillo, tuerca, contratuerca, tuerca redonda y arandela." & vbCrLf & _
           "El PDF asigna longitud y designacion UNC/UNF por estudiante.", vbInformation
End Sub

Private Sub CreateGearPart(ByRef p As QuizProfile, ByVal teeth As Long, ByVal outputFolder As String)
    Dim model As Object, eq As Object, sk As Object, feat As Object
    Set model = NewPart
    Set eq = model.GetEquationMgr
    AddEq eq, "Z", CStr(teeth)
    AddEq eq, "M", CStr(p.ModuleM) & "mm"
    AddEq eq, "Alfa", CStr(p.AlphaDeg) & "deg"
    AddEq eq, "A", CStr(p.HelixDeg) & "deg"
    AddEq eq, "Dp", """M"" * ""Z"""
    AddEq eq, "De", """Dp"" + 2 * ""M"""
    AddEq eq, "Di", """Dp"" - 2.5 * ""M"""
    AddEq eq, "Ct", "pi * ""M"""
    AddEq eq, "r", "0.3 * ""M"""

    model.Extension.SelectByID2 "Front Plane", "PLANE", 0#, 0#, 0#, False, 0, Nothing, 0
    Set sk = model.SketchManager.CreateSketch
    sk.CreateCircle 0#, 0#, 0#, (p.ModuleM * teeth / 2#) / 1000#, 0#, 0#
    model.SketchManager.InsertSketch True
    model.ClearSelection2 True
    Set feat = model.FeatureManager.FeatureExtrusion2(True, False, False, swEndCondMidPlane, swEndCondMidPlane, 0.04, 0.04, False, False, False, False, 0#, 0#, False, False, False, False, True, True, True, 0, 0#, False)
    If Not feat Is Nothing Then feat.Name = "Gear blank - Z" & CStr(teeth)
    model.EditRebuild3
    model.SaveAs3 outputFolder & "\\Gear_Z" & CStr(teeth) & ".SLDPRT", 0, 2
End Sub

Private Function NewPart() As Object
    Dim model As Object
    Set model = swApp.NewDocument("", swDocPART, 0, 0)
    If model Is Nothing Then
        MsgBox "SolidWorks no pudo crear la pieza. Verifica que exista una plantilla de pieza predeterminada.", vbCritical
        Err.Raise vbObjectError + 91, , "NewDocument devolvio Nothing"
    End If
    Set NewPart = model
End Function

Private Sub AddEq(ByVal eq As Object, ByVal name As String, ByVal expression As String)
    eq.Add2 -1, """" & name & """ = " & expression, True
End Sub

Private Function CleanName(ByVal value As String) As String
    CleanName = Replace(Replace(Replace(value, ",", ""), " ", "-"), ".", "")
End Function
