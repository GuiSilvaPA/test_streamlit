from __init__ import *

st.title(':black[Health Check]')
st.markdown('---')

# FILE UPLOADER

raw_data_1 = st.file_uploader('Upload Document 1', type=['csv'])

raw_data_2 = st.file_uploader('Upload Document 2', type=['csv'])


if (raw_data_1 is not None) and (raw_data_2 is not None):

    APT = APTIV(raw_data_1, raw_data_2)

    plots = APT.compare_plots()

    for plot in plots:
        st.pyplot(plot)
