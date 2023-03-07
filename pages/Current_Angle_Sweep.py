from __init__ import *

st.set_page_config(layout='wide')

st.title(':black[Current Angle Sweep]')
st.markdown('---')

# FILE UPLOADER

raw_data = st.file_uploader('Upload Document', type=['xlsx'])

# CONVERT DATAFRAME TO EXCEL

def to_excel(PCAS):

    data_to = PCAS.save_streamlit()
    output  = BytesIO()
    writer  = pd.ExcelWriter(output, engine='xlsxwriter')

    data_to.to_excel(writer, index=False, sheet_name='Sheet1')

    writer.sheets['Sheet1'].set_column('A:A', None, writer.book.add_format({'num_format': '0.00'}) )  
    writer.save()

    return  output.getvalue()



def plot_torque(data, index, new_inter):

    fig, ax = plt.subplots(1, 1, figsize=(15, 5))

    # AXIS = 1

    ax.plot(data['TqFB'].values, color='green', linewidth=2.5, label='ROUND: Torque_Horiba')

    # AXIS = 2

    ax2=ax.twinx()

    ax2.axvline(index[0], color='red', linewidth=1.5, linestyle='--', label='POINT: TqFB_ref')
    for val in index[1:]:  ax2.axvline(val, color='red', linewidth=1.5, linestyle='--')

    ax2.axvline(new_inter[0][0], color='pink', linewidth=2.5, linestyle='--', label='OLD')
    for val in new_inter[1:]:  ax2.axvline(val[0], color='pink', linewidth=2.5, linestyle='--')

    ax2.axvline(new_inter[0][1], color='cyan', linewidth=2.5, linestyle='--', label='NEW')
    for val in new_inter[1:]:  ax2.axvline(val[1], color='cyan', linewidth=2.5, linestyle='--')


    signal_index = data[data['Signal'] == 1].index.to_list()

    ax2.axvline(signal_index[0], color='orange', linewidth=1.5, linestyle='-', label='END: Cycle')
    for val in signal_index[1:]:  ax2.axvline(val, color='orange', linewidth=1.5, linestyle='-')

    # Parameter

    plt.xlim([0, 200])

    st.pyplot(fig)




# RUN PAGE


if raw_data is not None:

    PCAS = ProcessCurrentAngleSweep(raw_data)
    data, out_data, index, new_inter = PCAS.process_data()

    st.markdown('# Torque Plot')

    plot_torque(data, index, new_inter)

    data_to = PCAS.save_streamlit()    

    st.markdown('Output Table')

    st.dataframe(data_to)

    st.download_button(label     = "Download",
                       data      = to_excel(PCAS),
                       file_name = 'output_data.xlsx')

    st.markdown('# Plots')

    graph = PCAS.graphs()
    for plot in graph:
        st.plotly_chart(plot)