import joblib
import streamlit as st
import pandas as pd
import numpy as np
import datetime


model = joblib.load('model-v1.joblib')
types = list({'BATTERY': 1, 'THEFT': 1, 'OTHER OFFENSE': 1, 'NARCOTICS': 1, 'BURGLARY': 1, 'SEX OFFENSE': 1, 'CRIMINAL TRESPASS': 1, 'CRIM SEXUAL ASSAULT': 1, 'WEAPONS VIOLATION': 1, 'ROBBERY': 1, 'DECEPTIVE PRACTICE': 1, 'ASSAULT': 1, 'CRIMINAL DAMAGE': 1, 'OFFENSE INVOLVING CHILDREN': 1, 'MOTOR VEHICLE THEFT': 1, 'PUBLIC PEACE VIOLATION': 1, 'CONCEALED CARRY LICENSE VIOLATION': 1, 'PROSTITUTION': 1, 'HOMICIDE': 1, 'GAMBLING': 1, 'KIDNAPPING': 1, 'LIQUOR LAW VIOLATION': 1, 'INTERFERENCE WITH PUBLIC OFFICER': 1, 'STALKING': 1, 'INTIMIDATION': 1, 'ARSON': 1, 'CRIMINAL SEXUAL ASSAULT': 1, 'NON-CRIMINAL': 1, 'OTHER NARCOTIC VIOLATION': 1, 'OBSCENITY': 1, 'RITUALISM': 1, 'NON - CRIMINAL': 1, 'PUBLIC INDECENCY': 1, 'HUMAN TRAFFICKING': 1})
descriptions = list({'PARKING LOT/GARAGE(NON.RESID.)': 10138, 'STREET': 99115, 'SIDEWALK': 36155, 'APARTMENT': 42459, 'RESIDENCE': 63291, 'BAR OR TAVERN': 2058, 'SCHOOL, PRIVATE, BUILDING': 651, 'CONVENIENCE STORE': 1129, 'OTHER': 13275, 'DEPARTMENT STORE': 4730, 'RESIDENTIAL YARD (FRONT/BACK)': 3743, 'GAS STATION': 4320, 'RESIDENCE-GARAGE': 6721, 'SCHOOL, PUBLIC, BUILDING': 7178, 'CTA GARAGE / OTHER PROPERTY': 501, 'CHA PARKING LOT/GROUNDS': 2796, 'RESIDENCE PORCH/HALLWAY': 6173, 'SMALL RETAIL STORE': 7208, 'WAREHOUSE': 528, 'CHA APARTMENT': 1906, 'VEHICLE NON-COMMERCIAL': 5979, 'ALLEY': 8570, 'RESTAURANT': 6243, 'CTA BUS': 1193, 'AIRPORT/AIRCRAFT': 787, 'HOTEL/MOTEL': 1467, 'CTA STATION': 325, 'CTA PLATFORM': 1976, 'VACANT LOT / LAND': 86, 'COLLEGE/UNIVERSITY GROUNDS': 307, 'VACANT LOT/LAND': 1256, 'BARBERSHOP': 414, 'CHA HALLWAY/STAIRWELL/ELEVATOR': 1220, 'GOVERNMENT BUILDING/PROPERTY': 699, 'HOSPITAL BUILDING/GROUNDS': 1110, 'BANK': 1489, 'AIRPORT TERMINAL LOWER LEVEL - NON-SECURE AREA': 117, 'CTA TRAIN': 1434, 'GROCERY FOOD STORE': 4829, 'CONSTRUCTION SITE': 662, 'PARK PROPERTY': 2954, 'LIBRARY': 336, 'SCHOOL, PRIVATE, GROUNDS': 216, 'OTHER (SPECIFY)': 555, 'POLICE FACILITY/VEH PARKING LOT': 903, 'SCHOOL, PUBLIC, GROUNDS': 1521, 'DRUG STORE': 1702, 'TAVERN/LIQUOR STORE': 1117, 'ABANDONED BUILDING': 555, 'NURSING HOME/RETIREMENT HOME': 742, 'VEHICLE-COMMERCIAL': 316, 'PARKING LOT / GARAGE (NON RESIDENTIAL)': 942, 'ATM (AUTOMATIC TELLER MACHINE)': 377, 'COMMERCIAL / BUSINESS OFFICE': 2872, 'MEDICAL/DENTAL OFFICE': 370, 'DAY CARE CENTER': 170, 'HOSPITAL BUILDING / GROUNDS': 148, 'FIRE STATION': 57, 'CAR WASH': 157, 'CHURCH/SYNAGOGUE/PLACE OF WORSHIP': 801, 'ATHLETIC CLUB': 472, 'OTHER RAILROAD PROP / TRAIN DEPOT': 291, 'TAVERN / LIQUOR STORE': 53, 'POLICE FACILITY / VEHICLE PARKING LOT': 87, 'CURRENCY EXCHANGE': 554, 'RESIDENCE - GARAGE': 343, 'DRIVEWAY - RESIDENTIAL': 1100, 'RESIDENCE - YARD (FRONT / BACK)': 406, 'TAXICAB': 390, 'AIRPORT BUILDING NON-TERMINAL - NON-SECURE AREA': 53, 'RESIDENCE - PORCH / HALLWAY': 455, 'OTHER COMMERCIAL TRANSPORTATION': 142, 'AIRPORT TERMINAL UPPER LEVEL - SECURE AREA': 237, 'SPORTS ARENA/STADIUM': 260, 'AUTO': 65, 'AUTO / BOAT / RV DEALERSHIP': 67, 'SCHOOL - PUBLIC BUILDING': 149, 'CLEANING STORE': 234, 'MOVIE HOUSE/THEATER': 118, 'FACTORY/MANUFACTURING BUILDING': 348, 'AIRPORT TERMINAL LOWER LEVEL - SECURE AREA': 51, 'APPLIANCE STORE': 115, 'HOTEL / MOTEL': 175, 'CTA BUS STOP': 362, 'COLLEGE/UNIVERSITY RESIDENCE HALL': 82, 'COIN OPERATED MACHINE': 64, 'CHURCH / SYNAGOGUE / PLACE OF WORSHIP': 55, 'AIRPORT PARKING LOT': 55, 'NURSING / RETIREMENT HOME': 107, 'HIGHWAY/EXPRESSWAY': 63, 'CHA PARKING LOT / GROUNDS': 55, 'SCHOOL - PUBLIC GROUNDS': 114, 'JAIL / LOCK-UP FACILITY': 57, 'AIRPORT EXTERIOR - NON-SECURE AREA': 61, 'POOL ROOM': 58})

