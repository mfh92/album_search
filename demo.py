#!/home/mark7/opt/python-3.12.0/bin/python3

   ##  cd "C:/Users/micks/Desktop/mh/computer skills/mh Python/music search 2023"
                                         #  skip re, time, random = already in the standard lib (regular expressions tool splits words containing 'EP' from other words)
import re
import time
import random
from langdetect import detect            #  distinguishes English-like text from text with non-Roman alphabets.
import pandas    as pd
import requests                          #  required for bs4
from    bs4  import BeautifulSoup, Tag

# import  pkg_resources
# pkg_resources.require("streamlit==0.52.0")  #  1.x.x  -> 'illegal command' error
import streamlit as st                           

################################################################################
### -----  numerical constants 

maxSecNameLng = 50                       #  un-skip sections w/ Names longer than this value, assuming that no sectionName should be longer than (or as long as) the data under it.

sourceLng = 20                           #  longer = end ,  shorter = skip (ex. 'Source:[9]\n')

PauseTime = 1.5                          #  n seconds between requests to avoid a spam flag

nArtistsToTry = 3                        #  results must wait until this many artists have been visited

################################################################################
### -----  introduce the app

st.title('Album list generator')
st.markdown("This program web-scrapes the musical artist names from a chosen genre,")
secondLine = "and then visits the page for each of " + str(nArtistsToTry) + " artists to web-scrape all full-length studio album titles." 
st.markdown(secondLine)

################################################################################
### -----  load the genres for the selectbox either from web-scraping or from a hard-coded list                      

### IDEALLY, these next 31 lines will find NmAndUrDict from wiki each time the app is run:
# responsFirst = requests.get( 'https://en.wikipedia.org/wiki/Lists_of_musicians' )
# responsFirst.raise_for_status()          #  show an err msg if status != 200 (if status is not fine)
# Fsoup        = BeautifulSoup( responsFirst.text, 'html.parser' )
# 
# def PopTag(x):                           #  x = a required placeholder, even if x is not passed in to the function
#   return x and re.search('Pops', x)      #  this 1 tag '<i>Top of the Pops</i>' interferes w/ searching
# 
# def editOrCat(x):                      
#   return x and re.search('(^edit$)|(Categor)', x)              #  edit = fullMatch, Categor = partialMatch
# 
# u = Fsoup.find_all( href = PopTag )                            #  do not use 'a' here
# for tag in u:
#   tag.unwrap()                                                 #  remove <i>'s but not its contents, both in the tag and in Fsoup
# 
# to_remove = Fsoup.find_all('a', string = editOrCat)            #  36 total = 34 edit's + 2 categ's
# for tag in to_remove:
#     tag.extract()                                              #  remove <a>'s and contents from both the tags and Fsoup
# 
# for str in list(Fsoup.strings):                                #  edit the contents of all tags which contain either "List of" or "Lists of"
#   str.replace_with(str.replace("List of " , ""))
# 
# for str in list(Fsoup.strings):                                #  not 'st.'
#   str.replace_with(str.replace("Lists of ", ""))
# 
# Alinks      = Fsoup.find_all('a')                              #  find all hyperlink tags (601 of them)
# artList     = Alinks[80:541]                                   #  len = 461
# v           = [itm.string for itm in artList]
# h           = ['https://en.wikipedia.org' + itm['href'] for itm in artList]   #  .get() is good, too
# NmAndUrDict = dict(zip(v, h))                                  #  key:value pairs 
#    gnms        = list(NmAndUrDict)                             #  ?why fails? w/ just keys
###  gnms.insert(0, "-- select --"      #  it would be nice to be able to display this upon initialization		

  # optionally use these 4 lines if 'GenreNamesAndUrls.txt' has been saved in a local directory
##### fle = open('GenreNamesAndUrls.txt', 'r')    #  in case  wiki/Lists_of_musicians changes. 
##### s   = fle.read()                          
##### NmAndUrDict = eval(s)                     
##### fle.close()

  #  if not using either or the 2 above methods to fill NmAndUrDict, then hard-code it:
