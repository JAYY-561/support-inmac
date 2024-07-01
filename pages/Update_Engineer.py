import streamlit as st
import pandas as pd
from st_supabase_connection import SupabaseConnection, execute_query


conn = st.connection("supabase",type=SupabaseConnection)

st.set_page_config(page_title='Support Ticket Workflow', page_icon='data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAMAAABF0y+mAAAAY1BMVEX////9+PjXjI6+P0K/QkXBSErpv8D14+PJZWi6MTS7NTjFVljryMjCT1G6MjW7Njm5LTDTfoDgqaq4Jir67+/ThIbx19fz3d3doqP25+fIYGPReXvdnqDYkpP79PTluLm+QELIVu6CAAAAy0lEQVR4AX2SBQ7DQAwEHc4xlMP//2TpnNJGHbFW2pGBPsjyokxUNf3StEI+EaqBUBvrnvhAQCxkCncRsv3BplDKI4SnVrgnQmV/lAfIsrPjVlFvKLnVmgsqOw59j8q6TEppIyoHkZS2OqKy9zxIu6FU3OrHCcLZcmtZozJfW7sTKtdBxGFPRN/DHAtWuohTRs9KowkIr0FQORnBp9wYRHOrLGcCzju+iDrilKvS9nsIG7UqB0LlwsqixnCQT5zo8CL7sJRlcUd8v9YNS1IRq/svf5IAAAAASUVORK5CYII=')
st.image("https://i0.wp.com/inmac.co.in/wp-content/uploads/2022/09/INMAC-web-logo.png?w=721&ssl=1")
st.title( 'Update Engineer')

engineers = list(pd.DataFrame(execute_query(conn.table("Engineers").select("name", count="None"), ttl=None).data)["name"])

engineerInput = st.selectbox("Engineer", options=engineers, index=None)
if engineerInput is not "" and engineerInput is not None:
    data = execute_query(conn.table("Engineers").select("*", count="None").eq('name', engineerInput), ttl=None).data[0]
    with st.form('engineer'):
        number = st.text_input('Phone Number*', value=data["contact_number"])
        email = st.text_input('Email ID*', value=data["email"])
        field = st.toggle("Field Engineer", value=data["field"])
        location = st.text_input('Location', value=data["location"])
        placeholder_for_selectbox = st.empty()
        placeholder_for_optional_text = st.empty()

        col1Bottom, col2Bottom = st.columns([1,1])
        with col1Bottom:
                delete = st.form_submit_button("Delete Ticket", type="primary", use_container_width=True)
        with col2Bottom:
                save = st.form_submit_button("Save Changes", use_container_width=True)


    with placeholder_for_selectbox:
        if data["domain"] in ["Hardware Engineer", "PM Engineer", "Printer Engineer", "Other"]:
            selection = st.selectbox("Domain", ["Hardware Engineer", "PM Engineer", "Printer Engineer", "Other"], index=0)
        else:
            selection = "Other"
        
    with placeholder_for_optional_text:
        if selection == "Other":
            domain = st.text_input("If other, Specify")
        else:
            domain = selection

        if save:
            if number != "" and email != "" and domain != "":
                execute_query(conn.table('Engineers').update([{
                    "contact_number":number,
                    "email":email,
                    "field":field,
                    "location":location,
                    "domain":domain
                    }]).eq('name', engineerInput), ttl='0')
                st.rerun()
            else:
                st.write("Please fill all required fields")
        
        if delete:
            execute_query(conn.table('Engineers').delete(count=None).eq('name', engineerInput), ttl='0')
            st.rerun()
    

