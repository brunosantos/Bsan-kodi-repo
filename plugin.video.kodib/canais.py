import sys
from default import addCanal, p_umcanal, art, librtmpwindow, mensagemprogresso, activado, \
    addDir
from mensagens import sintomecomsorte, librtmpwindow
from programacao import p_todos, p_umcanal
from utils import savefile, addDir, addCanal
from resources.lib.daring import selfAddon, tvporpath, changeview
from servidores import info_servidores

def setupCanais(canaison, empty, nrcanais, programas):
    if selfAddon.getSetting("canais-rtp1") == "true": canaison.append('[B]RTP 1[/B]'); addCanal(
        "[B]RTP 1[/B] " + p_umcanal(programas, 'RTP1', 'nomeprog'), empty, 16, tvporpath + art + 'rtp1-ver2.png',
        nrcanais, p_umcanal(programas, 'RTP1', 'descprog'))
    if selfAddon.getSetting("canais-rtp2") == "true":  canaison.append('[B]RTP 2[/B]'); addCanal(
        "[B]RTP 2[/B] " + p_umcanal(programas, 'RTP2', 'nomeprog'), empty, 16, tvporpath + art + 'rtp2-ver2.png',
        nrcanais, p_umcanal(programas, 'RTP2', 'descprog'))
    if selfAddon.getSetting("canais-sic") == "true":  canaison.append('[B]SIC[/B]'); addCanal(
        "[B]SIC[/B] " + p_umcanal(programas, 'SIC', 'nomeprog'), empty, 16, tvporpath + art + 'sic-ver3.png', nrcanais,
        p_umcanal(programas, 'SIC', 'descprog'))
    if selfAddon.getSetting("canais-tvi") == "true":  canaison.append('[B]TVI[/B]'); addCanal(
        "[B]TVI[/B] " + p_umcanal(programas, 'TVI', 'nomeprog'), empty, 16, tvporpath + art + 'tvi-ver2.png', nrcanais,
        p_umcanal(programas, 'TVI', 'descprog'))
    if selfAddon.getSetting("canais-sporttv1") == "true":
        canaison.append('[B]SPORTTV 1[/B]');
        addCanal("[B]SPORTTV 1[/B] " + p_umcanal(programas, 'SPTV1', 'nomeprog'), empty, 16,
                 tvporpath + art + 'sptv1-ver2.png', nrcanais, p_umcanal(programas, 'SPTV1', 'descprog'))
        # canaison.append('[B]SPORTTV 1 HD[/B]'); addCanal("[B]SPORTTV 1 HD[/B] " + p_umcanal(programas,'SPTV1','nomeprog'),empty,16,tvporpath + art + 'sptvhd-ver2.png',nrcanais,p_umcanal(programas,'SPTV1','descprog'))
    if selfAddon.getSetting("canais-sporttv2") == "true": canaison.append('[B]SPORTTV 2[/B]'); addCanal(
        "[B]SPORTTV 2[/B] " + p_umcanal(programas, 'SPTV2', 'nomeprog'), empty, 16, tvporpath + art + 'sptv2-ver2.png',
        nrcanais, p_umcanal(programas, 'SPTV2', 'descprog'))
    if selfAddon.getSetting("canais-sporttv3") == "true": canaison.append('[B]SPORTTV 3[/B]'); addCanal(
        "[B]SPORTTV 3[/B] " + p_umcanal(programas, 'SPTV3', 'nomeprog'), empty, 16, tvporpath + art + 'sptv3-ver2.png',
        nrcanais, p_umcanal(programas, 'SPTV3', 'descprog'))
    if selfAddon.getSetting("canais-sporttv4") == "true": canaison.append('[B]SPORTTV 4[/B]'); addCanal(
        "[B]SPORTTV 4[/B] " + p_umcanal(programas, 'SPTV4', 'nomeprog'), empty, 16, tvporpath + art + 'sptv4-ver2.png',
        nrcanais, p_umcanal(programas, 'SPTV4', 'descprog'))
    if selfAddon.getSetting("canais-sporttv5") == "true": canaison.append('[B]SPORTTV 5[/B]'); addCanal(
        "[B]SPORTTV 5[/B] " + p_umcanal(programas, 'SPTV5', 'nomeprog'), empty, 16, tvporpath + art + 'sptv5-ver2.png',
        nrcanais, p_umcanal(programas, 'SPTV5', 'descprog'))
    if selfAddon.getSetting("canais-btv1") == "true": canaison.append('[B]Benfica TV 1[/B]'); addCanal(
        "[B]Benfica TV 1[/B] " + p_umcanal(programas, 'SLB', 'nomeprog'), empty, 16, tvporpath + art + 'btv1-ver1.png',
        nrcanais, p_umcanal(programas, 'SLB', 'descprog'))
    if selfAddon.getSetting("canais-btv2") == "true": canaison.append('[B]Benfica TV 2[/B]'); addCanal(
        "[B]Benfica TV 2[/B] " + p_umcanal(programas, 'SLB2', 'nomeprog'), empty, 16, tvporpath + art + 'btv2-ver1.png',
        nrcanais, p_umcanal(programas, 'SLB2', 'descprog'))
    if selfAddon.getSetting("canais-sportingtv") == "true": canaison.append('[B]Sporting TV[/B]'); addCanal(
        "[B]Sporting TV[/B] " + p_umcanal(programas, 'SCP', 'nomeprog'), empty, 16, tvporpath + art + 'scptv-ver1.png',
        nrcanais, p_umcanal(programas, 'SCP', 'descprog'))
    if selfAddon.getSetting("canais-portocanal") == "true": canaison.append('[B]Porto Canal[/B]'); addCanal(
        "[B]Porto Canal[/B] " + p_umcanal(programas, 'PORTO', 'nomeprog'), empty, 16,
        tvporpath + art + 'pcanal-ver2.png', nrcanais, p_umcanal(programas, 'PORTO', 'descprog'))
    if selfAddon.getSetting("canais-abolatv") == "true": canaison.append('[B]A Bola TV[/B]'); addCanal(
        "[B]A Bola TV[/B] " + p_umcanal(programas, 'ABOLA', 'nomeprog'), empty, 16, tvporpath + art + 'abola-ver1.png',
        nrcanais, p_umcanal(programas, 'ABOLA', 'descprog'))
    if selfAddon.getSetting("canais-cmtv") == "true": canaison.append('[B]CM TV[/B]'); addCanal(
        "[B]CM TV[/B] " + p_umcanal(programas, 'CMTV', 'nomeprog'), empty, 16, tvporpath + art + 'cmtv-ver1.png',
        nrcanais, p_umcanal(programas, 'CMTV', 'descprog'))
    if selfAddon.getSetting("canais-ss5") == "true": canaison.append('[B]Casa dos Segredos 5[/B]'); addCanal(
        "[B]Casa dos Segredos 5[/B] " + p_umcanal(programas, 'SEM', 'nomeprog'), empty, 16,
        tvporpath + art + 'casadseg-ver1.png', nrcanais, p_umcanal(programas, 'SEM', 'descprog'))
    if selfAddon.getSetting("canais-rtpac") == "true": canaison.append('[B]RTP Açores[/B]'); addCanal(
        "[B]RTP Açores[/B] " + p_umcanal(programas, 'RTPAC', 'nomeprog'), empty, 16, tvporpath + art + 'rtpac-ver1.png',
        nrcanais, p_umcanal(programas, 'RTPAC', 'descprog'))
    if selfAddon.getSetting("canais-rtpaf") == "true": canaison.append('[B]RTP Africa[/B]'); addCanal(
        "[B]RTP Africa[/B] " + p_umcanal(programas, 'RTPA', 'nomeprog'), empty, 16, tvporpath + art + 'rtpaf-ver1.png',
        nrcanais, p_umcanal(programas, 'RTPA', 'descprog'))
    if selfAddon.getSetting("canais-rtpi") == "true": canaison.append('[B]RTP Informação[/B]'); addCanal(
        "[B]RTP Informação[/B] " + p_umcanal(programas, 'RTPIN', 'nomeprog'), empty, 16,
        tvporpath + art + 'rtpi-ver1.png', nrcanais, p_umcanal(programas, 'RTPIN', 'descprog'))
    if selfAddon.getSetting("canais-rtpint") == "true": canaison.append('[B]RTP Internacional[/B]'); addCanal(
        "[B]RTP Internacional[/B] " + p_umcanal(programas, 'RTPINT', 'nomeprog'), empty, 16,
        tvporpath + art + 'rtpint-ver1.png', nrcanais, p_umcanal(programas, 'RTPINT', 'descprog'))
    if selfAddon.getSetting("canais-rtpmad") == "true": canaison.append('[B]RTP Madeira[/B]'); addCanal(
        "[B]RTP Madeira[/B] " + p_umcanal(programas, 'RTPMD', 'nomeprog'), empty, 16,
        tvporpath + art + 'rtpmad-ver1.png', nrcanais, p_umcanal(programas, 'RTPMD', 'descprog'))
    if selfAddon.getSetting("canais-rtpmem") == "true": canaison.append('[B]RTP Memória[/B]'); addCanal(
        "[B]RTP Memória[/B] " + p_umcanal(programas, 'RTPM', 'nomeprog'), empty, 16,
        tvporpath + art + 'rtpmem-ver1.png', nrcanais, p_umcanal(programas, 'RTPM', 'descprog'))
    if selfAddon.getSetting("canais-sick") == "true": canaison.append('[B]SIC K[/B]'); addCanal(
        "[B]SIC K[/B] " + p_umcanal(programas, 'SICK', 'nomeprog'), empty, 16, tvporpath + art + 'sick-ver2.png',
        nrcanais, p_umcanal(programas, 'SICK', 'descprog'))
    if selfAddon.getSetting("canais-sicmulher") == "true": canaison.append('[B]SIC Mulher[/B]'); addCanal(
        "[B]SIC Mulher[/B] " + p_umcanal(programas, 'SICM', 'nomeprog'), empty, 16, tvporpath + art + 'sicm-ver3.png',
        nrcanais, p_umcanal(programas, 'SICM', 'descprog'))
    if selfAddon.getSetting("canais-sicnoticias") == "true": canaison.append('[B]SIC Noticias[/B]'); addCanal(
        "[B]SIC Noticias[/B] " + p_umcanal(programas, 'SICN', 'nomeprog'), empty, 16, tvporpath + art + 'sicn-ver2.png',
        nrcanais, p_umcanal(programas, 'SICN', 'descprog'))
    if selfAddon.getSetting("canais-sicradical") == "true": canaison.append('[B]SIC Radical[/B]'); addCanal(
        "[B]SIC Radical[/B] " + p_umcanal(programas, 'SICR', 'nomeprog'), empty, 16,
        tvporpath + art + 'sicrad-ver2.png', nrcanais, p_umcanal(programas, 'SICR', 'descprog'))
    if selfAddon.getSetting("canais-tvi24") == "true": canaison.append('[B]TVI24[/B]'); addCanal(
        "[B]TVI24[/B] " + p_umcanal(programas, 'TVI24', 'nomeprog'), empty, 16, tvporpath + art + 'tvi24-ver2.png',
        nrcanais, p_umcanal(programas, 'TVI24', 'descprog'))
    if selfAddon.getSetting("canais-tvificcao") == "true": canaison.append('[B]TVI Ficção[/B]'); addCanal(
        "[B]TVI Ficção[/B] " + p_umcanal(programas, 'TVIFIC', 'nomeprog'), empty, 16, tvporpath + art + 'tvif-ver2.png',
        nrcanais, p_umcanal(programas, 'TVIFIC', 'descprog'))
    if selfAddon.getSetting("canais-maistvi") == "true": canaison.append('[B]Mais TVI[/B]'); addCanal(
        "[B]Mais TVI[/B] " + p_umcanal(programas, 'SEM', 'nomeprog'), empty, 16, tvporpath + art + 'maistvi-ver2.png',
        nrcanais, p_umcanal(programas, 'SEM', 'descprog'))
    if selfAddon.getSetting("canais-artv") == "true": canaison.append('[B]ARTV[/B]'); addCanal(
        "[B]ARTV[/B] " + p_umcanal(programas, 'ARTV', 'nomeprog'), empty, 16, tvporpath + art + 'artv-ver1.png',
        nrcanais, p_umcanal(programas, 'ARTV', 'descprog'))
    if selfAddon.getSetting("canais-economico") == "true": canaison.append('[B]Económico TV[/B]'); addCanal(
        "[B]Económico TV[/B] " + p_umcanal(programas, 'ETVHD', 'nomeprog'), empty, 16, tvporpath + art + 'econ-v1.png',
        nrcanais, p_umcanal(programas, 'ETVHD', 'descprog'))
    if selfAddon.getSetting("canais-euronews") == "true": canaison.append('[B]Euronews[/B]'); addCanal(
        "[B]Euronews[/B] " + p_umcanal(programas, 'EURN', 'nomeprog'), empty, 16, tvporpath + art + 'euronews-ver1.png',
        nrcanais, p_umcanal(programas, 'EURN', 'descprog'))
    if selfAddon.getSetting("canais-hollywood") == "true": canaison.append('[B]Hollywood[/B]'); addCanal(
        "[B]Hollywood[/B] " + p_umcanal(programas, 'HOLLW', 'nomeprog'), empty, 16, tvporpath + art + 'hwd-ver2.png',
        nrcanais, p_umcanal(programas, 'HOLLW', 'descprog'))
    if selfAddon.getSetting("canais-mov") == "true": canaison.append('[B]MOV[/B]'); addCanal(
        "[B]MOV[/B] " + p_umcanal(programas, 'SEM', 'nomeprog'), empty, 16, tvporpath + art + 'mov-ver2.png', nrcanais,
        p_umcanal(programas, 'SEM', 'descprog'))
    if selfAddon.getSetting("canais-axn") == "true": canaison.append('[B]AXN[/B]'); addCanal(
        "[B]AXN[/B] " + p_umcanal(programas, 'AXN', 'nomeprog'), empty, 16, tvporpath + art + 'axn-ver2.png', nrcanais,
        p_umcanal(programas, 'AXN', 'descprog'))
    if selfAddon.getSetting("canais-axnblack") == "true": canaison.append('[B]AXN Black[/B]'); addCanal(
        "[B]AXN Black[/B] " + p_umcanal(programas, 'AXNBL', 'nomeprog'), empty, 16, tvporpath + art + 'axnb-ver2.png',
        nrcanais, p_umcanal(programas, 'AXNBL', 'descprog'))
    if selfAddon.getSetting("canais-axnwhite") == "true": canaison.append('[B]AXN White[/B]'); addCanal(
        "[B]AXN White[/B] " + p_umcanal(programas, 'AXNWH', 'nomeprog'), empty, 16, tvporpath + art + 'axnw-ver2.png',
        nrcanais, p_umcanal(programas, 'AXNWH', 'descprog'))
    if selfAddon.getSetting("canais-fox") == "true": canaison.append('[B]FOX[/B]'); addCanal(
        "[B]FOX[/B] " + p_umcanal(programas, 'FOX', 'nomeprog'), empty, 16, tvporpath + art + 'fox-ver2.png', nrcanais,
        p_umcanal(programas, 'FOX', 'descprog'))
    if selfAddon.getSetting("canais-foxcrime") == "true": canaison.append('[B]FOX Crime[/B]'); addCanal(
        "[B]FOX Crime[/B] " + p_umcanal(programas, 'FOXCR', 'nomeprog'), empty, 16, tvporpath + art + 'foxc-ver2.png',
        nrcanais, p_umcanal(programas, 'FOXCR', 'descprog'))
    if selfAddon.getSetting("canais-foxlife") == "true": canaison.append('[B]FOX Life[/B]'); addCanal(
        "[B]FOX Life[/B] " + p_umcanal(programas, 'FLIFE', 'nomeprog'), empty, 16, tvporpath + art + 'foxl-ver3.png',
        nrcanais, p_umcanal(programas, 'FLIFE', 'descprog'))
    if selfAddon.getSetting("canais-foxmovies") == "true": canaison.append('[B]FOX Movies[/B]'); addCanal(
        "[B]FOX Movies[/B] " + p_umcanal(programas, 'FOXM', 'nomeprog'), empty, 16, tvporpath + art + 'foxm-ver2.png',
        nrcanais, p_umcanal(programas, 'FOXM', 'descprog'))
    if selfAddon.getSetting("canais-syfy") == "true": canaison.append('[B]Syfy[/B]'); addCanal(
        "[B]Syfy[/B] " + p_umcanal(programas, 'SYFY', 'nomeprog'), empty, 16, tvporpath + art + 'syfy-ver1.png',
        nrcanais, p_umcanal(programas, 'SYFY', 'descprog'))
    if selfAddon.getSetting("canais-disney") == "true": canaison.append('[B]Disney Channel[/B]'); addCanal(
        "[B]Disney Channel[/B] " + p_umcanal(programas, 'DISNY', 'nomeprog'), empty, 16,
        tvporpath + art + 'disney-ver1.png', nrcanais, p_umcanal(programas, 'DISNY', 'descprog'))
    if selfAddon.getSetting("canais-disneyj") == "true": canaison.append('[B]Disney Junior[/B]'); addCanal(
        "[B]Disney Junior[/B] " + p_umcanal(programas, 'DISNYJ', 'nomeprog'), empty, 16,
        tvporpath + art + 'djun-ver1.png', nrcanais, p_umcanal(programas, 'DISNYJ', 'descprog'))
    if selfAddon.getSetting("canais-cpanda") == "true": canaison.append('[B]Canal Panda[/B]'); addCanal(
        "[B]Canal Panda[/B] " + p_umcanal(programas, 'PANDA', 'nomeprog'), empty, 16,
        tvporpath + art + 'panda-ver2.png', nrcanais, p_umcanal(programas, 'PANDA', 'descprog'))
    if selfAddon.getSetting("canais-pbiggs") == "true": canaison.append('[B]Panda Biggs[/B]'); addCanal(
        "[B]Panda Biggs[/B] " + p_umcanal(programas, 'BIGGS', 'nomeprog'), empty, 16,
        tvporpath + art + 'pbiggs-ver1.png', nrcanais, p_umcanal(programas, 'BIGGS', 'descprog'))
    if selfAddon.getSetting("canais-motors") == "true": canaison.append('[B]Motors TV[/B]'); addCanal(
        "[B]Motors TV[/B] " + p_umcanal(programas, 'MOTOR', 'nomeprog'), empty, 16, tvporpath + art + 'motors-ver1.png',
        nrcanais, p_umcanal(programas, 'MOTOR', 'descprog'))
    if selfAddon.getSetting("canais-chelsea") == "true": canaison.append('[B]Chelsea TV[/B]'); addCanal(
        "[B]Chelsea TV[/B] " + p_umcanal(programas, 'CHELS', 'nomeprog'), empty, 16, tvporpath + art + 'chel-v1.png',
        nrcanais, p_umcanal(programas, 'CHELS', 'descprog'))
    if selfAddon.getSetting("canais-cacapesca") == "true": canaison.append('[B]Caça e Pesca[/B]'); addCanal(
        "[B]Caça e Pesca[/B] " + p_umcanal(programas, 'CAÇAP', 'nomeprog'), empty, 16,
        tvporpath + art + 'cacapesca-v1.png', nrcanais, p_umcanal(programas, 'CAÇAP', 'descprog'))
    if selfAddon.getSetting("canais-torostv") == "true": canaison.append('[B]Toros TV[/B]'); addCanal(
        "[B]Toros TV[/B] " + p_umcanal(programas, 'TOROTV', 'nomeprog'), empty, 16, tvporpath + art + 'toros-v1.png',
        nrcanais, p_umcanal(programas, 'TOROTV', 'descprog'))
    if selfAddon.getSetting("canais-discovery") == "true": canaison.append('[B]Discovery Channel[/B]'); addCanal(
        "[B]Discovery Channel[/B] " + p_umcanal(programas, 'DISCV', 'nomeprog'), empty, 16,
        tvporpath + art + 'disc-ver2.png', nrcanais, p_umcanal(programas, 'DISCV', 'descprog'))
    if selfAddon.getSetting("canais-discturbo") == "true": canaison.append('[B]Discovery Turbo[/B]'); addCanal(
        "[B]Discovery Turbo[/B] " + p_umcanal(programas, 'DISCT', 'nomeprog'), empty, 16,
        tvporpath + art + 'discturbo-v1.png', nrcanais, p_umcanal(programas, 'DISCT', 'descprog'))
    if selfAddon.getSetting("canais-odisseia") == "true": canaison.append('[B]Odisseia[/B]'); addCanal(
        "[B]Odisseia[/B] " + p_umcanal(programas, 'ODISS', 'nomeprog'), empty, 16,
        tvporpath + art + 'odisseia-ver1.png', nrcanais, p_umcanal(programas, 'ODISS', 'descprog'))
    if selfAddon.getSetting("canais-historia") == "true": canaison.append('[B]História[/B]'); addCanal(
        "[B]História[/B] " + p_umcanal(programas, 'HIST', 'nomeprog'), empty, 16, tvporpath + art + 'historia-ver1.png',
        nrcanais, p_umcanal(programas, 'HIST', 'descprog'))
    if selfAddon.getSetting("canais-ngc") == "true": canaison.append('[B]National Geographic Channel[/B]'); addCanal(
        "[B]National Geographic Channel[/B] " + p_umcanal(programas, 'NGC', 'nomeprog'), empty, 16,
        tvporpath + art + 'natgeo-ver1.png', nrcanais, p_umcanal(programas, 'NGC', 'descprog'))
    if selfAddon.getSetting("canais-eurosport") == "true": canaison.append('[B]Eurosport[/B]'); addCanal(
        "[B]Eurosport[/B] " + p_umcanal(programas, 'EURSP', 'nomeprog'), empty, 16, tvporpath + art + 'eusp-ver2.png',
        nrcanais, p_umcanal(programas, 'EURSP', 'descprog'))
    if selfAddon.getSetting("canais-eurosport2") == "true": canaison.append('[B]Eurosport 2[/B]'); addCanal(
        "[B]Eurosport 2[/B] " + p_umcanal(programas, 'EURS2', 'nomeprog'), empty, 16,
        tvporpath + art + 'eusp2-ver1.png', nrcanais, p_umcanal(programas, 'EURS2', 'descprog'))
    if selfAddon.getSetting("canais-espn") == "true": canaison.append('[B]ESPN[/B]'); addCanal(
        "[B]ESPN[/B] " + p_umcanal(programas, 'SEM', 'nomeprog'), empty, 16, tvporpath + art + 'espn-ver1.png',
        nrcanais, p_umcanal(programas, 'SEM', 'descprog'))
    if selfAddon.getSetting("canais-fashion") == "true": canaison.append('[B]Fashion TV[/B]'); addCanal(
        "[B]Fashion TV[/B] " + p_umcanal(programas, 'FASH', 'nomeprog'), empty, 16, tvporpath + art + 'fash-ver1.png',
        nrcanais, p_umcanal(programas, 'FASH', 'descprog'))
    if selfAddon.getSetting("canais-traceu") == "true": canaison.append('[B]TRACE Urban[/B]'); addCanal(
        "[B]TRACE Urban[/B] " + p_umcanal(programas, 'TRACE', 'nomeprog'), empty, 16, tvporpath + art + 'traceu.png',
        nrcanais, p_umcanal(programas, 'TRACE', 'descprog'))
    if selfAddon.getSetting("canais-virginrtv") == "true": canaison.append('[B]Virgin Radio TV[/B]'); addCanal(
        "[B]Virgin Radio TV[/B] " + p_umcanal(programas, 'SEM', 'nomeprog'), empty, 16, tvporpath + art + 'virginr.png',
        nrcanais, p_umcanal(programas, 'SEM', 'descprog'))
    if selfAddon.getSetting("canais-djingtv") == "true": canaison.append('[B]DJing TV[/B]'); addCanal(
        "[B]DJing TV[/B] " + p_umcanal(programas, 'SEM', 'nomeprog'), empty, 16, tvporpath + art + 'djingtv.png',
        nrcanais, p_umcanal(programas, 'SEM', 'descprog'))
    # canaison.append('[B]Clubbing TV[/B]'); addCanal("[B]Clubbing TV[/B] " + p_umcanal(programas,'SEM','nomeprog'),empty,16,tvporpath + art + 'djingtv.png',nrcanais,p_umcanal(programas,'SEM','descprog'))
    if selfAddon.getSetting("canais-vh1") == "true": canaison.append('[B]VH1[/B]'); addCanal(
        "[B]VH1[/B] " + p_umcanal(programas, 'VH1', 'nomeprog'), empty, 16, tvporpath + art + 'vh1plus.png', nrcanais,
        p_umcanal(programas, 'VH1', 'descprog'))
    if selfAddon.getSetting("canais-mtv") == "true": canaison.append('[B]MTV[/B]'); addCanal(
        "[B]MTV[/B] " + p_umcanal(programas, 'MTV', 'nomeprog'), empty, 16, tvporpath + art + 'mtv-ver1.png', nrcanais,
        p_umcanal(programas, 'MTV', 'descprog'))
    if selfAddon.getSetting("canais-tpai") == "true": canaison.append('[B]TPA Internacional[/B]'); addCanal(
        "[B]TPA Internacional[/B] " + p_umcanal(programas, 'TPA', 'nomeprog'), empty, 16,
        tvporpath + art + 'tpa-ver1.png', nrcanais, p_umcanal(programas, 'TPA', 'descprog'))
    if selfAddon.getSetting("canais-tvglobo") == "true": canaison.append('[B]TV Globo[/B]'); addCanal(
        "[B]TV Globo[/B] " + p_umcanal(programas, 'GLOBO', 'nomeprog'), empty, 16, tvporpath + art + 'globo-v1.png',
        nrcanais, p_umcanal(programas, 'GLOBO', 'descprog'))
    if selfAddon.getSetting("canais-tvrecord") == "true": canaison.append('[B]TV Record[/B]'); addCanal(
        "[B]TV Record[/B] " + p_umcanal(programas, 'TVREC', 'nomeprog'), empty, 16, tvporpath + art + 'record-v1.png',
        nrcanais, p_umcanal(programas, 'TVREC', 'descprog'))