NmAndUrDict = {'--select--': 'http://www.harbison.one', '1970s Christian pop artists': 'https://en.wikipedia.org/wiki/List_of_1970s_Christian_pop_artists', 'acid rock artists': 'https://en.wikipedia.org/wiki/List_of_acid_rock_artists', 'adult alternative artists': 'https://en.wikipedia.org/wiki/List_of_adult_alternative_artists', 'alternative country musicians': 'https://en.wikipedia.org/wiki/List_of_alternative_country_musicians', 'alternative hip hop artists': 'https://en.wikipedia.org/wiki/List_of_alternative_hip_hop_artists', 'alternative metal artists': 'https://en.wikipedia.org/wiki/List_of_alternative_metal_artists', 'alternative rock artists': 'https://en.wikipedia.org/wiki/List_of_alternative_rock_artists', 'ambient music artists': 'https://en.wikipedia.org/wiki/List_of_ambient_music_artists', 'anarcho-punk bands': 'https://en.wikipedia.org/wiki/List_of_anarcho-punk_bands', 'Arabic pop musicians': 'https://en.wikipedia.org/wiki/List_of_Arabic_pop_musicians', 'avant-garde metal artists': 'https://en.wikipedia.org/wiki/List_of_avant-garde_metal_artists', 'baroque pop artists': 'https://en.wikipedia.org/wiki/List_of_baroque_pop_artists', 'bassoonists': 'https://en.wikipedia.org/wiki/List_of_bassoonists', 'bebop musicians': 'https://en.wikipedia.org/wiki/List_of_bebop_musicians', 'bhangra artists': 'https://en.wikipedia.org/wiki/List_of_bhangra_artists', 'big band musicians': 'https://en.wikipedia.org/wiki/List_of_big_band_musicians', 'black metal bands': 'https://en.wikipedia.org/wiki/List_of_black_metal_bands', 'blue-eyed soul artists': 'https://en.wikipedia.org/wiki/List_of_blue-eyed_soul_artists', 'bluegrass musicians': 'https://en.wikipedia.org/wiki/List_of_bluegrass_musicians', 'blues musicians': 'https://en.wikipedia.org/wiki/List_of_blues_musicians', 'blues rock musicians': 'https://en.wikipedia.org/wiki/List_of_blues_rock_musicians', 'boogie woogie musicians': 'https://en.wikipedia.org/wiki/List_of_boogie_woogie_musicians', 'brass bands': 'https://en.wikipedia.org/wiki/Brass_band#Brass_bands', 'British blues musicians': 'https://en.wikipedia.org/wiki/List_of_British_blues_musicians', 'British music hall musicians': 'https://en.wikipedia.org/wiki/List_of_British_music_hall_musicians', 'Britpop musicians': 'https://en.wikipedia.org/wiki/List_of_Britpop_musicians', 'C-pop artists': 'https://en.wikipedia.org/wiki/List_of_C-pop_artists', 'Cajun musicians': 'https://en.wikipedia.org/wiki/List_of_people_related_to_Cajun_music', 'calypso musicians': 'https://en.wikipedia.org/wiki/List_of_calypso_musicians', 'Celtic musicians': 'https://en.wikipedia.org/wiki/List_of_Celtic_musicians', 'Chicago blues musicians': 'https://en.wikipedia.org/wiki/List_of_Chicago_blues_musicians', 'Christian country artists': 'https://en.wikipedia.org/wiki/List_of_Christian_country_artists', 'Christian hardcore bands': 'https://en.wikipedia.org/wiki/List_of_Christian_hardcore_bands', 'Christian hip hop artists': 'https://en.wikipedia.org/wiki/List_of_Christian_hip_hop_artists', 'Christian metal artists': 'https://en.wikipedia.org/wiki/List_of_Christian_metal_artists', 'Christian punk bands': 'https://en.wikipedia.org/wiki/List_of_Christian_punk_bands', 'Christian rock bands': 'https://en.wikipedia.org/wiki/List_of_Christian_rock_bands', 'Christian vocal artists': 'https://en.wikipedia.org/wiki/List_of_Christian_vocal_artists', 'Christian worship music artists': 'https://en.wikipedia.org/wiki/List_of_Christian_worship_music_artists', 'cool jazz and West Coast jazz musicians': 'https://en.wikipedia.org/wiki/List_of_cool_jazz_and_West_Coast_jazz_musicians', 'country blues musicians': 'https://en.wikipedia.org/wiki/List_of_country_blues_musicians', 'country music performers': 'https://en.wikipedia.org/wiki/List_of_country_music_performers', 'country performers by era': 'https://en.wikipedia.org/wiki/List_of_country_performers_by_era', 'country rock musicians': 'https://en.wikipedia.org/wiki/List_of_country_rock_musicians', 'crooners': 'https://en.wikipedia.org/wiki/List_of_crooners', 'dance-pop artists': 'https://en.wikipedia.org/wiki/List_of_dance-pop_artists', 'dance-punk artists': 'https://en.wikipedia.org/wiki/List_of_dance-punk_artists', 'dance-rock artists': 'https://en.wikipedia.org/wiki/List_of_dance-rock_artists', 'dark ambient artists': 'https://en.wikipedia.org/wiki/List_of_dark_ambient_artists', 'dark cabaret artists': 'https://en.wikipedia.org/wiki/List_of_dark_cabaret_artists', 'dark rock bands': 'https://en.wikipedia.org/wiki/List_of_dark_rock_bands', 'death metal bands': 'https://en.wikipedia.org/wiki/List_of_death_metal_bands', 'deathcore artists': 'https://en.wikipedia.org/wiki/List_of_deathcore_artists', 'Delta blues musicians': 'https://en.wikipedia.org/wiki/List_of_Delta_blues_musicians', 'disco artists': 'https://en.wikipedia.org/wiki/List_of_disco_artists', 'doo-wop musicians': 'https://en.wikipedia.org/wiki/List_of_doo-wop_musicians', 'doom metal bands': 'https://en.wikipedia.org/wiki/List_of_doom_metal_bands', 'downtempo artists': 'https://en.wikipedia.org/wiki/List_of_downtempo_artists', 'dream pop artists': 'https://en.wikipedia.org/wiki/List_of_dream_pop_artists', 'drone artists': 'https://en.wikipedia.org/wiki/List_of_drone_artists', 'dub artists': 'https://en.wikipedia.org/wiki/List_of_dub_artists', 'dubstep musicians': 'https://en.wikipedia.org/wiki/List_of_dubstep_musicians', 'electric blues musicians': 'https://en.wikipedia.org/wiki/List_of_electric_blues_musicians', 'electro house artists': 'https://en.wikipedia.org/wiki/List_of_electro_house_artists', 'electro-industrial bands': 'https://en.wikipedia.org/wiki/List_of_electro-industrial_bands', 'electroclash bands and artists': 'https://en.wikipedia.org/wiki/List_of_electroclash_bands_and_artists', 'emo artists': 'https://en.wikipedia.org/wiki/List_of_emo_artists', 'experimental musicians': 'https://en.wikipedia.org/wiki/List_of_experimental_musicians', 'Eurodisco artists': 'https://en.wikipedia.org/wiki/List_of_Eurodisco_artists', 'Eurobeat artists': 'https://en.wikipedia.org/wiki/List_of_Eurobeat_artists', 'Eurodance artists': 'https://en.wikipedia.org/wiki/List_of_Eurodance_artists', 'Europop artists': 'https://en.wikipedia.org/wiki/List_of_Europop_artists', 'fado musicians': 'https://en.wikipedia.org/wiki/List_of_fado_musicians', 'female heavy metal singers': 'https://en.wikipedia.org/wiki/List_of_female_heavy_metal_singers', 'female rock singers': 'https://en.wikipedia.org/wiki/List_of_female_rock_singers', 'folk musicians': 'https://en.wikipedia.org/wiki/List_of_folk_musicians', 'folk metal bands': 'https://en.wikipedia.org/wiki/List_of_folk_metal_bands', 'folk rock artists': 'https://en.wikipedia.org/wiki/List_of_folk_rock_artists', 'free funk musicians': 'https://en.wikipedia.org/wiki/List_of_free_funk_musicians', 'free improvising musicians and groups': 'https://en.wikipedia.org/wiki/List_of_free_improvising_musicians_and_groups', 'funk musicians': 'https://en.wikipedia.org/wiki/List_of_funk_musicians', 'funk rock bands': 'https://en.wikipedia.org/wiki/List_of_funk_rock_bands', 'G-funk musicians': 'https://en.wikipedia.org/wiki/List_of_G-funk_musicians', 'gangsta rap artists': 'https://en.wikipedia.org/wiki/List_of_gangsta_rap_artists', 'garage rock bands': 'https://en.wikipedia.org/wiki/List_of_garage_rock_bands', 'glam metal bands and artists': 'https://en.wikipedia.org/wiki/List_of_glam_metal_bands_and_artists', 'glam punk artists': 'https://en.wikipedia.org/wiki/List_of_glam_punk_artists', 'glam rock artists': 'https://en.wikipedia.org/wiki/List_of_glam_rock_artists', 'gospel blues musicians': 'https://en.wikipedia.org/wiki/List_of_gospel_blues_musicians', 'gospel musicians': 'https://en.wikipedia.org/wiki/List_of_gospel_musicians', 'gothic metal bands': 'https://en.wikipedia.org/wiki/List_of_gothic_metal_bands', 'gothic rock artists': 'https://en.wikipedia.org/wiki/List_of_gothic_rock_artists', 'grindcore bands': 'https://en.wikipedia.org/wiki/List_of_grindcore_bands', 'groove metal bands': 'https://en.wikipedia.org/wiki/List_of_groove_metal_bands', 'hard rock musicians (A–M)': 'https://en.wikipedia.org/wiki/List_of_hard_rock_musicians_(A%E2%80%93M)', 'hard rock musicians (N–Z)': 'https://en.wikipedia.org/wiki/List_of_hard_rock_musicians_(N%E2%80%93Z)', 'hardcore punk bands': 'https://en.wikipedia.org/wiki/List_of_hardcore_punk_bands', 'heavy metal bands': 'https://en.wikipedia.org/wiki/List_of_heavy_metal_bands', 'Hi-NRG artists and songs': 'https://en.wikipedia.org/wiki/List_of_Hi-NRG_artists_and_songs', 'hip hop groups': 'https://en.wikipedia.org/wiki/List_of_hip_hop_groups', 'hip hop musicians': 'https://en.wikipedia.org/wiki/List_of_hip_hop_musicians', 'horror punk bands': 'https://en.wikipedia.org/wiki/List_of_horror_punk_bands', 'house music artists': 'https://en.wikipedia.org/wiki/List_of_house_music_artists', 'indie pop artists': 'https://en.wikipedia.org/wiki/List_of_indie_pop_artists', 'indie rock musicians': 'https://en.wikipedia.org/wiki/List_of_indie_rock_musicians', 'Indo pop musicians': 'https://en.wikipedia.org/wiki/List_of_Indonesian_pop_musicians', 'industrial metal bands': 'https://en.wikipedia.org/wiki/List_of_industrial_metal_bands', 'industrial music bands': 'https://en.wikipedia.org/wiki/List_of_industrial_music_bands', 'intelligent dance music artists': 'https://en.wikipedia.org/wiki/List_of_intelligent_dance_music_artists', 'Italo disco artists and songs': 'https://en.wikipedia.org/wiki/List_of_Italo_disco_artists_and_songs', 'J-pop artists': 'https://en.wikipedia.org/wiki/List_of_J-pop_artists', 'Japanoise artists': 'https://en.wikipedia.org/wiki/List_of_Japanoise_artists', 'jazz fusion musicians': 'https://en.wikipedia.org/wiki/List_of_jazz_fusion_musicians', 'jazz musicians': 'https://en.wikipedia.org/wiki/List_of_jazz_musicians', 'jump blues musicians': 'https://en.wikipedia.org/wiki/List_of_jump_blues_musicians', 'jungle and drum and bass artists': 'https://en.wikipedia.org/wiki/List_of_jungle_and_drum_and_bass_artists', 'K-pop artists': 'https://en.wikipedia.org/wiki/List_of_K-pop_artists', 'klezmer musicians': 'https://en.wikipedia.org/wiki/List_of_klezmer_musicians', 'Latin American rock musicians': 'https://en.wikipedia.org/wiki/List_of_Latin_American_rock_musicians', 'Latin freestyle musicians and songs': 'https://en.wikipedia.org/wiki/List_of_Latin_freestyle_musicians_and_songs', 'Latin pop artists': 'https://en.wikipedia.org/wiki/List_of_Latin_pop_artists', 'lo-fi bands': 'https://en.wikipedia.org/wiki/List_of_lo-fi_bands', 'lovers rock artists': 'https://en.wikipedia.org/wiki/List_of_lovers_rock_artists', 'mainstream rock performers': 'https://en.wikipedia.org/wiki/List_of_mainstream_rock_performers', 'maritime music performers': 'https://en.wikipedia.org/wiki/List_of_maritime_music_performers', 'math rock groups': 'https://en.wikipedia.org/wiki/List_of_math_rock_groups', 'mathcore bands': 'https://en.wikipedia.org/wiki/List_of_mathcore_bands', 'merengue musicians': 'https://en.wikipedia.org/wiki/List_of_merengue_musicians', 'metalcore bands': 'https://en.wikipedia.org/wiki/List_of_metalcore_bands', 'melodic death metal bands': 'https://en.wikipedia.org/wiki/List_of_melodic_death_metal_bands', 'minimalist artists': 'https://en.wikipedia.org/wiki/List_of_minimalist_artists', 'new-age music artists': 'https://en.wikipedia.org/wiki/List_of_new-age_music_artists', 'new jack swing artists': 'https://en.wikipedia.org/wiki/List_of_new_jack_swing_artists', 'new wave artists and bands': 'https://en.wikipedia.org/wiki/List_of_new_wave_artists_and_bands', 'new wave of American heavy metal bands': 'https://en.wikipedia.org/wiki/List_of_new_wave_of_American_heavy_metal_bands', 'new wave of British heavy metal bands': 'https://en.wikipedia.org/wiki/List_of_new_wave_of_British_heavy_metal_bands', 'noise musicians': 'https://en.wikipedia.org/wiki/List_of_noise_musicians', 'nu metal bands': 'https://en.wikipedia.org/wiki/List_of_nu_metal_bands', 'Oi! bands': 'https://en.wikipedia.org/wiki/List_of_Oi!_bands', 'operatic pop artists': 'https://en.wikipedia.org/wiki/List_of_operatic_pop_artists', 'Piedmont blues musicians': 'https://en.wikipedia.org/wiki/List_of_Piedmont_blues_musicians', 'political hip hop artists': 'https://en.wikipedia.org/wiki/List_of_political_hip_hop_artists', 'polka artists': 'https://en.wikipedia.org/wiki/List_of_polka_artists', 'pop punk bands': 'https://en.wikipedia.org/wiki/List_of_pop_punk_bands', 'post-disco artists and songs': 'https://en.wikipedia.org/wiki/List_of_post-disco_artists_and_songs', 'post-dubstep musicians': 'https://en.wikipedia.org/wiki/List_of_post-dubstep_musicians', 'post-grunge bands': 'https://en.wikipedia.org/wiki/List_of_post-grunge_bands', 'post-hardcore bands': 'https://en.wikipedia.org/wiki/List_of_post-hardcore_bands', 'post-metal bands': 'https://en.wikipedia.org/wiki/List_of_post-metal_bands', 'post-punk bands': 'https://en.wikipedia.org/wiki/List_of_post-punk_bands', 'post-punk revival bands': 'https://en.wikipedia.org/wiki/List_of_post-punk_revival_bands', 'post-rock bands': 'https://en.wikipedia.org/wiki/List_of_post-rock_bands', 'power metal bands': 'https://en.wikipedia.org/wiki/List_of_power_metal_bands', 'power pop artists and songs': 'https://en.wikipedia.org/wiki/List_of_power_pop_artists_and_songs', 'progressive house artists': 'https://en.wikipedia.org/wiki/List_of_progressive_house_artists', 'progressive metal artists': 'https://en.wikipedia.org/wiki/List_of_progressive_metal_artists', 'progressive rock artists': 'https://en.wikipedia.org/wiki/List_of_progressive_rock_artists', 'progressive rock supergroups': 'https://en.wikipedia.org/wiki/List_of_progressive_rock_supergroups', 'psychedelic folk artists': 'https://en.wikipedia.org/wiki/List_of_psychedelic_folk_artists', 'psychedelic pop artists': 'https://en.wikipedia.org/wiki/List_of_psychedelic_pop_artists', 'psychedelic rock artists': 'https://en.wikipedia.org/wiki/List_of_psychedelic_rock_artists', 'psychobilly bands': 'https://en.wikipedia.org/wiki/List_of_psychobilly_bands', 'punk blues musicians and bands': 'https://en.wikipedia.org/wiki/List_of_punk_blues_musicians_and_bands', 'punk rock bands, 0–K': 'https://en.wikipedia.org/wiki/List_of_punk_rock_bands,_0%E2%80%93K', 'punk rock bands, L–Z': 'https://en.wikipedia.org/wiki/List_of_punk_rock_bands,_L%E2%80%93Z', '1970s punk rock musicians': 'https://en.wikipedia.org/wiki/List_of_1970s_punk_rock_musicians', 'musicians in the second wave of punk rock': 'https://en.wikipedia.org/wiki/List_of_musicians_in_the_second_wave_of_punk_rock', 'R&B musicians': 'https://en.wikipedia.org/wiki/List_of_R%26B_musicians', 'ragtime musicians': 'https://en.wikipedia.org/wiki/List_of_ragtime_musicians', 'raï musicians': 'https://en.wikipedia.org/wiki/List_of_ra%C3%AF_musicians', 'rap rock bands': 'https://en.wikipedia.org/wiki/List_of_rap_rock_bands', 'reggae musicians': 'https://en.wikipedia.org/wiki/List_of_reggae_musicians', 'reggae fusion artists': 'https://en.wikipedia.org/wiki/List_of_reggae_fusion_artists', 'reggae rock artists': 'https://en.wikipedia.org/wiki/List_of_reggae_rock_artists', 'reggaeton musicians': 'https://en.wikipedia.org/wiki/List_of_reggaeton_musicians', 'riot grrrl bands': 'https://en.wikipedia.org/wiki/List_of_riot_grrrl_bands', 'rock and roll artists': 'https://en.wikipedia.org/wiki/List_of_rock_and_roll_artists', 'rocksteady musicians': 'https://en.wikipedia.org/wiki/List_of_rocksteady_musicians', 'roots reggae artists': 'https://en.wikipedia.org/wiki/List_of_roots_reggae_artists', 'roots rock bands and musicians': 'https://en.wikipedia.org/wiki/List_of_roots_rock_bands_and_musicians', 'rappers (female)': 'https://en.wikipedia.org/wiki/List_of_rappers_(female)', 'scat singers': 'https://en.wikipedia.org/wiki/List_of_scat_singers', 'screamo bands': 'https://en.wikipedia.org/wiki/List_of_screamo_bands', 'shoegazing musicians': 'https://en.wikipedia.org/wiki/List_of_shoegazing_musicians', 'ska musicians': 'https://en.wikipedia.org/wiki/List_of_ska_musicians', 'smooth jazz musicians': 'https://en.wikipedia.org/wiki/List_of_smooth_jazz_musicians', 'soft rock artists and songs': 'https://en.wikipedia.org/wiki/List_of_soft_rock_artists_and_songs', 'soul musicians': 'https://en.wikipedia.org/wiki/List_of_soul_musicians', 'soul-blues musicians': 'https://en.wikipedia.org/wiki/List_of_soul-blues_musicians', 'soul jazz musicians': 'https://en.wikipedia.org/wiki/List_of_soul_jazz_musicians', 'southern rock bands': 'https://en.wikipedia.org/wiki/List_of_southern_rock_bands', 'speed metal bands': 'https://en.wikipedia.org/wiki/List_of_speed_metal_bands', 'street punk bands': 'https://en.wikipedia.org/wiki/List_of_street_punk_bands', 'surf musicians': 'https://en.wikipedia.org/wiki/List_of_surf_musicians', 'swing musicians': 'https://en.wikipedia.org/wiki/List_of_swing_musicians', 'symphonic metal bands': 'https://en.wikipedia.org/wiki/List_of_symphonic_metal_bands', 'synth-pop artists': 'https://en.wikipedia.org/wiki/List_of_synth-pop_artists', 'technical death metal bands': 'https://en.wikipedia.org/wiki/List_of_technical_death_metal_bands', 'Texas blues musicians': 'https://en.wikipedia.org/wiki/List_of_Texas_blues_musicians', 'Thai pop artists': 'https://en.wikipedia.org/wiki/List_of_Thai_pop_artists', 'thrash metal bands': 'https://en.wikipedia.org/wiki/List_of_thrash_metal_bands', 'thrashcore bands': 'https://en.wikipedia.org/wiki/List_of_thrashcore_bands', 'trip hop artists': 'https://en.wikipedia.org/wiki/List_of_trip_hop_artists', 'UK garage artists': 'https://en.wikipedia.org/wiki/List_of_UK_garage_artists', 'video game musicians': 'https://en.wikipedia.org/wiki/List_of_video_game_musicians', 'Viking metal bands': 'https://en.wikipedia.org/wiki/List_of_Viking_metal_bands', 'vocal groups': 'https://en.wikipedia.org/wiki/List_of_vocal_groups', 'vocal trance artists': 'https://en.wikipedia.org/wiki/List_of_vocal_trance_artists', 'West Coast blues musicians': 'https://en.wikipedia.org/wiki/List_of_West_Coast_blues_musicians', 'hip hop artists': 'https://en.wikipedia.org/wiki/List_of_hip_hop_artists', 'accordionists': 'https://en.wikipedia.org/wiki/List_of_accordionists', 'banjo players': 'https://en.wikipedia.org/wiki/List_of_banjo_players', 'jazz banjoists': 'https://en.wikipedia.org/wiki/List_of_jazz_banjoists', 'beatboxers': 'https://en.wikipedia.org/wiki/List_of_beatboxers', 'cellists': 'https://en.wikipedia.org/wiki/List_of_cellists', 'clarinetists': 'https://en.wikipedia.org/wiki/List_of_clarinetists', 'contemporary classical double bass players': 'https://en.wikipedia.org/wiki/List_of_contemporary_classical_double_bass_players', 'historical classical double bass players': 'https://en.wikipedia.org/wiki/List_of_historical_classical_double_bass_players', 'jazz bassists': 'https://en.wikipedia.org/wiki/List_of_jazz_bassists', 'drummers': 'https://en.wikipedia.org/wiki/List_of_drummers', 'female drummers': 'https://en.wikipedia.org/wiki/List_of_female_drummers', 'jazz drummers': 'https://en.wikipedia.org/wiki/List_of_jazz_drummers', 'Appalachian dulcimer players': 'https://en.wikipedia.org/wiki/List_of_Appalachian_dulcimer_players', 'hammered dulcimer players': 'https://en.wikipedia.org/wiki/List_of_hammered_dulcimer_players', 'flautists': 'https://en.wikipedia.org/wiki/List_of_flautists', 'guitarists': 'https://en.wikipedia.org/wiki/List_of_guitarists', 'bass guitarists': 'https://en.wikipedia.org/wiki/List_of_bass_guitarists', 'classical guitarists': 'https://en.wikipedia.org/wiki/List_of_classical_guitarists', 'jazz guitarists': 'https://en.wikipedia.org/wiki/List_of_jazz_guitarists', 'lead guitarists': 'https://en.wikipedia.org/wiki/List_of_lead_guitarists', 'rhythm guitarists': 'https://en.wikipedia.org/wiki/List_of_rhythm_guitarists', 'slide guitarists': 'https://en.wikipedia.org/wiki/List_of_slide_guitarists', 'harmonicists': 'https://en.wikipedia.org/wiki/List_of_harmonicists', 'harpists': 'https://en.wikipedia.org/wiki/List_of_harpists', 'classical harpists': 'https://en.wikipedia.org/wiki/List_of_classical_harpists', 'harpsichordists': 'https://en.wikipedia.org/wiki/List_of_harpsichordists', 'horn players': 'https://en.wikipedia.org/wiki/List_of_horn_players', 'organists': 'https://en.wikipedia.org/wiki/List_of_organists', 'jazz organists': 'https://en.wikipedia.org/wiki/List_of_jazz_organists', 'percussionists': 'https://en.wikipedia.org/wiki/List_of_percussionists', 'jazz percussionists': 'https://en.wikipedia.org/wiki/List_of_jazz_percussionists', 'classical pianists': 'https://en.wikipedia.org/wiki/List_of_classical_pianists', 'jazz pianists': 'https://en.wikipedia.org/wiki/List_of_jazz_pianists', 'pop and rock pianists': 'https://en.wikipedia.org/wiki/List_of_pop_and_rock_pianists', 'pipe bands': 'https://en.wikipedia.org/wiki/List_of_pipe_bands', 'saxophonists': 'https://en.wikipedia.org/wiki/List_of_saxophonists', 'jazz saxophonists': 'https://en.wikipedia.org/wiki/List_of_jazz_saxophonists', 'classical trombonists': 'https://en.wikipedia.org/wiki/List_of_classical_trombonists', 'jazz trombonists': 'https://en.wikipedia.org/wiki/List_of_jazz_trombonists', 'trumpeters': 'https://en.wikipedia.org/wiki/List_of_trumpeters', 'jazz trumpeters': 'https://en.wikipedia.org/wiki/List_of_jazz_trumpeters', 'tuba players': 'https://en.wikipedia.org/wiki/List_of_tuba_players', 'vibraphonists': 'https://en.wikipedia.org/wiki/List_of_vibraphonists', 'jazz vibraphonists': 'https://en.wikipedia.org/wiki/List_of_jazz_vibraphonists', 'violinists': 'https://en.wikipedia.org/wiki/Lists_of_violinists', 'classical violinists': 'https://en.wikipedia.org/wiki/List_of_classical_violinists', 'electric violinists': 'https://en.wikipedia.org/wiki/List_of_electric_violinists', 'female violinists': 'https://en.wikipedia.org/wiki/List_of_female_violinists', 'fiddlers': 'https://en.wikipedia.org/wiki/List_of_fiddlers', 'Indian violinists': 'https://en.wikipedia.org/wiki/List_of_Indian_violinists', 'jazz violinists': 'https://en.wikipedia.org/wiki/List_of_jazz_violinists', 'Persian violinists': 'https://en.wikipedia.org/wiki/List_of_Persian_violinists', 'popular music violinists': 'https://en.wikipedia.org/wiki/List_of_popular_music_violinists', 'violinist/composers': 'https://en.wikipedia.org/wiki/List_of_violinist/composers', 'violists': 'https://en.wikipedia.org/wiki/List_of_violists', 'African musicians': 'https://en.wikipedia.org/wiki/List_of_African_musicians', 'Egyptian composers': 'https://en.wikipedia.org/wiki/List_of_Egyptian_composers', 'Ghanaian musicians': 'https://en.wikipedia.org/wiki/List_of_Ghanaian_musicians', 'South African musicians': 'https://en.wikipedia.org/wiki/List_of_South_African_musicians', 'Nigerian musicians': 'https://en.wikipedia.org/wiki/List_of_Nigerian_musicians', 'Ugandan musicians': 'https://en.wikipedia.org/wiki/List_of_Ugandan_musicians', 'Afghan singers': 'https://en.wikipedia.org/wiki/List_of_Afghan_singers', 'Azerbaijani composers': 'https://en.wikipedia.org/wiki/List_of_Azerbaijani_composers', 'Azerbaijani opera singers': 'https://en.wikipedia.org/wiki/List_of_Azerbaijani_opera_singers', 'Chinese composers': 'https://en.wikipedia.org/wiki/List_of_Chinese_composers', 'Chinese musicians': 'https://en.wikipedia.org/wiki/List_of_Chinese_musicians', 'Philippine-based music groups': 'https://en.wikipedia.org/wiki/List_of_Philippine-based_music_groups', 'Indonesian pop musicians': 'https://en.wikipedia.org/wiki/List_of_Indonesian_pop_musicians', 'Indonesian musicians and musical groups': 'https://en.wikipedia.org/wiki/List_of_Indonesian_musicians_and_musical_groups', 'Iranian composers': 'https://en.wikipedia.org/wiki/List_of_Iranian_composers', 'Iranian musicians': 'https://en.wikipedia.org/wiki/List_of_Iranian_musicians', 'Iranian singers': 'https://en.wikipedia.org/wiki/List_of_Iranian_singers', 'Iranian hip hop artists': 'https://en.wikipedia.org/wiki/List_of_Iranian_hip_hop_artists', 'Israeli classical composers': 'https://en.wikipedia.org/wiki/List_of_Israeli_classical_composers', 'Israeli musical artists': 'https://en.wikipedia.org/wiki/List_of_Israeli_musical_artists', 'Indian composers': 'https://en.wikipedia.org/wiki/List_of_Indian_composers', 'Indian film music directors': 'https://en.wikipedia.org/wiki/List_of_Indian_film_music_directors', 'Indian playback singers': 'https://en.wikipedia.org/wiki/List_of_Indian_playback_singers', 'bands from Delhi': 'https://en.wikipedia.org/wiki/List_of_bands_from_Delhi', 'Japanese musicians': 'https://en.wikipedia.org/wiki/List_of_musical_artists_from_Japan', 'Japanese hip hop musicians': 'https://en.wikipedia.org/wiki/List_of_Japanese_hip_hop_musicians', 'musical artists from Japan': 'https://en.wikipedia.org/wiki/List_of_musical_artists_from_Japan', 'Pakistani ghazal singers': 'https://en.wikipedia.org/wiki/List_of_Pakistani_ghazal_singers', 'Pakistani musicians': 'https://en.wikipedia.org/wiki/List_of_Pakistani_musicians', 'Pakistani musical groups': 'https://en.wikipedia.org/wiki/List_of_Pakistani_musical_groups', 'Pakistani pop singers': 'https://en.wikipedia.org/wiki/List_of_Pakistani_pop_singers', 'Pakistani qawwali singers': 'https://en.wikipedia.org/wiki/List_of_Pakistani_qawwali_singers', 'South Korean idol groups': 'https://en.wikipedia.org/wiki/List_of_South_Korean_idol_groups', 'South Korean idol groups (1990s)': 'https://en.wikipedia.org/wiki/List_of_South_Korean_idol_groups_(1990s)', 'South Korean idol groups (2000s)': 'https://en.wikipedia.org/wiki/List_of_South_Korean_idol_groups_(2000s)', 'South Korean idol groups (2010s)': 'https://en.wikipedia.org/wiki/List_of_South_Korean_idol_groups_(2010s)', 'South Korean musicians': 'https://en.wikipedia.org/wiki/List_of_South_Korean_musicians', 'Sri Lankan musicians': 'https://en.wikipedia.org/wiki/List_of_Sri_Lankan_musicians', 'Austrian composers': 'https://en.wikipedia.org/wiki/List_of_Austrian_composers', 'Belarusian musical groups': 'https://en.wikipedia.org/wiki/List_of_Belarusian_musical_groups', 'Belarusian musicians': 'https://en.wikipedia.org/wiki/List_of_Belarusian_musicians', 'Belgian bands and artists': 'https://en.wikipedia.org/wiki/List_of_Belgian_bands_and_artists', 'music artists and bands from England': 'https://en.wikipedia.org/wiki/List_of_music_artists_and_bands_from_England', 'bands from Bristol': 'https://en.wikipedia.org/wiki/List_of_bands_from_Bristol', 'bands and artists from Merseyside': 'https://en.wikipedia.org/wiki/List_of_bands_and_artists_from_Merseyside', 'bands originating in Leeds': 'https://en.wikipedia.org/wiki/List_of_bands_originating_in_Leeds', 'Cornish musicians': 'https://en.wikipedia.org/wiki/List_of_Cornish_musicians', 'music artists and bands from Manchester': 'https://en.wikipedia.org/wiki/List_of_music_artists_and_bands_from_Manchester', 'bands from Glasgow': 'https://en.wikipedia.org/wiki/List_of_bands_from_Glasgow', 'Scottish musicians': 'https://en.wikipedia.org/wiki/List_of_Scottish_musicians', 'Welsh musicians': 'https://en.wikipedia.org/wiki/List_of_Welsh_musicians', 'British classical composers': 'https://en.wikipedia.org/wiki/List_of_British_classical_composers', 'British Invasion artists': 'https://en.wikipedia.org/wiki/List_of_British_Invasion_artists', 'punk bands from the United Kingdom': 'https://en.wikipedia.org/wiki/List_of_punk_bands_from_the_United_Kingdom', 'UK noise musicians': 'https://en.wikipedia.org/wiki/List_of_UK_noise_musicians', 'Bulgarian musicians and singers': 'https://en.wikipedia.org/wiki/List_of_Bulgarian_musicians_and_singers', 'Czech musical groups': 'https://en.wikipedia.org/wiki/List_of_Czech_musical_groups', 'Danish composers': 'https://en.wikipedia.org/wiki/List_of_Danish_composers', 'Danish musicians': 'https://en.wikipedia.org/wiki/List_of_Danish_musicians', 'Dutch composers': 'https://en.wikipedia.org/wiki/List_of_Dutch_composers', 'Dutch hip hop musicians': 'https://en.wikipedia.org/wiki/List_of_Dutch_hip_hop_musicians', 'Dutch musicians': 'https://en.wikipedia.org/wiki/List_of_Dutch_musicians', 'bands from Finland': 'https://en.wikipedia.org/wiki/List_of_bands_from_Finland', 'Finnish jazz musicians': 'https://en.wikipedia.org/wiki/List_of_Finnish_jazz_musicians', 'Finnish composers': 'https://en.wikipedia.org/wiki/List_of_Finnish_composers', 'Finnish musicians': 'https://en.wikipedia.org/wiki/List_of_Finnish_musicians', 'Finnish singers': 'https://en.wikipedia.org/wiki/List_of_Finnish_singers', 'French composers': 'https://en.wikipedia.org/wiki/List_of_French_composers', 'French singers': 'https://en.wikipedia.org/wiki/List_of_French_singers', 'German composers': 'https://en.wikipedia.org/wiki/List_of_German_composers', 'German musicians': 'https://en.wikipedia.org/wiki/List_of_German_musicians', 'Greek composers': 'https://en.wikipedia.org/wiki/List_of_Greek_composers', 'Greek musical artists': 'https://en.wikipedia.org/wiki/List_of_Greek_musical_artists', 'bands from Iceland': 'https://en.wikipedia.org/wiki/List_of_bands_from_Iceland', 'Chronological list of Italian classical composers': 'https://en.wikipedia.org/wiki/Chronological_list_of_Italian_classical_composers', 'Italian composers': 'https://en.wikipedia.org/wiki/List_of_Italian_composers', 'Norwegian musicians': 'https://en.wikipedia.org/wiki/List_of_Norwegian_musicians', 'Polish musicians and musical groups': 'https://en.wikipedia.org/wiki/List_of_Polish_musicians_and_musical_groups', 'Portuguese musicians': 'https://en.wikipedia.org/wiki/List_of_Portuguese_musicians', 'Portuguese singers': 'https://en.wikipedia.org/wiki/List_of_Portuguese_singers', 'Romanian composers': 'https://en.wikipedia.org/wiki/List_of_Romanian_composers', 'Romanian musicians': 'https://en.wikipedia.org/wiki/List_of_Romanian_musicians', 'Romanian singers': 'https://en.wikipedia.org/wiki/List_of_Romanian_singers', 'Russian composers': 'https://en.wikipedia.org/wiki/List_of_Russian_composers', 'Russian opera singers': 'https://en.wikipedia.org/wiki/List_of_Russian_opera_singers', 'Serbian musicians': 'https://en.wikipedia.org/wiki/List_of_Serbian_musicians', 'Slovenian musicians': 'https://en.wikipedia.org/wiki/List_of_Slovenian_musicians', 'bands from Spain': 'https://en.wikipedia.org/wiki/List_of_bands_from_Spain', 'Spanish musicians': 'https://en.wikipedia.org/wiki/List_of_Spanish_musicians', 'bands from Gothenburg': 'https://en.wikipedia.org/wiki/List_of_bands_from_Gothenburg', 'In Flames band members': 'https://en.wikipedia.org/wiki/List_of_In_Flames_band_members', 'Swedes in music': 'https://en.wikipedia.org/wiki/List_of_Swedes_in_music', 'Swedish death metal bands': 'https://en.wikipedia.org/wiki/List_of_Swedish_death_metal_bands', 'Swedish hip hop musicians': 'https://en.wikipedia.org/wiki/List_of_Swedish_hip_hop_musicians', 'Turkish musicians': 'https://en.wikipedia.org/wiki/List_of_Turkish_musicians', 'Turkish pop musicians': 'https://en.wikipedia.org/wiki/List_of_Turkish_pop_musicians', 'Ukrainian opera singers': 'https://en.wikipedia.org/wiki/List_of_Ukrainian_opera_singers', 'bands from Los Angeles': 'https://en.wikipedia.org/wiki/List_of_bands_from_Los_Angeles', 'bands from the San Francisco Bay Area': 'https://en.wikipedia.org/wiki/List_of_bands_from_the_San_Francisco_Bay_Area', 'Los Angeles rappers': 'https://en.wikipedia.org/wiki/List_of_Los_Angeles_rappers', 'music directors of the Ojai Music Festival': 'https://en.wikipedia.org/wiki/List_of_music_directors_of_the_Ojai_Music_Festival', 'musicians from the Inland Empire': 'https://en.wikipedia.org/wiki/List_of_musicians_from_the_Inland_Empire', 'musicians from Chicago': 'https://en.wikipedia.org/wiki/List_of_musicians_from_Chicago', 'Maryland music groups': 'https://en.wikipedia.org/wiki/List_of_Maryland_music_groups', 'Maryland music people': 'https://en.wikipedia.org/wiki/List_of_Maryland_music_people', 'bands formed in New York City': 'https://en.wikipedia.org/wiki/List_of_bands_formed_in_New_York_City', 'hip hop musicians from New York City': 'https://en.wikipedia.org/wiki/List_of_hip_hop_musicians_from_New_York_City', 'New York hardcore bands': 'https://en.wikipedia.org/wiki/List_of_New_York_hardcore_bands', 'Houston rappers': 'https://en.wikipedia.org/wiki/List_of_Houston_rappers', 'musicians from Denton, Texas': 'https://en.wikipedia.org/wiki/List_of_musicians_from_Denton,_Texas', 'bands from Lincoln, Nebraska': 'https://en.wikipedia.org/wiki/List_of_bands_from_Lincoln,_Nebraska', 'Chicago hardcore punk bands': 'https://en.wikipedia.org/wiki/List_of_Chicago_hardcore_punk_bands', 'hip hop musicians from Atlanta': 'https://en.wikipedia.org/wiki/List_of_hip_hop_musicians_from_Atlanta', 'musicians from Seattle': 'https://en.wikipedia.org/wiki/List_of_musicians_from_Seattle', 'Utah musical groups': 'https://en.wikipedia.org/wiki/List_of_Utah_musical_groups', 'American folk musicians in Washington': 'https://en.wikipedia.org/wiki/List_of_American_folk_musicians_in_Washington', 'American death metal bands': 'https://en.wikipedia.org/wiki/List_of_American_death_metal_bands', 'American female country singers': 'https://en.wikipedia.org/wiki/List_of_American_female_country_singers', 'American grunge bands': 'https://en.wikipedia.org/wiki/List_of_American_grunge_bands', 'The Minus 5 members': 'https://en.wikipedia.org/wiki/List_of_The_Minus_5_members', 'Native American musicians': 'https://en.wikipedia.org/wiki/List_of_Native_American_musicians', 'one-hit wonders in the United States': 'https://en.wikipedia.org/wiki/List_of_one-hit_wonders_in_the_United_States', 'symphony orchestras in the United States': 'https://en.wikipedia.org/wiki/List_of_symphony_orchestras_in_the_United_States', 'bands from Canada': 'https://en.wikipedia.org/wiki/List_of_bands_from_Canada', 'Canadian composers': 'https://en.wikipedia.org/wiki/List_of_Canadian_composers', 'Canadian musicians': 'https://en.wikipedia.org/wiki/List_of_Canadian_musicians', 'bands from British Columbia': 'https://en.wikipedia.org/wiki/List_of_bands_from_British_Columbia', 'musicians from British Columbia': 'https://en.wikipedia.org/wiki/List_of_musicians_from_British_Columbia', 'Winnipeg musicians': 'https://en.wikipedia.org/wiki/List_of_Winnipeg_musicians', 'musical groups from Halifax, Nova Scotia': 'https://en.wikipedia.org/wiki/List_of_musical_groups_from_Halifax,_Nova_Scotia', 'Anglo-Quebecer musicians': 'https://en.wikipedia.org/wiki/List_of_Anglo-Quebecer_musicians', 'Montreal music groups': 'https://en.wikipedia.org/wiki/List_of_Montreal_music_groups', 'musicians from Quebec': 'https://en.wikipedia.org/wiki/List_of_musicians_from_Quebec', 'Jamaican musicians': 'https://en.wikipedia.org/wiki/List_of_Jamaican_musicians', 'Argentine musicians': 'https://en.wikipedia.org/wiki/List_of_Argentine_musicians', 'Ecuadorian musicians': 'https://en.wikipedia.org/wiki/List_of_Ecuadorian_musicians', 'Brazilian composers': 'https://en.wikipedia.org/wiki/List_of_Brazilian_composers', 'Brazilian musicians': 'https://en.wikipedia.org/wiki/List_of_Brazilian_musicians', 'Australian composers': 'https://en.wikipedia.org/wiki/List_of_Australian_composers', 'Australian female composers': 'https://en.wikipedia.org/wiki/List_of_Australian_female_composers', 'Indigenous Australian musicians': 'https://en.wikipedia.org/wiki/List_of_Indigenous_Australian_musicians', 'New Zealand musicians': 'https://en.wikipedia.org/wiki/List_of_New_Zealand_musicians', 'all-female bands': 'https://en.wikipedia.org/wiki/List_of_all-female_bands', 'anarchist musicians': 'https://en.wikipedia.org/wiki/List_of_anarchist_musicians', 'atheists in music': 'https://en.wikipedia.org/wiki/List_of_atheists_in_music', 'band name etymologies': 'https://en.wikipedia.org/wiki/List_of_band_name_etymologies', "bands named after other performers' songs": 'https://en.wikipedia.org/wiki/List_of_bands_named_after_other_performers%27_songs', 'best-selling boy bands': 'https://en.wikipedia.org/wiki/Boy_band#Best-selling_boy_bands', 'best-selling girl groups': 'https://en.wikipedia.org/wiki/List_of_best-selling_girl_groups', 'best-selling music artists': 'https://en.wikipedia.org/wiki/List_of_best-selling_music_artists', 'child music prodigies': 'https://en.wikipedia.org/wiki/List_of_child_music_prodigies', 'club DJs': 'https://en.wikipedia.org/wiki/List_of_club_DJs', 'deaths in rock and roll': 'https://en.wikipedia.org/wiki/List_of_deaths_in_rock_and_roll', 'girl groups': 'https://en.wikipedia.org/wiki/List_of_girl_groups', 'honorifics given to artists in popular music': 'https://en.wikipedia.org/wiki/Honorific_nicknames_in_popular_music', 'instrumental bands': 'https://en.wikipedia.org/wiki/List_of_instrumental_bands', 'jam bands': 'https://en.wikipedia.org/wiki/List_of_jam_bands', 'lead vocalists': 'https://en.wikipedia.org/wiki/List_of_lead_vocalists', 'multilingual bands and artists': 'https://en.wikipedia.org/wiki/List_of_multilingual_bands_and_artists', 'murdered hip hop musicians': 'https://en.wikipedia.org/wiki/List_of_murdered_hip_hop_musicians', 'music arrangers': 'https://en.wikipedia.org/wiki/List_of_music_arrangers', 'musicians known for destroying instruments': 'https://en.wikipedia.org/wiki/List_of_musicians_known_for_destroying_instruments', 'musicians who play left-handed': 'https://en.wikipedia.org/wiki/List_of_musicians_who_play_left-handed', 'nicknames of jazz musicians': 'https://en.wikipedia.org/wiki/List_of_nicknames_of_jazz_musicians', 'Pashto-language singers': 'https://en.wikipedia.org/wiki/List_of_Pashto-language_singers', 'royal musicians': 'https://en.wikipedia.org/wiki/List_of_royal_musicians', 'radio orchestras': 'https://en.wikipedia.org/wiki/List_of_radio_orchestras', 'singer-songwriters': 'https://en.wikipedia.org/wiki/List_of_singer-songwriters', 'symphony orchestras': 'https://en.wikipedia.org/wiki/List_of_symphony_orchestras', 'composers': 'https://en.wikipedia.org/wiki/Lists_of_composers', 'singers': 'https://en.wikipedia.org/wiki/Lists_of_singers'}
FirstOpt    =  '--select--'
ThisShouldNotBeHardCoded = [FirstOpt, 'crooners', 'Arabic pop musicians', 'gospel blues musicians', 'bands from British Columbia', 'harmonicists', 'UK garage artists', 'speed metal bands', 'Greek musical artists', 'psychedelic folk artists', 'progressive metal artists', 'nu metal bands', 'beatboxers', 'reggae fusion artists', 'dub artists', 'downtempo artists', 'polka artists', 'jazz musicians', 'Polish musicians and musical groups', 'bassoonists', 'hip hop musicians from New York City', 'jazz organists', 'bands originating in Leeds', 'folk rock artists', 'music artists and bands from Manchester', 'folk metal bands', 'electro house artists', 'Danish musicians', 'British blues musicians', 'free funk musicians', 'ragtime musicians', 'baroque pop artists', 'Indo pop musicians', 'hip hop groups', 'punk bands from the United Kingdom', 'pop and rock pianists', 'rocksteady musicians', 'American female country singers', 'calypso musicians', 'bands from Iceland', 'blues rock musicians', 'Norwegian musicians', 'country music performers', 'jungle and drum and bass artists', 'classical guitarists', 'Nigerian musicians', 'Eurobeat artists', 'Pakistani musicians', 'jazz pianists', 'emo artists', 'musicians from the Inland Empire', 'Christian country artists', 'dark cabaret artists', 'Portuguese musicians', 'free improvising musicians and groups', 'Russian opera singers', 'glam rock artists', 'New Zealand musicians', 'Swedish hip hop musicians', 'fado musicians', 'South African musicians', 'Japanoise artists', 'Winnipeg musicians', 'dream pop artists', 'Iranian singers', 'vocal trance artists', 'screamo bands', 'dance-pop artists', 'Indian violinists', 'percussionists', 'Argentine musicians', 'Ugandan musicians', 'reggae musicians', 'Finnish musicians', 'soul-blues musicians', 'Europop artists', 'Thai pop artists', 'Ghanaian musicians', 'funk rock bands', 'Italo disco artists and songs', 'Pakistani ghazal singers', 'pop punk bands', 'K-pop artists', 'soul jazz musicians', 'musicians in the second wave of punk rock', 'riot grrrl bands', 'symphonic metal bands', 'Viking metal bands', 'shoegazing musicians', 'house music artists', 'Pakistani pop singers', 'Belgian bands and artists', 'bebop musicians', 'technical death metal bands', 'rap rock bands', 'brass bands', 'political hip hop artists', 'gospel musicians', 'bands from Delhi', 'girl groups', 'gothic rock artists', 'Romanian singers', 'big band musicians', 'new wave artists and bands', 'indie pop artists', 'Finnish singers', 'groove metal bands', 'jazz guitarists', 'thrashcore bands', 'hammered dulcimer players', 'dark ambient artists', 'electric violinists', 'grindcore bands', 'glam punk artists', 'multilingual bands and artists', 'nicknames of jazz musicians', 'melodic death metal bands', 'vibraphonists', 'dance-punk artists', 'progressive rock artists', 'Dutch hip hop musicians', 'Jamaican musicians',  'operatic pop artists', 'bands from the San Francisco Bay Area', 'female heavy metal singers', 'dance-rock artists', 'jump blues musicians', 'bands from Los Angeles', 'musical groups from Halifax, Nova Scotia', 'Montreal music groups', 'R&B musicians', 'French singers', 'klezmer musicians', 'indie rock musicians', 'Eurodance artists', 'jazz vibraphonists', 'psychobilly bands', 'bands from Finland', 'smooth jazz musicians', 'folk musicians', 'female violinists', 'Pashto-language singers', 'British Invasion artists', 'bhangra artists', 'musical artists from Japan', 'banjo players', 'industrial music bands', 'lo-fi bands', 'psychedelic pop artists', 'deathcore artists', 'post-dubstep musicians', 'math rock groups', 'New York hardcore bands', 'trumpeters', 'Canadian musicians', 'Chinese musicians', 'merengue musicians', 'musicians from British Columbia', 'swing musicians', 'jam bands', 'accordionists', 'country rock musicians', 'funk musicians', 'Cajun musicians', 'hip hop musicians from Atlanta', 'roots rock bands and musicians', 'trip hop artists', 'hip hop artists', 'new-age music artists', 'Iranian musicians', 'jazz trombonists', 'Britpop musicians', 'soul musicians', 'jazz bassists', 'Philippine-based music groups', 'southern rock bands', 'Latin American rock musicians', 'bands from Gothenburg', 'hardcore punk bands', 'West Coast blues musicians', 'Portuguese singers', 'Utah musical groups', 'power pop artists and songs', 'rock and roll artists', 'Latin pop artists', 'Ecuadorian musicians', 'reggaeton musicians', 'UK noise musicians', 'Celtic musicians', 'ambient music artists', 'alternative rock artists', 'jazz violinists']
outsdeLbl   = 'Select a genre:'
selG        = st.selectbox(outsdeLbl, ThisShouldNotBeHardCoded, label_visibility = "hidden")      #  the dropdown box.  Do no randomize the order.

