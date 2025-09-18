# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customise your Smoothie!:cup_with_straw:")
st.write(
  """Choose the custom fruits you want in your custome Smoothie!
  """)
title = st.text_input("Name on Smoothie", 'Name on Smoothie')
st.write("The name on the Smoothie will be:", title)

cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
st.dataframe(data=my_dataframe, use_container_width=True)

indgredients_list = st.multiselect(
    "Choose upto 5 indgredients:", my_dataframe, max_selections=5
   
    )
if indgredients_list:
   # st.write("You selected:", indgredients_list)
   # st.text(indgredients_list)

    ingredients_string=''

    for fruit_chosen in indgredients_list:
        ingredients_string += fruit_chosen + ' '
    # st.write( ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)values ('""" + ingredients_string + """','"""+ title+"""')"""

  #  st.write(my_insert_stmt)
   # st.stop()
    time_to_insert =st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
#st.text(smoothiefroot_response.json())
sf_df=st.dataframe(data=smoothiefroot_response.json(),user_container_width=True)
