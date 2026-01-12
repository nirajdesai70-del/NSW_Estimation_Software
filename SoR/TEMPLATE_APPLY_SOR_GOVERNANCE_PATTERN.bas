Attribute VB_Name = "APPLY_SOR_GOVERNANCE_PATTERN"
Option Explicit

'========================
' SoR Governance Macro (PATTERN-BASED)
' For MPCB, MCCB, ACB, and future categories
' - Uses pattern matching instead of hardcoded sheet names
' - Colors tabs by role (DATA/README/ARCHIVE/OTHER)
' - Protects sheets (DATA locked; archive locked; readme locked)
' - Protects workbook structure
'========================

'CONFIG: set password (optional). Leave blank "" if you don't want password.
Private Const PWD As String = ""   ' e.g. "YourPasswordHere"

'DATA SHEET PATTERN: item_<category>_<series>_work
'Examples: item_mpcb_gv2_work, item_mccb_nsx_work, item_contactor_tesys_eocr_work
Private Function IsDataSheet(ByVal wsName As String) As Boolean
    Dim n As String
    n = LCase(Trim(wsName))
    
    'Pattern: item_*_work OR nsw_item_master_engineering_view OR accessory_master
    IsDataSheet = ( _
        (Left(n, 5) = "item_" And Right(n, 5) = "_work") Or _
        n = "nsw_item_master_engineering_view" Or _
        n = "accessory_master" _
    )
End Function

'ARCHIVE detection (by name)
Private Function IsArchiveSheet(ByVal wsName As String) As Boolean
    Dim n As String
    n = LCase(Trim(wsName))
    
    'explicit archive sheet + any pattern containing archive/old/legacy
    IsArchiveSheet = (InStr(1, n, "archive", vbTextCompare) > 0 Or _
                      InStr(1, n, "old", vbTextCompare) > 0 Or _
                      InStr(1, n, "legacy", vbTextCompare) > 0)
End Function

'README/CONTROL detection
Private Function IsReadmeSheet(ByVal wsName As String) As Boolean
    Dim n As String
    n = LCase(Trim(wsName))
    
    IsReadmeSheet = (Left(n, 6) = "readme" Or _
                     InStr(1, n, "control", vbTextCompare) > 0 Or _
                     InStr(1, n, "governance", vbTextCompare) > 0)
End Function

'Apply protection settings for a worksheet
Private Sub ProtectSheetSafe(ByVal ws As Worksheet, ByVal allowFilterSort As Boolean)
    On Error Resume Next
    
    'Unprotect first (if already protected)
    ws.Unprotect Password:=PWD
    
    'Lock all cells by default
    ws.Cells.Locked = True
    
    'Allow filter/sort if needed
    If allowFilterSort Then
        'Enable filters if header row exists
        ws.EnableAutoFilter = True
        'Protect with permissions
        ws.Protect Password:=PWD, _
                   DrawingObjects:=True, Contents:=True, Scenarios:=True, _
                   AllowFiltering:=True, AllowSorting:=True, _
                   AllowUsingPivotTables:=True
    Else
        ws.Protect Password:=PWD, _
                   DrawingObjects:=True, Contents:=True, Scenarios:=True
    End If
    
    On Error GoTo 0
End Sub

'Tab color helper
Private Sub SetTabColor(ByVal ws As Worksheet, ByVal role As String)
    'Role colors (RGB)
    'DATA = Blue, README = Green, ARCHIVE = Red, OTHER = Gray, WORK = Yellow (unused here)
    Select Case role
        Case "DATA"
            ws.Tab.Color = RGB(0, 112, 192)      'Blue
        Case "README"
            ws.Tab.Color = RGB(0, 176, 80)       'Green
        Case "ARCHIVE"
            ws.Tab.Color = RGB(192, 0, 0)        'Red
        Case Else
            ws.Tab.Color = RGB(128, 128, 128)    'Gray
    End Select
End Sub

'Workbook structure protect
Private Sub ProtectWorkbookStructure()
    On Error Resume Next
    'Unprotect first
    ThisWorkbook.Unprotect Password:=PWD
    'Protect structure (prevents sheet add/delete/rename/move)
    ThisWorkbook.Protect Password:=PWD, Structure:=True, Windows:=False
    On Error GoTo 0
End Sub

'========================
' MAIN ENTRYPOINT
'========================
Public Sub APPLY_SOR_GOVERNANCE()
    Dim ws As Worksheet
    Dim role As String
    
    Application.ScreenUpdating = False
    Application.DisplayAlerts = False
    
    For Each ws In ThisWorkbook.Worksheets
        role = "OTHER"
        
        If IsDataSheet(ws.Name) Then
            role = "DATA"
            SetTabColor ws, role
            ProtectSheetSafe ws, True   'allow filter/sort
        ElseIf IsArchiveSheet(ws.Name) Then
            role = "ARCHIVE"
            SetTabColor ws, role
            ProtectSheetSafe ws, False
        ElseIf IsReadmeSheet(ws.Name) Then
            role = "README"
            SetTabColor ws, role
            ProtectSheetSafe ws, False
        Else
            'Other sheets: keep visible but locked and gray
            SetTabColor ws, role
            ProtectSheetSafe ws, False
        End If
    Next ws
    
    'Protect workbook structure last
    ProtectWorkbookStructure
    
    Application.DisplayAlerts = True
    Application.ScreenUpdating = True
    
    MsgBox "SoR Governance Applied: Tabs colored + sheets protected + workbook structure locked.", vbInformation
End Sub

'Optional: Remove protections (admin use only)
Public Sub REMOVE_SOR_GOVERNANCE()
    Dim ws As Worksheet
    
    Application.ScreenUpdating = False
    Application.DisplayAlerts = False
    
    ThisWorkbook.Unprotect Password:=PWD
    
    For Each ws In ThisWorkbook.Worksheets
        On Error Resume Next
        ws.Unprotect Password:=PWD
        ws.Tab.ColorIndex = xlColorIndexNone
        On Error GoTo 0
    Next ws
    
    Application.DisplayAlerts = True
    Application.ScreenUpdating = True
    
    MsgBox "SoR Governance Removed: Sheets unprotected and tab colors cleared.", vbInformation
End Sub



