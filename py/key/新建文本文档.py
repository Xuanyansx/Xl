
# -*- coding: utf-8 -*-
"""
Written by MaYiming in HeNan XuChang on 2022.4.15
"""
 
import win32con
import win32api
import time
 
 
key_map = {
    "0": 49, "1": 50, "2": 51, "3": 52, "4": 53, "5": 54, "6": 55, "7": 56, "8": 57, "9": 58,
    "A": 65, "B": 66, "C": 67, "D": 68, "E": 69, "F": 70, "G": 71, "H": 72, "I": 73, "J": 74,
    "K": 75, "L": 76, "M": 77, "N": 78, "O": 79, "P": 80, "Q": 81, "R": 82, "S": 83, "T": 84,
    "U": 85, "V": 86, "W": 87, "X": 88, "Y": 89, "Z": 90
}
   
   
def key_down(key):
    """
    函数功能：按下按键
    参    数：key:按键值
    """
    key = key.upper()
    vk_code = key_map[key]
    win32api.keybd_event(vk_code,win32api.MapVirtualKey(vk_code,0),0,0)
   
   
def key_up(key):
    """
    函数功能：抬起按键
    参    数：key:按键值
    """
    key = key.upper()
    vk_code = key_map[key]
    win32api.keybd_event(vk_code, win32api.MapVirtualKey(vk_code, 0), win32con.KEYEVENTF_KEYUP, 0)
   
   
def key_press(key):
    """
    函数功能：点击按键（按下并抬起）
    参    数：key:按键值
    """
    key_down(key)
    time.sleep(0.01)
    key_up(key)
 
 
def count_note(Note):
    """
    函数功能：为连接的音符数计数
    参    数：Note：相连的音符（中间无空格） 字符串类型
    """
    i = 0
    count = 0
    while i < len(Note):
        if Note[i] == '(':
            count += 1
            while 1:
                i += 1
                if Note[i] == ')':
                    i += 1
                    break
        else:
            count += 1
            i += 1
    return count
 
def play_note(Note, time_div, time_div_div, time_interval):
     
    """
    函数功能：播放连接的音符
    参    数：Note：相连的音符（中间无空格） 字符串类型
             time_div: 音符时值一次分割
             time_div_div：音符时值二次分割
             time_interval：单个小节的时值
    """
    play_time = time_interval / time_div / time_div_div
    i = 0
    while i < len(Note):
        if Note[i] == '(':
            while 1:
                i += 1
                if Note[i] == ')':
                    time.sleep(play_time)
                    i += 1
                    break
                else:
                    key_press(Note[i])
        elif Note[i].isalpha():
            key_press(Note[i])
            time.sleep(play_time)
            i += 1
        elif Note[i] == '1':
            time.sleep(play_time)
            i += 1
        else:
            i += 1
 
     
 
 
def play_music(music, time_interval):
     
    """
    函数功能：播放曲谱
    参    数：Music：曲谱 字符串类型
             time_interval：单个小节的时值
    """
     
    music_section = music.split("/")
    for i in range(len(music_section)):
        if music_section[i][-2:] == "  ":
            music_section[i] = music_section[i] + '1'
 
    for x in music_section:
        Notes = x.split()
        time_div = len(Notes)
        for y in Notes:
            time_div_div = count_note(y)
            play_note(y, time_div, time_div_div, time_interval)
 
 
 
 
 
 
