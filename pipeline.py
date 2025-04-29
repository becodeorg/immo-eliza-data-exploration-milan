from custom_transformers import *
from sklearn.pipeline import Pipeline
import pandas as pd

TO_DROP_LIST = ['Unnamed: 0', 
                'id',
                'url', 
                'postCode', 
                'province', 
                'locality', 
                'monthlyCost', 
                'hasBalcony', 
                'accessibleDisabledPeople', 

                #gardenSurface eq same 
                'hasGarden',

                #too many missing values
                'gardenOrientation', 
                'diningRoomSurface', 
                'terraceOrientation',

                #poorly correlated cols
                'parkingCountIndoor', 
                'parkingCountOutdoor', 
                'floorCount', 
                'streetFacadeWidth', 
                'kitchenSurface']

NA_BOOL_REPLACE_LIST = ['hasTerrace', 
                   'hasLivingRoom', 
                   'hasBasement', 
                   'hasLift', 
                   'hasVisiophone', 
                   'hasDiningRoom', 
                   'hasAttic', 
                   'hasOffice', 
                   'hasPhotovoltaicPanels',
                   'hasHeatPump', 
                   'hasArmoredDoor', 
                   'hasThermicPanels', 
                   'hasFireplace', 
                   'hasDressingRoom', 
                   'hasSwimmingPool', 
                   'hasAirConditioning']

NA_NUMERIC_REPLACE_LIST = ['gardenSurface', 'livingRoomSurface', 'terraceSurface']

MEAN_REPLACE_LIST = ['bedroomCount', 'habitableSurface', 'bathroomCount']


df = pd.read_csv('./datasets/Kangaroo.csv')

cleaning_pipe = Pipeline(steps=[
    ('drop_duplicates', DuplicateDropper(subset=['id'])),

    #calculate peb score from label before dropping locations

    #calculate buildingCondition & floodZoneType

    ('drop_columns', ColumnDropper(columns_to_drop=TO_DROP_LIST)), #Drop useless columns
    ('drop_price_na', NADropper(subset='price')), #Drop price rows with NaN
    ('replace_na_bools', NAReplacer(column=NA_BOOL_REPLACE_LIST, new_value='False')), #Assume NaN is not having the feature
    ('replace_na_numerics', NAReplacer(column=NA_NUMERIC_REPLACE_LIST, new_value=0.0)), #Assume NaN is 0 for numerics (not present)
    ('replace_kitchen_type_na', NAReplacer(column='kitchenType', new_value='NOT_INSTALLED')), #Assume NaN is no kitchen

    #Remove Outliers here

    ('replace_na_mean', NAReplacer(column=MEAN_REPLACE_LIST, new_value='mean')), #Fill NaN with mean value
    # ('room_count_replace_na', RoomCountCalculator()), #Estimate roomCount from other features
    # ('prepare_strings', StringPrepare()), #prepare every strings
    # ('boolean_transformer', BooleanTransformer()), #Convert boolean strings to integers (True=1, False=0)
])

cleaned_set = cleaning_pipe.fit_transform(df)

# print(cleaned_set.head(20))
print(cleaned_set.isna().sum()) #Check if there are still NaN values
