Attribute VB_Name = "PlanningCampagnes"
Option Explicit

Public Sub ActualiserCampagnes()
    Dim ws As Worksheet, zone As Range, data As Variant
    Dim i As Long, j As Long, col As Long, lastRow As Long
    Dim ligne(1 To 3) As Variant, rule As FormatCondition

    Set ws = ThisWorkbook.Worksheets("Ev - Campagne - Choix")
    lastRow = ws.Cells(ws.Rows.Count, "A").End(xlUp).Row
    If lastRow < 2 Then Exit Sub
    Set zone = ws.Range("A2:C" & lastRow)
    data = zone.Value

    For i = 2 To UBound(data, 1)
        For col = 1 To 3
            ligne(col) = data(i, col)
        Next col
        j = i - 1
        Do While j >= 1
            If CleDate(data(j, 2)) <= CleDate(ligne(2)) Then Exit Do
            For col = 1 To 3
                data(j + 1, col) = data(j, col)
            Next col
            j = j - 1
        Loop
        For col = 1 To 3
            data(j + 1, col) = ligne(col)
        Next col
    Next i

    zone.Value = data
    ws.Range("B2:B" & lastRow).NumberFormat = "dd/mm/yyyy"
    ws.Range("C2:C" & lastRow).FormulaR1C1 = _
        "=IF(RC[-2]="""","""",IF(NOT(ISNUMBER(RC[-1])),""Date a confirmer"",IF(RC[-1]<TODAY(),""Passee"",IF(TODAY()>=EDATE(RC[-1],-1),""A finaliser"",IF(TODAY()>=EDATE(RC[-1],-2),""A preparer"",""A venir"")))))"
    zone.FormatConditions.Delete

    Set rule = zone.FormatConditions.Add(Type:=xlExpression, _
        Formula1:="=IF(ISNUMBER($B2),AND($B2>=TODAY(),TODAY()>=EDATE($B2,-1)),FALSE)")
    rule.Interior.Color = RGB(217, 234, 211)

    Set rule = zone.FormatConditions.Add(Type:=xlExpression, _
        Formula1:="=IF(ISNUMBER($B2),AND(TODAY()>=EDATE($B2,-2),TODAY()<EDATE($B2,-1)),FALSE)")
    rule.Interior.Color = RGB(252, 229, 205)
End Sub

Private Function CleDate(ByVal valeur As Variant) As Double
    CleDate = 3000001
    If Not IsDate(valeur) Then Exit Function
    CleDate = CDbl(CDate(valeur))
    If CDate(valeur) < Date Then CleDate = CleDate + 3000000
End Function