# 七里香
seven = "SDGH/(NQ) C /(AQ) DE /(VW) (AQ) /\
F (AH)QH/(BG) SH/(GQ) (SW) /(ZE) B /\
(MS)D(BG)H/(NQ) C /(AQ) DE /(VW) (AQ) /\
F (AH)Q/(BW) S /(GQ) S/(BSGJ)/G/(NQ) C /\
(AJ) (DQ)Q /V A /F (AQ)/\
(BQ) (SJ) /(GH) (SJ)H /ZGB  /M (BG)/\
(NG) C /(AF) (CD)G/V Z /N (ZG)/\
(BG) (XH) /(MS) (XF)F/ZDB  /M (BG)/\
(NQ) C /(AJ) (DQ)Q /V A /F (AQ)/\
(BQ) (SJ) /(GQ) (SW)W/ZQB /(MQ) (BJ)/\
(NQ) (CQ)Q /AJDJ /VHA  /(FH) (AJ)H/\
BGX  /(MSG) X /(BGJ)  /G Q /\
(NQ) C /(AD) (CH) /(VH) Z /(NG) (ZW)/\
(BW) X /(MD) (XF)F/ZDB  /M (BG)/\
(NG) (CF) /(AF) (CD)D/VS ZS /NA ZD/\
BSX /M (XF) /(ZD) B /(MG) (BQ)/\
(NQ) C /(AD) (CH) /(VH) (ZG) /(NG) (ZW)/\
(BW) (XD) /(MD) (XF) /(ZF) (BDG) /(MG) (BE)/\
(NE) (CW) /(AW) (DQ) /(VQ) (AW) /(FQ) (AE)/\
(BE) SW/G S /(BSGJ)G /Q QQ"
 
# 红莲华
red = "(VQ)(AJ)(FQ) V /(BQ)(SJ)(GQ) BA/\
(NQ)(AJ)(DH) GG/CS)MD D G/\
(VH) A F (VH) Q/BW)SG (BQ) W/\
(NDQE) (XBSG) (CNDH) (XBSG) (CNDQ)(DQ)(DQ)(DQ)/\
(CNDH) (XBSG) (CNDH) (XBSG) (CNQE)(QE)(QE)(QE)/\
(CNDH) (XBSG) (CNDH) (XBSG) (CNDQ)(DQ)(DQ)(DQ)/\
(CNDH) (XBSG) (CNDH) (XBSG) (CND)GE/\
(NH)(AQ)(DJ) G(NH) G/B X M S SA(BS)F/\
(VD)(ZN)(VN) Z /BN (XA)S (BD) S (XD) G/\
(NH)(AQ)(DJ) G(NH) G/B S (DG) EWEW(BSE) R/\
(VE)(AQ)(FQ) VQ/(BJ) (SJ) (GQ)W BQ/\
(NW)(AQ)(DH) Q(NE) W/B WSW (GW) W EB Q/\
(VW)(AQ)(FH) Q(VT) /B WSW (GW) W QB Q/\
(NW)(AQ)(DH) Q(NE) W/B SW(GE)W(BE)(ST)E/\
(VW)(AQ)(FQ) VQ/(BJ)(SJ)(GQ)W B/\
(VQ)(AJ)(FQ)  /(BQ)(SJ)(GQ) BA/\
(NQ)(AJ)(DH) GG/(CS)MD D G/\
(VAH) (VA) (VA)H (VA)Q /(BSW) (BS) (BS) (BS)Q (BS)W/\
(NADQE) G(NAD)H (NADQ) W (NADQE) (QT) (NADQY)/\
G (BSG) (BSQE)\
(VW)E(AFT) EVW (VE)E(AF) (VQ)/\
(BW)E(SGT) EBW (BE)E(SG) (BG)/\
(NG) QQ(AD)(NG) G(NQ) (ADW)Q/\
(BT)B(SGR)B E (BS)W (BS)Q/\
VV(AF)(VQ)Q(VW)(AFE)(VW)/\
BB(SG)(BW)W(BE)(SGT)(BE)/\
(CNDH) (XBSG) (CNDH) (XBSG) (CNDQ)(DQ)(DQ)(DQ)/\
(CN) (CN)G(CN) (BSG)(BSQE)/\
(VW)E(AFT) EVW (VE)E(AF) (VQ)/\
(BW)E(SGT) EBW (BE)Q(SG) (BQ)/\
(NQ) W(AD) (NQE) (ND)(ADQ)J/\
NN(ADT)N (BSE) (BS)W (BS)Q/\
VV(AF)(VQ) (VW)(AFE)(VW)/(BS) GG H/"
 
