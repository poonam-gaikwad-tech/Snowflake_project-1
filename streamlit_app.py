# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(f":cup_with_straw: Customise your Smoothie!:cup_with_straw:")
st.write(
  """Choose the custom fruits you want in your custome Smoothie!
  """)
title = st.text_input("Name on Smoothie", 'Name on Smoothie')
st.write("The name on the Smoothie will be:", title)

cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

pd_df = my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()
                                                                                            
indgredients_list = st.multiselect(
    "Choose upto 5 indgredients:", 
    my_dataframe,
    max_selections=5
   )
if indgredients_list:
    ingredients_string=''

    for fruit_chosen in indgredients_list:
        ingredients_string += fruit_chosen + ' '

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        #st.write('The search value for ', fruit_chosen,' is ', search_on, '.')

        st.subheader(fruit_chosen + 'Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+search_on)   
        fv_df= st.dataframe(data=fruityvice_reponse.json(), width='stretch')


    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)values ('""" + ingredients_string + """','"""+ title+"""')"""


    time_to_insert =st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")


