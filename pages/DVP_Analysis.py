from __init__ import *

st.set_page_config(layout='wide')







st.title(':black[DVP Analysis]')
st.markdown('---')
# \n









def simple_plot(data, x, y, color='b', label=None, title=''):

    x_plot = data[x]
    y_plot = data[y]

    plt.scatter(x_plot, y_plot, color=color, label=label)
    plt.title(title+'\nVoltage: ' + str(data['Voltage'].unique()[0]) + 'V')
    plt.grid()

def simple_plot_stat(data, x, y, param, line=False, color='b', label=None, title=''):

    df_stat =data.groupby(x)[y].describe().reset_index()

    x_plot = df_stat[x]
    y_plot = df_stat[param]

    plt.scatter(x_plot, y_plot, color=color, label=label)
    if line: plt.plot(x_plot, y_plot, color=color)
    plt.title(title+'\nVoltage: ' + str(data['Voltage'].unique()[0]) + 'V')
    plt.grid()



def simple_plot_colors(data, graphs, title):
        
    figs = []
    for graph in graphs:

        fig = plt.figure(figsize=(8, 8))

        colormap = plt.cm.gist_rainbow
        colors   = [colormap(i) for i in np.linspace(0, 1, len(data[graph['c']].unique()))]

        for idx, c_var in enumerate(data[graph['c']].unique()):

            filt = (data[graph['c']] == c_var)

            data = data.sort_values(by=[graph['c'], graph['x']])


            plt.scatter(data[filt][graph['x']], data[filt][graph['y']], color=colors[idx], label=graph['label'] + ' ' + str(c_var))
            plt.plot(data[filt][graph['x']], data[filt][graph['y']], color=colors[idx])

        plt.grid()
        plt.xlabel(graph['xlabel'])
        plt.ylabel(graph['ylabel'])
        plt.title(title + '\nVoltage: ' + str(data['Voltage'].unique()[0]) + 'V')

        figs.append(fig)

    return figs




















@st.cache_data
def plot(data):

    figs = []
    for graph in errorComparison[:3]:

        cmap    = plt.cm.get_cmap('gist_rainbow', len(data[graph['c']].unique()))
        colors = [matplotlib.colors.rgb2hex(cmap(i)) for i in range(cmap.N)]

        fig = px.line(data.sort_values(by=[graph['c'], graph['x']]),
                    x=graph['x'], y=graph['y'],
                    color=graph['c'],
                            
                    title   = graph['title'],
                    markers = True,
                    width   = 800,
                    height  = 800,
                    color_discrete_sequence=colors)

        # fig = plt.figure(figsize=(8, 8))
        # x, y = data[graph['x']], data[graph['y']]
        # plt.scatter(x, y)

        figs.append(fig)

    return figs

def usual_plots_simple(data, param, title):

    if not isinstance(param, list):
        param = [param]

        
    figs = []
    for plots in param:

        fig = plt.figure(figsize=(8, 8))

        for plot in plots:

            data = data.sort_values(by=[plot['x']])

            if plot['stat']:           
                simple_plot_stat(data, plot['x'], plot['y'], plot['stat'], line=plot['line'], color=plot['color'], label=plot['label'], title=title)
            else:
                simple_plot(data, plot['x'], plot['y'], label=plot['label'], title=title)

        figs.append(fig)

    return figs


def usual_plots_advanced(data, param):
        
    if not isinstance(param, list):
        param = [param]

    figs = []
    for plots in param:

        fig = plt.figure(figsize=(8, 8))   

        data = data.sort_values(by=[plots['c'], plots['x']])
        
        simple_plot_colors(data, plots)

        figs.append(fig)

    return fig







def transpose(lst):
    return list(map(list, zip(*lst)))

# FILE UPLOADER














def create_download_link(val, filename):
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Download file</a>'



















raw_data = st.file_uploader('Upload Document', type=['csv', 'dat'], accept_multiple_files=True)