# 卡农
kanong = "(ZBD)  /(XBM)  /(CNA)  /(CBM) /\
(ZVN)  /(ZBA)  /(ZVN)  /(XBM)  /\
(ZBQE)  /(BSJW)  /(NDHQ)  /(CMGJ) /\
(VAFH)  /(ZBDG)  /(VAFH)  /(BSGJ)  /\
(ZBQE)  /(BSJW) F /(NDHQ)  /(CMGJ) S /\
(VAFH)  /(ZBDG) D /(VAFH)  /(BSGJ) F /\
(ZDQ) B A  /(BGJ) X (MF) /\
(NDQ) C (AHE) /(CET) M (DWY) /\
(VHR) Z (NQ)  /(ZGE) B (AD)  /\
(VSF) Z (NHQ) /(BGQ) X (MFQ) J /\
(ZQ)(BJ)(AQ)(BD) /(BG) X (MGJ) X /\
(NDQ) C (AHE) C /(CT)(ME)(DT)(MY)/\
(VHR)(ZGE)(NFW)(ZHR) /(ZE)(BW)(AQ)(BJ) /\
(VFH)(ZSF)(NHQ) Z /(BGQ)(XF)(MDQ)(XSJ) /\
(ZQ)(BJ)(AQ)(BF) /(BG) X (MGJ) X /\
(NDQ) C (AHE) C /(CT)(ME)(DT)(MY) /\
(VHR)(ZGE)(NFW)(ZHR) /(ZE)(BW)(AQ)(BJ) /\
(VFH)(ZDG)(NSF)(ZHQ) /(BGQ) XS(MJ) (XW)G /\
(ZQE) BG(AE) (BQ)W /B XE(MR)E(XW) /\
(NW) CQA (CJ)Q /(CJ) (BG)DMG (BM)A /\
(VFH) Z(GJ) N (ZHQ) /(ZDG) B A (BA)A /\
(VH)AZA (NF)H(ZQ)W /(BQ) XJMQ(XW)G /\
(ZQE) BG(AE) (BQ)W /B XE(MR)E(XW) /\
(NW) CQA (CJ)Q /(CJ) (BG)DMG (BM)A /\
(VFH) Z(HQ)NH(ZR) /(ZE) (BW)QA (BA)A /\
(VH)AZA (NF)H(ZQ)W /(BJ) XQM (XW)Q /\
(ZT) (BE)R(AT) (BE)R /(BT)G(XH)J(MQ)W(XE)R /\
(NE) (CQ)W(AE) (CD)F /(CG)H(BG)F(MG)Q(BJ)Q /\
(VH) (ZQ)J(NH) (ZG)F /(ZG)F(BD)F(AG)H(BJ)Q /\
(VH) (ZQ)J(NQ) (ZJ)Q /(BJ)H(XJ)Q(MW)E(XR)T /\
(ZT) (BE)R(AT) (BE)R /(BT)G(XH)J(MQ)W(XE)R /\
(NE) (CQ)W(AE) (CD)F /(CG)H(BG)F(MG)Q(BJ)Q /\
(VH) (ZQ)J(NH) (ZG)F /(ZG)F(BD)F(AG)H(BJ)Q /\
(VH) (ZQ)J(NQ) (ZJ)Q /(BJ)H(XJ)Q(MW)E(XR)T /\
(ZT) (BE)R(AT) (BE)R /(BT)G(XH)J(MQ)W(XE)R /\
(NE) (CQ)W(AE) (CD)F /(CG)H(BG)F(MG)Q(BJ)Q /\
(VH) (ZQ)J(NH) (ZG)F /(ZG)F(BD)F(AG)H(BJ)Q /\
(VH) (ZQ)J(NQ) (ZJ)Q /(BJ)H(XJ)Q(MW)E(XR)T /\
(ZE) (BQ)W(AE) (BW)Q /(BW)J(XQ)W(ME)W(XQ)J /\
(NQ) (CH)J(AQ) (CA)S /(CD)F(BD)S(MD)Q(BJ)Q /\
(VH) (ZQ)J(NH) (ZG)F /(ZG)F(BD)F(AG)H(BJ)Q /\
(VH) (ZQ)J(NQ) (ZJ)Q /(BJ)H(XJ)Q(MW)Q(XH)J /\
(ZQ) B A D  / B X M S /  N C N A /  C B M D /\
V Z N A  /  Z C B A  /  V Z N A  /  B X M S  /\
(ZT) (BE)R(AT) (BE)R /(BT)G(XH)J(MQ)W(XE)R /\
(NE) (CQ)W(AE) (CD)F /(CG)H(BG)F(MG)Q(BJ)Q /\
(VH) (ZQ)J(NH) (ZG)F /(ZG)F(BD)F(AG)H(BJ)Q /\
(VH) (ZQ)J(NQ) (ZJ)Q /(BJ)H(XJ)Q(MW)E(XR)T /\
(ZT) (BE)R(AT) (BE)R /(BT)G(XH)J(MQ)W(XE)R /\
(NE) (CQ)W(AE) (CD)F /(CG)H(BG)F(MG)Q(BJ)Q /\
(VH) (ZQ)J(NH) (ZG)F /(ZG)F(BD)F(AG)H(BJ)Q /\
(VH) (ZQ)J(NQ) (ZJ)Q /(BJ)H(XJ)Q(MW)E(XR)T /\
(ZT) (BE)R(AT) (BE)R /(BT)G(XH)J(MQ)W(XE)R /\
(NE) (CQ)W(AE) (CD)F /(CG)H(BG)F(MG)Q(BJ)Q /\
(VH) (ZQ)J(NH) (ZG)F /(ZG)F(BD)F(AG)H(BJ)Q /\
(VH) (ZQ)J(NQ) (ZJ)Q /(BJ)H(XJ)Q(MW)E(XR)T /\
(ZE) (BQ)W(AE) (BW)Q /(BW)J(XQ)W(ME)W(XQ)J /\
(NQ) (CH)J(AQ) (CA)S /(CD)F(BD)S(MD)Q(BJ)Q /\
(VH) (ZQ)J(NH) (ZG)F /(ZG)F(BD)F(AG)H(BJ)Q /\
(VH) (ZQ)J(NQ) (ZJ)Q /(BJ)H(XJ)Q(MW)Q(XH)J /\
(ZQ) B A D  / B X M S /  N C N A /  C B M D /\
V Z N A  /  Z C B A  /  V Z N A  /  B X M S  /"
 