if selG == FirstOpt:
  raise SystemExit("nothing has been selected yet")      #  implied 'else'

################################################################################
### -----  text constants 
                                                         #  section startWords
baseStarts = [ 'Discography', 'Album_discography',
  'Select_discography',    'Selected_discography', 
  'Solo_discography',    'Solo_album_discography',
  'Discography_and_videography', 'Album', 'Albums',
  'Partial_discography', 'Repertoire',  'Releases',
  'Recordings', 'Studio_albums', 'Studio_releases',
  ]
                                                         #  include or skip sub-sections based on the id of its primary section since the primary sec was interrupted by these words
dumbWords = [ 'the EP', 'following list', 'as noted', 
  'where noted', 'as indicated', 'where indicated',
  'been nominated', 'also won', 'was issued',
  'was re-issued', 'was released', 'was re-released',
  'was featured', 'ppeared on', 'released in',
  'the album as', 'album came in', 'in the musical',
  ]
                                                         #  skip sections w/ [Compilations, Awards, Tours, Remixes, References, Singles, Accolades, Filmography, Grammy, sideman, With_others, Members, Arranger, Videos, Split_albums, Extended_plays, Bibliography, Biography, Guest_Appearances, Appearances, Demo, Artist_played_with, Various, Collaborative, DVD, Appears_on, Musician, Bootleg, Comics, Producer, Reviews, Miscellaneous, Tribute, Accompanist, Legacy, Books, Photobooks, Fandom, Lineup, Line-up, Line up, Films, Television, Box Set, Movies, Radio, Poetry, Departure, Reissues, Re-releases, Related Bands, Timeline, Musical Style, '(hit records)', 'Best albums', Reception, Concerts (must be plural), Broadway, Dance, Critical Acclaim, Contributions, Mixtape, Acting Credits, Songs, Engineered, Mixed, Gallery, Covers of _, Audio clips, Personnel, Actor (u.c. only), Best of (u.c. only) ] - even if lower-case or singular.  Maybe not skip 'Other' ??
