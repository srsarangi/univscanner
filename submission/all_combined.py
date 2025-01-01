from scraper_files.albany import albany_faculty
from scraper_files.ammanu import ammanu
from scraper_files.auburn import auburn_faculty
from scraper_files.buet import buet_faculty_scraper
from scraper_files.caluniv import calcutta_university
from scraper_files.clarkson import clarkson_faculty
from scraper_files.clarku import scrape_clarku_faculty
from scraper_files.cnu import extract_cnu_faculty
from scraper_files.csie import csie
from scraper_files.cuchd import extract_data_from_cuchd
from scraper_files.dortmund import dortmund_faculty
from scraper_files.guest import gust_faculty
from scraper_files.hacettepe import hacettepe
from scraper_files.kku import scrape_kku
from scraper_files.kmutt import kmutt_faculty
from scraper_files.konkuk import konkuk
from scraper_files.ksu import ksu_faculty
from scraper_files.lsu import lsu_faculty_scraper
from scraper_files.manas import manas_faculty
from scraper_files.marburg import marburg
from scraper_files.nit_t import nitt_faculty
from scraper_files.nsu_ece import nsu_ece_faculty
from scraper_files.okstate import okstate_faculty
from scraper_files.rhodes import rhodes_faculty
from scraper_files.rutgers import rutgers_faculty
from scraper_files.sbu import sbu_faculty
from scraper_files.syracuse import syracuse_faculty
from scraper_files.thapar import thapar_faculty
from scraper_files.toronto import torontomu_faculty
from scraper_files.ttu import texas_tech
from scraper_files.tudublin import tudublin_faculty
from scraper_files.ua_cs import extract_ua_cs_faculty
from scraper_files.ud import ud_faculty
from scraper_files.unisa import unisa_faculty
from scraper_files.uop import uop_faculty
from scraper_files.vit import vit_chennai
from scraper_files.wayne import wayne_state_faculty
from scraper_files.wpi import wpi_faculty
from scraper_files.konkuk_copy import extract_konkuk_faculty
from scraper_files.ccu import ccu_faculty
from scraper_files.ceid import extract_ceid_faculty
from scraper_files.gifu import gifu_university_faculty
from scraper_files.gmu import gmu_faculty
from scraper_files.kpi import kpi_faculty
from scraper_files.loyola import loyola_faculty
from scraper_files.Massachusetts import massachusetts
from scraper_files.new_england import extract_une_professors
from scraper_files.seoul import seoul_faculty
from scraper_files.sungshin import sungshin
from scraper_files.vermont import vermont

import csv

def main():
    with open('all_combined.csv', 'a', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["University", "Country", "Name", "Email", "Website"])
        writer.writerows(albany_faculty())
        writer.writerows(ammanu())
        writer.writerows(auburn_faculty())
        # writer.writerows(buet_faculty_scraper())  # This scraper is not working
        writer.writerows(calcutta_university())
        writer.writerows(clarkson_faculty())
        writer.writerows(scrape_clarku_faculty())
        writer.writerows(extract_cnu_faculty())
        writer.writerows(csie())
        writer.writerows(extract_data_from_cuchd())
        writer.writerows(dortmund_faculty())
        writer.writerows(gust_faculty())
        writer.writerows(hacettepe())
        writer.writerows(scrape_kku())
        writer.writerows(kmutt_faculty())
        writer.writerows(konkuk())   # some error in this file 
        writer.writerows(ksu_faculty())
        writer.writerows(lsu_faculty_scraper())
        writer.writerows(manas_faculty())
        writer.writerows(marburg())
        writer.writerows(nitt_faculty())
        writer.writerows(nsu_ece_faculty())
        writer.writerows(okstate_faculty())
        writer.writerows(rhodes_faculty())
        writer.writerows(rutgers_faculty())
        writer.writerows(sbu_faculty())
        writer.writerows(syracuse_faculty())
        writer.writerows(thapar_faculty())
        writer.writerows(torontomu_faculty())
        writer.writerows(texas_tech())
        writer.writerows(tudublin_faculty())
        writer.writerows(extract_ua_cs_faculty())
        writer.writerows(ud_faculty())
        writer.writerows(unisa_faculty())
        writer.writerows(uop_faculty())
        # writer.writerows(vit_chennai()) # this didn't write anything
        writer.writerows(wayne_state_faculty())
        writer.writerows(wpi_faculty())
        writer.writerows(extract_konkuk_faculty())
        writer.writerows(ccu_faculty())
        writer.writerows(extract_ceid_faculty())
        writer.writerows(gifu_university_faculty())
        writer.writerows(gmu_faculty())
        writer.writerows(kpi_faculty())
        writer.writerows(loyola_faculty())
        writer.writerows(massachusetts())
        writer.writerows(extract_une_professors())
        writer.writerows(seoul_faculty())
        writer.writerows(sungshin())
        writer.writerows(vermont())


if __name__ == "__main__":
    main()