# 青花瓷
Qinghuaci = "  TY/T E /W E/\
(VW)(NQ)/(AH)S/D  /WE /\
(CW)(BQ)/(AG)S/D /WE /\
(XW)(NQ)/(SH)D/(GQ)W /  H/\
(ZE)B/AS/(DQ)W /(ME)T /\
(NT)C/(AE)S/(DW)G/(HQ)N/\
(XW)(NQ)/(SH)D/(GQ)(DW)/(SE)(NE) /\
B(TY) X /C B /N A /S D /\
G   /    /   W/QH /\
(VW)(AE)/(SH)D/(GW)E/(VT)E /\
B(XW)/SD/G T/(BT)E /\
(CW)(ME)/(SG)D/(GW)E/(CT)W /\
N(CQ)/AS/D Q/(BW)E /\
(VT)(AY)/(ST)(DE)/(GT)E/(VE)W /\
(BW)X/SD/G Q/(BW)Q /\
(ZW)B/(AQ)(SW)/DE/GT /\
Z(BE)/AS/D T/(BT)E /\
(VW)(AE)/(SH)D/(GW)E/(VT)E /\
B(XW)/SD/G T/(BT)E /\
(CW)(ME)/(SG)D/(GW)E/(CT)W /\
N(CQ)/AS/D Q/(BW)E /\
(VT)(AY)/(ST)(DE)/(GT)E/(VE)W /\
(BW)X/S(DG)/(GE) /WW /\
Z(BQ)/NA/SA/SD /\
G  /   /   /ET /\
(VY)A/SD/G /TE /\
(BW)X/SD/G /QW /\
(CQT)M/SD/G /TW /\
(NQ)C/AS/D /(BQ)W /\
(VE)A/(SW)D/(GQ)D/(SH)A /\
(XQ)N/(SW)D/(GE)D/(SY)N /\
B (TY)X/CB/NA/SD / \
G /   /   W/QH /\
(ZQ)B/(AQ)(SH)/(DQ) /QH /\
(ZQ)(BH)/(AG)S/D W/(MQ)H /\
(NQ)C/(AQ)(SH)/(DQ)  /QE /\
(NW)(CQ)/(AQ)S/DG /(BH)E /\
(VE)A/(SE)(DW)/(GE) /EW /\
(VE)(AT)/S(DE)/GE /(VE)E /\
(BW)(XW)/(SW)(DW)/(GW)  /QE /\
B(XW)/SD/G W/(BQ)H /\
(ZQ)B/(AQ)(SH)/(DQ) /QH /\
(ZQ)(BH)/(AG)S/D G/(MH)E /\
(NT)C/(AT)(SE)/(DT)  /TE /\
(NW)(CQ)/(AQ)S/D W/(BQ)W /\
(VE)(AW)/(SW)(DQ)/(GW) /QH /\
(BW)(XQ)/(SQ)(DH)/(GQ) /QW /\
Z(BQ)/NA/SA/SD/\
(ZQR)B/(AE)S/(DW) T/(BT)E/\
(VW)(AE)/(SH)D/(GW)E/(VT)E /\
B(XW)/SD/G T/(BT)E /\
(CW)(ME)/(SG)D/(GW)E/(CT)W /\
N(CQ)/AS/D Q/(BW)E /\
(VT)(AY)/(ST)(DE)/(GT)E/(VE)W /\
(BW)X/SD/G Q/(BW)Q /\
(ZW)B/(AQ)(SW)/DE/GT /\
Z(BE)/AS/D T/(BT)E /\
(VW)(AE)/(SH)D/(GW)E/(VT)E /\
B(XW)/SD/G T/(BT)E /\
(CW)(ME)/(SG)D/(GW)E/(CT)W /\
N(CQ)/AS/D Q/(BW)E /\
(VT)(AY)/(ST)(DE)/(GT)E/(VE)W /\
(BW)X/S(DG)/(GE) /WW /\
Z(BQ)/NA/SA/SD /\
G  /   /   /   /"
 
