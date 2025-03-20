# # import streamlit as st
# # import pickle
# # import pandas as pd

# # car_df = pickle.load(open('car.pkl', 'rb'))  # Load as DataFrame
# # car_list = car_df['carBrand'].tolist()  # Extract titles as a list

# # similarity = pickle.load(open('similarity.pkl', 'rb'))

# # def recommend(car):
# #     # Get index of the selected movie
# #     if car not in car_df['carBrand'].values:
# #         return ["car not found!"]
    
# #     car_index = car_df[car_df['_id'] == car].index[0]

# #     # Find similar movies
# #     distance = similarity[car_index]
# #     car_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]
    
# #     # Get movie titles
# #     reco_movies = [car_df.iloc[i[0]]['carBrand'] for i in car_list]
    
# #     return reco_movies

# # st.title('car Recommendation System')

# # select_car_name = st.selectbox(
# #     'Select a cars:',
# #     car_list  # Use the corrected list
# # )

# # if st.button("Recommend"):
# #     recommendations = recommend(select_car_name)
# #     for i in recommendations:
# #         st.write(i)



# import streamlit as st
# import pickle
# import pandas as pd
# import pymongo
# from PIL import Image
# from io import BytesIO

# # MongoDB connection
# MONGO_URI = "mongodb://localhost:27017/urban_drive"
# DB_NAME = "urban_drive"
# COLLECTION_NAME = "car"

# client = pymongo.MongoClient(MONGO_URI)
# db = client["urban_drive"]
# collection = db["car"]

# # Load car dataset
# car_df = pickle.load(open('car.pkl', 'rb'))  # Load as DataFrame
# car_list = car_df['carBrand'].tolist()  # Extract car brands as a list

# similarity = pickle.load(open('similarity.pkl', 'rb'))

# def get_car_image(car_id):
#     car_data = collection.find_one({"_id": car_id})
#     if car_data and "image" in car_data:
#         return Image.open(BytesIO(car_data["image"]))
#     return None

# def recommend(car):
#     if car not in car_df['carBrand'].values:
#         return ["Car not found!"], []
    
#     car_index = car_df[car_df['carBrand'] == car].index[0]
#     distance = similarity[car_index]
#     car_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]
    
#     reco_cars = [car_df.iloc[i[0]]['_id'] for i in car_list]  # Get car IDs
#     return reco_cars

# st.title('Car Recommendation System')

# select_car_name = st.selectbox(
#     'Select a car:',
#     car_list
# )

# if st.button("Recommend"):
#     recommendations = recommend(select_car_name)
    
#     if recommendations:
#         for car_id in recommendations:
#             car_data = car_df[car_df['_id'] == car_id].iloc[0]
#             st.subheader(f"{car_data['carBrand']} {car_data['carModel']} ({car_data['yearOfRegistration']})")
#             car_image = get_car_image(car_id)
#             if car_image:
#                 st.image(car_image, caption=f"{car_data['carBrand']} {car_data['carModel']}", use_column_width=True)
#             else:
#                 st.write("Image not available")
#     else:
#         st.write("No recommendations found.")



import streamlit as st
import pickle
import pandas as pd
import pymongo
from PIL import Image
from io import BytesIO

# MongoDB connection
MONGO_URI = "mongodb://localhost:27017/urban_drive"
DB_NAME = "urban_drive"
COLLECTION_NAME = "car"

client = pymongo.MongoClient(MONGO_URI)
db = client["urban_drive"]
collection = db["car"]

# Load car dataset
car_df = pickle.load(open('car.pkl', 'rb'))  # Load as DataFrame
car_list = car_df['carBrand'].tolist()  # Extract car brands as a list

similarity = pickle.load(open('similarity.pkl', 'rb'))

def get_car_image(car_data, image_type):
    if image_type in car_data and car_data[image_type]:
        return Image.open(BytesIO(car_data[image_type]))
    return None

def recommend(car):
    if car not in car_df['carBrand'].values:
        return ["Car not found!"], []
    
    car_index = car_df[car_df['carBrand'] == car].index[0]
    distance = similarity[car_index]
    car_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]
    
    reco_cars = [car_df.iloc[i[0]]['_id'] for i in car_list]  # Get car IDs
    return reco_cars

st.title('Car Recommendation System')

select_car_name = st.selectbox(
    'Select a car:',
    car_list
)

if st.button("Recommend"):
    recommendations = recommend(select_car_name)
    
    if recommendations:
        for car_id in recommendations:
            car_data_row = car_df[car_df['_id'] == car_id]
            
            if not car_data_row.empty:
                car_data = car_data_row.iloc[0].to_dict()  # Convert to dictionary to avoid Series issue
                
                st.subheader(f"{car_data.get('carBrand', 'Unknown')} {car_data.get('carModel', 'Unknown')} ({car_data.get('yearOfRegistration', 'Unknown')})")

                cover_image = get_car_image(car_data, 'coverImageBytes')
                exterior_image = get_car_image(car_data, 'exteriorImageBytes')
                interior_image = get_car_image(car_data, 'interiorImageBytes')

                if cover_image:
                    st.image(cover_image, caption="Cover Image", use_column_width=True)
                if exterior_image:
                    st.image(exterior_image, caption="Exterior Image", use_column_width=True)
                if interior_image:
                    st.image(interior_image, caption="Interior Image", use_column_width=True)
                if not (cover_image or exterior_image or interior_image):
                    st.write("Images not available")
            else:
                st.write("Car data not found in DataFrame")
    else:
        st.write("No recommendations found.")
