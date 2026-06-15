# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":tropical_drink: Customize Your Smoothie :tropical_drink:")
st.write(
  """Choose the fruit you want in your cutom smoothie !
  """)


name_on_order = st.text_input("Name on Smoothie: ")
st.write("Name on the smoothie will be: ", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredient_list = st.multiselect('Choose upto to 5 ingredients : '
                                ,my_dataframe,max_selections=5)

if ingredient_list:
    st.write(ingredient_list)
    st.text(ingredient_list)
    ingredients_string = ''

    for fruit_chosen in ingredient_list:
        ingredients_string +=fruit_chosen+ ' '

    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                    values ('""" +ingredients_string + """','"""+ name_on_order + """')"""
    time_to_insert = st.button('submit order')
    #st.write(my_insert_stmt)
    #st.stop()

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f"Thanks {name_on_order}, your smoothie is ordered!", icon="✅")


import requests

smoothiefroot_response = requests.get(
    "https://my.smoothiefroot.com/api/fruit/watermelon"
)
#st.write(f"Response Status: {smoothiefroot_response.status_code}")
#st.text(smoothiefroot_response.json())
st_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=true)