#反方向的钟
Fanfangxiang = "(VEY) (AWT) /(FHE) (GW) /B (XDH) /(SG)  /\
N (CS) /(AD) G /     /     /\
(VEY) (AWT) /(FHE) (GW) /B (XDH) /(SG) D /\
N (CS) /(AD) G /H    /      /\
(VEY) (AWT) /(FHE) (GW) /B (XDH) /(SG) D /\
N (CS) /(AD) G /     /     /\
(VEY) (AWT) /(FHE) (GW) /B (XDH) /(SG) D /\
N (CS) /(AD) G /H    /    /\
 G/(VY)(AT)/(FE)W /B S /(GE)H /\
N (AQ) /D W /N (DE) /H T /\
(VY)(AT)/(FE)W /B S /(GE)H /\
N A /(AD) A /N (DG)H /(BQ)W(SE)T /\
(VY)(AT)/(FE)W /B S /(GE)H /\
N (AQ) /D W /N (DE) /H T /\
(VY)(AT)/(FE)W /B S /(GE)H /\
N A /(DH) A /N A /(DH)\
(AE)/(VE) (AW)E /G (HE) /(BE) (SW)E /G (JE) /\
(NE) (DW)E /G (HE) /E (NW)E /D (HE) /\
(VE) (AW)E /G (HE) /(BE) (SW)E /G(JE) /\
(NE) (DW)E /G (HE) /E (NW)E /D (HQE) /\
(VQE) (AJW)(QE) /G (HQE) /(BQE) (SJW)(QE) /G (HQE) /\
(NQE) (DJW)(QE) /G (HQE)Q/(JW) (NQE) /D (HQE) /\
(VQE) (AJW)(QE) /G (HQE) (BQE) /(SJW)(QE) /G (HQE) /\
(NQE) (DJW)(QE) /G HH /H (NG) /C M /\
N (AH) /(DH) J /(BQ) (SW) /(GJ) Q /\
(VH) (AJ) /F H /C M /(DE)  /\
N (AH) /(DH) J /(BQ) (SW) /(GJ) QJ /\
(VH) (AJ) /F H /C M /(DE)  /\
(VH) (AJ) /F H /C M /(DE)  /\
(XJ) (NQ) /(SF) (NJ) /(SF) (NQ) /(SFW) (NJ) /\
C H(MJ) /(DH)JMH /(DJ) (MY)U /DY(MU) /\
(NDQE) /(CMDJ) /(VAHQ) /(CMJW) /\
(VY) (AT) /(FHE) (AW) /B S /(GJE) (SQ) /\
N (AW) /(DH) (AE) /N (AT) /(DH) A /\
(VY) (AT) /(FHE) (AW) /B S /(GJE) (SW) /\
N A /(DHQ) (AW) /N (AQ) /(DH) A /\
(VY) (AT) /(FHE) (AW) /B S /(GJE) (SQ) /\
N (AW) /(DH) (AE) /N (AT) /(DH) A /\
(VY) (AT) /(FHE) (AW) /B S /(GJE) (SH) /\
N A /(DH) A /N (AG)H /(BQ)W(SE)T /\
(VY) (AT) /(FHE) (AW) /B S /(GJE) (SQ) /\
N (AW) /(DH) (AE) /N (AT) /(DH) A /\
(VY) (AT) /(FHE) (AW) /B S /(GJE) (SW) /\
N A /(DHQ) (AW) /N (AQ) /B S /\
(VY) (AT) /(FHE) (AW) /B S /(GJE) (SQ) /\
N (AW) /(DH) (AE) /N (AT) /(DH) A /\
(VY) (AT) /(FHE) (AW) /B S /(GJE) (SH) /\
N A /(DH) A /N A /(DH) N /\
(VA)(ZS)/(ND) H /B (XG) /M DS /\
(NA)(CS)/(AD) G /B (XH) /M QJ /\
(VQ)(ZH)/(ND) S /B X /(MD) H /\
N C /A D /N (DG) /B (DG) /\
(VY) (AT) /(FHE) (AW) /B S /(GJE) (SQ) /\
N (AW) /(DH) (AE) /N (AT) /(DH) A /\
(VY) (AT) /(FHE) (AW) /B S /(GJE) (SW) /\
N A /(DHQ) (AW) /N (AQ) /(DH) A /\
(VY) (AT) /(FHE) (AW) /B S /(GJE) (SQ) /\
N (AW) /(DH) (AE) /N (AT) /(DH) A /\
(VY) (AT) /(FHE) (AW) /B S /(GJE) (SH) /\
N A /(DH) A /N (AG)H /(BQ)W(SE)T /\
(VY) (AT) /(FHE) (AW) /B S /(GJE) (SQ) /\
N (AW) /(DH) (AE) /N (AT) /(DH) A /\
(VY) (AT) /(FHE) (AW) /B S /(GJE) (SW) /\
N A /(DHQ) (AW) /N (AQ) /B S /\
(VY) (AT) /(FHE) (AW) /B S /(GJE) (SQ) /\
N (AW) /(DH) (AE) /N (AT) /(DH) A /\
(VY) (AT) /(FHE) (AW) /B S /(GJE) (SH) /\
N A /(DH) A /N A /(DH) N "
 