skipWords = [ 'ompila', 'ward', 'Tour', 'emix',
  'ingle',  'ccolad', 'ilmogr', 'rammy', 'ideman', 
  'Other', 'other', 'rrange', 'embers', 'ember of', 
  'band member of', 'ideo',  'plit', 'xtend', 'uest',
  'emo', 'ayed', 'ariou', 'ollab', 'DVD', 'VHS', 'ppear',
  'usicia', 'ootleg', 'heatre', 'Theater', 'nmade',
  'omics', 'oducer', 'oducti', 'eview', 'iscell', 'ribut',
  'ccomp', 'egacy', 'Book', 'book', 'Fandom', 'ineup',
  'ine-up', 'ine Up', 'ine up', 'Film', 'film', 'levisio',
  'ox set', 'ox Set', 'ovies', 'adio', 'oetry', 'epartu',
  'eissu', 'e-rele', 'elated', 'imelin', 'tyle', '(hit r',
  'Best al', 'eception', 'ncerts', 'oadway', 'Dance',
  'dance', 'ical ac', 'ical Ac', 'ontribu', 'ixtape',
  'cting cred', 'cting Cred', 'Songs',  'songs', 'nginee',
  'mixed', 'Mixed', 'allery', 'overs of', 'udio clip', 
  'rsonnel', 'Actor', 'Best of',
  ]
                                                         #  end section searching w/ [References, Sources, External_Links, Bibliography, Biography, See_also, Notes, Footnotes, Endorsements, Production, Song Inspirations, Further Reading, Fictional Discography, Controversy, 'Published articles', 'Categories']   Assuming that a 'Performance Discog.' precedes a 'Production Discog.' 