def canais():
    librtmpwindow()
    info_servidores()

    nrcanais=62
    canaison=[]
    empty='nada'
    #GA("None","listacanais")
    if selfAddon.getSetting("prog-lista3") == "true":
        mensagemprogresso.create('TV Portuguesa', 'A carregar listas de programação.','Por favor aguarde.')
        mensagemprogresso.update(0)
        if mensagemprogresso.iscanceled(): sys.exit(0)
        programas=p_todos()
        mensagemprogresso.close()
    else: programas=[]

    sintomecomsorte()

    if activado==True: addCanal("[B]Lista Completa[/B]",empty,16,tvporpath + art + 'gravador-ver1.png',nrcanais,'')
    addDir("[B][COLOR white]Informações[/COLOR][/B]",'nada',1,tvporpath + art + 'defs-ver2.png',1,'Clique aqui para voltar ao menu principal.',True)
    if selfAddon.getSetting("listas-pessoais") == "true":
        addDir("[B][COLOR white]Listas Pessoais[/COLOR][/B]",'nada',6,tvporpath + art + 'listas-ver2.png',1,'Outras listas de canais criadas pela comunidade.',True)

    if selfAddon.getSetting("radios") == "true": addDir("[B][COLOR white]Radios[/COLOR][/B]",'nada',19,tvporpath + art + 'radios-v1.png',1,'Oiça comodamente radios nacionais.',True)
    if selfAddon.getSetting("eventos") == "true": canaison.append('[B][COLOR white]Eventos[/COLOR][/B]'); changeview()
    if selfAddon.getSetting("praias") == "true": addDir("[B][COLOR white]Praias[/COLOR][/B]",'nada',26,tvporpath + art + 'versao-ver2.png',1,'Webcams das melhores praias nacionais.',True)

    setupCanais(canaison, empty, nrcanais, programas)

    try:
        canaison=''.join(canaison)
        savefile('canaison', canaison)
    except: pass

    vista_canais()
    xbmcplugin.setContent(int(sys.argv[1]), 'livetv')


def vista_canais():
      menuview=selfAddon.getSetting('vistacanais')
      if menuview == "0": xbmc.executebuiltin("Container.SetViewMode(500)")#miniatura
      elif menuview == "1": xbmc.executebuiltin("Container.SetViewMode(560)")#guia
      elif menuview == "2": xbmc.executebuiltin("Container.SetViewMode(50)")#lista
      elif menuview == "3": xbmc.executebuiltin("Container.SetViewMode(51)")#lista grande