# 花海
Huahai = "/     /    /Q WN/(BSE) TT/\
V A /(DG) A(DG)/(BE) (SW)/(GQ) (SW)E/\
Z B /(SG) B /A S /(BSD) JQ/\
V (AJ)Q /F (GQ) /(BJ) (XQ)J/S GH/\
ZGB /S B /Q W /(BSE) TT/\
V A /(DG) A(DG)/(CE) (MW)/(DQ) (MW)Q/\
N C /A D /(BQ) (SW) /(GE) (ST)Q/\
X N /S NQ/(BQ) (XJ)H/S (GJ)Q/\
Z B /(AF) B /(AD)  /\
QE E/Z B /(SG) B /(SGE) W /(BSQ) W/\
M (BE) /(SG) B /(SG)  /(BSQ)E E/\
N C /(AD) C /(ADR) E /(CAT) Q/\
B Z /(AF) B /(AF)  /(AFQ)R R/\
V A /(AF) A /(BR) (XE) /(SQ) G/\
Z (BE) /S B /D  /QE W/\
X N /(SQ)E /W D /QE W/\
B S /(GQ) S /(BSGJ)  /QE E/\
Z B /(SG) B /(SGE) W /(BSQ) W/\
M (BT) /(SG) B /(SG)  /(BSQ)E E/\
N C /(AD) C /(ADR) E /(CAT) Q/\
B Z /(AF) B /(AF)   /(BQ)R R/\
V Z /N Z /(BF) (XD) /(VA) (BG)/\
C (MD) /B Q /N C /(AD) C/\
(XT) (NR) /(SE) (NQ) /(BQ) S /(GJ) (SQ)/\
Z B /(SG) B /\
QE E/Z B /(SG) B /(SGE) W /(BSQ) W/\
M (BE) /(SG) B /(SG)  /(BSQ)E E/\
N C /(AD) C /(ADR) E /(CAT) Q/\
B Z /(AF) B /(AF)  /(AFQ)R R/\
V Z /N Z /(BF) (XD) /(VA) (BG)/\
C (MD) /B Q /N C /(AD) C /\
(XT) (NR) /(SE) (NQ) /(BQ) S /(GJ) (SQ)/\
Z B /(SG) B /\
Q W /(BSE) TT/\
V A /(DG) A(DG)/(BE) (SW) /(GQ) (SW)E/\
Z B /(SG) B /A S /(BSD) JQ/\
V (AJ)Q /F (AQ) /(BJ) (XH)G/(SG) HH/\
ZGB /(SG) B /Q W /(BSE) TT/\
V A /(DG) A(DG)/(CE) (MW) /(DQ) (MW)Q/\
N C /(AD) C /(BA) (XS) /(XBD) G/\
(XG) (NF) /(SF) (ND) /(XQ) N /(SD) (ND)/\
(BS) X /S G /(BQ)(SW) /(SGE) TT/\
V A /(DG) A(DG) /(BE) (SW) /(GQ) (SW)E/\
Z B /(SG) B /A S /(BSD) JQ/\
V (AJ)Q /F (AQ) /(BJ) (XH)G/(SG) HH/\
ZGB /(SG) B /Q W /(BSE) TT/\
V A /(DG) A(DG) /(CE) (MW) /(DQ) (MW)Q/\
N C /(AD) C /(BQ) (SW) /(GE) (ST)Q/\
(XVN)  /      /(BSQ) J /H   /\
     /J   /(ZQ) B /(AF) B /\
(ZBAD) "
 