enddWords = [ 'eferen', 'ource', 'xterna', 'Link',
  'iblio', 'iogra', 'See also', 'Also see', 'See Also',
  'Also See', 'Note', 'Notes', 'ootnot', 'ndorse', 
  'oducti', 'ong inspir', 'Reading', 'reading',
  'ictional', 'ontrover', 'rticles', 'ast edited',
  ]               
                                                         #  assuming no album titles use these words+punctuation
unAlbmWrds = [ 'CITATION', 'TEMPLATE', 'BILLBOARD',
  '(JANUA', '(FEBRU', '(MARCH', '(APRIL', '(MAY',
  '(JUNE', '(JULY', '(AUGUS', '(SEPTEM', '(OCTOB',
  '(NOVEM', '(DECEM', 'FIND SOURC', '(PARTIAL',
  'DETAILED LI', 'COMPLETE DI', ': THE STORY OF',
  'YING THIS FILE', 'ERENT TITLE', 'ED. ', 'AN EDITION', 
  ]                 
                                                         #  same-album dup removal
reIssuWrds = [ 'lso issued', 'eissued', 'e-issued', 
  'dentical music', 'eprint', 'e-released',
  'ka ', '.k.a.', '. k. a.', 's part of', 'lso entit', 
  'lso title', 'ther editio', 'ssued in', 'ssued as', 
  'eleased as', 'dition of', 'lso known as',
  ]                                           
                                                         #  un-skip albums that were sched to skip since a 'concert'
