Option Explicit
'============================================================
' RandomCorner : �p�����鎞�͕K���Ƃ�B����ȊO�̓����_���B
'============================================================

Dim intColor
Dim intSize
Dim intBoard()

Const BLANK = 0
Const BLACK = 1
Const WHITE = -1

'--------------------
' �W�����͂̎󂯎��
'--------------------
intColor = CInt(WScript.StdIn.Readline()) ' ���
Wscript.StdErr.WriteLine(intColor)

intSize = CInt(WScript.StdIn.Readline()) ' �ՖʃT�C�Y
Wscript.StdErr.WriteLine(intSize)

ReDim intBoard(intSize-1, intSize-1) ' �΂̔z�u

Dim x
Dim y

For y=0 To intSize-1
    Dim strLine
    Dim aryStrings
    Dim intTmp

    strLine = WScript.StdIn.ReadLine()
    Wscript.StdErr.WriteLine(strLine)
    aryStrings = Split(strLine, " ")

    For x=0 To intSize-1
        intBoard(y, x) = CInt(aryStrings(x))
    Next

Next

'--------------------
' ��̌��𒲂ׂ�
'--------------------
Dim aryPossibles

aryPossibles = GetPossibles(intColor, intSize, intBoard)



'--------------------
' ���ʏo��
'--------------------
'�p������ꍇ�͗D�悷��
'����ȊO�̓����_��
Wscript.StdOut.WriteLine("0 0")


'�u����ꏊ�����ׂĕԂ�
Function GetPossibles(intColor, intSize, intBoard)
    Dim aryPossibles()
    Dim intReversible
    Dim x
    Dim y
    Dim intCnt

    intCnt = 0

    For y=0 To intSize-1
        For x=0 To intSize-1
            intReversible = IsReversible(intColor, intSize, intBoard, x, y)

            If intReversible > 0 Then
                ReDim Preserve aryPossibles(intCnt)

                aryPossibles(intCnt) = CStr(x) + " " + CStr(y)
                Wscript.StdErr.WriteLine("POSSIBLE : " + CStr(x) + " " + CStr(y))
                intCnt = intCnt + 1
            End If
        Next
    Next

    GetPossibles = aryPossibles

End Function


'�΂��Ђ�����Ԃ��邩���肷��
Function IsReversible(intColor, intSize, intBoard, x, y)
    Dim intRet
    Dim aryDirs
    Dim aryDir

    intRet = 0
    aryDirs = Array(Array(-1, 1), Array(0, 1), Array(1, 1), Array(-1, 0), Array(1, 0), Array(-1, -1), Array(0, 1), Array(1, -1))

    If intBoard(y, x) = BLANK Then
        For Each aryDir in aryDirs
            Dim intNextX
            Dim intNextY
            Dim intTmp

            intNextX = x
            intNextY = y

            Do
                intNextX = intNextX + aryDir(0)
                intNextY = intNextY + aryDir(1)

                '���W���͈͓�
                If (intNextX >= 0) And (intNextX < intSize) And (intNextY >= 0) And (intNextY < intSize) Then
                    Dim intNextValue

                    intNextValue = intBoard(intNextY, intNextX)

                    '�΂��u����Ă���
                    If intNextValue <> BLANK Then
                        '�u�����΂Ɠ����F���u����Ă���
                        If intNextValue = intColor Then
                            Exit Do
                        End If

                        intTmp = intTmp + 1
                    Else
                        intTmp = 0
                        Exit Do
                    End If
                Else
                    intTmp = 0
                    Exit Do
                End If
            Loop

            intRet = intRet + intTmp
        Next
    End If

    IsReversible = intRet

End Function
'============================================================
' END
'============================================================