#稻香
Daoxiang = "A G (WT)EQ /B G (JT) /\
N H (QWT) /C S (QT) /\
X N (QT) /B G (QT) /\
Z B (ASGW) Q(ASGW)/ QB (ASGW) QW/\
Z (BE) (ST)DA /B (XW) (SJ) (DG)/\
N (CE) (AT) D /C (MW) (DJ) (MG)/\
(XQ) N A (NG)/(BQ) X S (DG)/\
(ZQ) B (ASG) A(ASG)/ AB (ASG)Q(BQ)Q/\
(ZQ) (BH)QD (BQ)Q/(BW)W(SW)W (GE) (SQ)/\
(NQ) (CH)QA (DQ)Q/(CW)W(MW)W (DE) (MQ)/\
(XQ) (NH)QA (NQ)Q/(BW)W(SW)W (GQ) (SE)/\
(ZE) B (ASG) A(ASGQ) Q (BQ)Q (ASGQ)Q(BQ)H/\
(ZQ) (BH)QD (BQ)Q/(BW)W(SW)W (GE) (SQ)/\
(NQ) (CH)QA (DQ)Q/(CW)W(MW)W (DE) (MQ)/\
X NQ(AQR) NE/BW(SW)Q(GW)Q(SE) /\
(ZQ) B (ASG) A(ASG)/ AB (ASGE) (BT)/\
(ZT) (BT)T DT BT /BT (ST)T (GE) (SW)Q/\
(NQ) (CE)E AE DE /CE (ME)E (DE) (MQ)H/\
(XH) (NQ)QA (NQ)Q/(BW) (SW)W(GQ) (SE)/\
(ZE) B (ASG) A(ASG)/ AB (ASGE) (BT)/\
(ZT) (BT)T DT BT /BT (ST)T (GE) (SW)Q/\
(NQ) (CE)E AE DE /CE (ME)E (DE) (MQ)H/\
(XH) (NQ)QA (NQ)Q/(BW) (SW)WG (SQ)/\
(ZQ) B (ASG) A(ASG)/ AB (ASG) B/\
Z (BE) (ST)DA /B (XW) (SJ) (DG)/\
N (CE) (AT) D /C (MW) (DJ) (MG)/\
(XQ) N A (NG)/(BQ) X S (DG)/\
(ZQ) B (ASG) A(ASG)/ AB (ASG) B/\
Z (BE) (ST)DA /B (XW) (SJ) (DG)/\
N (CE) (AT) D /C (MW) (DJ) (MG)/\
(XQ) N A (NG)/(BQ) X S (DG)/\
(ZQ) B (ASG) A(ASG)/ AB (ASG)Q(BQ)Q/\
(ZQ) (BQ)Q(DQ)H(BQ) /(BQ)Q(SQ)Q(GQ) (SQ)/\
NQ(CQ)Q(AQ)Q(DQ)Q/(CQ)Q(MQ)Q(DQ) (MQ)/\
X (NH)Q(AQ)H(NQ)H/(BQ)Q(SH)Q GQ(SQ)Q/\
(ZQ)Q(BQ)Q(SQ)Q(ADQ)/            QQQ/\
(ZQ) (BQ)Q(DQ)Q(BQ)Q/(BE) (SW) GQ(SQ)Q/\
(NQ)Q(CQ)Q(AQ)Q(DQ)Q/(CE) (MW) DQ(MQ)H/\
(XG) (NQ)Q AQ NH/(BQ)H(XQ)H(SQ) (DW)/\
(ZW) (BQ) S (BQT) D (BQT) (AE)E(BE)E/\
(ZT) (BE) (DE)E BE/BE(SE)E(GE)E(SE)E/\
(NT) (CE) (AE)E DE/CE(ME)E(DE)E(ME)E/\
(XT) (NE) AE(NE)E/(BQ) (SQ) GQ(SQ)Q/\
(ZT)E(BE) (DE)W(BW) /(SW)Q(BQ) (AQ)W(BE)/\
(ZW) (BQ) (DH)Q(BQ)Q/(BQ)Q(SQ)Q(GQ)W(SE)/\
(NW) (CQ) (AH)Q(DQ)Q/(CQ)Q(MQ)Q(DQ)W(MQ)/\
X NQ(AQR) NE/BW(SW)Q(GW)Q(SE) /\
(ZQ) B (ASG) A(ASG)/ AB (ASGE) (BT)"
 
# 延迟3秒播放 
time.sleep(5)
# 播放音乐
#七里香
#play_music(seven,0.8)
 
# 反方向的钟
#play_music(Fanfangxiang,0.7)
 
 
# 花海
#play_music(Huahai,0.8)
 
 
# 红莲华
play_music(red,0.9)
 
 
# 卡农
#play_music(kanong,0.9)
 
 
#青花瓷
#play_music(Qinghuaci,0.8)
 
# 稻香
play_music(Daoxiang,1.35)