unConcert = ['CONCERTO', 'CONCERT ORCHESTRA', 'CONCERT BAND'
  ]
                                                         #  un-skip parents that were sched to skip since w/ 'TV'
unTVWords = ['TVT R', 'TV FREAK'
  ]

formatWds = [ '7"', '10"', 'REMIX', 'XTENDED',
  'COMPIL', 'SPLIT AL', 'VARIOUS', 'COLLABO',
  'LEGACY', 'BOX SET', 'BOXED SET', 'BOOTL',
  'LIVE CON',  'LIVE! IN', 'LIVE FROM', 'LIVE! FROM', 
  'LIVE AT',   'LIVE! AT', 'LIVE WITH', 'LIVE! WITH', 'LIVE PERF',  
  ]
                                                         #  remove non-audio media
vidWords = [ 'VIDEO', 'FILM', 'TV', 'TELEV', 'DVD',
  'MOVIE', 'MOTION PIC', 'VHS',
  ]
                                                         #  29 = intersection( 55 avail. codes w/ 'langdetect' module  +  362 languages on www.quora.com/What-are-the-languages-that-use-the-same-alphabet-as-the-English-language )
englshLke = [ 'af', 'ca', 'cs', 'cy', 
  'da', 'de', 'en', 'es', 'et', 'fr', 
  'hr', 'hu', 'id', 'it', 'lt', 'lv',
  'nl', 'no', 'pl', 'pt', 'ro', 'sk', 
  'sl', 'so', 'sq', 'sv', 'sw', 'tr', 'vi',
  ]    #         Afrikaans, Catalan, Czech, Welsh, 
#  Danish, German, English, Spanish, Estonian, French, 
#  Croatian, Hungarian, Indonesian, Italian, Lithuanian, Latvian, 
#  Dutch (Flemish), Norwegian, Polish, Portuguese, Romanian, Slovak, 
#  Slovenian, Somali, Albanian, Swedish, Swahili, Turkish, Vietnamese     

### -- the end of constants --
  
################################################################################
### -----  helper programs for web-scraping for albums from an artist's webpage

def findStart( A, sp ):      
  tryD    = baseStarts[:]                                #  list is local to each Artist
  origLen = len( A )
  for j in range( 0, origLen ):                          #  assuming that the primary source for an Artist under a different name would be a different url
    tryD.append( A + '_discography' )   
    tryD.append( 'Discography_as_' + A )                 #  remove right-end text one char at-a-time [ex. 'A_(band)' -> 'A_(band' -> 'A_(ban' -> ... ]
    A = A[:-1]                                    
  i = 0                                                  #  assuming no page has more than one of these sections
  while i < len( tryD ):
    re = sp.find( id = tryD[i] )                         #  assume 'discog' is in no other type of tag (skip <p>, etc)
    if re: 
      break                                              #  ok to return 'None' if no matches
    i += 1                                               #    ex. 'Discography_(producer)' does not count
  return re                     

# -----        a custom data structure based on r = resultSet from bs4
class Sec:                                            
  def __init__( self, rnk, sgo, txt, typ ):               
    self.rnk = rnk                                       #  rank = i in r[i] from the bs4 resultSet
    self.sgo = sgo                                       #  the 'stop / skip / go' condition
    self.txt = txt                                       #  text = displayed section name
    self.typ = typ                                       #  type = r[i].name = {'id','p',...}

# -----
def idSkipVsEnd( t, sc ):
  u = t.upper()
  sc.sgo  = 'endd'                                       #  default for any enddWord except 'Source'
  dun     = True                                        
  if 'Note' in t:
    if 'CREDIT' in u:                                    #  skip 1-word sec, not multi-word ex. 'note: credited to...'
      sc.sgo  = 'skip'                               
      dun     = False
  if 'SOURCE' in u:                                      #  'Source' sometimes is a sub-section to skip  + other times is an ending section 
    if len( t ) > sourceLng:
      sc.sgo  = 'skip'                                   #  must be 'elif'.  Assume only 1 of the 2 conditions will apply.
      dun     = False
    elif ('References in' in t):                         #  all un-avoided sections are included up to the first enddWord, then stop
      sc.sgo  = 'skip'                                   #  ex. 'References in X to A' may precede the Discography and 'end References' for urlA A
      dun     = False
  return sc, dun

