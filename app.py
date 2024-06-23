import streamlit as st
import pandas as pd

# Set the title of the app
st.set_page_config(layout='wide')

col1, col2, col3 = st.columns([3, 3, 3])

@st.experimental_fragment
def upload_1():
    uploaded_file_1 = st.file_uploader("Choose a file", type=["csv"], key='file_1')

    if uploaded_file_1:
        if uploaded_file_1.type is not None:
        
            df_1 = pd.read_csv(uploaded_file_1, sep=";")

            st.write(df_1.head())

            return df_1

@st.experimental_fragment
def upload_2():
    uploaded_file_2 = st.file_uploader("Choose a file", type=["csv"], key='file2')

    if uploaded_file_2:
        if uploaded_file_2.type is not None:
    
            df_2 = pd.read_csv(uploaded_file_2, sep=";")

            st.write(df_2.head())

            return df_2
with col1:
    st.title("上传在途数据")
    zaitu_df = upload_1()
    
    
    # Create a file uploader widget


with col2:
    st.title("上传入库数据")
    storage_df = upload_2()

@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode("utf-8-sig")

# Add a button to process the uploaded file
# merged_df = None
st.session_state['data'] = False
if st.button("运算", type="primary"):
    zaitu_grouped_df = zaitu_df.groupby(["发票号码", "货号"])['数量'].sum().reset_index()
    storage_grouped_df = storage_df.groupby(['供应商对货单号', '产品'])['数量'].sum().reset_index()
    merged_df = zaitu_grouped_df.merge(storage_grouped_df, how="outer", left_on=['发票号码', '货号'], right_on=['供应商对货单号', '产品'], suffixes=['_在途', '_入库']).sort_values(by=['数量_在途', '数量_入库'])
    merged_df['判断相同'] =  merged_df['数量_在途'] == merged_df['数量_入库']
    file_out = convert_df(merged_df)

    st.session_state['data'] = True


with col3:
    if st.session_state.get('data', None) == True:
        st.download_button(
        label="Download data as CSV",
        data=file_out,
        file_name="output.csv",
        mime="text/csv",
)