@st.cache

def predict(primary_type, location_description, distance, time_of_day, domestic):
    data = [time_of_day, domestic, distance]

    for i in range(len(types)):
        if primary_type == types[i]:
            data.append(1)
        else:
            data.append(0)
    
    for i in range(len(descriptions)):
        if location_description == descriptions[i]:
            data.append(1)
        else:
            data.append(0)

    df = pd.DataFrame([data])

    return model.predict(df)


st.title('Chicago Proper Arrest Prediction')
st.image('https://www.travelandleisure.com/thmb/wwUPgdpCUuD5sAPFLQf4YasjH0M=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/chicago-illinois-CHITG0221-e448062fc5164da0bba639f9857987f6.jpg') # idk find one
st.header('Enter the circumstances of the crime:')

primary_type = st.selectbox('Type of crime:', types)
location_description = st.selectbox('Location description:', descriptions)
domestic = st.checkbox('Domestic?')
time = st.time_input('Time of day:', datetime.time(8, 45))
distance = st.number_input('Distance from the center of the city:', min_value = 0, max_value=25, value=0)

if st.button('Predict Arrest'):
    arrest = predict(primary_type=primary_type, location_description=location_description, distance=distance, time_of_day=time, domestic=domestic)
    if arrest:
        st.error('The model predicts that you will get arrested.')
    else:
        st.success('The model predicts that you will NOT get arrested.')