# --  Sec( .rnk, .sgo, .txt, .typ )  !=  idSc()
def idSec( allSc, tg, ritg, tp ):                        #  ritg = r.index(tg)
  tTx     = tg.text
  UTX     = tTx.upper()                                  #  tp may be 'id' or 'tg.name', but not <span>  
  tTBrCt  = tTx.count('\n')
  doneNow = False
  newSc   = Sec( ritg, '', tTx, tp )
  if ('DISCOG' in UTX):                                  #  possibly multiple sections to be checked later.  Assuming it would be too redundant for a page to have both a (regular)'Discog' and an (ArtistName)'Discog' at once. 
    newSc.sgo = 'unkDisc'                                #    the 3 types of 'unk's may be combined or separated
  elif ( True in (e in tTx for e in dumbWords) ):        #  check for sub-section notes before EP check
    newSc.sgo = 'unkSubSc'
  elif ( max( tTBrCt, len(tg.find_all('li')) ) > 1 ):    #  assume no section name needs multiple lines 
    newSc.sgo = 'unkData'
  elif ( True in (e in tTx for e in skipWords) ):        #  assuming skipWords is a complete list of section names to avoid
    if 'ilm sound' not in tTx:                           #  'Film soundtracks' are not skipped, but 'Films' are skipped.
      if ( len( tTx ) < maxSecNameLng ):                 #  yes skip genuine sections w/ short secTitles, but do not skip a section which included a skipWord that is irrelevant to the rest of the data
        newSc.sgo = 'skip'          
        Comment = 'here'                                 #  prevent some duplicate results
  elif ( ('WITH' in UTX) | ('EP' in tTx) ):              #  w/o  + EP + album = good = no  skip    elif since the previous condition applies to a pseudo-section, not a real Sec.  Don't include many reasons to change OK2Add.
    if ('EP' in tTx):                                    #  w/o  + EP         = bad  = yes skip
      if ('lbum' not in tTx):                            #  w/o       + album = good               Yes add sections named "without [this Artist]", but not ones "with [another group]".
        newSc.sgo = 'skip'                               #  w/o               = good     
        Comment = 'here'                                 #  with + EP + album = good               Yes add a combo. "Album and EP" section, but not one for only EPs.          
    elif ('ithout' not in tTx):                          #  with + EP         = bad         
      newSc.sgo = 'skip'                                 #  with      + album = bad   
      Comment = 'here'                                   #  with              = bad         
  if ( ('LIVE' in UTX) and (newSc.sgo != 'unkData') ):
    if ('STUDIO' not in UTX ):                           #  allow a 'Live and Studio' combo.
      newSc.sgo = 'skip' 
  if len( newSc.sgo ) < 1:                               #  if no  sgo  yet
    if ( True in (e in tTx for e in enddWords) ):
      newSc, doneNow = idSkipVsEnd( tTx, newSc )         #  different urls use the same words for different purposes
    else:
      newSc.sgo = 'okSc'                                 #  default if not skip or endd
  if len( tTx ) > 1: 
    allSc.append( newSc )                                #  skip 1-letter sections
  minL = min( len(newSc.txt), 20 )
    #  print( 'r', newSc.rnk, newSc.sgo, newSc.txt[0:minL] ) 
  return allSc, doneNow

# -----
def bettrSectns( sc ):    #  sc = .rnk + .sgo + .txt + .typ
  for j in sc:
    if (j.sgo == 'unkDisc'):
      if j.rnk == 0:                                     #  use only the initial discog, 
        j.sgo = 'okSc'                                   #    not "B discog" where B is a different artist than A
      else: 
        j.sgo = 'skip'
  i = 0 
  ya = ['unkSubSc', 'unkData']
  for j in sc:
    if ( (j.sgo in ya) & (i > 0) ):                      #  change the id of a sub-section to that of its parent section 
      prevJ = sc[ i-1 ]                            
      j.sgo = prevJ.sgo
    i += 1                                              
  return sc                                         

# -----
def getSections( r ):  #  .rnk + .sgo + .txt + .typ  =  sc
  zc =      [ Sec( 0,'okSc', r[0].text, r[0].name ) ]      #  the 0th index always starts an OK Section
  for tg in r:                                              
    if (len(tg.text) > 2):
      if not (tg.text.startswith('[') or  \
              tg.text.startswith('cita') ):                #  skip 'citation' sections. 
        if tg.get('id'):                                   #  avoid dups by checking    
          zc, dun = idSec( zc, tg, r.index(tg), 'id' )     #    each type only one-at-a-time w/ elif's
          if dun: break
        elif tg.name in ['p','dt']:                        #  attr 'id' is not a 'name'                  
          zc, dun = idSec( zc, tg, r.index(tg), tg.name )  #    also 'li', 'td' ??
          if dun: break
  undupd = []                                              #  remove any duplicates
  for i in zc:
    if i.rnk not in [ undupd[j].rnk for j in range(0,len(undupd)) ]:
      undupd.append( i )
  undupd.sort( key = lambda x: x.rnk )                     #  can not 'return u.sort()' in 1 step
  btrSec = bettrSectns( undupd )                           #  sc improved 
    #  print('(', len(undupd), 'sections total )')
  return btrSec

# -----
def getResults( r, sc ):                                   #  sc = Sec( .rnk, .sgo, .txt, .typ )  data structure
  i = 0                        
  brks  = [ e.rnk for e in sc ]                            #  each break is the start of a new section (any type of sec)
  yesEm = []                                               #  good indeces for r
  for j in range( 0, len(sc) - 1 ):
    for k in range( brks[j], brks[j+1] ):                  #  Each sec ends 1 before the next sec.
      if sc[j].sgo == 'okSc':                              #    And the last sec ends 1 before the 1st enddWord.
        yesEm.append( k )                                  
  rByThisARaw = {}                                         #  Raw may have dups
  rByThisA    = {}  
  for y in yesEm:                                          #  each tag from 'Discog' to 1st_endd section
    toAdd = r[y].text.strip()
    if ( (r[y].name == 'i') and (safAlbm( toAdd )) ):      #  strip whitespace from both ends      
      rByThisARaw[ y ] = toAdd
  for k, v in rByThisARaw.items():                         #  check new tag against old records
      if v not in rByThisA.values():                       #    do not allow a tag of tags. Ex. 'unique' tags = 17 with this logic, not 42 w/out it.
        rByThisA[ k ] = v                                  #    This also removes duplicates.
  return rByThisA                                          #  skip album names with citations or other messages different than an album title.  Keep index of r + text, but not tags

# -----
def safAlbm( strng ):
  if not strng:                                            #  False if st is empty
    return False
  if (strng.startswith('[') or \
      strng.startswith('cita') ):                          #  skip 'citation' sections. 
    return False
  else:
    u = strng.upper()                                      #  False = not True  if  a match
  return not ( True in (e in u for e in unAlbmWrds) )      #  True  = not False if no match

# -----
def delBooks( r, data ):                                   #  data = dict(k = indices, v = text) 
  toDel = []
  for i in data.keys():                                    #  assuming that all books list an ISBN
    if 'ISBN' in r[i].parent.text:                         #    also assuming that the parent does not contain multiple data
      toDel.append( i )                                  
    if 'Billboard' in r[i].text:                           #  assuming that no album title uses these words
      toDel.append( i )
    if 'agazin' in r[i].text:                              #    (ditto)
      toDel.append( i )
  undupToDel = list( dict.fromkeys( toDel ) )
  print('books del', undupToDel)
  for m in undupToDel:                                     #  maybe also save in a seperate list    
    data.pop( m )
  return data

# -----                                                    #  data = dict(k = indices, v = text) 
def delByLang( r, data ):
  toDel = []                                               #  del non-English data if it
  for i in data.keys():                                    #    is paired w/ dup English data.
    try:               
      dtLngI = detect( data[i] )                           #  from the  langdetect  module  
      if not (True in (e in dtLngI for e in englshLke)):
        for j in data.keys():                              # '!=' checks both directions at once
          if ( (i != j) and (r[i].parent.text == r[j].parent.text) ): 
            try:
              dtLngJ = detect( data[j] )                 
            except:
              continue                                     #  skip to the next key
            finally:
              if (True in (e in dtLngJ for e in englshLke)):    
                toDel.append( i )
    except:                              
      continue                                             #  skip to the next key
  undupToDel = list( dict.fromkeys( toDel ) )              #  i = non-E, j = E.
  print('Lang del', undupToDel)
  for m in undupToDel:                                     #  maybe also save in a seperate list    
    data.pop( m )
  return data

# -----
def delSingles( r, data ):                                 #  data = dict(k = indices, v = text) 
  toDel = []
  for i in data.keys():                                    #  data = audio albums only, not any other form of media
    phrse = r[i].parent.text                            
    u = phrse.upper()
    if 'EP' in u:                                          #  test separately from other formatWds
      v   = re.split(r'\s', u)                             #  words from splitting u by whitespaces 
      w   = [re.sub(r'\W+', '', e) for e in v]             #  remove chars like '().,' from each word, even if not on an end (ex. 'E.P.' -> 'EP')
      b   = ['EP' in e for e in w]                         #  booleans
      idx = [j for j, val in enumerate(b) if val]          #  1000+ words contain 'ep' = too many to list
      for k in idx:                                        #  do not delete the same data more than once, even if multiple bad words in it
        if ( (i not in toDel) and (w[k] == 'EP') ):       
          toDel.append( i )                                #  assuming no other '_ep' 3-letter words will be used    
    if           'CONCERT' in u:
      if not (True in (e in u for e in unConcert)):        #  ex. 'Concerto' contains 'Concert' (a bad format)
        toDel.append( i )                                  
    if           'TRIBUTE' in u:
      if not ('DISTRIBUTE' in u):                          #  'Distributed' contains 'tribute' (a bad format)
        toDel.append( i )                                  
    if         'LIVE IN'   in u:                           #  probably a live recording
      if not  ('LIVE INTO' in u):                          #  probably not  (ditto)
        toDel.append( i )                                  
    if        'SINGLE'  in u:
      if not ('SINGLES' in u):                             #  save an album w/ plural 'singles', but not a single 'single'
        toDel.append( i )                                  
    if (True in (e in u for e in formatWds)):              #  all other bad formats
      toDel.append( i )                                
  undupToDel = list( dict.fromkeys( toDel ) )
  print('singls del', undupToDel)
  for m in undupToDel:                                     #  maybe also save in a seperate list    
    data.pop( m )
  return data

# -----
def delVideos( r, data ):                                  #  data = di ct(k = indices, v = text) 
  toDel = []
  for i in data.keys():                                    #  data = audio albums only, not any other form of media
    phrse = r[i].parent.text                            
    u = phrse.upper()
    if       (True in (e in u for e in vidWords ) ):
      if not (True in (e in u for e in unTVWords) ):       #  un-skip some special words that contain 'TV'           
        toDel.append( i )                                  
  undupToDel = list( dict.fromkeys( toDel ) )
  print('vid del', undupToDel)
  for m in undupToDel:                                     #  maybe also save in a seperate list    
    data.pop( m )
  return data

