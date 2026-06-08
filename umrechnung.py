# Zahlensystem-Umrechnungen: Hex / Bin / Dez

HEX = '0123456789ABCDEF'


def f_hex2dez(sHex):
    sHex = sHex.strip().upper()
    iDez = 0
    for cZiffer in sHex:
        iWert = HEX.index(cZiffer)   # wirft ValueError bei Murks-Eingabe, ist hier gewollt
        iDez = iDez * 16 + iWert
    return iDez


def f_dez2hex(iZahl):
    if iZahl == 0:
        return '0'                   # Schleife unten dreht bei 0 nie, sonst kaeme '' raus
    sHex = ''
    while iZahl > 0:
        iRest = iZahl % 16
        sHex = HEX[iRest] + sHex
        iZahl = iZahl // 16
    return sHex


def f_hex2bin(sHex):
    sHex = sHex.strip().upper()
    sBin = ''
    for cZiffer in sHex:
        iWert = HEX.index(cZiffer)
        # eine Hex-Ziffer ist genau 1 Nibble = 4 Bit, drum stellenweise abbauen
        sNibble = ''
        for iStelle in (8, 4, 2, 1):
            if iWert >= iStelle:
                sNibble = sNibble + '1'
                iWert = iWert - iStelle
            else:
                sNibble = sNibble + '0'
        sBin = sBin + sNibble
    sBin = sBin.lstrip('0')
    return sBin if sBin else '0'     # falls alles Null war, bleibt '0' stehen


def f_bin2hex(sBin):
    sBin = sBin.strip()
    # von rechts in 4er-Gruppen lesen, also links auf ein Vielfaches von 4 auffuellen
    while len(sBin) % 4 != 0:
        sBin = '0' + sBin
    sHex = ''
    for iStart in range(0, len(sBin), 4):
        sNibble = sBin[iStart:iStart + 4]
        iWert = 0
        for cBit in sNibble:
            iWert = iWert * 2 + int(cBit)
        sHex = sHex + HEX[iWert]
    sHex = sHex.lstrip('0')
    return sHex if sHex else '0'


if __name__ == '__main__':
    print('Was umrechnen?')
    print('  1) Hex -> Bin')
    print('  2) Bin -> Hex')
    print('  3) Dez -> Hex')
    print('  4) Hex -> Dez')
    sWahl = input('Auswahl: ').strip()

    if sWahl == '1':
        print(f_hex2bin(input('Hex-Zahl: ')))
    elif sWahl == '2':
        print(f_bin2hex(input('Bin-Zahl: ')))
    elif sWahl == '3':
        print(f_dez2hex(int(input('Dezimalzahl: '))))
    elif sWahl == '4':
        print(f_hex2dez(input('Hex-Zahl: ')))
    else:
        print('Keine gueltige Auswahl.')
