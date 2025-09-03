Function SaveAs(OriginalFile,Extension) 
    Dim ExportFormat 
    Dim acroApp
    NewFileName = Replace(OriginalFile,".pdf",".docx")
    Set acroApp = CreateObject("AcroExch.App")
    Dim acroAVDoc 
    Set acroAVDoc = CreateObject("AcroExch.AVDoc")
    Call acroAVDoc.Open(OriginalFile,"")
    If acroAVDoc Is Nothing Then
        Exit Function
    End If
    Dim acroPDDoc 
    Set acroPDDoc = acroAVDoc.GetPDDoc
    Dim jso 
    Set jso = acroPDDoc.GetJSObject
    Select Case LCase(extension)
        Case "eps": ExportFormat = "com.adobe.acrobat.eps"
        Case "html", "htm": ExportFormat = "com.adobe.acrobat.html"
        Case "jpeg", "jpg", "jpe": ExportFormat = "com.adobe.acrobat.jpeg"
        Case "jpf", "jpx", "jp2", "j2k", "j2c", "jpc": ExportFormat = "com.adobe.acrobat.jp2k"
        Case "docx": ExportFormat = "com.adobe.acrobat.docx"
        Case "doc": ExportFormat = "com.adobe.acrobat.doc"
        Case "png": ExportFormat = "com.adobe.acrobat.png"
        Case "ps": ExportFormat = "com.adobe.acrobat.ps"
        Case "rft": ExportFormat = "com.adobe.acrobat.rft"
        Case "xlsx": ExportFormat = "com.adobe.acrobat.xlsx"
        Case "xls": ExportFormat = "com.adobe.acrobat.spreadsheet"
        Case "txt": ExportFormat = "com.adobe.acrobat.accesstext"
        Case "tiff", "tif": ExportFormat = "com.adobe.acrobat.tiff"
        Case "xml": ExportFormat = "com.adobe.acrobat.xml-1-00"
        Case Else: ExportFormat = "Wrong Input"
    End Select
    
    If ExportFormat <> "Wrong Input" Then
            Call jso.SaveAs(NewFileName, ExportFormat)
            SaveAs = True
    Else
        SaveAs = False
    End If
    'Release the objects.
    acroPDDoc.Close
    acroAVDoc.Close True
    acroApp.Exit
    Set jso = Nothing
    Set acroPDDoc = Nothing
    Set acroAVDoc = Nothing
    Set acroApp = Nothing
End Function

Sub DoBatchConvert(Dir,Extension)
    set objFSO = CreateObject("Scripting.FileSystemObject")
    objStartFolder = "."
    Set objFolder = objFSO.GetFolder(objStartFolder)
    Set colFiles = objFolder.Files
    For Each objFile in colFiles
        If objFSO.GetExtensionName(objFile.Name) = "pdf" Then
            Call SaveAs(objFile.Path,Extension)
        End If
    Next
End Sub

DoBatchConvert ".","docx"