if raw_data != []:

    titles = [dt.name.split('.')[0] for dt in raw_data]


    if not isinstance(raw_data, list):
        raw_data = [raw_data]

    data = [pd.read_csv(rd) for rd in raw_data]
    data = [d[var_dict.keys()] for d in data]

    

    new_data = []
    for d in data:

        d['dcCurrentDelta'] = d['r1o Idc_yokogawa'] -    d['n IdcEst']
        d['acCurrentDelta'] = d['n IrmsEst'] -           d['wt SIGMA I']
        d['dcVoltageDelta'] = d['r1o Vdc_yokogawa'] -    d['Voltage']
        d['currentRiple']   = d['wt Ele1 IPPeak'] -      d['wt Ele1 IMPeak']
        d['voltageRiple']   = d['wt Ele1 UPPeak'] -      d['wt Ele1 UMPeak']
        d['torqueFB_IdIq']  = d['r1o Measured_Torque'] - d['n TorqueAchieved_IdIq']
        d['torqueFB_Pwr']   = d['r1o Measured_Torque'] - d['n TorqueAchieved_DCPwr']
        d['torqueFB_Ach']   = d['r1o Measured_Torque'] - d['n TorqueAchieved_IdIq']
        d['totalLossDelta'] = d['r1o Pdc_yokogawa'] -    d['r1o Mes Mech_Pwr_W'] - d['n PlossEst']
        d['torqueCmd_IdIq'] = d['n TorqueCmdFinal'] -    d['n TorqueAchieved_IdIq']
        d['torqueCmd_Pwr']  = d['n TorqueCmdFinal'] -    d['n TorqueAchieved_DCPwr']
        d['torqueCmd_Ach']  = d['n TorqueCmdFinal'] -    d['n TorqueAchieved']
        d['torqueCmd_FB']   = d['n TorqueCmdFinal'] -    d['r1o Measured_Torque']

        new_data.append(d)

    # figs = plot(data)

    new_data_pos = [d[d['MotorSpeedSPT'] > 0] for d in new_data]

    figs_overview, figs_errorComparison, figs_wattLossEff = [], [], []

    for data, pos, title in zip(new_data, new_data_pos, titles):

        for volt in data['Voltage'].unique():

            if volt != 0:

                figs_overview.append(usual_plots_simple(data[data['Voltage'] == volt], overview, title))
                figs_errorComparison.append(simple_plot_colors(pos[pos['Voltage'] == volt], errorComparison, title))
                figs_wattLossEff.append(simple_plot_colors(pos[pos['Voltage'] == volt], wattLossEff, title))
                                    
    figs_overview        = transpose(figs_overview)
    figs_errorComparison = transpose(figs_errorComparison)
    figs_wattLossEff     = transpose(figs_wattLossEff)
    

    my_bar = st.progress(0, text='Creating Plots ...')


    export_as_pdf = st.button("Export Report")


    if export_as_pdf:
        pdf = FPDF('P', 'mm', 'A4')
        pdf.add_page()
        pdf.set_font('Times', 'B', 36)


        # OVERVIEW ===========================================
        pdf.image('header1.png', x=0, y=0, w=210)
        pdf.cell(0, 240, 'Chapter: Overview', align='C')

        for fig, t in zip(figs_overview, overview):
            pdf.add_page()
            pdf.image('header1.png', x=0, y=0, w=210)

            pdf.set_font('Times', 'B', 18)
            pdf.set_text_color(255)
            pdf.cell(0, 0, t[0]['title'], align='L')

            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
                fig[0].savefig(tmpfile.name, bbox_inches="tight")
                pdf.image(tmpfile.name, x=10, y = 30,  w=85)

            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
                fig[1].savefig(tmpfile.name, bbox_inches="tight")
                pdf.image(tmpfile.name, x=110, y = 30,  w=85)

            # with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
            #     fig[2].savefig(tmpfile.name, bbox_inches="tight")
            #     pdf.image(tmpfile.name, x=10, y = 120,  w=85)

            # with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:                
            #     fig[3].savefig(tmpfile.name, bbox_inches="tight")
            #     pdf.image(tmpfile.name, x=110, y = 120,  w=85)

            # with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
            #     fig[4].savefig(tmpfile.name, bbox_inches="tight")
            #     pdf.image(tmpfile.name, x=60, y = 210,  w=85)




        # ERROR ===========================================


        pdf.image('header1.png', x=0, y=0, w=210)
        pdf.add_page()
        pdf.set_text_color(0)
        pdf.set_font('Times', 'B', 36)
        pdf.cell(0, 240, 'Chapter: Error Comparison', align='C')

        for fig, t in zip(figs_errorComparison, errorComparison):
            pdf.add_page()
            pdf.image('header1.png', x=0, y=0, w=210)

            pdf.set_font('Times', 'B', 18)
            pdf.set_text_color(255)
            pdf.cell(0, 0, t['title'], align='L')

            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
                fig[0].savefig(tmpfile.name, bbox_inches="tight")
                pdf.image(tmpfile.name, x=10, y = 30,  w=85)

            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
                fig[1].savefig(tmpfile.name, bbox_inches="tight")
                pdf.image(tmpfile.name, x=110, y = 30,  w=85)

            # with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
            #     fig[2].savefig(tmpfile.name, bbox_inches="tight")
            #     pdf.image(tmpfile.name, x=10, y = 120,  w=85)

            # with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:                
            #     fig[3].savefig(tmpfile.name, bbox_inches="tight")
            #     pdf.image(tmpfile.name, x=110, y = 120,  w=85)

            # with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
            #     fig[4].savefig(tmpfile.name, bbox_inches="tight")
            #     pdf.image(tmpfile.name, x=60, y = 210,  w=85)


        # eff ===========================================
        pdf.image('header1.png', x=0, y=0, w=210)
        pdf.cell(0, 240, 'Chapter: Loss Efficency', align='C')

        for fig, t in zip(figs_wattLossEff, wattLossEff):
            pdf.add_page()
            pdf.image('header1.png', x=0, y=0, w=210)

            pdf.set_font('Times', 'B', 18)
            pdf.set_text_color(255)
            pdf.cell(0, 0, t['title'], align='L')

            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
                fig[0].savefig(tmpfile.name, bbox_inches="tight")
                pdf.image(tmpfile.name, x=10, y = 30,  w=85)

            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
                fig[1].savefig(tmpfile.name, bbox_inches="tight")
                pdf.image(tmpfile.name, x=110, y = 30,  w=85)

            # with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
            #     fig[2].savefig(tmpfile.name, bbox_inches="tight")
            #     pdf.image(tmpfile.name, x=10, y = 120,  w=85)

            # with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:                
            #     fig[3].savefig(tmpfile.name, bbox_inches="tight")
            #     pdf.image(tmpfile.name, x=110, y = 120,  w=85)

            # with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
            #     fig[4].savefig(tmpfile.name, bbox_inches="tight")
            #     pdf.image(tmpfile.name, x=60, y = 210,  w=85)











        
        html = create_download_link(pdf.output(dest="S").encode("latin-1"), "test")

        st.markdown(html, unsafe_allow_html=True)








    # OVERVIEW ================================================================================


    st.markdown('# Overview')

    for i, (fig, graph) in enumerate(zip(figs_overview, overview)):

        with st.container():            

            st.markdown('## ' + graph[0]['title'])
            st.markdown('---')


            cols = st.columns(len(figs_overview[0]))
            for idx, col in enumerate(cols):
                with col:
                    # st.plotly_chart(fig)
                    st.pyplot(fig[idx])

        my_bar.progress(int((i + 1)*(100/(len(overview)+len(errorComparison)))), text='Creating Plots ...')

    # ERROR COMPARISON ================================================================================

    st.markdown('# Error Comparison')

    for i,( fig, graph) in enumerate(zip(figs_errorComparison, errorComparison)):

        with st.container():            

            st.markdown('## ' + graph['title'])
            st.markdown('---')


            cols = st.columns(len(figs_errorComparison[0]))
            for idx, col in enumerate(cols):
                with col:
                    # st.plotly_chart(fig)
                    st.pyplot(fig[idx])

        my_bar.progress(int((i + 1 + len(overview))*(100/(len(overview)+len(errorComparison)))), text='Creating Plots ...')

    # ERROR COMPARISON ================================================================================

    st.markdown('# Loss Efficency')

    for i,( fig, graph) in enumerate(zip(figs_wattLossEff, wattLossEff)):

        with st.container():            

            st.markdown('## ' + graph['title'])
            st.markdown('---')


            cols = st.columns(len(figs_wattLossEff[0]))
            for idx, col in enumerate(cols):
                with col:
                    # st.plotly_chart(fig)
                    st.pyplot(fig[idx])

        # my_bar.progress(int((i + 1 + len(overview))*(100/(len(overview)+len(errorComparison)))), text='Creating Plots ...')


