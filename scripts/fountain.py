#!/usr/bin/env python

import hashlib
import random
import time
import sys


links = [
    "/gesellschaft/zeitgeschehen/2013-12/nsu-prozess-siegfried-mundlos",
    "/gesellschaft/zeitgeschehen/2013-12/hannover-einstellung-prozess-wulff",
    "/wirtschaft/2013-12/bankenunion-eu-schulz-widerstand-parlament",
    "/karriere/beruf/2013-12/bag-urteil-hiv-kuendigung",
    "/sport/2013-12/dartwm-shorty-seyler-phil-taylor",
    "/karriere/bewerbung/2013-12/karrierebuch-anti-bewerbungsratgeber",
    "/wirtschaft/2013-12/eu-finanzminister-bankenunion",
    "/politik/ausland/2013-12/kuba-markt-import-autos",
    "/politik/ausland/2013-12/syrien-assad-terrorkampagne-vereinte-nationen",
    "/gesellschaft/zeitgeschehen/2013-12/wulff-prozess-gericht-zwischenbilanz",
    "/politik/deutschland/2013-12/ruecktritt-holger-apfel-npd",
    "/wirtschaft/2013-12/infografik-realloehne",
    "/news/2013-12/19/justiz-abmahnungen-wegen-sex-videos-staatsanwaltschaft-ermittelt-19151205",
    "/politik/deutschland/2013-12/grosse-koalition-ministerien-zuschnitt-neue-aufgaben",
    "/gesellschaft/zeitgeschehen/2013-12/grossbritannien-london-urteil-mord-soldat",
    "/lebensart/2013-12/stadtleben-nachbarschaft-buergerbeteiligung-running-dinner",
    "/wirtschaft/unternehmen/2013-12/tarifeinigung-pin-verdi",
    "/digital/datenschutz/2013-12/datenschutzbeauftragte-vosshoff-bundestag-gewaehlt",
    "/news/2013-12/19/internet-rechtsprofessorstreaming-keine-urheberrechts-verletzung-19140805",
    "/wirtschaft/2013-12/wirtschaftswissenschaftler-mindestlohn-kritik",
    "/politik/ausland/2013-12/russland-putin-chodorkowski-begnadigung",
    "/politik/deutschland/2013-12/rente-beitragssenkung-bundestag",
    "/community/2013-12/leserorakel-jahresausblick-2014",
    "/news/2013-12/19/d-wohlfahrtsverband-warnt-vor-sozialer-veroedung-ganzer-regionen-19130411",
    "/karriere/beruf/2013-12/arbeitsrecht-arbeit-feiertage-ausgleich",
    "/mobilitaet/2013-12/auto-neuheiten-2014",
    "/wirtschaft/2013-12/malte-buhse-oekonomen-retten-die-welt",
    "/politik/ausland/2013-12/pussy-riot-amnestie-putin",
    "/politik/deutschland/2013-12/holger-apfel-npd-ruecktritt",
    "/digital/datenschutz/2013-12/nsa-eu-mike-rogers",
    "/news/2013-12/19/d-bundeswehr-fliegt-deutsche-aus-dem-suedsudan-aus-19113208",
    "/wirtschaft/2013-12/commerzbank-krise",
    "/news/2013-12/19/olympia-innenminister-de-maizire-reist-nach-sotschi-19110606",
    "/gesellschaft/zeitgeschehen/2013-12/armutsbericht-paritaetischer-wohlfahrtsverband",
    "/sport/2013-12/boris-becker-tennis-djokovic",
    "/politik/ausland/2013-12/bundesregierung-nsa-datenueberwachung",
    "/news/2013-12/19/geheimdienste-us-experten-fordern-umfassende-reform-der-geheimdienstueberwachung-19103005",
    "/politik/ausland/2013-12/suedsudan-luftbruecke-juba",
    "/wirtschaft/2013-12/loehne-inflation-statistisches-bundesamt",
    "/kultur/musik/2013-12/alben-des-jahres-2013",
    "/lebensart/partnerschaft/2013-12/artikel-link-magazin-aufmacher",
    "/news/2013-12/19/fussball-australisches-sturm-talent-yeboah-vor-wechsel-nach-gladbach-19083806",
    "/politik/ausland/2013-12/todesstrafe-usa-giftspritze",
    "/news/2013-12/19/justiz-musikerinnen-der-punkband-pussy-riot-hoffen-auf-freilassung-19082805",
    "/digital/datenschutz/2013-12/reaktionen-usa-kommission-umbau-nsa",
    "/wirtschaft/2013-12/us-haushalt-kongress-shutdown",
    "/news/2013-12/19/finanzen-us-kongress-einigt-sich-auf-zwei-jahres-haushalt-19074407",
    "/kultur/literatur/2013-12/zeit-krimibestenliste-2013",
    "/2013/52/ski-luxus-guenther-aigner",
    "/2013/52/oesterreich-rot-schwarze-regierung-programm",
    "/2013/52/wladimir-putin-dresdner-stollen-moskau",
    "/2013/52/weihnachten-familienfest",
    "/2013/52/infografik-asyl",
    "/2013/52/leipzig-u-bahn-citytunnel",
    "/2013/52/pofalla-altmaier-kanzleramt",
    "/digital/2013-12/resolution-deutschland-brasilien-nsa",
    "/studium/uni-leben/2013-12/studenten-gruender-blogbox-universitaet",
    "/wirtschaft/2013-12/bankenunion-eu-gipfel",
    "/news/2013-12/19/ukraine-eu-gipfel-opposition-proteste-klitschko-fordert-von-eu-solidaritaet-mit-demonstranten-in-kiew-19024605",
    "/wirtschaft/2013-12/eu-einigt-sich-auf-neue-regeln-zur-bankenabwicklung",
    "/wissen/2013-12/gaia-esa-weltraumteleskop-start-milchstrasse",
    "/digital/datenschutz/2013-12/nsa-reform-expertenkommission-obama",
    "/politik/2013-12/grieichenland-parlament-streicjt-parteiengeld-fuer-neonazis",
    "/wirtschaft/2013-12/us-notenbank-fed-konjunkturprogramm",
    "/politik/ausland/2013-12/glenn-greenwald-eu-parlament",
    "/studium/hochschule/2013-12/khorchide-muenster-islam-universitaet",
    "/politik/ausland/2013-12/ukraine-janukowitsch-moskauer-vertraege",
    "/digital/internet/2013-12/facebook-boersengang-klage",
    "/wissen/gesundheit/2013-12/vogelgrippe-h10h8-china",
    "/gesellschaft/zeitgeschehen/2013-12/vater-uwe-mundlos-siegfried-nsu-prozess",
    "/politik/deutschland/2013-12/hessen-cdu-schwarz-gruen-koalitionsvertrag",
    "/digital/internet/2013-12/redtube-abmahnung-staatsanwaltschaft-ermittlungen",
    "/wirtschaft/2013-12/sigmar-gabriel-eeg-eu-verfahren-superminister",
    "/politik/deutschland/2013-12/verfassungsgericht-europawahl-sperrklausel",
    "/wirtschaft/unternehmen/2013-12/amazon-bezos-wachstum",
    "/wirtschaft/2013-12/infografik-armutsrisiko",
    "/news/2013-12/18/d-uwe-mundlos-vater-beleidigt-richter-als-kleiner-klugsch-18165208",
    "/kultur/film/2013-12/brad-pitt-til-schweiger-50-jahre",
    "/kultur/film/2013-12/rundfunkbeitrag-kef-senkung",
    "/politik/deutschland/2013-12/hessen-schwarz-gruen-koalition",
    "/sport/2013-12/bundesliga-fcbayern-langeweile-spannung",
    "/news/2013-12/18/konflikte-hunderte-tote-bei-gewalt-im-suedsudan---unruhen-weiten-sich-aus-18152806",
    "/politik/ausland/2013-12/syrien-plan-chemiewaffen-vernichtung",
    "/news/2013-12/18/prozesse-karlsruhe-verhandelt-ueber-drei-prozent-huerde-bei-europawahl-18151012",
    "/news/2013-12/18/regierung-cdu-und-gruene-in-hessen-stellen-koalitionsvertrag-vor-18144405",
    "/wirtschaft/unternehmen/2013-12/Debeka-Datenschutz",
    "/politik/deutschland/2013-12/guido-westerwelle-stiftung",
    "/politik/ausland/2013-12/putin-duma-amnestie-greenpeace-pussy-riot",
    "/sport/2013-12/tennis-becker-djokovic-trainer",
    "/politik/deutschland/2013-12/gerd-mueller-minister-entwicklungshilfe",
    "/wirtschaft/2013-12/ukraine-russland-eu",
    "/news/2013-12/18/eu-bundesregierung-oekostrom-rabatte-laufen-vorerst-weiter-18135406",
    "/news/2013-12/18/bundestag-wagenknecht-wirft-grosser-koalition-wahlbetrug-vor-18132806",
    "/wissen/gesundheit/2013-12/eu-kommission-klonfleisch",
    "/news/2013-12/18/d-vater-von-uwe-mundlos-sagt-als-zeuge-im-nsu-prozess-aus-18122606",
    "/politik/ausland/2013-12/sudan-fluechtlinge-israel",
    "/digital/internet/2013-12/google-zeitgeist-fragen-twerking",
    "/gesellschaft/2013-12/italien-lampedusa-fluechtlinge-misshandlung",
    "/wirtschaft/2013-12/eu-kommission-eeg-verfahren",
    "/news/2013-12/18/d-eu-verfahren-gegen-deutschland-wegen-eeg-umlage-18115604"
    ]


def main():
    link = links[random.randint(0, 99)]
    user = hashlib.md5(str(random.randint(0, 100))).hexdigest()
    sys.stdout.write("%s,foo=bar; wt3_eid=%s; bar=foo;\n" % (link, user))
    sys.stdout.flush()

if __name__ == '__main__':
    while True:
        main()
        time.sleep(1)