# -----
def delReissus( r, data ):                                 #  data = dict(k = indices, v = text) 
  toDel = []
  for i in data.keys():
    phrse = r[i].parent.text                               #  parents of only data, not a len = 20000 parent of a header
    if (True in (e in phrse for e in reIssuWrds)):
      if data[i] in phrse:                                 #  j must be 'close' to i  
        for j in data.keys():
          if ((i < j) and (i not in toDel) and (data[j] in phrse)):
            if ( (r[j].parent.text in phrse) or \
                 (phrse in r[j].parent.text) ):            #  'j == p' also works, except if w/ footnote citations
              toDel.append( i )
  undupToDel = list( dict.fromkeys( toDel ) )
  print('reiss del', undupToDel)
  for m in undupToDel:                                     #  maybe also save in a seperate list    
    data.pop( m )
  return data                                              #  save only the last album name (reading left-to-rt), not any earlier ones

# -----
def reportIt( msg, tA ):
  print('start report', msg)
  if msg == 'bad url':                                     #  better than having no info in the aCounts dict
    aCounts[ tA ] = -1
    print(' bad url for', tA )                             #  the attempt failed at this url
    faildPage.append( tA )                 
  if msg == 'no discog':
    aCounts[ tA ] = -2                                     #  no Discog-type of section exists on this webpage
    print(' no discog sec. found for', tA )
    faildDiscog.append( tA )                     

def attemptSoup( urlStr ):
  Urespons = requests.get( urlStr )
  Urespons.raise_for_status()                              #  show an err msg if status != 200 (if status is not fine)
  bs = BeautifulSoup( Urespons.text, 'html.parser' )  
  return bs 

#  --  end of the helper programs  --

################################################################################
### -----  global vars

faildPage   = []                                           #  no webpage at this url
faildDiscog = []                                           #  no 'Discog' section on the webpage
aCounts     = {}                                           #  dict of n of albums per artist
ANm         = []                                           #  list of artist's names
ApartU      = []                                           #  partial urls by artist
# AfullU
ResArtistNm = []                                           #  for the results
ResAlbumNm  = []                                           #       "
SourceList  = []                                           #       "

################################################################################
### -----  use Gsoup to scrape the webpage of one artist at a time

def findAlbums( nmA, urlA ):                               #  assume no auto-scraping if no 'Discography' section
  responsAlb = requests.get( urlA )                         
  if not responsAlb.ok:                                    #  <Response [200]>
    reportIt( 'bad url', urlA )
    return                    
  soup = BeautifulSoup( responsAlb.text, 'html.parser' )   #  must be single-quotes
  newSource = 'artist source: ' + urlA
  SourceList.append(newSource)
  s = findStart( urlA, soup )
  if not s:                                                #  can not 'find_all' based on null s  
    reportIt( 'no discog', urlA )
    return  
  p    = s.find_previous()                                 #  go back 1 tag to include the Discog-type startTag in "next"
  r    = p.find_all_next()                                 #  create a ResultSet (of all types) after the Previous Tag
  sc   = getSections( r )                                  #  sc has custom data structure Sec( rnk + sgo + txt )
  datA = getResults(  r, sc   )     #  use .copy() if nec                   
  datB = delBooks(    r, datA )                            #  data = dict( 
  datC = delByLang(   r, datB )                            #    k = index,
  datD = delSingles(  r, datC )                            #    v = text  )
  datE = delVideos(   r, datD )         
  datF = delReissus(  r, datE )                            #  reissue data pairs can be damaged if del before the Language test         
  for x in datF.values():                                
    ResArtistNm.append(nmA)                                #  saved in global vars
    ResAlbumNm.append(x)
  aCounts[ urlA ] = len( datF )                            #  'append' each n of records to the dict
  print( '  ', len(datF), ' albums for ', nmA, ' ' )

################################################################################
### -----  find the Genre Soup after a genre is selected from the box

def citatoon(x):                      
  return x and re.compile('#|index|cite|jpg|pedia').search(x)  #  skip tags that include any of these strings

TheG    = NmAndUrDict[selG]                                #  the genre URL w/ a list of links to artists in that genre
st.write("genre source: {}".format(TheG))
Gsoup   = attemptSoup(TheG)                    

for tag in Gsoup.find_all(href = citatoon):           
  tag.decompose()                                          #  ex. improve Gsoup to 46 from 86 <a>'s and good indeces remain from 29 to 38.

################################################################################
### -----  find the bounds for good tags of artists of the selected genre

if TheG == 'http://www.harbison.one': 
  iThis = 0
else:  
  iThis  = ThisShouldNotBeHardCoded.index(selG)
strtTags = [0, 23, 23, 23, 20, 22, 26, 32, 20, 22, 31, 27, 24, 24, 24, 28, 26, 27, 97, 23, 23, 21, 22, 29, 30, 48, 21, 19, 27, 27, 24, 28, 24, 23, 21, 22, 23, 23, 24, 23, 40, 20, 27, 21, 70, 42, 27, 41, 22, 39, 21, 32, 21, 21, 21, 53, 28, 25, 26, 21, 21, 21, 23, 21, 21, 23, 30, 20, 55, 23, 21, 21, 22, 36, 27, 23, 23, 20, 21, 20, 33, 27, 20, 27, 24, 54, 27, 55, 21, 28, 39, 28, 26, 23, 20, 182, 35, 69, 31, 23, 31, 21, 27, 23, 28, 111, 20, 27, 22, 21, 23, 27, 21, 22, 22, 32, 28, 23, 28, 21, 29, 187, 23, 31, 22, 21, 23, 25, 22, 25, 32, 25, 25, 25, 24, 23, 25, 23, 23, 21, 363, 28, 21, 28, 21, 31, 23, 21, 20, 30, 20, 29, 21, 30, 22, 21, 29, 21, 26, 25, 23, 24, 23, 28, 31, 32, 20, 25, 27, 69, 23, 22, 27, 68, 63, 30, 27, 21, 21, 23, 26, 20, 21, 22, 21, 21, 28, 24, 21, 28, 29, 40]
enndTags = [9, 136, 152, 51, 193, 459, 148, 189, 147, 66, 218, 399, 93, 138, 192, 146, 68, 260, 388, 124, 585, 112, 103, 464, 320, 136, 139, 194, 144, 43, 79, 91, 101, 984, 373, 617, 80, 579, 97, 98, 302, 465, 2196, 246, 254, 314, 45, 232, 844, 240, 62, 81, 90, 91, 228, 122, 102, 466, 78, 59, 395, 50, 122, 149, 122, 155, 79, 314, 112, 93, 49, 120, 638, 150, 102, 32, 120, 134, 78, 75, 60, 330, 838, 162, 227, 193, 235, 141, 155, 530, 113, 303, 288, 105, 92, 245, 171, 372, 36, 612, 149, 267, 45, 354, 907, 309, 198, 491, 52, 92, 233, 154, 128, 80, 471, 589, 140, 141, 121, 512, 76, 310, 99, 412, 377, 76, 80, 480, 58, 164, 1684, 451, 69, 1472, 145, 142, 92, 415, 298, 1029, 895, 70, 68, 69, 952, 275, 153, 45, 77, 107, 41, 218, 125, 284, 1801, 107, 60, 100, 128, 298, 265, 159, 209, 142, 230, 119, 140, 4038, 295, 344, 192, 83, 561, 680, 257, 139, 110, 124, 486, 68, 191, 54, 217, 101, 569, 38, 238, 28, 80, 399, 1326, 113]
nTgsBtwn = [b - a for (a, b) in zip(strtTags, enndTags)]

  # st.markdown(len(ThisShouldNotBeHardCoded))
  # st.markdown(len(strtTags))
  # st.markdown(len(enndTags))

 #  -- alternatively, it may be preferred to find a nice 'middle value' like 60 that works for most genres and then delete the other genre from the list -- 
nBtwn    = nTgsBtwn[iThis]
lwBound  = strtTags[iThis]
upBound  = enndTags[iThis]                                 #  '+ 1' was already done when enndTags were created
iList    = random.sample(range(lwBound, upBound), nArtistsToTry)

################################################################################
### -----  call the main function once per artist w/ pauses after each call

for itm in Gsoup.find_all( 'a' ):                            #  ex. /wiki/ABBA
  if itm.get('href') is not None:
    ApartU.append(itm.get('href'))
  if itm.text is not None:                                   #  index of Nm = index of url
    ANm.append(itm.text)

if ApartU: 
  AfullU = ['https://en.wikipedia.org' + x for x in ApartU]  #  full url's to look up
			  
for a in iList:                                       
  findAlbums( ANm[a], AfullU[a] )                            #  call the function
  time.sleep(PauseTime)                                      #  pause between calls to avoid a spam flag

# if len(ResArtistNm) < 12:                                  #  the result looks weak if too few albums returned
#   iList2nd = [ x + 1 for x in iList ]                               
#   if iList2nd are legal indeces:                           #  try once again to get at least 11 album results
#     for a in iList2nd:                                     
#       findAlbums( ANm[a], AfullU[a] )            
#       time.sleep(PauseTime)                           

################################################################################
### -----  display the resutls

print( [ aCounts[AfullU[i]] for i in iList ] )             #  on cmd prompt

if len(ResAlbumNm) > 0:
  tmp = list(zip(ResAlbumNm, ResArtistNm))                 #  shuffle 2 lists in the same order
  random.shuffle(tmp)
  toople1, toople2 = zip(*tmp)                             #  the * operator
  L1  = list(toople1) 
  L2  = list(toople2)                                      #  tbl = for the browser
  tbl = pd.DataFrame( {"Album": L1, "Artist": L2} )
  st.dataframe(tbl.set_index( tbl.columns[0] ))            #  hide the index column which looks weird starting at 0
else:
  st.write("  -- no discographies found for these artists --")
  
ReepA   = 'Of the '+ str(nBtwn) + ' ' + '[' + str(selG) + ']'
ReepB   = ' available, these ' + str(nArtistsToTry) + ' were selected:'
Reeport = ReepA + ReepB
st.write(Reeport)
for e in SourceList:                                       #  write just text, not list []s
  st.write(e)

### -----  end of the program  ----- ###########################################
################################################################################
################################################################################

##  to do:  
##    increase nArtistsToTry for genres like 'bassoonists' where 'discog' sections are rare
##    enable iList2nd to increase n of results + update nArtistsToTry
##    report applicable 'no discog' or 'no url' on the browser
##    zero results   https://en.wikipedia.org/wiki/Mario_Frangoulis  
##    avoid jpgs ex. https://en.wikipedia.org/wiki/List_of_musicians_from_Chicago
##  

